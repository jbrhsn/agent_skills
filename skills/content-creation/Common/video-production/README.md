# Video Production

Narrated, audio-synchronized Remotion video from an article or idea. The skill drives a 7-phase pipeline entirely on your local machine: voiceover transcript → Kokoro TTS synthesis → Whisper word-level timestamps → scene storyboard → Remotion project scaffold → per-scene composition with captions → scene review gates → final merged MP4 + hero PNG.

---

## Prerequisites

### System dependencies

| Tool | Install | Notes |
|---|---|---|
| Node.js ≥ 18 | `brew install node` | Required by Remotion |
| Python ≥ 3.11 | `brew install python` | Required by the three scripts |
| `uv` | `pip install uv` | Script runner (PEP 723) |
| `espeak-ng` | `brew install espeak-ng` | Kokoro phoneme conversion |
| `ffmpeg` | `brew install ffmpeg` | Remotion rendering backend |

### Python packages (installed per-script via `uv run`)

| Package | Used by |
|---|---|
| `kokoro-onnx` | `01_tts.py` |
| `soundfile` | `01_tts.py` |
| `numpy` | `01_tts.py` |
| `openai-whisper` | `02_timestamps.py` |

No global `pip install` is needed — `uv run` handles isolated installs automatically from the PEP 723 headers in each script.

---

## One-time asset setup

Download the Kokoro ONNX model and voices file into the shared asset cache. Run this once per machine from the repo root:

```bash
bash skills/content-creation/Common/video-production/scripts/04_setup_assets.sh
```

This places files into `{repo-root}/.video_production_assets/kokoro/`:
- `kokoro-v1.0.onnx` (~330 MB FP32)
- `voices-v1.0.bin` (~54 voices)

The Whisper model downloads automatically into `~/.cache/whisper/` on first use of `02_timestamps.py`.

---

## Project layout

When the skill runs, it creates or updates a Remotion workspace **beside** your content file. The default workspace name is `remotion-infographic/`; the user can specify any folder:

```
your-project/
├── source.md                        ← your article or idea
├── transcript.txt                   ← generated, you approve it
├── storyboard.json                  ← generated, you approve it
└── remotion-infographic/
    ├── package.json
    ├── tsconfig.json
    ├── src/
    │   ├── config.ts                ← shared dimensions, fps, scene timings
    │   ├── index.ts
    │   ├── Root.tsx                 ← Series master + per-scene compositions
    │   └── scenes/
    │       ├── Scene1.tsx
    │       └── SceneN.tsx
    └── public/
        └── audio/
            ├── scene-1.wav
            ├── scene-1-timestamps.json
            ├── scene-N.wav
            ├── scene-N-timestamps.json
            └── metadata.json
```

---

## Pipeline phases

| Phase | What happens | User gate |
|---|---|---|
| 1a | Voiceover transcript drafted | ✅ Approve transcript |
| 1b | Kokoro TTS synthesizes WAV per scene | — |
| 2 | Whisper extracts word-level timestamps | — |
| 3a | Creative direction presented | ✅ Approve style + palette |
| 3b | Storyboard JSON built | ✅ Approve storyboard |
| 4 | Remotion project scaffolded | — |
| 5 | Scene TSX files composed with audio + captions | — |
| 6 | Each scene rendered as preview MP4 | ✅ Approve each scene |
| 7 | Full video merged, hero PNG rendered, delivered | — |

---

## Voices

See [references/kokoro-voices.md](references/kokoro-voices.md) for the full list of 54 Kokoro v1.0 voices. Default: `af_heart` (American Female, warm). The agent will suggest alternatives during Phase 1a.

---

## Caption styles

| Style | Description |
|---|---|
| `word-highlight` | Current word highlighted, others dimmed (TikTok/Reels standard) |
| `popping-word` | Each word pops in with a scale animation |
| `moving-pill` | A pill background slides to each word |

---

## Gitignore

The skill automatically adds these rules to the containing repo's `.gitignore`:

```gitignore
# Video production assets (large models)
.video_production_assets/

# Local Remotion video production workspaces
**/remotion-infographic/
**/remotion-infographic/*
```

---

## References

- [SKILL.md](SKILL.md) — agent prompt and phase instructions
- [references/video-production-pipeline.md](references/video-production-pipeline.md) — technical contracts, schemas, TypeScript templates
- [references/kokoro-voices.md](references/kokoro-voices.md) — voice reference
- [../remotion-infographics/references/retention-and-styles.md](../remotion-infographics/references/retention-and-styles.md) — visual style and retention research guidance (shared)
- [../remotion-infographics/references/remotion-production.md](../remotion-infographics/references/remotion-production.md) — Remotion render, verification, and delivery standards (shared)

