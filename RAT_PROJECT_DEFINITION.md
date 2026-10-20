# RAT

> A cross-platform terminal enhancement toolkit that makes the command line more useful, readable, and personal — without replacing the user's shell or terminal emulator.

## 1. Project Definition

**Project name:** RAT

**CLI command:** `rat`

**Project type:** Open-source, local-first, cross-platform terminal enhancement toolkit

**Primary language:** Python

**Target platforms:**
- Linux
- macOS
- Windows

**Target shells:**
- Bash
- Zsh
- Fish (planned)
- PowerShell
- Windows Command Prompt

## 2. Vision

RAT should make the ordinary terminal feel modern, polished, informative, and personal.

The goal is **not** to create another terminal emulator or shell. RAT should work on top of the user's existing terminal and shell.

The long-term vision is:

> **RAT turns the terminal from a basic command interface into a useful, beautiful, and customizable developer environment.**

It should remain:
- Local-first
- Fast
- Cross-platform
- Open source
- Privacy-respecting
- Optional rather than intrusive
- Useful without an internet connection

## 3. Core Philosophy

### Do not replace the terminal

RAT should work inside existing environments such as:

- Windows Terminal
- GNOME Terminal
- Konsole
- macOS Terminal
- iTerm2
- other ANSI-compatible terminals

It should also work with existing shells rather than forcing users to migrate.

### Do not require cloud services

RAT must not require:
- an account
- a cloud backend
- an API key
- telemetry
- an internet connection

The user's terminal information and local files should remain on their machine.

### Do not sacrifice performance for appearance

The enhanced prompt must feel instant.

A slow prompt is worse than a boring prompt.

Target:

> Prompt rendering should normally remain below approximately 50ms on a typical development machine.

## 4. Problem

Traditional terminals are powerful but often provide very little contextual information.

A user may see:

```text
user@machine:~/project$
```

while having no immediate visual information about:

- Git branch
- Git state
- Python virtual environment
- Node version
- project context
- command status
- useful filesystem information

Existing tools solve individual pieces of this problem, but RAT aims to provide a coherent, cross-platform experience.

## 5. Product Positioning

RAT is:

- A terminal enhancement toolkit
- A modern CLI utility collection
- A customizable shell prompt
- A developer environment information layer
- A foundation for future terminal themes and plugins

RAT is **not**:

- A terminal emulator
- A replacement for Bash
- A replacement for Zsh
- A replacement for PowerShell
- A replacement for Windows Terminal
- An AI command executor
- A cloud terminal service

## 6. Version 1 Scope

Version 1 should be intentionally small and reliable.

### Core features

#### 6.1 Enhanced Prompt

RAT should provide an optional enhanced shell prompt showing useful context.

Potential information:

- Current directory
- Git repository
- Git branch
- Git working-tree state
- Ahead/behind status
- Python virtual environment
- Node environment
- Last command exit status

Example:

```text
~/Documents/project  main ✓
❯
```

The prompt must be configurable so users can choose what is displayed.

#### 6.2 `rat ls`

A modern, readable directory listing.

Example:

```text
📁 src/
📁 public/
📁 tests/

📄 package.json       2.1 KB
📄 README.md          6.4 KB
📄 vite.config.js     1.2 KB

5 directories • 3 files
```

Initial options may include:

```bash
rat ls
rat ls -a
rat ls -l
rat ls --size
```

#### 6.3 `rat tree`

Display a readable directory tree.

Example:

```text
📁 project
├── 📁 src
│   ├── 📁 components
│   ├── 📁 hooks
│   ├── 📄 App.jsx
│   └── 📄 main.jsx
├── 📁 public
├── 📄 package.json
└── 📄 README.md
```

Possible options:

```bash
rat tree
rat tree --depth 2
rat tree --depth 3
rat tree --files
```

#### 6.4 `rat doctor`

Inspect the local environment and identify useful information or potential problems.

Example:

```text
RAT Doctor

System
────────────────────────────
✓ OS             Ubuntu
✓ Architecture   x86_64
✓ Shell          bash
✓ Terminal       GNOME Terminal

Development
────────────────────────────
✓ Git            2.x
✓ Python         3.x
✓ Node           24.x
✓ npm            11.x
✓ Docker         28.x

Terminal
────────────────────────────
✓ Unicode
✓ ANSI
✓ TrueColor

Warnings
────────────────────────────
⚠ Python virtual environment active
⚠ PATH contains duplicate entries
```

It should support machine-readable output later:

```bash
rat doctor --json
```

#### 6.5 `rat git`

RAT should provide a readable presentation layer around common Git information.

Initial command:

```bash
rat git status
```

Example:

```text
Repository
────────────────────────────────

Branch      main
Status      Modified
Ahead       2
Behind      0

Changes

  M  src/app.js
  M  src/styles.css
  ?  screenshots/

3 changed files
```

RAT should not attempt to replace Git.

Git itself remains the source of truth.

#### 6.6 `rat config`

Allow users to inspect and eventually modify RAT configuration.

Example:

```bash
rat config
```

Potential output:

