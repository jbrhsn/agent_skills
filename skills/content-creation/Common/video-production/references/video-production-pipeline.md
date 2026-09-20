# Video Production Pipeline — Technical Reference

Agent-facing technical reference for the `video-production` skill. Load this at the start of every new project and before writing any code.

---

## 1. Asset management

### Cache directory convention

All reusable model assets live under `{repo-root}/.video_production_assets/` — at the root of the repository the user is working in. This directory is gitignored and shared across all video projects in that repo.

```
{repo-root}/.video_production_assets/
└── kokoro/
    ├── kokoro-v1.0.onnx          ← FP32 ONNX model (~330 MB)
    └── voices-v1.0.bin           ← all 54 voices (~200 MB)
```

Always resolve the repo root by walking up from the current working directory to find the `.git` folder (or the first directory containing `AGENTS.md`, `.opencode.json`, or similar). Never hard-code an absolute path to the assets directory in a script or config file.

### Gitignore rules

Add the following to the containing repository's `.gitignore`. Check for existing entries before adding; do not duplicate:

```gitignore
# Video production assets (large models, not for version control)
.video_production_assets/

# Local Remotion video production workspaces
**/remotion-infographic/
**/remotion-infographic/*
```

---

## 2. Kokoro TTS — `scripts/01_tts.py`

### CLI contract

```
uv run 01_tts.py \
  --text path/to/transcript.txt \
  --voice VOICE_ID \
  --assets-dir path/to/.video_production_assets \
  --out-dir path/to/remotion-infographic/public/audio
```

### Transcript format

The input `transcript.txt` uses `---` on its own line as the scene separator. Scenes are numbered from 1. Whitespace-only content between separators is skipped.

```
This is the narration for scene one. It covers the hook.
---
Scene two builds on the hook with supporting evidence.
---
Scene three delivers the practical takeaway.
```

### Output contract

For N scenes the script writes:

- `public/audio/scene-1.wav` … `scene-N.wav` — 24 kHz, mono, normalized float32 WAV
- `public/audio/metadata.json` — structured synthesis metadata

`metadata.json` schema:

```json
{
  "voice": "af_heart",
  "generated_at": "2025-09-20T08:00:00Z",
  "scenes": [
    {
      "scene": 1,
      "file": "scene-1.wav",
      "duration_s": 4.23,
      "text": "This is the narration for scene one. It covers the hook."
    }
  ]
}
```

### Error handling

The script exits with a non-zero code and a clear message if:
- The assets directory is missing or incomplete (instructs user to run `04_setup_assets.sh`)
- A scene produces zero audio samples (empty text after stripping)
- The output directory cannot be created

---

## 3. Whisper timestamps — `scripts/02_timestamps.py`

### CLI contract

```
uv run 02_timestamps.py \
  --audio path/to/public/audio/scene-N.wav \
  --model base \
  --out path/to/public/audio/scene-N-timestamps.json
```

Supported `--model` values: `tiny`, `base`, `small`, `medium`, `large`. Default: `base`. The model downloads automatically to `~/.cache/whisper/` on first use.

### Output schema

```json
{
  "scene": "scene-1",
  "audio_file": "scene-1.wav",
  "duration_s": 4.23,
  "words": [
    { "word": "This",    "start": 0.00, "end": 0.18 },
    { "word": "is",      "start": 0.20, "end": 0.28 },
    { "word": "the",     "start": 0.30, "end": 0.36 },
    { "word": "hook.",   "start": 0.38, "end": 0.60 }
  ]
}
```

Timing values are in seconds (floats, two decimal places). The `words` array may be empty for scenes with audio shorter than 0.5 s; this is valid and the captions component will simply render nothing.

---

## 4. Storyboard JSON schema

Write this file to `{project-dir}/storyboard.json` after the creative direction is approved. Derive `duration_s` and `duration_frames` from `metadata.json`.

