# RAT Current Project Context

Snapshot date: 2026-10-30. Package version: **0.1.1**. Distribution: `rat-terminal`; executable and Python module: `rat` / `python -m rat`.

This file records the repository as it exists now, to ground future RAT work. Read source for exact behavior; README, tests, and `V0.2_IMPLEMENTATION.md` provide supporting user and verification details. The v0.1 context and v0.2 plan were written for the pre-rename Crux package and are historical references, not the current path or command authority.

## Product direction

RAT is a local-first terminal enhancement toolkit. It runs inside an existing shell and terminal and does not require an account, backend, telemetry, API key, or network connection at runtime. It must remain reversible and preserve native shell behavior by default. Current stated platforms are Linux, macOS, and Windows. Automatic integration is implemented for Bash, Zsh, and PowerShell; Fish and cmd are unsupported.

## Repository map

| Path | Purpose |
| --- | --- |
| `rat/cli/` | Typer commands, command registration, shared output/error handling, CLI fast entry point |
| `rat/core/` | Platform/shell/terminal detection, filesystem and Git data, environment diagnostics, text escaping, atomic storage |
| `rat/config/` | TOML defaults, validation, reading and bounded safe editing |
| `rat/prompt/` | Prompt context and shell-specific output builder |
| `rat/render/` | Rich output, semantic themes, syntax highlighting and terminal palette sequences |
| `rat/integrations/` | Reversible shell profile integration and guarded GNOME Terminal palette persistence/recovery |
| `tests/` | CLI, core, config, profile, installer, rendering and integration regression coverage |
| `scripts/` | Prompt benchmark, installer verification, installed-wheel smoke checks |
| `contexts/` | Current-state and architecture context documents |
| `plan/` | Proposed and in-progress implementation plans |
| `.github/workflows/` | Test/build and release workflows |
| `HUMAN_TESTING.md`, `ACCEPTANCE.md` | Manual cross-platform and interactive acceptance procedures |
| `RELEASE.md`, `installation.md`, `MIGRATING.md` | Release, installation and Crux-to-RAT migration guidance |

The `build/`, `dist/`, and `*.egg-info/` trees are generated artifacts, not the source of truth. There are no repository-level `AGENTS.md` instructions in this checkout.

## Runtime architecture

```text
rat executable / python -m rat
          |
    rat/cli/entry.py ---- prompt fast path ---- rat/prompt/builder.py
          |                                      | config + core context
    rat/cli/main.py                              | plain or shell prompt text
          |
    rat/cli/<command>.py ---- rat/core + rat/config
          |                         |
    rat/render/renderer.py <--------+------ Rich/Pygments output
          |
    terminal or redirected output
```

Commands are short-lived processes; there is no daemon, database, plugin loader, or persistent cache. Configuration is TOML under the platform-specific RAT config directory. Git and filesystem information is collected locally on demand.

| Module | Responsibility |
| --- | --- |
| `rat/cli/entry.py` | Avoid Typer/Rich import for `rat prompt`; argparse dispatches to prompt builder |
| `rat/cli/main.py`, `common.py` | Public CLI registration, global color option, shared config/renderer and safe errors |
| `rat/cli/{ls,tree,git,cat,config,doctor,theme,init}.py` | User-facing command behavior and shell/install lifecycle |
| `rat/core/filesystem.py` | Directory entries, hidden filtering, sorting, sizes and bounded tree presentation |
| `rat/core/git.py` | Local Git status subprocess and porcelain-v2 parsing |
| `rat/core/diagnostics.py` | Read-only installation, profile, shell-support and GNOME health report |
| `rat/config/manager.py` | Defaults, TOML validation, typed setting edits and safe atomic replacement |
| `rat/prompt/builder.py` | Path, Git, Python environment, Node project marker, exit status, colors and OSC sequences |
| `rat/render/` | Semantic output roles, five themes, syntax coloring and terminal palette data |
| `rat/integrations/manager.py` | Marked profile blocks, backups, atomic update/removal, optional Bash/Zsh native wrappers |
| `rat/integrations/terminal_theme.py` | GNOME default-profile color backup, verified apply and guarded restore |

## Current public behavior

Public CLI: `rat doctor`, `rat config` (including `get`, `set`, `reset`), `rat theme`, `rat ls`, `rat tree`, `rat git status`, `rat view`, `rat install`/`rat init`, and `rat uninstall`. `rat prompt` is the integration fast path. Internal `_ls`, `_tree`, `_git`, and `_cat` helpers support optional integration.

