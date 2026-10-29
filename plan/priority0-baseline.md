# Priority 0 — RAT baseline results

Date: 2026-10-30  
Scope: Local baseline for the Priority 0 work in [`plan-rat-enhancements.md`](plan-rat-enhancements.md).

## Checkout and environment

- Starting checkout: `6897cf4e21ec6d6c8650d1d851ebd9d075c6eae3` (`docs: record successful Windows macOS and Linux CI matrix`, tagged `v0.1.1`). The working tree was clean before this task.
- Work branch: `work/priority-0-baseline`.
- RAT version: `0.1.1`; `rat --help` lists the public doctor, ls, tree, install/uninstall, theme, view, config, and git command groups.
- Host: Linux x86_64, kernel `7.0.0-38-generic`; Bash `5.3.9`; Python `3.14.3`; Git `2.53.0`.
- `python` is not on PATH; checks used `.venv/bin/python` or `python3`.
- Zsh, PowerShell (`pwsh`), and Fish are unavailable. Native macOS and Windows were not available for manual checks.
- Installed executable before reinstall: `/home/sheraz-manzoor/.local/bin/rat`, linked to the isolated install at `/home/sheraz-manzoor/.local/share/rat/venv/bin/rat`.
- `rat doctor --json`: config valid; Bash integration installed; native wrappers disabled; GNOME Terminal session and its `gsettings`/`dconf` commands detected; duplicate PATH entries warning reported. Doctor was run non-interactively, so it reports terminal color/interactivity as unavailable in this session.

## Automated checks

| Check | Result |
| --- | --- |
| `.venv/bin/python -m pytest -q -rs` | **108 passed, 2 skipped** in 7.44 s. Skips: real Zsh and PowerShell tests; executables unavailable. |
| `.venv/bin/python -m build --no-isolation --outdir /tmp/rat-priority0-dist` | Source archive and universal wheel built successfully. |
| `scripts/smoke_installed.py` against the existing isolated installation | **58 checks passed** for executable and module entry points; Python socket connections and DNS blocked; local Git covered. |
| Disposable Bash profile install/uninstall | Dry run made no changes; one marked block and one backup created; existing `ls` alias still ran; uninstall restored exact original bytes; repeated uninstall was a no-op. |
| `rat --version`, `rat --help`, `rat doctor --json` | Version/help succeeded; diagnostic state recorded above. |

## Prompt benchmark

Commands, each with 30 samples and temporary directories/config/repositories:

```sh
.venv/bin/python scripts/benchmark_prompt.py --samples 30 --output /tmp/rat-priority0-source-benchmark.json
.venv/bin/python scripts/benchmark_prompt.py --executable /home/sheraz-manzoor/.local/share/rat/venv/bin/rat --samples 30 --output /tmp/rat-priority0-benchmark.json
```

Times below are median / p95 milliseconds. They include complete process startup. The raw JSON files are outside the repository and are machine-specific.

| Scenario | Source | Installed executable |
| --- | ---: | ---: |
| Outside repository, missing config | 82.844 / 96.003 | 93.680 / 138.564 |
| Clean repository | 86.274 / 92.249 | 83.208 / 91.740 |
| Dirty repository | 87.161 / 94.290 | 89.064 / 100.386 |
| Clean repository, 1,000 files | 96.607 / 120.546 | 96.362 / 106.984 |
| Dirty repository, 1,000 files | 95.864 / 127.529 | 99.138 / 117.486 |
| Repository, optional tools unavailable | 90.635 / 118.664 | 95.089 / 132.941 |
| Invalid config | 88.590 / 118.343 | 81.130 / 99.835 |
| Optional tools unavailable | 97.007 / 141.145 | 78.190 / 96.715 |

Every measured median exceeds the approximately 50 ms goal. These results justify profiling in Priority 1; they do not justify a daemon or cache by themselves.

## Hosted and manual coverage

- `verification/RAT_RENAME.md` records that hosted CI candidate `93e9a75` passed Ubuntu, macOS, and Windows on Python 3.11 and 3.14 ([workflow run](https://github.com/sheraz4196/rat/actions/runs/39508424418)). This is repository-recorded prior evidence, not a new workflow run triggered by this task.
- Local disposable Bash profile lifecycle passed as described above. The current personal profile was not used for this disposable test.
- Not performed: interactive keyboard/history/completion/job-control checks; native macOS/Windows checks; real Zsh/PowerShell; live GNOME color apply/restore; terminal emulator OSC reset verification. Keep these acceptance items open.

## Priority 0 conclusion

Baseline requirements are complete for this available Linux/Bash environment. Results distinguish local automated checks, a disposable profile check, existing hosted CI evidence, and unavailable or unperformed manual checks. Priority 1 can now compare prompt changes to the measurements above.
