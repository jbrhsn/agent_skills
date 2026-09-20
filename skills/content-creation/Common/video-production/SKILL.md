---
name: video-production
description: Produce a narrated, audio-synchronized multi-scene video from an article or idea. Generates a voiceover transcript, synthesizes speech with Kokoro TTS (local), extracts word-level timestamps with Whisper (local), designs a scene-by-scene storyboard, scaffolds and composes a Remotion project with captions, renders scene previews for approval, then merges into a final MP4 and hero PNG.
---

# Video Production

Turn the supplied article, `source.md`, draft, or idea into a narrated, multi-scene video. Deliver a merged MP4, a hero PNG from the exact final frame, and an editable Remotion project. All synthesis (TTS) and transcription (Whisper) run locally; no external audio APIs are used. Preserve the author's core message, opinions, voice, factual scope, and uncertainty throughout every phase.

Read [references/video-production-pipeline.md](references/video-production-pipeline.md) at the start of each new project and before writing any code. It contains the definitive technical contracts for every script, the storyboard JSON schema, the Remotion TypeScript patterns, and asset management rules. Load the `lean-coder` skill before writing or editing any code.

---

## Phase 1 — Transcript draft and voiceover synthesis

### 1a. Draft the voiceover transcript

Read the source material. Identify the audience, the single most valuable takeaway, and the evidence or story that supports it. Draft a narration script as plain prose — no bullet lists, no raw URLs. Divide it into scenes with a `---` separator on its own line. Each scene should take 3–8 seconds to speak at a natural pace (~2.5 words per second). Aim for 4–8 scenes for a 20–45 second video; longer videos require explicit user direction.

Present the full transcript to the user with a scene-by-scene breakdown (scene number, approximate duration in seconds, first and last sentence). Ask for approval or revision before proceeding. Do not treat silence as approval. An explicit "looks good" or "proceed" is required.

### 1b. Synthesize audio

After transcript approval, check that the Kokoro assets exist:

```
{repo-root}/.video_production_assets/kokoro/kokoro-v1.0.onnx
{repo-root}/.video_production_assets/kokoro/voices-v1.0.bin
```

If either file is missing, instruct the user to run `scripts/04_setup_assets.sh` from the skill directory and wait for confirmation before continuing.

Write the approved transcript to a plain text file at `{project-dir}/transcript.txt`, using `---` as the scene separator.

Run the TTS synthesizer. Replace `{voice}` with the user's chosen voice or the recommended default `af_heart`. Replace `{repo-root}` and `{project-dir}` with the actual paths:

```bash
uv run scripts/01_tts.py \
  --text {project-dir}/transcript.txt \
  --voice {voice} \
  --assets-dir {repo-root}/.video_production_assets \
  --out-dir {project-dir}/public/audio
```

Confirm that `public/audio/scene-N.wav` files and `public/audio/metadata.json` exist and are non-empty before proceeding. Report the duration of each audio file from `metadata.json`.

---

## Phase 2 — Timestamp extraction

Run the Whisper timestamp extractor for each scene audio file. Use model `base` unless the user specifies otherwise. Run sequentially; do not skip scenes with audio shorter than 0.5 s (they will produce an empty words array, which is valid):

```bash
uv run scripts/02_timestamps.py \
  --audio {project-dir}/public/audio/scene-N.wav \
  --model base \
  --out {project-dir}/public/audio/scene-N-timestamps.json
```

This phase is fully automated — no user gate is needed. Confirm each `scene-N-timestamps.json` is valid JSON with a `words` array before moving on.

---

## Phase 3 — Visual direction and storyboard

### 3a. Research and creative direction

Read [references/retention-and-styles.md](../remotion-infographics/references/retention-and-styles.md) before designing. Apply the same research standards as the `remotion-infographics` skill: separate platform guidance from observed popularity, prefer examples from the last 30–90 days, disclose when current research is inaccessible.

Ask the user for a visual theme and color scheme unless already supplied. Present at least five distinct style options, recommend one, and include a compact timed storyboard for the recommended direction. Offer two or three palettes with hex colors and background/text/accent roles. Describe caption style options (`word-highlight`, `popping-word`, `moving-pill`). Ask for approval or revisions before writing any files.

### 3b. Build the storyboard JSON

After the direction is approved, write `{project-dir}/storyboard.json` following the exact schema in [references/video-production-pipeline.md](references/video-production-pipeline.md). One object per scene; derive `duration_s` from `metadata.json`; derive `duration_frames` as `Math.round(duration_s * fps)`. Populate `visual_direction.elements` with concrete animation cues — not vague descriptions.

Present the storyboard JSON to the user as a summary table (scene, title, duration, key elements). Ask for a final check before proceeding to code. A second silence after previous approval on direction is not sufficient — confirm the storyboard JSON explicitly.

---

## Phase 4 — Remotion project scaffold

