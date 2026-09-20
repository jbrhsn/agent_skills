# Remotion production and verification

## Project setup

Inspect the existing runtime, package manager, and lockfile before installing. For a new project, consult the current [Remotion installation guide](https://www.remotion.dev/docs) for compatible React, TypeScript, and Remotion dependencies. Pin matching versions of `remotion` and any `@remotion/*` packages and retain the lockfile. Use project-local tools rather than depending on global installs or an unpinned remote CLI on each render.

Create `src/index.ts` to register the root, `src/Root.tsx` to register the composition, scene components, a TypeScript configuration, and package scripts for Studio, type checking, video rendering, and hero rendering. Keep dimensions, fps, duration, and content props in a shared configuration. Derive the last-frame index from that configuration so duration edits cannot leave a stale hero command. Store assets in `public/` where appropriate and document asset rights and source links in the project README.

Use the approved dimensions and an integer `durationInFrames = Math.round(seconds * fps)`. Define scene boundaries in frames, with intentional overlaps only. Reserve the ending hold in the timeline rather than hoping animations finish before the last frame.

## Reliable motion and visual quality

Use [frame-driven animation](https://www.remotion.dev/docs/animating-properties) with `useCurrentFrame()`, `useVideoConfig()`, `interpolate()`, and `spring()` where appropriate. Keep rendering deterministic: avoid unseeded randomness, wall-clock timing, and CSS animations or transitions whose state is not derived from the frame. Use `Sequence` thoughtfully; its local frame origin affects animation timing.

Use code-native typography, SVG, shapes, charts, and diagrams when they explain the idea well. Keep easing, spacing, line weights, corner treatments, and typography consistent. Limit simultaneous moving elements and avoid flashy transitions that interrupt a relationship the viewer needs to understand. Hold final labels and chart values steady.

Load fonts and assets reliably before rendering using the installed version's supported loading APIs. Resolve missing images, glyphs, and font fallbacks before delivery. Keep raster assets large enough for their displayed size. Preview at a realistic phone size; a visually impressive full-resolution frame can still have unreadable labels in a feed. Check current destination UI overlays rather than assuming one universal safe-area margin. Avoid rapid flashing and unnecessary camera shake.

If audio is included, verify playback, rights, intelligibility, levels, caption timing, and the ending. Do not let music obscure narration or cut speech at the boundary. The infographic must still communicate its central idea without sound.

## Render both deliverables

Use the locally installed CLI through package scripts. The examples below illustrate the [render command](https://www.remotion.dev/docs/cli/render) and [still command](https://www.remotion.dev/docs/cli/still); replace the composition identifier and derive the numeric last frame before execution:

```text
remotion render src/index.ts Infographic out/infographic.mp4 --codec=h264 --pixel-format=yuv420p
remotion still src/index.ts Infographic out/infographic-hero.png --frame=<durationInFrames-minus-1>
```

Use the same props, dimensions, assets, and composition for both. Select encoding quality by inspecting fine text and gradients in the encoded MP4, not just the lossless PNG. Do not assume a high resolution alone produces a clear video. Check version-specific options in official documentation or local CLI help before using them.

The hero must render the exact last composition frame. If an article also needs a different aspect ratio, treat it as an additional explicitly requested layout; do not silently replace the required PNG with a crop or unrelated poster.

## Verification and completion

1. Run TypeScript checking and fix errors. Render the full MP4 and final PNG successfully.
2. Inspect sampled frames covering the opening, densest content, scene boundaries, and final frame. Temporary review stills belong inside the ignored workspace, not among the two delivery assets.
3. Review playback at normal speed when a player is available. Confirm the hook is immediately legible, text has time to be read, each beat adds useful information, and the hero settles for its planned hold. Static stills alone cannot verify pacing or audio.
4. Use `ffprobe` or equivalent media inspection to verify codec, pixel dimensions, fps, and duration against the composition; check the PNG dimensions and readability. Decode the MP4's last frame and visually compare it with the hero when tooling allows. Expect compression differences, not pixel equality between H.264 and PNG.
5. Confirm the final wording, values, units, source credits, and qualifications against the article. Correct rendering and factual defects, then rerender and recheck affected outputs.
6. Verify the workspace and output paths are covered by Git ignore rules, and identify any already tracked files. Never use automatic `git rm --cached` or broad cleanup as part of this check.

Report the outputs that actually exist, the checks performed, and any unavailable playback or metadata tools. Do not claim retention was tested from a render review. Dependency, browser, or renderer failures require a concrete blocker report, not a substituted mock MP4 or an assertion that commands alone constitute completion.
