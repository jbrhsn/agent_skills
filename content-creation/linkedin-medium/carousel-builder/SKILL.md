---
name: carousel-builder
description: Use when the user wants to turn carousel slide copy into actual rendered LinkedIn carousel image files: generates per-slide SVG files (1080x1350 portrait) locally with multiple themes, and automatically combines them into a single multi-page PDF. No image APIs or models.
---

# Carousel Builder

Turns carousel slide copy (typically 8–12 slides) into **actual rendered
SVG files** for LinkedIn (1080x1350 portrait, themed), then **combines them
into a single multi-page PDF**. Pure local rendering — no external image APIs,
no image-generation models.

## When to use
- The user has carousel slide copy and wants postable slide images plus a single PDF deck.
- Slide copy can be provided as a plain list of slides, or read from `linkedin/carousels/<slug>/slides.json` if that file already exists. This skill is **standalone**: a list of slide copy is enough to run it.

## Output
1. **Per-slide SVG files** at `linkedin/carousels/<slug>/<slug>-NN.svg` — the primary output.
2. **A single combined PDF** at `linkedin/carousels/<slug>/<slug>.pdf` — one page per slide, generated automatically after the full SVG render.

The PDF step needs `cairosvg` and `Pillow` (both optional). If either is missing, the SVGs remain valid postable output on their own. Ask the user whether to create a local `.venv` with `uv` and install the missing PDF dependencies; only then run the installer path.

## Theme catalog
All themes live in `templates/` as `.svg` files. They share the exact same 1080x1350 canvas, MARGIN 100, FOOTER_BAND 140 geometry, and the same `{{TITLE_BLOCK}}` `{{BODY_BLOCK}}` `{{FOOTER}}` `{{COUNTER}}` `{{INDEX}}` `{{TOTAL}}` placeholders, so the slide-1 preview and the auto-fit spec stay valid regardless of theme. Select one with `--template`.