```json
[
  {
    "scene": 1,
    "title": "Hook",
    "duration_s": 4.23,
    "duration_frames": 127,
    "audio_file": "scene-1.wav",
    "timestamps_file": "scene-1-timestamps.json",
    "narration": "This is the narration for scene one. It covers the hook.",
    "hold_frames": 15,
    "visual_direction": {
      "background": "#0f172a",
      "palette": {
        "primary": "#38bdf8",
        "text": "#f0f9ff",
        "muted": "#94a3b8"
      },
      "layout": "full-bleed-text",
      "caption_style": "word-highlight",
      "caption_position": "bottom",
      "elements": [
        {
          "type": "heading",
          "text": "The Hook Statement",
          "style": { "fontSize": 64, "fontWeight": "bold", "color": "#f0f9ff" },
          "animation": "fade-up",
          "enter_frame": 0,
          "exit_frame": null
        },
        {
          "type": "subtext",
          "text": "A supporting detail",
          "style": { "fontSize": 36, "color": "#94a3b8" },
          "animation": "fade-up",
          "enter_frame": 12,
          "exit_frame": null
        }
      ],
      "camera_move": null
    }
  }
]
```

### Element types

| `type` | Description |
|---|---|
| `heading` | Large display text |
| `subtext` | Smaller supporting text |
| `stat` | A big number or metric with an optional label |
| `diagram` | SVG-based flow or relationship diagram |
| `comparison` | Side-by-side before/after or A vs B layout |
| `list` | Staggered bullet or numbered list |
| `image` | Raster image from `public/` |
| `highlight-box` | Colored card or callout background |

### Animation values

`"fade-up"`, `"fade-in"`, `"scale-in"`, `"slide-left"`, `"slide-right"`, `"stagger"` (for list items), `"none"`.

`enter_frame` is relative to the scene's local frame 0. `exit_frame: null` means the element stays until the end of the scene.

---

## 5. Remotion project structure

### `src/config.ts`

```typescript
// src/config.ts
// Auto-generated by 03_scaffold.py — edit to adjust timing or dimensions.
export const VIDEO_CONFIG = {
  fps: 30,
  width: 1080,
  height: 1920,
} as const;

// Scene timing — derived from storyboard.json. Update if you re-synthesize audio.
export const SCENES: Array<{
  id: string;
  durationFrames: number;
  audioFile: string;
  timestampsFile: string;
}> = [
  { id: "Scene1", durationFrames: 127, audioFile: "audio/scene-1.wav", timestampsFile: "audio/scene-1-timestamps.json" },
  // …additional scenes
];

export const TOTAL_FRAMES = SCENES.reduce((sum, s) => sum + s.durationFrames, 0);
export const LAST_FRAME = TOTAL_FRAMES - 1;
```

### `src/index.ts`

```typescript
import { registerRoot } from "remotion";
import { Root } from "./Root";
registerRoot(Root);
```

### `src/Root.tsx`

```tsx
import React from "react";
import { Composition, Series } from "remotion";
import { VIDEO_CONFIG, SCENES, TOTAL_FRAMES } from "./config";
import { Scene1 } from "./scenes/Scene1";
// import additional scene components

const VideoFull: React.FC = () => (
  <Series>
    <Series.Sequence durationInFrames={SCENES[0].durationFrames}>
      <Scene1 />
    </Series.Sequence>
    {/* Additional Series.Sequence entries per scene */}
  </Series>
);

export const Root: React.FC = () => (
  <>
    {/* Master composition — full video */}
    <Composition
      id="VideoFull"
      component={VideoFull}
      durationInFrames={TOTAL_FRAMES}
      fps={VIDEO_CONFIG.fps}
      width={VIDEO_CONFIG.width}
      height={VIDEO_CONFIG.height}
    />
    {/* Per-scene compositions for isolated preview */}
    <Composition
      id="Scene1"
      component={Scene1}
      durationInFrames={SCENES[0].durationFrames}
      fps={VIDEO_CONFIG.fps}
      width={VIDEO_CONFIG.width}
      height={VIDEO_CONFIG.height}
    />
    {/* Additional scene compositions */}
  </>
);
```

### `src/scenes/SceneN.tsx` — template

