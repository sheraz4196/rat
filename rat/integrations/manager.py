"""Marked, reversible profile edits; never restore a stale profile backup."""
import re
import shutil
import os
import tempfile
from pathlib import Path

START = '# >>> rat >>>'
END = '# <<< rat <<<'
PATTERN = re.compile(r'^# >>> rat >>>\r?\n.*?^# <<< rat <<<\r?\n?', re.M | re.S)


def block(shell, enhance_commands=False, keep_prompt=False):
    if shell == 'bash':
        # Command substitution is evaluated by Bash after decoding PS1, so prompt
        # data is never evaluated as shell syntax. Existing hooks remain intact.
        body = '''if command -v rat >/dev/null 2>&1; then
  if [ "${_RAT_ACTIVE:-}" != 1 ]; then
    _RAT_OLD_PS1=$PS1
    _RAT_ACTIVE=1
    PS1='$(rat prompt --status "$?" --shell bash 2>/dev/null || printf "%s" "$ " )'
  fi
fi'''
    elif shell == 'zsh':
        body = '''if (( $+commands[rat] )); then
  if [[ ${_RAT_ACTIVE:-} != 1 ]]; then
    _RAT_OLD_PS1=$PS1
    _RAT_ACTIVE=1
    _RAT_OLD_PROMPT_SUBST=$options[promptsubst]
    setopt promptsubst
    PS1='$(rat prompt --status "$?" --shell zsh 2>/dev/null || print -r -- "%# ")'
  fi
fi'''
    elif shell == 'powershell':
        body = '''if (Get-Command rat -ErrorAction SilentlyContinue) {
  if (-not $global:RatActive) {
    $global:RatOldPrompt = $function:prompt
    $global:RatActive = $true
    function global:prompt {
      $ratSuccess = $?
      $ratLastExitCode = $global:LASTEXITCODE
      $ratCode = if ($ratSuccess) { 0 } else { 1 }
      try {
        $ratOutput = & rat prompt --status $ratCode --shell powershell 2>$null
        if ($LASTEXITCODE -eq 0 -and $ratOutput) { return ($ratOutput -join "`n") }
      } catch {} finally { $global:LASTEXITCODE = $ratLastExitCode }
      if ($global:RatOldPrompt) { return (& $global:RatOldPrompt) }
      return "PS $($executionContext.SessionState.Path.CurrentLocation)> "
    }
  }
}'''
    else:
        raise ValueError('Safe automatic integration is available for bash, zsh, and powershell. cmd and Fish remain unchanged.')
    if keep_prompt:
        body = '# rat: prompt=preserved\n'
    if not keep_prompt and shell in ('bash', 'zsh'):
        body += """
if ! alias rat_restore_prompt >/dev/null 2>&1 && ! typeset -f rat_restore_prompt >/dev/null 2>&1; then
  function rat_restore_prompt {
    if [ "${_RAT_ACTIVE:-}" = 1 ]; then
      PS1=$_RAT_OLD_PS1
      unset _RAT_ACTIVE
"""
        if shell == 'zsh':
            body += '      if [[ $_RAT_OLD_PROMPT_SUBST == off ]]; then unsetopt promptsubst; fi\n'
        body += '    fi\n  }\nfi\n'
    elif not keep_prompt:
        body += """
if (-not (Get-Command rat_restore_prompt -ErrorAction SilentlyContinue)) {
  function global:rat_restore_prompt {
    if ($global:RatActive) {
      if ($global:RatOldPrompt) { Set-Item -Path Function:global:prompt -Value $global:RatOldPrompt }
      else { Remove-Item Function:global:prompt -ErrorAction SilentlyContinue }
      $global:RatActive = $false
    }
  }
}
"""
    if enhance_commands:
        if shell == 'powershell':
            raise ValueError('Native wrappers are unavailable for PowerShell; use rat git status.')
        body += '\n# rat: native-wrappers=enabled\n'
        body += """
if command -v rat >/dev/null 2>&1; then
  if ! alias cat >/dev/null 2>&1 && ! typeset -f cat >/dev/null 2>&1; then
  function cat {
    local _rat_file
    if [ -t 0 ] && [ -t 1 ] && [ "$#" -gt 0 ]; then
      for _rat_file in "$@"; do
        case "$_rat_file" in
          -*) command cat "$@"; return $? ;;
        esac
        if [ ! -f "$_rat_file" ]; then
          command cat "$@"
          return $?
        fi
      done
      rat _cat -- "$@"
    else
      command cat "$@"
    fi
  }
  fi
  if ! alias git >/dev/null 2>&1 && ! typeset -f git >/dev/null 2>&1; then
  function git {
    if [ -t 0 ] && [ -t 1 ] && [ "$#" -eq 1 ] && [ "$1" = status ]; then
      rat _git status
    else
      command git "$@"
    fi
  }
  fi
  if ! alias ls >/dev/null 2>&1 && ! typeset -f ls >/dev/null 2>&1; then
  function ls {
    if [ -t 0 ] && [ -t 1 ] && [ "$#" -eq 0 ]; then
      rat _ls
    else
      command ls "$@"
    fi
  }
  fi
  if ! alias tree >/dev/null 2>&1 && ! typeset -f tree >/dev/null 2>&1; then
  function tree {
    if [ -t 0 ] && [ -t 1 ] && [ "$#" -eq 0 ]; then
      rat _tree
    else
      command tree "$@"
    fi
  }
  fi
fi"""
    return START + '\n' + body + '\n' + END + '\n'


