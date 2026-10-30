# RAT Enhancement Plan

**Status:** Proposed work plan  
**Baseline:** RAT 0.1.1, repository snapshot 2026-10-30  
**Context:** [`RAT_CURRENT_CONTEXT.md`](../contexts/RAT_CURRENT_CONTEXT.md)  
**Intent:** Find and close the most useful quality gaps in the existing RAT product without expanding it into a shell replacement or cloud service.

## Product guardrails

- Keep RAT local-first, optional, reversible, and useful offline at runtime.
- Preserve native shell commands, aliases, functions, PATH, prompt frameworks, pipes, redirection, history, completion, and job control by default.
- Prefer namespaced commands and read-only features. Native command wrappers remain explicit opt-in.
- Keep prompt execution fast; measure the complete executable path before and after changes.
- Bound file and process work, escape untrusted terminal text, and degrade gracefully when optional tools/capabilities are unavailable.
- Do not claim platform or shell support without implementation and actual verification.

## Priority 0 — Establish a current baseline

**Status: Complete for the available local Linux/Bash environment (2026-10-30).** Results and unavailable platform checks are recorded in [`priority0-baseline.md`](priority0-baseline.md). Cross-platform interactive acceptance remains open.

1. Read this context alongside README, `ACCEPTANCE.md`, `HUMAN_TESTING.md`, release/installation guidance, source, and tests.
2. Record checkout commit, working tree state, actual `rat --version`/`rat --help`, test counts, build/smoke results, and available shells/platforms.
3. Repeat `scripts/benchmark_prompt.py` for source and installed executable using the same scenarios/sample count; store raw measurements outside the repository and record medians/p95.
4. Run the disposable-profile install/uninstall/manual checklist on each available shell. Keep live GNOME and unavailable OS/shell checks explicitly marked pending.

**Exit condition:** A dated, reproducible baseline distinguishes automated checks, manual checks, skips, and unavailable environments.

## Priority 1 — Prompt startup and useful context

The current measured full-process latency exceeds the approximately 50 ms target. Profile first; avoid speculative caching or a daemon.

1. Break down startup time across interpreter startup, imports, config, terminal detection, environment probes, Git, and output.
2. Reduce imports on the prompt path; keep Typer/Rich/Pygments out of prompt execution and avoid optional tool subprocesses per prompt.
3. Evaluate replacing or reducing the prompt-path dependency on heavyweight modules, while keeping one source of truth for configuration, escaping, theme, and shell formatting.
4. Preserve Git timeout/fallback semantics and accurately distinguish unknown status from clean status.
5. Add benchmark comparison evidence and subprocess-level regression coverage. Avoid brittle hard CI timing failures across heterogeneous runners.

**Acceptance:** Materially lower median and p95 in repeated installed-process measurements on supported Python versions, with all prompt output and failure fallbacks intact. Reassess the 50 ms goal using more than one OS before making a universal claim.

## Priority 2 — Filesystem performance and output quality

1. Add bounded/streaming directory traversal or a clearly documented scan limit so `--max-entries` bounds work as well as display where feasible.
2. Define consistent behavior for inaccessible directories, permission errors, broken symlinks, huge directories, and filenames containing control characters.
3. Consider a true long listing with permissions, modified time, and optional owner where portable; preserve current size listing and do not silently change `--long` semantics.
4. Add useful sorting and extension/type filters only if they remain simple and consistent across text and JSON output.
5. Evaluate `rat find` as a bounded local filename search (ignore rules, hidden-file behavior, symlink policy, output cap, JSON schema). Keep content search separate due to privacy, binary, and performance implications.
6. Keep JSON schemas versioned and update documentation/tests in the same change.

**Acceptance:** Large-directory cost and limits are explicit and tested; text/JSON remain stable and terminal-safe.

## Priority 3 — Prompt and diagnostic context

1. Evaluate project-root discovery for common markers (Git root, pyproject, package manifests) without repeated expensive filesystem walks.
2. Improve Node/toolchain context only if it can be collected without making each prompt slower (for example, show declared project/environment state rather than shelling out to version managers).
3. Add opt-in indicators for active toolchains such as Conda, Poetry/uv, Node version managers, and containers only where reliable and cheap.
4. Make `doctor` distinguish unavailable, unsupported, and misconfigured states and give actionable but read-only guidance.
5. Add debug/trace output only if it avoids leaking environment secrets or local file contents.

**Acceptance:** New prompt segments are configurable, cheap, escaped, and do not misreport absent data as healthy/clean.

## Priority 4 — Shell support and lifecycle confidence

1. Close acceptance gaps for Bash, Zsh, and PowerShell, including aliases/functions, existing prompts, PATH, noninteractive use, redirection, pipes, status codes, Ctrl+C/Ctrl+D, history, completion, and background jobs.
2. Run the manual checklist on native Windows, macOS, and Linux; record PowerShell version and terminal details.
3. Validate terminal OSC reset and GNOME apply/restore on actual compatible terminals/desktops.
4. Consider Fish integration as the next shell only after specifying native fallback, prompt composition, profile ownership, uninstall, and real Fish tests. Keep cmd support a separate decision.
5. Improve install/doctor feedback where manual testing shows confusion; retain preview, backup, idempotency, and narrow removal.

**Acceptance:** No unsupported platform is advertised; unavailable interactive checks remain visible as gaps rather than inferred passes.

## Priority 5 — Read-only developer utilities

Evaluate additions based on repeated user need and implementation cost:

- Git diff/stat/log presentation, with pager/TTY/large-output limits and no writes.
- Project-aware `rat open` only if it delegates to the user's configured tool and has predictable fallback behavior.
- Local port/process inspection only with clear OS-specific behavior and no privileged actions.
- Shell completions and concise command examples to improve discoverability.

Start with one feature, define its contract, and keep it composable with existing native tools. Do not add a broad dashboard or duplicate mature command-line applications.

## Priority 6 — Configuration, themes, packaging

1. Consider config schema versioning and explicit migrations before adding settings that materially alter existing behavior.
2. Evaluate user-defined local theme files with strict schema validation and safe fallback; avoid remote theme downloads/marketplaces in this plan.
3. Review theme contrast/accessibility and narrow-terminal/ASCII output in manual checks.
4. Keep license/release decisions with the maintainer; verify packaging metadata and fresh install for any code change.

## Deferred ideas

Do not include plugins, AI command execution, cloud sync, telemetry, remote execution, animations, persistent daemon/cache, command history manager, notifications, or write-capable Git in this enhancement cycle. Revisit only with a concrete user problem, scoped design, and explicit privacy/compatibility review.

## Delivery sequence

1. Establish baseline and close measurable platform acceptance.
2. Profile and improve prompt startup.
3. Address filesystem work bounds and listing usability.
4. Add only the most valuable prompt/doctor context improvements.
5. Decide whether to implement Fish after its compatibility design and test environment exist.
6. Select one read-only developer utility based on user feedback.
7. Reassess configuration/theme extensibility and release readiness.

For each implementation phase, update the context document when actual behavior changes, add focused regression coverage, update README and acceptance guidance, and record evidence and remaining platform gaps. This is a proposal, not a claim that the listed features are implemented.