- Prompt: compact two-line output with home-shortened path; Git branch/dirty/ahead/behind; Python/Conda environment; presence of `package.json`; nonzero prior status. Prompt Git status uses a 30 ms subprocess timeout, but process startup is outside that budget.
- Filesystem: directory-first `ls`, optional hidden entries/icons/sizes, symlink labels and counts. `--long` means sizes, not permissions/owner/time. Tree defaults to depth 3 and 1,000 shown entries and does not traverse directory symlinks. `ls --json` and `tree --json` expose schema version 1.
- Git: read-only local `status` summary; no fetch or write commands.
- Viewer: syntax-highlighted UTF-8/BOM text for regular files, line numbers and wrapping; 2 MiB per-file bound; not a pager or Markdown renderer.
- Config: inspect/JSON plus typed get/set/reset; atomic edits preserve unrelated parsed settings/comments where supported and reject unsafe or unsupported TOML layouts.
- Themes: `default`, `dark`, `light`, `cobalt`, `monochrome`; prompt/output semantics, OSC palette, optional GNOME profile sync, palette reset request and guarded GNOME restore.
- Diagnostics: text/JSON local environment and integration health; read-only, no automatic repairs.
- Shell lifecycle: preview/confirm, explicit profile support, marker-owned update/removal, one-time backup and atomic writes. Native command wrapping is off by default; opt-in Bash/Zsh wrappers avoid existing aliases/functions and route only a narrow interactive request. PowerShell wraps prompt only; Fish/cmd integration is unavailable.
- Distribution: `rat-terminal` 0.1.1, MIT license, Python 3.11+, Typer/Rich/Pygments. README says not published to PyPI. Source installer and pipx are documented.

## Verification evidence and limits

On 2026-10-30 in this checkout, Python 3.14.3 ran the suite with **108 passed, 2 skipped**; the skips were real Zsh and PowerShell tests because those executables were unavailable. Source distributions and wheel built successfully, and the installed executable/module smoke test passed **58 checks** with Python socket connections and DNS blocked. A disposable Bash-profile install/uninstall round trip passed. The environment was Linux x86_64 with Bash 5.3.9; macOS, Windows, Zsh, PowerShell, and Fish were not available for local manual testing. The repository's [`verification/RAT_RENAME.md`](../verification/RAT_RENAME.md) records a successful hosted six-combination matrix for candidate `93e9a75`; that CI evidence does not establish interactive desktop behavior. GNOME behavior is mock-tested, not confirmed on a live GNOME desktop. Manual acceptance still includes real shell/OS runs and interactive history, completion, interrupts, job control, and emulator behavior. Full dated evidence is in [`priority0-baseline.md`](../plan/priority0-baseline.md).

The 2026-10-30 end-to-end prompt measurements miss the approximately 50 ms product goal on this host: Python 3.14 installed medians ranged from 78.190 to 99.138 ms, while source medians ranged from 82.844 to 97.007 ms, depending on scenario. Treat these as host-specific baseline measurements; rerun with the same method before comparing changes.

## Known improvement opportunities

1. Reduce end-to-end prompt startup based on profiling, while retaining a dependency-light fast path and correct shell status/context.
2. Complete real Bash/Zsh/PowerShell and Linux/macOS/Windows manual acceptance; validate live terminal and GNOME palette behavior.
3. Bound filesystem work, not only displayed output: each visited directory is currently scanned/sorted as a whole, so a display cap is not a strict time or memory bound.
4. Clarify and expand listing modes: current `--long` is size-oriented; there are no permissions/owner/time columns, sorting/filter controls, or a find/search command.
5. Broaden prompt context carefully: Node is detected by a current-directory `package.json` marker without a Node version; there is no project-root discovery or broader toolchain-manager context.
6. Extend shell coverage only with dedicated compatibility tests and native fallbacks; Fish/cmd are not implemented.
7. Add a read-only Git diff/log view if user demand warrants it; current RAT Git scope is status only.
8. Improve user-facing completion/help discoverability and integration diagnostics based on manual feedback.

Treat plugins, remote/theme downloads, AI command execution, cloud sync, animations, a daemon, and write-capable Git as high-scope ideas rather than automatic next steps. They are not needed to address the measured gaps and require separate product and safety justification.
