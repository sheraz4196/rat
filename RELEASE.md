# Rat release preparation

The next release is **v0.1.1**, the Crux → Rat rename, under the MIT license. Keep Crux's existing `v0.1.0` tag/release intact. New wheels and source archives must use `rat_terminal`; changing a GitHub repository name alone does not regenerate package names or entry points. PyPI publication is not configured.

## Validate the release candidate

1. Read [MIGRATING.md](MIGRATING.md), [RELEASE_NOTES.md](RELEASE_NOTES.md) and [HUMAN_TESTING.md](HUMAN_TESTING.md). Record manual results honestly; CI does not establish desktop behavior.
2. Ensure `pyproject.toml`, `rat/__init__.py` and version expectations in tests agree on `0.1.1`.
3. In a Python 3.11+ development environment, run:

   ```sh
   python -m pip install -e '.[dev]'
   python -m pytest -q -rs
   python -m build
   python scripts/verify_wheel.py dist/rat_terminal-0.1.1-py3-none-any.whl
   ```

4. Extract the source archive into a fresh temporary directory. Run its tests from the extracted package root with the development interpreter, and run `scripts/verify_installer.py --source PATH_TO_EXTRACTED_ROOT` on Linux/macOS. Use disposable homes/profiles; do not test by overwriting personal startup files.
5. Inspect archives: only `rat` is the runtime package; entry points name `rat`; the sdist contains tests, migration and human guides. Do not upload old `crux_terminal` files left in a local `dist` directory.
6. Confirm native-shell tests execute in actual Ubuntu/macOS/Windows CI runs. The reusable tests workflow targets Python 3.11/3.14, and the release job depends on the whole matrix succeeding.

Use local wheels with `PIP_NO_INDEX=1` and `PIP_FIND_LINKS=PATH` for offline verification. `verify_installer.py` also accepts `--wheelhouse PATH`. Dependency installation needs network or a complete wheelhouse; runtime does not.

## Repository rename and publication

Repository rename, pushing commits/tags and release publication require authenticated GitHub access. The user has authorized these operations for this rename. If access is unavailable, leave the validated changes committed locally and report publication as pending.

After validation, rename the existing GitHub repository rather than creating a replacement, preserving issues, stars and history. With an authenticated GitHub CLI:

```sh
gh repo rename rat --repo sheraz4196/crux --yes
git remote set-url origin git@github.com:sheraz4196/rat.git
```

Update any external links/settings that cannot redirect. The clone-first testing guide intentionally retains the original URL with an explicit local `rat` directory; that URL redirects after a successful GitHub rename. Do not create another repository at the old name, which would replace the redirect.

Push the reviewed release commit on its branch. Create a new annotated tag at that exact commit only after local verification is complete, without moving old tags:

```sh
git push -u origin HEAD
git tag -a v0.1.1 -m 'Rat v0.1.1: rename Crux terminal toolkit'
git push origin v0.1.1
```

If the tag already exists, inspect its target instead of overwriting it. The tag-triggered release workflow first runs the six platform/Python combinations, then tests/builds on Ubuntu, checks tag/version agreement, verifies wheel/source installation and generates SHA-256 checksums. Only after success does it publish the new Rat release using `RELEASE_NOTES.md`. Do not separately create a competing manual release while that workflow runs.

Check the actual workflow and published artifacts, not just the successful push:

```sh
gh run list --repo sheraz4196/rat --workflow release.yml
gh release view v0.1.1 --repo sheraz4196/rat
```

Expected release title: `Rat v0.1.1`. Assets: `rat_terminal-0.1.1-py3-none-any.whl`, `rat_terminal-0.1.1.tar.gz`, and `SHA256SUMS`. Download and verify their checksums before announcing. If CI fails, fix the issue and follow an explicit release/tag correction decision; do not silently force-update a published tag.

## Platform status

A configured matrix is not evidence that it passed. Local Linux results, skipped shells, hosted CI results and interactive Windows/macOS results must be reported separately. Native PowerShell wrappers, Fish and cmd integration remain unsupported. Runtime networking, telemetry, remote execution and theme downloads remain outside scope.
