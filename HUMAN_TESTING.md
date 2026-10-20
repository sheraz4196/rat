```sh
git clone https://github.com/sheraz4196/crux.git rat
cd rat
```

# Rat human testing guide

The original clone URL is intentional: it works before the GitHub rename and GitHub redirects it afterward. The checkout directory is `rat`. Use this guide on native Windows, macOS, or any Linux distribution with Python 3.11+; WSL results count as Linux, not native Windows. Git must already be installed to run the first command. Internet is needed for dependency installation, but Rat runs offline.

Record `git rev-parse HEAD` before testing. For a preview branch, check out the maintainer's exact branch or commit before installation; do not assume the default branch contains the rename. Record OS/distribution/version, CPU architecture, Python version, shell/version, terminal/version, font, and whether this is a VM. Try the default terminal font first; a Nerd Font is optional.

If Crux is already installed, follow [MIGRATING.md](MIGRATING.md) first. Start in a fresh terminal tab and use the disposable profile/configuration below before changing your normal shell. First complete the installation section for your OS, then return to the shared checks. Do not run all three OS installation sections.

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
