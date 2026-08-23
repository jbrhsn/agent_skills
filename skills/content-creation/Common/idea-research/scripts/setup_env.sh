#!/usr/bin/env bash
# Prepare the Python environment for idea-research.
# Scripts are stdlib-only, so there is nothing to install — this only ensures a
# runner exists and creates a venv when uv is available.
set -uo pipefail

if command -v uv >/dev/null 2>&1; then
  echo "uv: found ($(uv --version 2>/dev/null))"
  if [ ! -d ".venv" ]; then
    echo "uv: no .venv in $(pwd) — creating one"
    uv venv || { echo "STATUS: UV_VENV_FAILED"; exit 1; }
  else
    echo "uv: .venv already present"
  fi
  echo "STATUS: UV_READY"
  echo "Run scripts as: uv run scripts/<name>.py"
  exit 0
fi

echo "uv: NOT FOUND"
echo "STATUS: UV_MISSING"
echo
echo "ACTION REQUIRED — the agent must stop and ask the user:"
echo "  Install uv:  https://docs.astral.sh/uv/getting-started/installation/"
echo "  ...or confirm falling back to plain python3."
echo "Do NOT fall back to python3 without explicit user confirmation."
if command -v python3 >/dev/null 2>&1; then
  echo "(For reference, python3 is available: $(python3 --version 2>&1))"
else
  echo "(python3 is also unavailable — no fallback exists.)"
fi
exit 2
