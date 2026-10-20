# RAT v0.1.1

Crux is now Rat, a local-first terminal enhancement toolkit for Python 3.11+. This release supersedes Crux v0.1.0 without changing its historical tag.

- Renamed CLI/module to `rat` and distribution to `rat-terminal`; configuration, profile markers, backups and installer paths use the new name.
- Refuse installation over an existing Crux profile block; follow [MIGRATING.md](MIGRATING.md) before switching.
- Clone-first [human testing guide](HUMAN_TESTING.md) for Windows, Linux and macOS.
- Release publication waits for Ubuntu/macOS/Windows checks on Python 3.11 and 3.14.
- Directory listings, bounded trees, Git status summaries, and a syntax-highlighted file viewer.
- Bash, Zsh, and PowerShell prompt integration with guarded profile edits and backups.
- Five themes, editable TOML configuration, and read-only diagnostics.
- Optional Bash/Zsh native command wrappers that preserve existing aliases and functions.
- Terminal palette controls and guarded GNOME Terminal profile recovery.
- MIT license; wheel, source distribution, and SHA-256 checksums attached.

## Install

Download the attached wheel, then run:

```sh
pipx install ./rat_terminal-0.1.1-py3-none-any.whl
pipx ensurepath
rat --version
rat install --shell bash --yes
```

Use `--shell zsh` for Zsh or `--shell powershell --profile "$PROFILE"` for PowerShell. Dependency installation needs a package index or local wheels; runtime works offline. This release does not publish to PyPI.

## Known limitations

Fish/cmd integration and PowerShell native wrappers are unsupported. Terminal palette/reset support varies by emulator. Real interactive desktop acceptance, including GNOME profile restoration, remains manual; automated tests do not establish those behaviors. Prompt timing depends on the machine and repository.