```text
RAT Configuration

Theme       default
Prompt      enhanced
Icons       enabled
Animations  enabled
Git         enabled
```

Later:

```bash
rat config set icons false
rat config set theme cobalt
```

## 7. Future Theme System

Themes are intentionally outside the initial feature implementation, but the architecture must support them from day one.

The renderer should not hard-code visual colors throughout the codebase.

Instead, visual elements should use semantic theme roles such as:

```text
primary
secondary
success
warning
error
muted
directory
file
git
prompt
```

This allows future themes such as:

- Default
- Cobalt
- Dracula
- Nord
- Catppuccin
- Gruvbox
- Monokai
- Minimal
- Community-created themes

The user should eventually be able to select a theme with:

```bash
rat theme set cobalt
```

The RAT Cobalt theme may be inspired by the visual characteristics of the user's preferred Cobalt-style editor palette, but should be designed specifically for terminal readability rather than blindly copying another application's theme.

## 8. Configuration

RAT should use TOML configuration.

Linux/macOS:

```text
~/.config/rat/config.toml
```

Windows:

```text
%APPDATA%\RAT\config.toml
```

Example:

```toml
[general]
theme = "default"
icons = true
animations = true

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

Configuration paths should be resolved through a platform abstraction rather than hard-coded throughout the application.

## 9. Shell Integration

RAT will eventually provide:

```bash
rat init
```

The command should:

1. Detect the operating system.
2. Detect the current shell.
3. Check terminal capabilities.
4. Explain what will change.
5. Create a backup before modifying shell configuration.
6. Insert a clearly identifiable RAT integration block.
7. Enable the enhanced prompt.
8. Provide a clean uninstall path.

Example:

```text
RAT initialization

Detected:
  OS: Linux
  Shell: bash

RAT will modify:
  ~/.bashrc

Backup:
  ~/.bashrc.rat-backup

Continue? [Y/n]
```

RAT must never silently overwrite or destroy a user's shell configuration.

Integration blocks should be clearly marked:

```bash
# >>> rat >>>
...
# <<< rat <<<
```

This allows:

```bash
rat uninstall
```

to remove only RAT's integration.

## 10. Cross-Platform Architecture

Platform-specific behavior must be isolated.

Avoid spreading checks like this throughout the project:

```python
if sys.platform == "...":
    ...
```

Instead, provide centralized abstractions.

Example:

```text
core/
├── platform.py
├── terminal.py
├── shell.py
├── filesystem.py
├── git.py
└── environment.py
```

The rest of RAT should consume these abstractions.

Supported environments should include:

### Linux

- Bash
- Zsh
- Fish (planned)

### macOS

- Zsh
- Bash
- Fish (planned)

### Windows

- PowerShell
- Command Prompt
- Git Bash

## 11. Proposed Architecture

```text
rat/
│
├── rat/
│   ├── __init__.py
│   ├── __main__.py
│   │
│   ├── cli/
│   │   ├── main.py
│   │   ├── ls.py
│   │   ├── tree.py
│   │   ├── doctor.py
│   │   ├── git.py
│   │   └── config.py
│   │
│   ├── core/
│   │   ├── platform.py
│   │   ├── terminal.py
│   │   ├── shell.py
│   │   ├── filesystem.py
│   │   ├── git.py
│   │   └── environment.py
│   │
│   ├── prompt/
│   │   ├── builder.py
│   │   ├── git.py
│   │   ├── python.py
│   │   └── node.py
│   │
│   ├── render/
│   │   ├── renderer.py
│   │   ├── icons.py
│   │   ├── tables.py
│   │   └── theme.py
│   │
│   ├── config/
│   │   ├── manager.py
│   │   ├── defaults.py
│   │   └── schema.py
│   │
│   ├── integrations/
│   │   ├── bash.py
│   │   ├── zsh.py
│   │   ├── fish.py
│   │   ├── powershell.py
│   │   └── cmd.py
│   │
│   └── themes/
│       └── default.py
│
├── tests/
│   ├── test_platform.py
│   ├── test_filesystem.py
│   ├── test_git.py
│   ├── test_environment.py
│   ├── test_config.py
│   ├── test_render.py
│   └── test_prompt.py
│
├── pyproject.toml
├── README.md
├── LICENSE
├── CONTRIBUTING.md
└── .gitignore
```

This structure is intentionally modular so future features do not require rewriting the core.

## 12. Recommended Python Stack

### CLI

Use **Typer** for the command-line interface.

### Terminal rendering

Use **Rich** for:

- colors
- tables
- trees
- panels
- progress indicators
- terminal capability handling

### Configuration

Use Python's TOML support where available, with compatibility handling if required by the supported Python versions.

### System operations

Prefer Python standard-library modules:

- `pathlib`
- `subprocess`
- `shutil`
- `os`
- `sys`
- `platform`
- `tomllib`
- `json`

### Git

Initially invoke the installed Git executable through `subprocess`.

Do not introduce a heavy Git abstraction unless it provides a clear advantage.

## 13. Rendering Architecture

The application should separate **data** from **presentation**.

Bad:

```python
print("[blue]src/")
```

Preferred conceptual architecture:

```text
Filesystem Scanner
       ↓
