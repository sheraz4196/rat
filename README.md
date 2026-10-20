# RAT

Make the terminal yours. Rat is a local-first terminal enhancement toolkit for Python 3.11+. It runs inside your existing shell and terminal, without an account, backend, telemetry, or runtime network connection.

The next release is **v0.1.1**, under the [MIT license](LICENSE): Crux renamed to Rat. Existing users should follow [MIGRATING.md](MIGRATING.md) before switching. For hands-on Windows, Linux and macOS checks, start with the clone command in [HUMAN_TESTING.md](HUMAN_TESTING.md). See [installation.md](installation.md) for platform setup and [RELEASE.md](RELEASE.md) for release preparation. The earlier implementation evidence is retained in [V0.2_IMPLEMENTATION.md](V0.2_IMPLEMENTATION.md).

## Install

From this checkout on Linux/macOS:

```sh
./install.sh --shell bash
# Zsh: ./install.sh --shell zsh
```

The script creates or reuses an isolated environment under `${XDG_DATA_HOME:-~/.local/share}/rat/venv` and links `rat` into `~/.local/bin`. No virtual environment activation is required. Your existing PATH must include `~/.local/bin` to find the link in new shells; integration leaves PATH unchanged. Dependency installation needs a package index or local wheels; runtime operation works offline.

Alternatively, use pipx (including Windows):

```sh
pipx install .
pipx ensurepath
# Reopen the terminal if PATH changed.
rat install --shell bash --yes
# Zsh: rat install --shell zsh --yes
# PowerShell: rat install --shell powershell --profile "$PROFILE" --yes
```

The distribution is `rat-terminal`; it is not published to PyPI. Package installation alone does not edit profiles. Automatic integration is implemented for Bash, Zsh and PowerShell; local verification status is in the implementation report. Fish and cmd integration remain unsupported.

## Everyday commands

```sh
rat ls
rat ls src --hidden --size
rat ls --json
rat tree --depth 2 --max-entries 1000
rat tree --json
rat git status
rat view README.md
rat view rat/cli/cat.py pyproject.toml --no-color
```

Native `ls`, `tree`, `git`, and `cat` retain their normal behavior by default. Listing is directory-first, with optional icons, symlink labels, sizes and counts. `--long` adds sizes; it does not provide permissions/owner/time columns. Tree defaults to depth 3 and 1,000 entries and never descends through directory symlinks, including a symlink supplied as the root. Each visited directory is scanned/sorted as a whole, so the display cap is not a strict memory bound.

`ls --json` and `tree --json` produce structured data with `schema_version: 1`, without terminal markup. Listing includes `path`, `entries`, `directories`, and `files`. Entry fields are `name`, `path`, `directory`, `symlink`, byte `size` (or null), and `error` (or null). Tree adds a flat traversal list with `relative_path` and one-based entry `depth`, root `symlink`, `errors`, `count`, requested `depth`, `max_entries`, and `truncated`. JSON preserves actual names through JSON escaping; text output escapes terminal control characters.

Git summaries show branch, ahead/behind, index/worktree change codes, renames and untracked files. Git itself must be installed; Rat does not fetch or modify repositories.

## File viewer

`rat view FILE...` shows source with a filename/language/line-count frame, syntax colors, line numbers, indentation, and wrapped long lines. Markdown stays source rather than rendered prose. Multiple files have separate frames; unknown types fall back to plain text.

The viewer accepts regular UTF-8/UTF-8-BOM or BOM-marked UTF-16 text up to 2 MiB per file. Binary data, unsupported encodings, devices and streams require native `cat`. Embedded control characters are escaped. `rat view` deliberately keeps its formatted view when redirected, with color disabled.

## Prompt and shell compatibility

```sh
rat install --shell bash --dry-run
rat install --shell bash --yes
rat install --shell bash --keep-prompt --yes
rat uninstall --shell bash --yes
```

Installation replaces the prompt by default, explains this before confirmation, and saves the previous prompt for `rat_restore_prompt` in the current session. Use `--keep-prompt` for an existing prompt framework. Bash prompt hooks and Zsh hooks remain in place; a framework that rewrites PS1 may take precedence. Rat does not attempt to merge arbitrary prompt frameworks. If a function or alias named `rat_restore_prompt` already exists, Rat preserves it; use uninstall and reopen the shell to restore startup behavior.

The prompt shows a home-abbreviated path, Git branch/clean-or-dirty/ahead/behind, Python or Conda environment, a local `package.json` Node project marker, and nonzero exit status. Node versions are available in doctor rather than through a subprocess at every prompt. The fast prompt entry avoids Typer/Rich. Git has a 30 ms timeout; total startup overhead is measured separately and the approximately 50 ms target is not guaranteed.

### Optional native wrappers

```sh
rat install --shell bash --enhance-commands --yes
# Or --shell zsh. To disable, reinstall without --enhance-commands and reopen.
```

This explicit opt-in adds wrappers only where no existing alias/function owns `git`, `ls`, `tree`, or `cat`. Existing aliases/functions are never deleted or overridden. With both stdin and stdout on terminals, exact `git status`, argument-free `ls`/`tree`, and regular-file `cat` operands use Rat. Options, other Git subcommands, stdin, pipes, output redirection, and non-regular operands use native commands. Binary/large/unsupported-encoding files still require `command cat`. No general shell parser is used; use namespaced commands for predictable formatted output.

