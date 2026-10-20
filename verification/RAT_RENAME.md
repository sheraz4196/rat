# Rat 0.1.1 rename verification

Verified on Ubuntu with Python 3.14, 2026-10-21. These results describe the Rat rename, not the historical Crux implementation report.

- Checkout suite: **108 passed, 2 skipped** (`python -m pytest -q -rs`). The two skipped integration tests require unavailable local Zsh and PowerShell executables.
- Build: wheel and source archive generated successfully using `python -m build --no-isolation` with the existing development build dependencies.
- Clean wheel installation: **58 smoke checks passed** outside the checkout, exercising both `rat` and `python -m rat`. Python socket connections and DNS were blocked during runtime smoke checks; dependency installation used a local wheelhouse.
- Source installer: isolated install/link, alias/function/PATH/prompt preservation, one-time backup, repeated install, uninstall and unrelated-executable refusal all passed using a disposable home.
- Extracted source archive: **108 passed, 2 skipped**; the same installer verification passed from its extracted source tree.
- Archive inspection: wheel entry point is `rat = rat.cli.entry:main`; runtime package is `rat`, with no `crux` package. Source archive includes `HUMAN_TESTING.md`, `MIGRATING.md` and `RAT_PROJECT_DEFINITION.md`.
- `git diff --check` passed. The existing `v0.1.0` tag remains intact.

Artifacts are `dist/rat_terminal-0.1.1-py3-none-any.whl`, `dist/rat_terminal-0.1.1.tar.gz`, and `dist/SHA256SUMS` (generated locally, ignored by Git). GitHub builds its own artifacts from the release tag and generates matching checksums there.

The canonical GitHub repository was confirmed as `sheraz4196/rat`, and the original Crux URL redirects to it. The local origin now uses the Rat SSH URL. The rename commits are pushed on `fix-renaming-for-launch`.

Hosted CI for candidate `93e9a75` passed all six combinations: Ubuntu, macOS and Windows on Python 3.11 and 3.14. Evidence: [successful matrix run](https://github.com/sheraz4196/rat/actions/runs/39508424418). Both edited workflows also passed `actionlint` v1.7.7. The release workflow independently repeats the full matrix for the tag before publishing.

Interactive desktop acceptance remains unverified; use the clone-first human guide and record each platform/shell/terminal result separately. Automated CI passing does not establish visual terminal behavior.
