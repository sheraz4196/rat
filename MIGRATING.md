# Crux 0.1.0 → Rat 0.1.1

Rat is the renamed Crux terminal toolkit. The executable and Python module are `rat`; the Python distribution is `rat-terminal`. This project is not published to PyPI: install from this checkout or its release wheel. The old `v0.1.0` tag and release remain historical Crux artifacts; use new Rat artifacts for the renamed version.

## 1. Remove the old integration while Crux is installed

Use the same shell and explicit profile used for the old installation. First inspect a dry run, then uninstall:

```sh
# Bash; use --shell zsh for Zsh.
crux uninstall --shell bash --dry-run
crux uninstall --shell bash --yes
```

```powershell
# Run in the PowerShell host where you installed Crux.
crux uninstall --shell powershell --profile "$PROFILE" --dry-run
crux uninstall --shell powershell --profile "$PROFILE" --yes
```

For a custom profile add `--profile PATH` to both commands. Reopen the shell afterward to unload old functions/wrappers. Rat refuses to add a new block while Crux markers remain in that profile. It does not silently replace or remove the old block.

If Crux is no longer executable, inspect your profile and remove only the complete block between `# >>> crux >>>` and `# <<< crux <<<`, preserving everything else. Make a separate backup first; do not restore an entire old `.crux-backup` over newer profile changes. Reopen the shell.

## 2. Preserve configuration and GNOME recovery data

Before removing the old package, run `crux config` to locate its configuration directory. Rat uses separate locations:

| Data | Crux | Rat |
| --- | --- | --- |
| Linux/macOS config | `${XDG_CONFIG_HOME:-~/.config}/crux/` | `${XDG_CONFIG_HOME:-~/.config}/rat/` |
| Windows config | `%APPDATA%\CRUX\` | `%APPDATA%\RAT\` |
| Source-installer environment | `${XDG_DATA_HOME:-~/.local/share}/crux/venv` | `${XDG_DATA_HOME:-~/.local/share}/rat/venv` |
| Profile backup | `<profile>.crux-backup` | `<profile>.rat-backup` |

Rat does not automatically copy or delete old settings. To retain settings, copy `config.toml` into the new config directory only if it does not already exist; review an existing Rat config before merging. On Windows use the actual `$env:APPDATA` value; on Linux/macOS respect your configured `XDG_CONFIG_HOME`.

If you used GNOME profile synchronization, retain the original `gnome-terminal-<id>.backup.ini` and matching `.applied.json` ownership state. Either restore with `crux theme --restore-profile` before switching, or copy those recovery files alongside `config.toml` into Rat's config directory, preserving existing destination files. Do not overwrite an existing Rat backup with a different original state. Copying the config alone would leave Rat without the original recovery data. Keep a separate copy of the old directory until recovery is verified.

No shell uninstall automatically restores GNOME profile colors. `theme --reset-terminal` requests emulator defaults; it is not a substitute for guarded GNOME profile restoration.

## 3. Install Rat and verify it

From the renamed checkout, follow [installation.md](installation.md), then run:

```sh
rat --version
rat doctor
rat config
```

Expected version: `0.1.1`. Use `rat install --shell bash`, `--shell zsh`, or `--shell powershell --profile "$PROFILE"` as appropriate. Check `--dry-run` before applying. Prompt recovery is now `rat_restore_prompt`; the old `crux_restore_prompt` helper is not installed by Rat.

## 4. Remove the old package after verification

For pipx installations:

```sh
pipx uninstall crux-terminal
```

On Windows, `py -m pipx uninstall crux-terminal` also works. For an old source-installer installation, inspect the `~/.local/bin/crux` symlink and the old isolated `crux/venv` directory before removing them. Keep your old config, GNOME recovery files and profile backups until you are satisfied with migration. Do not delete unrelated executables or a shared environment.

The repository rename does not rename an existing local checkout directory. You may keep its directory name. Once the GitHub repository itself has been renamed, update its remote:

```sh
git remote set-url origin git@github.com:sheraz4196/rat.git
```

GitHub normally redirects old repository URLs after a rename. Do not run the remote update before the server-side rename exists. The clone-first human guide uses the original URL with an explicit local `rat` directory so it works on both sides of the transition.