Use `command git`, `command ls`, `command tree`, or `command cat` to bypass wrappers in Bash/Zsh. Native tree fallback needs a separately installed `tree` executable. PowerShell native wrappers are unavailable because internal pipeline detection is ambiguous; use `rat git status` and `rat view` there. Its native commands and aliases remain unchanged.

Profile changes are limited to the marked Rat block. Installation creates `<profile>.rat-backup` once, preserves unrelated text and modes, and refuses symlinked/non-UTF-8 profiles, symlinked backups, and ambiguous markers. Atomic replacement protects against failed writes. Install/update is idempotent; uninstall removes only the block. Reopen the shell after changes, including when upgrading from v0.1's native wrappers. Package/config/backups are retained on shell uninstall. `rat init` remains a hidden alias for install; `_ls`, `_tree`, `_git status`, `_cat`, and `prompt` remain callable compatibility helpers.

## Configuration

```sh
rat config
rat config --json
rat config get general.theme
rat config set general.theme cobalt
rat config set prompt.show_git false
rat config reset prompt.show_git
rat config reset             # confirmation required
rat config reset --yes
```

Configuration lives at `$XDG_CONFIG_HOME/rat/config.toml` or `~/.config/rat/config.toml` on Linux/macOS and `%APPDATA%\RAT\config.toml` on Windows. `rat config` prints the actual path. No file is required.

```toml
[general]
theme = "default"
icons = true
animations = false
terminal_palette = true

[prompt]
enabled = true
show_git = true
show_python = true
show_node = true

[ls]
show_icons = true
show_sizes = true

[git]
enabled = true
```

Invalid settings warn and fall back to defaults; animations are reserved. Config editing validates known `SECTION.KEY` settings and boolean/theme values, preserves unrelated parsed data and comments on supported simple table assignments, and writes atomically. Malformed files, symlinks and unsupported layouts are refused rather than overwritten. Reset changes only known settings; unrelated TOML remains. `get` prints the effective value as a JSON scalar. Setting `general.theme` changes the selection for future commands/prompts; use `rat theme NAME` for immediate terminal/profile application.

## Themes and recovery

```sh
rat theme
rat theme cobalt
rat theme light
rat theme cobalt --sync-profile
rat theme --reset-terminal
rat theme --restore-profile
```

All five existing themes are retained: `default`, `dark` (same palette as default), `light`, `cobalt`, and `monochrome`. They control semantic Rat output, prompt segments and syntax colors. When `general.terminal_palette` is enabled, prompts apply OSC 4/10/11/12 for background, foreground, cursor and sixteen ANSI colors. Emulator support varies and is not actively negotiated; unsupported emulators may ignore them. `NO_COLOR`, `TERM=dumb`, and `rat --no-color theme NAME` suppress runtime controls. Regular redirected command output never includes palette controls; `prompt --shell` deliberately generates shell-captured prompt controls unless suppressed.

GNOME Terminal theme selection can also save colors to its default profile using gsettings/dconf. Interactive selection requests sync automatically; `--sync-profile` requests it from scripts. Profile failures warn after the Rat theme is saved. Original profile data is backed up once beside configuration as `gnome-terminal-<id>.backup.ini`; last verified owned colors are recorded in an `.applied.json` file. Windows/macOS emulator profile settings are not written by Rat. Scrollbar handle styling remains controlled by the desktop.

`--reset-terminal` disables prompt palette writes and sends OSC 104/110/111/112 on interactive color-capable output to request emulator defaults. With redirected output it only saves the opt-out. It does not recover arbitrary colors that existed before Rat, and emulator reset support varies.

`--restore-profile` requires a GNOME session and verified ownership state. It restores only managed color keys, resetting originally unset keys, while retaining newer unrelated settings. If colors have changed since Rat last applied them, recovery refuses to overwrite them. Older v0.1 backups without ownership state need manual recovery: inspect the backup and selectively restore color settings in GNOME Terminal preferences. Do not load the whole backup over newer profile settings. Backups remain after recovery. A failed multi-key restore can be partial; preserve the backup and inspect preferences before retrying. Successful recovery disables prompt palette writes so the next prompt does not undo it. Selecting a theme again reenables palette writes. There is no automatic restoration on process exit or shell uninstall.

## Diagnostics and development

```sh
rat doctor
rat doctor --json
rat doctor --shell powershell --profile "$PROFILE"
python -m pip install -e '.[dev]'
python -m pytest -q -rs
python scripts/benchmark_prompt.py --samples 30
python -m build
```

Doctor remains read-only. It reports existing platform/tool/capability/config fields plus Rat version/location, inferred install method, selected profile marker health, unsupported shells/legacy integration, GNOME prerequisites and actionable guidance. Shell and install-method detection are best-effort; explicit profile/shell options resolve ambiguity. JSON additions preserve the previous top-level fields; warnings go to stderr.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [ACCEPTANCE.md](ACCEPTANCE.md). Tests use temporary profiles and never edit personal startup files. CI runs tests and builds on Ubuntu/macOS/Windows with Python 3.11/3.14 and smoke-tests installed wheels; configured CI does not prove a run passed.