def read_profile(path):
    path = Path(path)
    if path.is_symlink():
        raise ValueError('Refusing to edit a symlinked profile; specify its real path explicitly.')
    try:
        content = path.read_bytes()
    except FileNotFoundError:
        content = b''
    try:
        text = content.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError('Profile must be UTF-8; no changes made.') from exc
    if text.count(START) != text.count(END) or text.count(START) > 1:
        raise ValueError('Ambiguous RAT markers; no changes made.')
    if START in text and not PATTERN.search(text):
        raise ValueError('Malformed RAT block; no changes made.')
    return text


def edit_profile(path, shell, remove=False, enhance_commands=False, keep_prompt=False):
    path = Path(path)
    text = read_profile(path)
    if not remove and ('# >>> crux >>>' in text or '# <<< crux <<<' in text):
        raise ValueError('Crux integration found. Run crux uninstall for this shell/profile, reopen the shell, then install Rat. See MIGRATING.md.')
    if remove:
        updated = PATTERN.sub('', text)
    else:
        integration = block(shell, enhance_commands, keep_prompt)
        if START in text:
            if '# rat: original-no-final-newline\n' in text:
                integration = integration.replace(START + '\n', START + '\n# rat: original-no-final-newline\n', 1)
            updated = PATTERN.sub(lambda match: integration, text)
        else:
            # Put the separator inside our block's owned span by requiring a clean
            # line boundary. A missing final newline is restored on removal.
            prefix = '\n' if text and not text.endswith('\n') else ''
            updated = text + prefix + integration
            if prefix:
                updated = updated.replace(START + '\n', START + '\n# rat: original-no-final-newline\n', 1)
    if updated == text:
        return False
    if remove and '# rat: original-no-final-newline\n' in text:
        match = PATTERN.search(text)
        if match and match.start() > 0:
            updated = text[:match.start() - 1] + text[match.end():]
    path.parent.mkdir(parents=True, exist_ok=True)
    backup = path.with_name(path.name + '.rat-backup')
    if backup.is_symlink():
        raise ValueError('Refusing symlinked profile backup; no changes made.')
    if path.exists() and not backup.exists():
        shutil.copy2(path, backup)
    # Replace atomically so a failed write cannot truncate the profile.
    descriptor, temporary = tempfile.mkstemp(prefix='.rat-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(updated.encode('utf-8'))
            stream.flush()
            os.fsync(stream.fileno())
        if path.exists():
            shutil.copymode(path, temporary)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return True
