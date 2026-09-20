#!/usr/bin/env bash
# 04_setup_assets.sh
# One-time download of Kokoro ONNX model and voices into .video_production_assets/kokoro/
#
# Run from the repository root:
#   bash skills/content-creation/Common/video-production/scripts/04_setup_assets.sh
#
# Re-running is safe — files that already exist are skipped.
#
# Requirements:
#   - curl  (pre-installed on macOS; or: brew install curl)
#   - huggingface-cli  (pip install huggingface_hub[cli])  ← preferred
#     OR curl as fallback for direct HF download
#
# The script downloads to:
#   {repo-root}/.video_production_assets/kokoro/kokoro-v1.0.onnx  (~330 MB)
#   {repo-root}/.video_production_assets/kokoro/voices-v1.0.bin   (~200 MB)

set -euo pipefail

# ---------------------------------------------------------------------------
# Resolve repo root: walk up until we find a .git directory or AGENTS.md
# ---------------------------------------------------------------------------
find_repo_root() {
  local dir
  dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  while [[ "$dir" != "/" ]]; do
    if [[ -d "$dir/.git" ]] || [[ -f "$dir/AGENTS.md" ]]; then
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  # Fallback: use the current working directory
  echo "$(pwd)"
}

REPO_ROOT="$(find_repo_root)"
ASSETS_DIR="${REPO_ROOT}/.video_production_assets/kokoro"

HF_REPO="onnx-community/Kokoro-82M-v1.0-ONNX"
MODEL_FILE="kokoro-v1.0.onnx"
VOICES_FILE="voices-v1.0.bin"

echo "=== Kokoro ONNX asset setup ==="
echo "Target directory: ${ASSETS_DIR}"
echo ""

mkdir -p "${ASSETS_DIR}"

# ---------------------------------------------------------------------------
# Helper: download a file from Hugging Face
# ---------------------------------------------------------------------------
download_hf_file() {
  local filename="$1"
  local dest="${ASSETS_DIR}/${filename}"

  if [[ -f "$dest" ]]; then
    local size
    size=$(du -sh "$dest" | cut -f1)
    echo "  [SKIP] ${filename} already exists (${size})"
    return 0
  fi

  echo "  [DOWNLOADING] ${filename} from ${HF_REPO}..."

  # Prefer huggingface-cli if available
  if command -v huggingface-cli &>/dev/null; then
    huggingface-cli download \
      "${HF_REPO}" \
      "${filename}" \
      --local-dir "${ASSETS_DIR}" \
      --local-dir-use-symlinks False
  else
    # Direct curl fallback via HF resolve endpoint
    local url="https://huggingface.co/${HF_REPO}/resolve/main/${filename}"
    echo "    huggingface-cli not found; falling back to curl"
    echo "    URL: ${url}"
    curl -L --progress-bar -o "${dest}" "${url}"
  fi

  if [[ -f "$dest" ]]; then
    local size
    size=$(du -sh "$dest" | cut -f1)
    echo "  [OK] ${filename} downloaded (${size})"
  else
    echo "  [ERROR] Download failed for ${filename}" >&2
    exit 1
  fi
}

# ---------------------------------------------------------------------------
# Download model and voices
# ---------------------------------------------------------------------------
download_hf_file "${MODEL_FILE}"
download_hf_file "${VOICES_FILE}"

echo ""
echo "=== Setup complete ==="
echo "Assets location: ${ASSETS_DIR}"
echo ""
echo "Next steps:"
echo "  1. Ensure espeak-ng is installed: brew install espeak-ng"
echo "  2. Run the TTS script:  uv run scripts/01_tts.py --help"

