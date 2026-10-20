#!/bin/sh
# Install into an isolated environment; no activation needed.
set -eu
RAT_SOURCE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
RAT_HOME="${XDG_DATA_HOME:-$HOME/.local/share}/rat"
RAT_BIN="$HOME/.local/bin"
# Check ownership before touching the installation environment.
if [ -e "$RAT_BIN/rat" ] && [ ! -L "$RAT_BIN/rat" ]; then
  echo "Refusing to replace $RAT_BIN/rat; remove or rename it first." >&2
  exit 1
fi
if [ -L "$RAT_BIN/rat" ] && [ "$(readlink "$RAT_BIN/rat")" != "$RAT_HOME/venv/bin/rat" ]; then
  echo "Refusing to replace an unrelated Rat link: $RAT_BIN/rat" >&2
  exit 1
fi
if [ -L "$RAT_HOME/venv" ]; then
  echo "Refusing to install into a symlinked environment: $RAT_HOME/venv" >&2
  exit 1
fi
if [ -e "$RAT_HOME/venv" ]; then
  if [ ! -x "$RAT_HOME/venv/bin/python" ]; then
    echo "Existing Rat environment is incomplete: $RAT_HOME/venv; inspect it before retrying." >&2
    exit 1
  fi
else
  python3 -m venv "$RAT_HOME/venv"
fi
"$RAT_HOME/venv/bin/python" -m pip install "$RAT_SOURCE"
mkdir -p "$RAT_BIN"
ln -sfn "$RAT_HOME/venv/bin/rat" "$RAT_BIN/rat"
export PATH="$RAT_BIN:$PATH"
"$RAT_BIN/rat" install --yes "$@"
printf '%s\n' 'Rat installed. Open a new terminal; no virtual environment activation is needed.'
printf '%s\n' 'Integration leaves PATH unchanged. Ensure ~/.local/bin is on your existing PATH for new shells.'
