```sh
git clone https://github.com/sheraz4196/rat.git
cd rat
git checkout v0.1.1
```

# Rat human testing guide

The checkout directory is `rat`. The release checkout ensures you test the renamed version even if the default branch is older. Use this guide on native Windows, macOS, or any Linux distribution with Python 3.11+; WSL results count as Linux, not native Windows. Git must already be installed to run the first command. Internet is needed for dependency installation, but Rat runs offline.

Record `git rev-parse HEAD` before testing. For a preview branch, check out the maintainer's exact branch or commit before installation; do not assume the default branch contains the rename. Record OS/distribution/version, CPU architecture, Python version, shell/version, terminal/version, font, and whether this is a VM. Try the default terminal font first; a Nerd Font is optional.

If Crux is already installed, follow [MIGRATING.md](MIGRATING.md) first. Start in a fresh terminal tab and use the disposable profile/configuration below before changing your normal shell. First complete the installation section for your OS, then return to the shared checks. Do not run all three OS installation sections.

## Windows installation and cleanup

Use native PowerShell 7 in Windows Terminal, not WSL or cmd. Check `py --version` (3.11+), `git --version`, and `$PSVersionTable.PSVersion`. If `py` is unavailable but `python` exists, substitute `python` for `py`. Install missing Python/Git/PowerShell before continuing. Windows PowerShell 5.1 can be tested as a separate additional host, but record it separately from PowerShell 7.

Open a dedicated test tab. From the cloned repository:

```powershell
py -m venv .venv-test
& .\.venv-test\Scripts\python.exe -m pip install '.[dev]'
$env:PATH = "$PWD\.venv-test\Scripts;" + $env:PATH
$env:RAT_TEST_DIR = Join-Path ([IO.Path]::GetTempPath()) ("rat human test-" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $env:RAT_TEST_DIR | Out-Null
$env:APPDATA = Join-Path $env:RAT_TEST_DIR 'config'
$env:RAT_TEST_PROFILE = Join-Path $env:RAT_TEST_DIR 'profile.ps1'
rat install --shell powershell --profile "$env:RAT_TEST_PROFILE" --dry-run
[IO.File]::WriteAllText($env:RAT_TEST_PROFILE, "# rat human test`n")
Copy-Item -LiteralPath $env:RAT_TEST_PROFILE -Destination (Join-Path $env:RAT_TEST_DIR 'original.ps1')
rat install --shell powershell --profile "$env:RAT_TEST_PROFILE" --yes
rat install --shell powershell --profile "$env:RAT_TEST_PROFILE" --yes
pwsh -NoLogo -NoProfile -NoExit -Command '. $env:RAT_TEST_PROFILE'
```

No activation script is required. Expected: dry run does not create the profile; installation creates one Rat block and a `.rat-backup`; a second installation keeps both unchanged. The child PowerShell displays Rat's prompt. Run the shared checks inside it.

If policy blocks dot-sourcing, run `Get-ExecutionPolicy -List` and report the result. Do not bypass a managed policy. For your personal machine, see the documented CurrentUser `RemoteSigned` option in [installation.md](installation.md), record the previous policy, and restore it afterward if changed. This guide does not require a machine-wide policy change.

Check pipes and redirection:

```powershell
rat ls --json | ConvertFrom-Json | Format-List
rat ls > (Join-Path $env:RAT_TEST_DIR 'listing.txt')
$text = Get-Content -Raw (Join-Path $env:RAT_TEST_DIR 'listing.txt')
if ($text.Contains([string][char]27)) { throw 'Unexpected terminal escape in redirected output' }
Get-Command git, ls, cat
```

Expected: JSON parses and redirected text contains no escape character. Native commands and PowerShell aliases remain unchanged; native wrappers are unsupported. Check that `$LASTEXITCODE` from a native failing command survives prompt rendering. Test PowerShell 7 and Windows PowerShell separately if claiming both.

Type `exit` once to leave the child shell, then:

```powershell
rat uninstall --shell powershell --profile "$env:RAT_TEST_PROFILE" --yes
$original = Get-FileHash -LiteralPath (Join-Path $env:RAT_TEST_DIR 'original.ps1')
$removed = Get-FileHash -LiteralPath $env:RAT_TEST_PROFILE
if ($original.Hash -ne $removed.Hash) { throw 'Uninstall changed unrelated profile content' }
rat uninstall --shell powershell --profile "$env:RAT_TEST_PROFILE" --yes
```

Expected: exact original profile bytes restored; second uninstall is a no-op. Close the dedicated tab after completing all checks to discard temporary PATH/APPDATA changes. Inspect and then remove `.venv-test` and the directory recorded in `$env:RAT_TEST_DIR` when no longer needed. Your real `$PROFILE` should not have changed during this disposable test.

## Linux installation and cleanup (any distribution)

Use Bash or Zsh. Fish and cmd integration are unsupported. Check `python3 --version` (3.11+), `git --version` and `bash --version`. Install missing Python/pip/venv/Git using your distribution's package manager. On older releases, install a supported Python separately; package names vary by distribution.

For Ubuntu/Debian, typical prerequisites are `sudo apt install python3 python3-pip python3-venv git`; Fedora commonly uses `sudo dnf install python3 python3-pip git`; Arch commonly uses `sudo pacman -S python python-pip git`. Confirm the installed Python version afterward. Run the project installation as your normal user.

In the cloned repository, in a dedicated Bash testing tab:

```sh
python3 -m venv .venv-test
. .venv-test/bin/activate
python -m pip install '.[dev]'
export RAT_TEST_DIR="$(mktemp -d)"
export XDG_CONFIG_HOME="$RAT_TEST_DIR/config"
# Prevent theme commands from syncing your real GNOME default profile.
unset GNOME_TERMINAL_SERVICE
rat install --shell bash --profile "$RAT_TEST_DIR/bashrc" --dry-run
printf '# rat human test\n' > "$RAT_TEST_DIR/bashrc"
cp "$RAT_TEST_DIR/bashrc" "$RAT_TEST_DIR/original"
rat install --shell bash --profile "$RAT_TEST_DIR/bashrc" --yes
rat install --shell bash --profile "$RAT_TEST_DIR/bashrc" --yes
bash --noprofile --rcfile "$RAT_TEST_DIR/bashrc" -i
```

Expected: the dry run does not create a profile. Installation creates one Rat block and a `.rat-backup` containing the original comment; a second install keeps both unchanged. The child Bash displays Rat's prompt. Run the shared checks in that child shell. Check pipes and redirection:

```sh
rat ls --json | python -m json.tool
rat ls > "$RAT_TEST_DIR/listing.txt"
python -c 'import os; from pathlib import Path; assert "\x1b" not in (Path(os.environ["RAT_TEST_DIR"])/"listing.txt").read_text()'
```

Type `exit` once to return to the parent Bash. Then:

```sh
rat uninstall --shell bash --profile "$RAT_TEST_DIR/bashrc" --yes
cmp "$RAT_TEST_DIR/bashrc" "$RAT_TEST_DIR/original"
```

Expected: `cmp` prints nothing and exits zero. Repeating uninstall is a harmless no-op. Optional: repeat with `--enhance-commands` in the disposable profile and confirm native commands handle options/pipes/redirection; existing aliases/functions must survive. Do not use that option with PowerShell.

For Linux/Zsh, use the macOS Zsh profile procedure below with your Linux Python installation. Record it as a separate shell result.

Also check the supported Linux source installer separately in a disposable home:

```sh
python scripts/verify_installer.py --source .
```

Expected: the script reports isolated installation, backup, repeat-install and uninstall checks passed. It needs dependency downloads unless supplied `--wheelhouse PATH` containing all required wheels.

After all shared and optional checks, in the parent testing tab:

```sh
deactivate
```

Close the dedicated tab to discard the exported test configuration and GNOME environment change. You can delete the repository's `.venv-test` and the temporary directory printed by `echo "$RAT_TEST_DIR"` after inspecting the paths; neither is your normal Python environment or Rat config. Keep failure logs before cleanup.

## macOS installation and cleanup

Use Terminal.app with Zsh first; test iTerm2 or other emulators as separate results. Check `python3 --version` (3.11+), `git --version`, and `zsh --version`. Install missing tools before continuing. Use a supported Python from python.org or your package manager, not an old system Python. Record Intel versus Apple Silicon.

Open a dedicated test tab and run from the cloned repository:

```sh
python3 -m venv .venv-test
. .venv-test/bin/activate
python -m pip install '.[dev]'
export RAT_TEST_DIR="$(mktemp -d)"
export XDG_CONFIG_HOME="$RAT_TEST_DIR/config"
mkdir "$RAT_TEST_DIR/zsh"
rat install --shell zsh --profile "$RAT_TEST_DIR/zsh/.zshrc" --dry-run
printf '# rat human test\n' > "$RAT_TEST_DIR/zsh/.zshrc"
cp "$RAT_TEST_DIR/zsh/.zshrc" "$RAT_TEST_DIR/original"
rat install --shell zsh --profile "$RAT_TEST_DIR/zsh/.zshrc" --yes
rat install --shell zsh --profile "$RAT_TEST_DIR/zsh/.zshrc" --yes
ZDOTDIR="$RAT_TEST_DIR/zsh" zsh -d -i
```

Expected: dry run leaves the profile absent; installation creates one Rat block and a `.rat-backup`; repeat install keeps both unchanged. The child Zsh uses the disposable `.zshrc` rather than your normal one. Run the shared checks inside it. If using this procedure on Linux/Zsh, also unset `GNOME_TERMINAL_SERVICE` in the dedicated tab before launching the child to avoid real GNOME profile synchronization.

Check pipes and redirection:

```sh
rat ls --json | python -m json.tool
rat ls > "$RAT_TEST_DIR/listing.txt"
python -c 'import os; from pathlib import Path; assert "\x1b" not in (Path(os.environ["RAT_TEST_DIR"])/"listing.txt").read_text()'
```

Try themes and reset in each recorded emulator. macOS terminal profile settings are not written by Rat. Palette/background/cursor support varies; record partial support and screenshot readability. Test ASCII and Unicode names, paths with spaces, and terminal resizing during the file viewer.

Type `exit` once to leave the child Zsh, then:

```sh
rat uninstall --shell zsh --profile "$RAT_TEST_DIR/zsh/.zshrc" --yes
cmp "$RAT_TEST_DIR/zsh/.zshrc" "$RAT_TEST_DIR/original"
rat uninstall --shell zsh --profile "$RAT_TEST_DIR/zsh/.zshrc" --yes
```

Expected: `cmp` exits zero; repeat uninstall is a no-op. The new prompt disappears when the disposable shell closes. For Bash testing, repeat the Linux disposable Bash procedure using macOS's installed Bash and record its version; do not assume Zsh acceptance covers Bash.

Also run the source-installer check if testing that installation method:

```sh
python scripts/verify_installer.py --source .
```

After all shared checks, `deactivate` in the parent shell, then close the dedicated tab to discard test environment variables. Inspect and remove `.venv-test` and the directory printed by `echo "$RAT_TEST_DIR"` when finished. Your normal `.zshrc` and terminal profile should remain unchanged during the disposable test.

## Shared command checks

Run from the repository root after activating the testing environment for your OS:

```sh
rat --version
python -m rat --version
rat --help
rat doctor
rat doctor --json
rat config
rat config --json
rat ls
rat ls --json
rat tree --depth 2 --max-entries 20
rat tree --json
rat git status
rat view README.md pyproject.toml
```

Expected: both version commands report `0.1.1`; help names Rat; doctor reports your actual OS and test config path. Diagnostic warnings should explain missing optional tools. JSON must parse without color codes. Listings should be readable; tree stops at the requested bounds. Git status agrees with `git status --short --branch`. The viewer shows separate frames, line numbers and syntax colors. Native `git`, `ls` and `cat` should behave as they did before integration.

```sh
rat config set general.theme cobalt
rat config get general.theme
rat config set prompt.show_git false
rat config get prompt.show_git
rat config reset prompt.show_git
rat config reset --yes
rat view missing-file-for-rat-test.txt
```

Expected: get returns `"cobalt"`, then `false`; reset restores defaults. A missing file prints a useful error and exits nonzero (`echo $?` in Bash/Zsh, `$LASTEXITCODE` in PowerShell). Do not reset an existing personal configuration; these commands are for the isolated test configuration only.

## Automated checks and package installation

These commands are the same in the activated test environment on every OS:

```sh
python -m pytest -q -rs
python -m build
```

Record passed/failed/skipped totals and every skip reason. A missing native Zsh on macOS or PowerShell on Windows is an incomplete integration test. A passing suite does not replace the interactive checks below. Build must produce `dist/rat_terminal-0.1.1-py3-none-any.whl` and `dist/rat_terminal-0.1.1.tar.gz`.

For an additional clean-wheel check (installs dependencies into another temporary environment):

```sh
python scripts/verify_wheel.py dist/rat_terminal-0.1.1-py3-none-any.whl
```

Expected: the installed executable and `python -m rat` both work outside the checkout, with Python network connections blocked during the smoke checks.

## Interactive checks in the disposable shell

1. Confirm the prompt shows the current directory. Change into a path containing spaces and non-ASCII characters; it should display literal names without executing their contents.
2. Run `git status`, create an untracked file in a temporary Git repository, and confirm the prompt becomes dirty. Remove the file and confirm it becomes clean. Do not edit tracked project files for this check.
3. Run a failing command (`false` in Bash/Zsh; `cmd /c exit 7` in Windows PowerShell). The next prompt should show a nonzero status; run a successful command and verify it clears.
4. Check arrow-key history, Tab completion, Ctrl+C, Ctrl+L, and running a normal command. On Bash/Zsh also check Ctrl+Z followed by `fg`, then Ctrl+C. Test Ctrl+D last because it can close the test shell; PowerShell's binding depends on PSReadLine and host settings.
5. Test a pipe and redirection using the commands in your OS section. Normal redirected output must contain no escape sequences. `rat view` retains its formatting when redirected, with color disabled.
6. Try `rat theme default`, `rat theme dark`, `rat theme light`, `rat theme cobalt`, and `rat theme monochrome`. Text must remain readable. Record unsupported palette changes by terminal, including background/cursor colors, rather than assuming every emulator supports OSC controls.
7. Disconnect networking after installation and repeat version, listing, viewer, configuration and prompt checks. Reconnect when finished.
8. Run `rat theme --reset-terminal` before closing the test shell. It requests emulator defaults and disables future Rat palette writes; it cannot restore arbitrary prior runtime colors. If colors remain changed, close the disposable tab.

Themes inside GNOME Terminal can write its default profile even when the shell/config is disposable. On GNOME, first set `rat config set general.terminal_palette false` and use `rat --no-color theme NAME` for ordinary theme-selection checks. Test profile synchronization/restoration separately using the GNOME section in [ACCEPTANCE.md](ACCEPTANCE.md) and an isolated desktop account or disposable VM with its own default GNOME profile. A new tab alone does not isolate that profile.

## Optional real startup-profile acceptance

Only after the disposable checks pass, install into your normal profile with the appropriate `rat install --shell ...` command from [installation.md](installation.md). Inspect `--dry-run` first. Confirm the `.rat-backup` is created once, unrelated profile content is preserved, repeated install produces only one Rat block, and a newly opened terminal loads it. Test `--keep-prompt` with your existing prompt framework, then uninstall and reopen the terminal to verify your original startup behavior. Do not restore an entire old backup over newer unrelated edits.

## Report a result

Copy this into a GitHub issue or send it to the maintainer. Redact usernames, personal paths and repository details from diagnostics/screenshots.

```text
Commit / Rat version:
OS / distribution / version / architecture:
Python version:
Shell / version:
Terminal / version / font:
Install method (source venv / wheel / install.sh / pipx):
Automated tests (passed / failed / skipped, with skip reasons):
Install / prompt / commands / themes / offline / uninstall: PASS / FAIL / NOT TESTED
Exact failing command and exit code:
Expected result:
Actual result:
Relevant doctor output / error / screenshot:
```

Report each independent failure separately. Mark untested steps honestly. A successful run covers only the recorded OS, shell and terminal combination; it does not establish all Linux distributions or every terminal emulator.