Directory Data
       ↓
Renderer
       ↓
Theme
       ↓
Terminal Output
```

The same principle should apply to:

- Git information
- Doctor reports
- Prompt segments
- Tables
- Trees

This is essential for future themes and alternate output modes.

## 14. Performance Requirements

RAT should feel instant.

Important targets:

- Enhanced prompt normally under ~50ms.
- `rat ls` should remain fast in large directories.
- Avoid unnecessary subprocess calls.
- Cache information that does not need to be recomputed.
- Do not execute expensive checks on every prompt render.
- Git operations should be skipped when outside a repository.
- Large directory traversal should be bounded where appropriate.

Performance should be tested rather than assumed.

## 15. Privacy and Security

RAT is local-first.

By default:

- No telemetry.
- No analytics.
- No remote logging.
- No cloud account.
- No API keys.
- No command uploads.
- No remote execution.
- No network requirement.

RAT should only access files and system information required for the requested operation.

Shell integration must be transparent and reversible.

## 16. Accessibility and Compatibility

RAT should support environments where visual features are unavailable.

Requirements:

- `--no-color`
- graceful Unicode fallback
- sensible output when icons cannot be displayed
- useful output in narrow terminals
- machine-readable output where appropriate
- avoid relying exclusively on color to communicate state

Example:

```bash
rat ls --no-color
```

Future environment detection should automatically reduce visual features when necessary.

## 17. Version Roadmap

### v0.1 — Foundation

- Python package
- CLI entry point
- configuration system
- platform detection
- shell detection
- terminal capability detection
- renderer
- default theme abstraction

### v0.2 — Core Commands

- `rat ls`
- `rat tree`
- `rat doctor`
- `rat git status`
- `rat config`

### v0.3 — Prompt

- `rat init`
- Enhanced prompt
- Git context
- Python environment
- Node environment
- exit status
- Bash
- Zsh
- PowerShell
- Windows cmd

### v0.4 — Stability

- Windows testing
- macOS testing
- Linux testing
- performance improvements
- accessibility
- Unicode fallback
- error handling
- documentation
- automated CI

### v1.0 — Public Release

- Stable command interface
- Stable configuration format
- Reliable shell integration
- Comprehensive tests
- Installation documentation
- Contribution guide
- GitHub release
- Demo GIF/screenshots
- Clear roadmap

## 18. Post-v1 Features

Potential future features:

```text
rat theme
rat history
rat projects
rat ports
rat processes
rat open
rat aliases
rat notify
```

Additional functionality:

- Theme system
- Cobalt-inspired theme
- Dracula
- Nord
- Catppuccin
- Gruvbox
- Community themes
- Theme configuration
- Plugin system
- Better Git visualization
- Project shortcuts
- Command timing
- Process utilities
- Port inspection
- Shell integrations
- Developer environment integrations
- Optional notifications

## 19. Long-Term Vision

RAT can eventually become a complete terminal experience layer:

```text
                         RAT
                          │
          ┌───────────────┼───────────────┐
          │               │               │
       Visual          Utilities       Context
          │               │               │
       Themes            Files             Git
       Prompt            Ports            Python
       Icons             Processes        Node
       Layout            History          Docker
          │               │               │
          └───────────────┼───────────────┘
                          │
                   Existing Shell
                          │
              Bash / Zsh / PowerShell
                          │
                   Existing Terminal
```

The user should be able to make RAT look and behave according to their own workflow without giving up the tools they already know.

## 20. Project Principles

Every feature should be evaluated against these principles:

1. **Useful before beautiful.**
2. **Beautiful without becoming distracting.**
3. **Fast by default.**
4. **Cross-platform by design.**
5. **Local-first.**
6. **Privacy-respecting.**
7. **Reversible configuration changes.**
8. **Do not reinvent established tools unnecessarily.**
9. **Keep the core modular.**
10. **Do not add a feature simply because it looks impressive.**
11. **Preserve the user's existing shell and workflow.**
12. **Make customization a first-class architectural concern.**

## 21. Initial Success Criteria

RAT v1 is successful when a new user can:

```bash
pip install rat
rat doctor
rat ls
rat tree
rat git status
rat config
rat init
```

on Linux, macOS, or Windows and receive a polished, useful experience without:

- creating an account
- connecting a service
- providing an API key
- configuring a cloud service
- replacing their shell
- replacing their terminal emulator

The user should be able to uninstall RAT cleanly and return to their original terminal environment.

## 22. First Development Milestone

The first implementation milestone should **not** be themes or animations.

Build the foundation:

1. Create the Python package.
2. Configure the `rat` executable.
3. Implement platform detection.
4. Implement terminal detection.
5. Implement configuration loading.
6. Implement the renderer abstraction.
7. Add the default theme abstraction.
8. Implement `rat doctor`.
9. Add tests.
10. Then build `rat ls` and `rat tree`.

Once this foundation is stable, shell integration and the enhanced prompt can be built on top of it.

---

## Project Motto

> **RAT — Make the terminal yours.**
