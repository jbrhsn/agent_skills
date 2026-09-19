#!/usr/bin/env bash
# Check the runner without installing packages or creating a project environment.
set -uo pipefail

if command -v uv >/dev/null 2>&1; then
  uv --version
  echo "STATUS: UV_READY"
  echo "Run Python helpers with uv run and their resolved installed paths."
  exit 0
fi

echo "STATUS: UV_MISSING"
echo "Ask the user to confirm installing uv, then use the official installation method:"
echo "https://docs.astral.sh/uv/getting-started/installation/"
echo "Do not substitute bare Python. Continue independent browser research if useful."
exit 2
