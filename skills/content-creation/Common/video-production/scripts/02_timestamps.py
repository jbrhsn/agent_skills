#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "openai-whisper>=20231117",
# ]
# ///
"""
02_timestamps.py — Whisper word-level timestamp extractor

Transcribes a single scene WAV file using OpenAI Whisper with
word_timestamps=True and writes a structured JSON file containing
word-level start/end times in seconds.

Usage:
    uv run 02_timestamps.py \\
        --audio path/to/public/audio/scene-N.wav \\
        --model base \\
        --out path/to/public/audio/scene-N-timestamps.json

The output JSON is consumed by the Remotion scene components to drive
@remotion/captions word-highlight subtitle rendering.

Supported --model values: tiny, base, small, medium, large
Default: base  (best speed/quality balance for typical narration audio)

First run downloads the model to ~/.cache/whisper/ automatically.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import whisper


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Extract word-level timestamps from a voiceover WAV using Whisper.")
    p.add_argument("--audio", required=True, help="Path to the input WAV file (scene-N.wav).")
    p.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"],
                   help="Whisper model size (default: base).")
    p.add_argument("--out", required=True, help="Path to write the output JSON file.")
    p.add_argument("--language", default=None,
                   help="Force a specific language code (e.g. 'en'). Auto-detected if omitted.")
    return p.parse_args()


def extract_words(result: dict) -> list[dict]:
    """Flatten word-level entries from all segments into a single list."""
    words: list[dict] = []
    for segment in result.get("segments", []):
        for w in segment.get("words", []):
            word_text = w.get("word", "").strip()
            if not word_text:
                continue
            words.append(
                {
                    "word": word_text,
                    "start": round(float(w["start"]), 4),
                    "end": round(float(w["end"]), 4),
                }
            )
    return words


def get_audio_duration(audio_path: Path) -> float:
    """Return duration in seconds using soundfile if available, else fall back to Whisper's result."""
    try:
        import soundfile as sf  # optional; not in PEP 723 deps to keep this script lean
        info = sf.info(str(audio_path))
        return round(info.duration, 4)
    except ImportError:
        return 0.0


def main() -> None:
    args = parse_args()
    audio_path = Path(args.audio).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()

    if not audio_path.exists():
        print(f"ERROR: audio file not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Loading Whisper model '{args.model}' (downloads on first use to ~/.cache/whisper/)...")
    model = whisper.load_model(args.model)

    transcribe_kwargs: dict = {"word_timestamps": True}
    if args.language:
        transcribe_kwargs["language"] = args.language

    print(f"Transcribing: {audio_path.name}")
    result = model.transcribe(str(audio_path), **transcribe_kwargs)

    words = extract_words(result)

    # Derive duration: prefer soundfile info; fall back to last word end time
    duration_s = get_audio_duration(audio_path)
    if duration_s == 0.0 and words:
        duration_s = words[-1]["end"]

    # Derive scene name from the audio filename (e.g. "scene-2.wav" → "scene-2")
    scene_name = audio_path.stem  # filename without extension

    output = {
        "scene": scene_name,
        "audio_file": audio_path.name,
        "duration_s": round(duration_s, 4),
        "language": result.get("language", args.language or "unknown"),
        "words": words,
    }

    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  → {len(words)} words extracted, {duration_s:.2f}s duration")
    print(f"  → Written to: {out_path}")


if __name__ == "__main__":
    main()

