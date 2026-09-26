#!/usr/bin/env bash
# Check the runner and target-project environment without modifying either.
set -uo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: bash $0 /absolute/research-project" >&2
  exit 2
fi

project="$1"
if [[ ! -d "$project" ]]; then
  echo "STATUS: PROJECT_MISSING $project" >&2
  exit 2
fi

interpreter="$project/.venv/bin/python"

if command -v uv >/dev/null 2>&1; then
  uv --version
  echo "STATUS: UV_READY"
  if [[ ! -x "$interpreter" ]]; then
    echo "STATUS: VENV_MISSING $interpreter"
    echo "Create it with: uv venv $project/.venv"
    exit 2
  fi
  echo "Run Python helpers with uv run --python $interpreter python and their resolved installed paths."
  exit 0
fi

echo "STATUS: UV_MISSING"
echo "Ask the user to confirm installing uv, then use the official installation method:"
echo "https://docs.astral.sh/uv/getting-started/installation/"
echo "Do not substitute bare Python. Continue independent browser research if useful."
exit 2
