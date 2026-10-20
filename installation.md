# Installing Rat

Rat needs **Python 3.11 or newer**. Install it once, connect your shell, and open a new terminal. You do not need to activate a virtual environment each time.

Rat is not published to PyPI yet. Install from this repository or a locally built wheel; do not use `pip install rat`.

## Requirements

| Requirement | Details                                                                                                                                                  |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Python      | Python 3.11+, including `pip` and virtual-environment (`venv`) support. Keep Python installed after installing Rat.                                     |
| Shell       | Bash or Zsh on Linux/macOS; PowerShell on Windows. Fish and Command Prompt (`cmd.exe`) integration are currently unsupported.                            |
| Terminal    | A terminal supporting ANSI colours. Background, cursor, and palette changes require OSC 4/10/11/12 support; support varies by emulator.                  |
| Source code | Download or clone [the Rat repository](https://github.com/sheraz4196/rat). The install commands below run from the folder containing `pyproject.toml`. |
| Internet    | Needed to download Python, installation tools, and dependencies unless you already have local packages/wheels. Rat runs offline after installation.     |
| Git         | Optional for installation from a downloaded ZIP; required for Git status and repository information in the prompt.                                       |
| Fonts       | A Unicode-capable font for prompt symbols. A Nerd Font is optional, useful for file icons.                                                               |

The installer downloads Rat's Python dependencies (`typer`, `rich`, and `pygments`) automatically. Node.js, npm, and a compiler are not required for a normal installation. Namespaced `rat tree` needs no native tree utility. Install native `tree` separately if you use it or opt-in wrapper fallback.

## Windows

Use PowerShell in Windows Terminal for testing. PowerShell 7 is recommended. Install Python from [Python's official Windows instructions](https://docs.python.org/3/using/windows.html), then open a fresh PowerShell window and check:

```powershell
py --version
py -m pip --version
```

The Python version must be at least 3.11. If your installation exposes `python` instead of `py`, replace `py` with `python` in the commands below.

### Install

Install [pipx](https://pipx.pypa.io/stable/how-to/install-pipx.html), which keeps Rat in its own environment:

```powershell
py -m pip install --user pipx
py -m pipx ensurepath
```

Close and reopen Windows Terminal so the PATH change takes effect. Go to your downloaded or cloned Rat folder, replacing this example path with its actual location:

```powershell
Set-Location "$HOME\Downloads\rat"
py -m pipx install .
rat --version
rat install --shell powershell --profile "$PROFILE" --yes
```

`$PROFILE` selects the profile for the PowerShell host you are currently using. PowerShell 7, Windows PowerShell, and VS Code's PowerShell host can have different profiles. Run the integration command in each host where you want Rat. See [Microsoft's profile documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles).

Open a new PowerShell tab, then run:

```powershell
rat doctor
rat theme cobalt
rat git status
```

Run `rat git status` inside a Git repository. Use `rat view README.md` or `rat view path\to\code.py` for syntax-highlighted file viewing. PowerShell integration provides the prompt. Native `git`, `ls`, `tree`, `cat`, aliases and functions remain unchanged. Use namespaced Rat commands for formatted output; native wrappers are unavailable in PowerShell.

### If PowerShell blocks the profile

Check the effective policies:

```powershell
Get-ExecutionPolicy -List
```

On a personal computer, if policy prevents your local profile from loading, you can allow local scripts for your user account:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

This changes your user's script policy; it does not require an administrator shell. Organisation-managed policies can override it. Follow your organisation's policy on managed machines. See [Microsoft's execution-policy documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies).

Existing PowerShell profiles must be UTF-8 for Rat to edit them. If installation reports a non-UTF-8 profile, back up that file and save it as UTF-8 in your editor before retrying.

## Linux

Check Python first:

```sh
python3 --version
python3 -m pip --version
```

On Ubuntu/Debian, install the prerequisites if missing:

```sh
sudo apt update
sudo apt install python3 python3-pip python3-venv git
```

Check that `python3` is at least 3.11; older distributions may need a newer Python installed separately. On other distributions, use their package manager for Python, pip, venv support, and Git.

From the Rat source folder, choose your shell:

```sh
# Bash
sh install.sh --shell bash

# Or Zsh
sh install.sh --shell zsh
```

Run only the command matching your shell. The script installs Rat under `${XDG_DATA_HOME:-$HOME/.local/share}/rat/venv`, creates `~/.local/bin/rat`, and connects your shell. Integration leaves PATH unchanged. Ensure your existing PATH includes `~/.local/bin`; if not, add it through your own shell configuration before relying on the command in a new terminal. Run it as your normal user, without `sudo`.

Open a new terminal and run:

```sh
rat doctor
rat theme cobalt
```

If you prefer pipx, install it using your distribution's instructions, then run these commands from the Rat source folder:

```sh
pipx install .
pipx ensurepath
# Open a new terminal if PATH changed, then:
rat install --shell bash --yes
# For Zsh, replace bash with zsh.
```

## macOS

Install Python 3.11+ from [python.org](https://www.python.org/downloads/macos/) or through [Homebrew](https://docs.brew.sh/Installation). If Homebrew is already installed:

```sh
brew install python
python3 --version
python3 -m pip --version
```

Install Git if you need repository features and `git --version` does not work. Rat does not require a compiler; your chosen Python or Git installation method may have its own prerequisites.

From the Rat source folder, use Zsh unless you have configured a different shell:

```sh
sh install.sh --shell zsh
# If you use Bash instead:
# sh install.sh --shell bash
```

Open a new terminal:

```sh
rat doctor
rat theme cobalt
```

For a pipx installation, use `brew install pipx`, then follow the Linux pipx steps with `--shell zsh`. Avoid installing Rat into macOS's system Python.

If a Bash login shell does not show the prompt, make sure its existing login profile (`~/.bash_profile` or `~/.profile`) sources `~/.bashrc`. You can add this once to the login profile it actually loads:

```sh
if [ -f "$HOME/.bashrc" ]; then
  . "$HOME/.bashrc"
fi
```

## Verify the installation

In a newly opened terminal:

```sh
rat --version
rat doctor
rat config
rat theme
```

Available themes are `default`, `dark`, `light`, `cobalt`, and `monochrome`. Try `rat ls`, `rat tree`, `rat view README.md`, and `rat git status` inside a repository. Native commands are unchanged by default on every shell.

### Theme and startup behaviour

GNOME Terminal theme selection also saves colours to its **default profile**, using `gsettings` and `dconf`. This makes new windows start with the selected background and updates the scrollbar surround. The original profile is backed up once beside Rat's configuration. The scrollbar handle keeps the desktop's GTK styling.

Windows and macOS currently use runtime terminal colour sequences; Rat does **not** save Windows Terminal, Terminal.app, or iTerm2 profile settings. A background flash before the first prompt or unchanged scrollbar styling can therefore remain on those platforms. Set the emulator's saved profile colours to match your Rat theme if you want the same startup appearance. Some emulators may support only part of the runtime palette.

`NO_COLOR`, `TERM=dumb`, and `rat --no-color theme NAME` suppress runtime colour controls. `rat theme NAME --sync-profile` requests a GNOME default-profile update even when output is redirected; it is not a Windows/macOS profile installer.

## Update after changing or downloading the source

Installing from a source folder copies the package into the installation environment. Editing the source does not automatically update the installed `rat` command.

For pipx installations, run from the updated source folder:

```sh
pipx install --force .
```

On Windows you can use `py -m pipx install --force .` instead. For `install.sh` installations on Linux/macOS, rerun the script with the same shell option. The script reuses a valid existing environment. It refuses an unrelated executable/link or a symlinked/incomplete environment; inspect the existing installation before changing it.

If behaviour still looks outdated, check which executable your shell is using:

```powershell
# PowerShell
Get-Command rat -All
```

```sh
# Bash/Zsh
command -v rat
```

Use one installation method per machine to avoid competing copies on PATH. If `rat` is not found after pipx installation, run `pipx ensurepath` (or `py -m pipx ensurepath` on Windows) and reopen the terminal. If Linux reports missing `ensurepip`/venv support, install your distribution's venv package and retry.

## Configuration and removal

Configuration is stored at `%APPDATA%\RAT\config.toml` on Windows and `${XDG_CONFIG_HOME:-$HOME/.config}/rat/config.toml` on Linux/macOS. `rat config` prints the actual path.

Remove the shell integration before removing the package:

```powershell
# Windows: run in the same PowerShell host used during installation
rat uninstall --shell powershell --profile "$PROFILE" --yes
py -m pipx uninstall rat-terminal
```

```sh
# Linux/macOS: use bash or zsh as appropriate
rat uninstall --shell zsh --yes
# If installed with pipx:
pipx uninstall rat-terminal
```

For `install.sh` installations, after removing integration, remove the Rat link at `~/.local/bin/rat` and its isolated environment under `${XDG_DATA_HOME:-$HOME/.local/share}/rat/venv`. Open a new terminal afterward. Profile integration is removed by deleting only Rat's marked block; your other shell settings are preserved. Configuration files and GNOME Terminal's saved colors remain. Before uninstalling the package, use `rat theme --restore-profile` for guarded GNOME recovery, or `rat theme --reset-terminal` to disable prompt palette writes and request emulator defaults. Neither runs automatically on uninstall.

## v0.2 compatibility and recovery

Installation replaces the prompt and explains this before confirmation. Use `--keep-prompt` to retain an existing prompt framework, or `rat_restore_prompt` to restore the captured prompt in the current session. Reopen the shell after uninstall. No unrelated startup files or PATH entries are edited.

Bash/Zsh native-command enhancement is disabled by default. To opt in explicitly:

```sh
rat install --shell bash --enhance-commands --yes
```

Existing aliases/functions owning `git`, `ls`, `tree`, or `cat` are skipped. Supported routes require terminal stdin and stdout; pipes, redirection, stdin, non-regular operands and unsupported options use native programs. To disable wrappers or upgrade a v0.1 profile, rerun install without `--enhance-commands` and reopen the shell. Use namespaced commands for reliable formatting. PowerShell native wrappers, Fish and cmd integration are unsupported.

Config editing supports `rat config get SECTION.KEY`, `set SECTION.KEY VALUE`, and `reset [SECTION.KEY]`. Resetting all known settings confirms unless `--yes` is supplied; unrelated TOML is preserved. Edits refuse malformed, symlinked or unsafe layouts.

GNOME recovery uses both the original `gnome-terminal-<id>.backup.ini` and last verified `.applied.json` color state. `rat theme --restore-profile` refuses to overwrite colors changed since Rat's last write, preserves unrelated preferences, and disables prompt palette writes. Original v0.1 backups alone cannot prove ownership: inspect their color values and selectively restore them in terminal preferences. Preserve backups; do not blindly load their whole profile over newer settings. A partial restore failure requires manual inspection.

`rat theme --reset-terminal` requests OSC emulator defaults only on interactive output and saves `general.terminal_palette = false`. It does not recover arbitrary prior runtime colors. Selecting any theme reenables palettes. No restoration occurs automatically at process exit. See [README.md](README.md) for exact commands, JSON schemas and lifecycle limits.

Use `rat doctor --shell SHELL --profile PATH` to inspect a specific integration without editing it. See [RELEASE.md](RELEASE.md) for build/clean-install checks and [V0.2_IMPLEMENTATION.md](V0.2_IMPLEMENTATION.md) for actual platform results.