```tsx
import React from "react";
import { Audio, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { staticFile } from "remotion";
// @ts-expect-error — JSON import; ensure resolveJsonModule:true in tsconfig
import timestampData from "../../public/audio/scene-N-timestamps.json";
import { Captions } from "@remotion/captions";

// Derive frame timing from storyboard values
const HOLD_FRAMES = 15;

export const SceneN: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Heading fade-up
  const headingOpacity = interpolate(frame, [0, 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const headingY = interpolate(frame, [0, 12], [30, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <div style={{ width, height, background: "#0f172a", position: "relative", overflow: "hidden", fontFamily: "sans-serif" }}>
      {/* Voiceover audio — plays from local frame 0 */}
      <Audio src={staticFile("audio/scene-N.wav")} />

      {/* Heading element */}
      <div
        style={{
          position: "absolute",
          top: "20%",
          left: 48,
          right: 48,
          opacity: headingOpacity,
          transform: `translateY(${headingY}px)`,
          fontSize: 64,
          fontWeight: "bold",
          color: "#f0f9ff",
          lineHeight: 1.2,
        }}
      >
        Scene heading text
      </div>

      {/* Word-highlight captions — bottom third */}
      <div style={{ position: "absolute", bottom: 160, left: 32, right: 32 }}>
        <Captions
          words={timestampData.words}
          currentTime={frame / fps}
          // Style props depend on @remotion/captions version; see its docs
        />
      </div>
    </div>
  );
};
```

Replace placeholder values (`scene-N`, heading text, positions, colors) with scene-specific values from `storyboard.json`. Keep all animation values derived from `frame` — never from `Date.now()` or CSS transitions.

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react",
    "strict": true,
    "resolveJsonModule": true,
    "esModuleInterop": true,
    "outDir": "dist"
  },
  "include": ["src"]
}
```

### `package.json` (pinned dependencies)

```json
{
  "name": "video-production",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "studio": "npx remotion studio src/index.ts",
    "typecheck": "tsc --noEmit",
    "render": "npx remotion render src/index.ts VideoFull out/video.mp4 --codec=h264 --pixel-format=yuv420p",
    "hero": "npx remotion still src/index.ts VideoFull out/video-hero.png --frame=LAST_FRAME_PLACEHOLDER",
    "preview-scene": "npx remotion render src/index.ts"
  },
  "dependencies": {
    "remotion": "4.0.0",
    "@remotion/media": "4.0.0",
    "@remotion/captions": "4.0.0",
    "react": "18.3.1",
    "react-dom": "18.3.1"
  },
  "devDependencies": {
    "typescript": "5.4.0",
    "@types/react": "18.3.1"
  }
}
```

Pin `remotion` and all `@remotion/*` packages to the same version. Check the [Remotion changelog](https://www.remotion.dev/docs/changelog) for the current stable release before scaffolding a new project.

---

## 6. Render commands

### Preview a single scene

```bash
cd remotion-infographic
npx remotion render src/index.ts SceneN out/scenes/scene-N-preview.mp4 --codec=h264 --pixel-format=yuv420p
```

### Full video

```bash
cd remotion-infographic
npx remotion render src/index.ts VideoFull out/video.mp4 --codec=h264 --pixel-format=yuv420p
```

### Hero PNG

Derive `LAST_FRAME` as `TOTAL_FRAMES - 1`. Never hard-code; derive it from `metadata.json` total duration × fps − 1.

```bash
cd remotion-infographic
npx remotion still src/index.ts VideoFull out/video-hero.png --frame=<LAST_FRAME>
```

### Verify with ffprobe

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,duration -of json out/video.mp4
```

---

## 7. Audio synchronization checklist

- Each `SceneN.tsx` mounts `<Audio src={staticFile("audio/scene-N.wav")} />` at the start of the scene's local timeline (frame 0 after the enclosing `<Series.Sequence>` shifts the origin).
- Do not use `from` or `trimBefore` on the Audio component unless the WAV has intentional leading silence.
- All caption timing uses `currentTime = frame / fps` in seconds, matching the timestamps extracted by Whisper from the same WAV file.
- If the audio duration and `durationFrames` differ by more than 0.1 s, re-derive `durationFrames` from `metadata.json` and update `storyboard.json` and `src/config.ts`.
- Whisper's `word_timestamps=True` timestamps are relative to the start of the audio file — they align directly with frame 0 of the scene.

---

## 8. Verification steps

Follow the verification checklist in [../remotion-infographics/references/remotion-production.md](../remotion-infographics/references/remotion-production.md) §Verification and completion for rendering standards. Additional checks specific to narrated video:

1. After rendering each scene preview: confirm audio is audible, captions appear and advance word-by-word, no black frames at start or end.
2. After the full merge: use `ffprobe` to confirm total duration matches `sum(scene.duration_s)` within ±0.1 s.
3. The hero PNG must be the settled final hero frame. Decode the MP4's last frame and compare visually; expect H.264 compression differences from the PNG, not content differences.
4. Do not claim audio playback was verified from a still-frame inspection alone.