| Theme | Template file | Look |
|---|---|---|
| Default (dark) | `templates/slide.svg` | Slate dark, cyan accent. |
| Glassmorphism | `templates/slide-glassmorphism.svg` | Frosted translucent card over a blurred colorful gradient. |
| Neomorphism | `templates/slide-neomorphism.svg` | Soft monochrome UI with extruded/inset dual shadows. |
| Neon | `templates/slide-neon.svg` | Near-black cyberpunk with glowing pink/cyan text + grid. |
| Super Mario | `templates/slide-mario.svg` | Sky blue, `?`-block gold accent, brick footer, chunky type. |
| LinkedIn | `templates/slide-linkedin.svg` | Official LinkedIn blue (#0A66C2) on white, "in" mark. |
| Minimal light | `templates/slide-minimal-light.svg` | Editorial serif on off-white, single accent rule. |

Ask the user which theme they want (default = `slide.svg`). If none is specified, use the default. Themes control background, accent, footer band, and per-class fill/font-family/weight via inline `<style>`; the renderer only sets text geometry so auto-fit stays theme-independent.

Some themes rely on SVG filter effects (glassmorphism blur, neon glow, Mario textures). These render natively in all modern viewers and rasterize fine via `cairosvg`. If the final PDF is the priority, all seven themes produce clean pages.

## Folder rules (cwd-relative, never absolute)
All folders resolve relative to the **current working directory** where opencode
was launched.
- Carousel output goes under `linkedin/carousels/<slug>/`.
- **If `linkedin/` does NOT exist, STOP and ASK the user** how to proceed
  (create it? use a different path?). Never silently create the `linkedin/`
  folder tree.
- Read voice/brand tone from a `voice-tone/` folder (cwd-relative) if present,
  to keep wording/style consistent. Voice adapts to content. Keep it
  lightweight for this visual skill. If a `voice-tone/` folder is **expected but
  missing**, ask the user how to proceed rather than guessing.

## Review-first (mandatory stop point)
Never run end-to-end automatically.
1. Emit a **design spec** with `scripts/spec.py` (canvas, template, slide
   count, and per-slide auto-fit result incl. any overflow warnings).
2. Render **only slide 1** as a preview (`--only 1`).
3. **STOP.** Show the spec + preview file path and let the user review/approve.
   If the spec reports overflow on any slide, recommend shortening/splitting
   that slide's copy before proceeding.
4. Only after approval, render all slides AND combine them into the single PDF.

## Auto-fit & overflow
`render_svg.py` auto-fits each slide: it steps font sizes down until the
title+body fit the safe area above the reserved footer band. If a slide still
overflows at the smallest size, the script prints a WARNING naming the slide
and exits `3` (non-fatal). Shorten the copy or split the slide. Fonts use a
Linux-friendly fallback stack so PNG/PDF rasterization stays consistent when
Helvetica is absent.

## Slides JSON schema
`index`/`total` are auto-filled from array position. Do not include them.

```json
{
  "slug": "my-carousel",
  "slides": [
    {"title": "The hook", "body": "One clear idea per slide.", "footer": "@handle"},
    {"title": "Point two", "body": "Supporting detail here."}
  ]
}
```
- `title` (string, required), `body` (string, required)
- `footer` (string, optional: e.g. handle/CTA)
- `slug` names the output folder, per-slide file prefix, and the combined PDF name.
Use the **real per-slide content**. No lorem ipsum.

**Field validation:** `title` (string, required — error if missing or empty), `body` (string, required — error if missing or empty), `footer` (string, optional — if omitted, the footer band renders without attribution text; this is valid). Extra fields are ignored. An entry missing `title` or `body` should cause the agent to stop and ask the user to supply the missing content before writing `slides.json`.

## Workflow

### 0. Confirm folders
Check `linkedin/` exists (cwd-relative). If not, ask. Check `voice-tone/` if
tone consistency is expected; if missing, ask.
Resolve `SKILL_DIR` to this skill's own directory: project-local `.opencode/skills/carousel-builder` or global `~/.config/opencode/skills/carousel-builder`. Prefix all script and template paths below with `$SKILL_DIR`.
Probe PDF tooling up front: check whether `cairosvg` and `Pillow` are available. Report whether the final PDF step will succeed BEFORE rendering, so the limit is known now rather than discovered after all SVGs are written.

### 1. Assemble slides JSON
**Voice compliance gate (before writing slide copy).** If `voice-tone/profile.md` (or raw `voice-tone/` samples) is present, scan the slide titles and bodies against its "Avoided Words & Phrases" and "Punctuation & Formatting Quirks". Auto-fix mechanical violations (em-dashes to periods or commas, banned punctuation) and report what changed. Flag judgment calls (hype words, AI-voice markers) for the user. Never emit a banned pattern. If no voice-tone exists, skip silently.

Write the slide copy into a JSON file at the canonical path
`linkedin/carousels/<slug>/slides.json`, following the schema above. If a
`slides.json` already exists at that path, check there first before asking the user to re-enter the copy.

### 2. Emit spec + preview slide 1 (review-first)
Design spec (add `--template $SKILL_DIR/templates/slide-<theme>.svg` if a non-default theme is chosen):
```
python3 $SKILL_DIR/scripts/spec.py \
  linkedin/carousels/<slug>/slides.json \
  --path linkedin/carousels/<slug> \
  --template $SKILL_DIR/templates/slide.svg
```
SVG preview (same `--template` value as the spec):
```
python3 $SKILL_DIR/scripts/render_svg.py \
  linkedin/carousels/<slug>/slides.json \
  --out linkedin/carousels/<slug> \
  --template $SKILL_DIR/templates/slide.svg \
  --only 1
```
**STOP and let the user review the preview + design spec before continuing.**

### 3. Render all slides (after approval)
Drop `--only 1` to render every slide with the approved theme:
```
python3 $SKILL_DIR/scripts/render_svg.py \
  linkedin/carousels/<slug>/slides.json \
  --out linkedin/carousels/<slug> \
  --template $SKILL_DIR/templates/slide.svg
```

### 4. Combine into a single PDF (automatic)
Immediately after Step 3 completes successfully, combine the rendered SVGs into a single multi-page PDF:
```
python3 $SKILL_DIR/scripts/combine_pdf.py linkedin/carousels/<slug>
```
The PDF is written to `linkedin/carousels/<slug>/<slug>.pdf` (one page per slide, portrait 1080x1350). If `cairosvg` or `Pillow` is not installed, STOP and ask: "PDF dependencies are missing. Create a local `.venv` with `uv` and install `cairosvg pillow` now?" If the user approves, rerun:
```
python3 $SKILL_DIR/scripts/combine_pdf.py linkedin/carousels/<slug> --install-missing
```
If they decline, leave the SVGs as the postable output and report that the PDF was skipped.

## Scripts reference
- `scripts/spec.py`: reads slides JSON, prints design spec + per-slide
  auto-fit result (font sizes, line counts, overflow flags). `--path`,
  `--template`, `--json`, `--help`. Exit `3` if any slide overflows.
- `scripts/render_svg.py`: slides JSON → SVG files. Portrait 1080x1350,
  auto-fit font sizing with overflow warning (exit `3`). `--out`,
  `--template`, `--only`, `--help`.
- `scripts/combine_pdf.py`: SVGs → single multi-page PDF via `cairosvg` +
  `Pillow` (both optional). If unavailable, prints `uv` guidance and exits
  without error; with user approval, `--install-missing` creates `.venv`,
  installs `cairosvg pillow` with `uv`, and reruns the combine step.
  `--out`, `--scale`, `--install-missing`, `--help`.
- `templates/slide*.svg`: self-contained 1080x1350 slide templates sharing
  the renderer's MARGIN 100 / FOOTER_BAND 140 constants. Placeholders:
  `{{TITLE_BLOCK}}`, `{{BODY_BLOCK}}`, `{{FOOTER}}`, `{{COUNTER}}`,
  `{{INDEX}}`, `{{TOTAL}}`. Themes: `slide.svg` (default dark),
  `slide-glassmorphism.svg`, `slide-neomorphism.svg`, `slide-neon.svg`,
  `slide-mario.svg`, `slide-linkedin.svg`, `slide-minimal-light.svg`.
  Add a new theme by copying any of these and restyling — keep the canvas,
  geometry, `<style>` class names (`title`, `body`, `footer`), and
  placeholders identical.

All scripts use only the Python standard library for SVG generation;
`cairosvg` and `Pillow` are optional add-ons for the PDF combine step only and
must be installed through `uv` when the user approves dependency setup.

## Conventions

These are shared assumptions so the content skills interoperate. Each skill
still works standalone; none of these require another skill to be present.
- **Folders** (all cwd-relative): `drafts/`, `linkedin/`, `medium/`,
  `archive/`, `voice-tone/`. Never auto-create; ask the user if missing.
- **Slug**: lowercase, hyphenated, derived from the working title. Reused as
  the filename stem across skills so a piece is traceable.
- **Filenames**: `drafts/<slug>.md`, `linkedin/<slug>-<type>.md`,
  `medium/<slug>-<type>.md`, carousels at `linkedin/carousels/<slug>/` with
  `<slug>-NN.svg` per slide plus `<slug>.pdf` combined deck.
- **Overwrite policy**: never silently overwrite an existing file. If the
  target exists, ask the user: overwrite, write a `-v2` (then `-v3`...)
  variant, or pick a new name.
- **Status values** (if a tracker file like `content-log.md` or `content-log.json` exists at cwd): `idea` -> `drafted` -> `reviewed` -> `posted` -> `archived`. If such a tracker exists, after writing or moving a file ASK the user in one line whether to update it to the new status. Absence of a tracker must never block the skill.