Read [references/video-production-pipeline.md](references/video-production-pipeline.md) — specifically the scaffold and TypeScript template sections — before running this phase.

Run the scaffold script. Set `--fps`, `--width`, and `--height` to match the approved direction (default: 30 fps, 1080 × 1920 vertical):

```bash
uv run scripts/03_scaffold.py \
  --project-dir {project-dir} \
  --fps 30 \
  --width 1080 \
  --height 1920 \
  --storyboard {project-dir}/storyboard.json
```

After the scaffold runs, confirm the following files exist and are non-empty: `package.json`, `tsconfig.json`, `src/config.ts`, `src/index.ts`, `src/Root.tsx`, and one `src/scenes/SceneN.tsx` stub per scene.

Update the containing repository's `.gitignore` if not already done, adding:

```gitignore
# Video production assets (large models, not for version control)
.video_production_assets/

# Local Remotion video production workspaces
**/remotion-infographic/
**/remotion-infographic/*
```

Do not replace existing rules or duplicate entries. Check with `git check-ignore -v --no-index` when Git is available.

---

## Phase 5 — Scene-by-scene composition

Read the TypeScript template section in [references/video-production-pipeline.md](references/video-production-pipeline.md) before writing any `.tsx` file. Load the `lean-coder` skill and its TypeScript/React reference for this phase.

For each scene N, implement `src/scenes/SceneN.tsx`:
- Import `useCurrentFrame`, `useVideoConfig`, `interpolate`, `spring` from `remotion`.
- Import `Audio` from `@remotion/media` and `Captions` from `@remotion/captions`.
- Import the scene's timestamp data from the JSON file (use a static import or `staticFile` as appropriate for the Remotion version).
- Mount `<Audio src={staticFile("audio/scene-N.wav")} />` at frame 0 of the local sequence.
- Mount `<Captions words={...} currentFrame={frame} fps={fps} style={captionStyle} />` with the selected caption style from the storyboard.
- Implement all `visual_direction.elements` from the storyboard using frame-driven animation only — no CSS transitions, no wall-clock timing, no unseeded randomness.
- Reserve the last `hold_frames` (default 15) in a static hold matching the final frame of the element animations.

Keep `src/Root.tsx` updated: the `<Series>` master composition (`id="VideoFull"`) includes every scene; each scene also has its own composition (`id="SceneN"`) registered independently for preview rendering.

Run TypeScript checking after implementing all scenes before moving to Phase 6:

```bash
cd {project-dir} && npx tsc --noEmit
```

Fix all type errors before proceeding. Do not skip type checking.

---

## Phase 6 — Scene-by-scene review and approval

For each scene N, in order:

1. Render the scene preview:
   ```bash
   cd {project-dir} && npx remotion render src/index.ts SceneN out/scenes/scene-N-preview.mp4 --codec=h264 --pixel-format=yuv420p
   ```
2. Inspect the rendered frames: opening, midpoint, and final frame.
3. Verify: audio exists in the output, captions are visible and timed correctly, all visual elements from the storyboard are present, text is readable at mobile size, no black frames, last frame holds the intended composition.
4. Report findings and present the path to the preview MP4.
5. **Wait for explicit user approval** ("approve", "looks good", or "proceed to scene N+1") or a revision note. Do not advance to the next scene without approval.

For a revision: apply the requested change to `SceneN.tsx`, re-run `tsc --noEmit`, re-render only `SceneN`, and repeat the review loop for that scene. Do not re-render approved scenes unless they are directly affected by a change.

---

## Phase 7 — Final merge and delivery

Only begin Phase 7 after every scene has been explicitly approved in Phase 6.

### 7a. Render the full video

```bash
cd {project-dir} && npx remotion render src/index.ts VideoFull out/video.mp4 --codec=h264 --pixel-format=yuv420p
```

### 7b. Render the hero PNG

Derive the last frame index from `metadata.json` total duration and the configured fps. Do not hard-code it:

```bash
cd {project-dir} && npx remotion still src/index.ts VideoFull out/video-hero.png --frame={last-frame}
```

### 7c. Verify

Use `ffprobe` or equivalent to confirm codec, pixel dimensions, fps, and duration match the composition. Check the PNG dimensions and that it matches the expected last composition frame.

Inspect the opening, a dense mid-section, and the final frame of the merged MP4. Confirm audio is audible throughout, captions are correctly synchronized, and the hero PNG is the settled final hero composition — not a transition or an empty frame.

Fix any defects and rerender affected outputs. If playback tools are unavailable, report that explicitly; do not claim playback was verified from a still inspection.

### 7d. Deliver

Report:
- Links to `out/video.mp4`, `out/video-hero.png`, and the editable project directory
- Dimensions, fps, total duration, number of scenes
- Selected style, palette, voice, and caption style
- Checks performed (type check, per-scene preview, full render, metadata inspection, playback if available)
- Any unverified items with their specific blockers

Publishing or uploading requires separate authorization. Do not perform either automatically.

