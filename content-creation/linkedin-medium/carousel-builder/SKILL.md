---
name: carousel-builder
description: Use when the user wants to turn carousel slide copy into actual rendered LinkedIn carousel image files: generates per-slide SVG files or HTML/CSS slides (1080x1350 portrait) locally, with optional PNG export, no image APIs or models.
---

# Carousel Builder

Turns carousel slide copy (typically 8–12 slides) into **actual rendered image
files** for LinkedIn: either **SVG files** or **HTML/CSS slides**, using pure
local rendering. No external image APIs, no image-generation models.

## When to use
- The user has carousel slide copy and wants postable slide images.
- Slide copy can be provided as a plain list of slides, or read from `linkedin/carousels/<slug>/slides.json` if that file already exists. This skill is **standalone**: a list of slide copy is enough to run it.

## Rendering paths (user chooses)
1. **SVG**: `scripts/render_svg.py` writes one `.svg` per slide. Optional PNG
   via `scripts/svg_to_png.py` (uses `cairosvg` if installed). Single built-in
   dark style (no themes on this path).
2. **HTML/CSS**: `scripts/render_html.py` fills a template and writes one
   `.html` per slide. Optional PNG via a headless browser. **This path supports
   multiple visual themes** via `--template` (see the theme catalog below).

Always ask which path the user prefers before rendering. If they want a
specific look (glassmorphism, neon, brand colors, etc.), use the HTML path and
pick the matching theme template.

## Theme catalog (HTML path only)
All themes live in `templates/`, share the exact same 1080x1350 canvas,
MARGIN 100, FOOTER_BAND 140 geometry, and the same `{{TITLE}}` `{{BODY}}`
`{{FOOTER}}` `{{INDEX}}` `{{TOTAL}}` placeholders, so the slide-1 preview and
the auto-fit spec stay valid regardless of theme. Select one with `--template`.

| Theme | Template file | Look |
|---|---|---|
| Default (dark) | `templates/slide.html` | Slate dark, cyan accent (matches the SVG renderer). |
| Glassmorphism | `templates/slide-glassmorphism.html` | Frosted translucent card over a colorful blurred gradient. |
| Neomorphism | `templates/slide-neomorphism.html` | Soft monochrome UI with extruded/inset dual shadows. |
| Neon | `templates/slide-neon.html` | Near-black cyberpunk with glowing pink/cyan text + grid. |
| Super Mario | `templates/slide-mario.html` | Sky blue, `?`-block gold accent, brick footer, chunky type. |
| LinkedIn | `templates/slide-linkedin.html` | Official LinkedIn blue (#0A66C2) on white, "in" mark. |
| Minimal light | `templates/slide-minimal-light.html` | Clean editorial serif on off-white, single rule. |

Ask the user which theme they want (default = `slide.html`). If none is
specified, use the default. Theme choice affects only the HTML render; the
design spec and auto-fit (from `render_svg.py`'s logic) are theme-independent.

Some themes rely on effects a headless browser renders best (glassmorphism's
`backdrop-filter`, neon glows, Mario shadows). The `.html` files are always
valid; if a PNG rasterizer ignores an effect, the layout/text still render.

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
1. Emit a **design spec** with `scripts/spec.py` (canvas, palette, font, slide
   count, and per-slide auto-fit result incl. any overflow warnings).
2. Render **only slide 1** as a preview (`--only 1`).
3. **STOP.** Show the spec + preview file path and let the user review/approve.
   If the spec reports overflow on any slide, recommend shortening/splitting
   that slide's copy before proceeding.
4. Only after approval, render all slides and (optionally) export PNGs.

## Auto-fit & overflow
`render_svg.py` auto-fits each slide: it steps font sizes down until the
title+body fit the safe area above the reserved footer band. If a slide still
overflows at the smallest size, the script prints a WARNING naming the slide
and exits `3` (non-fatal). Shorten the copy or split the slide. The HTML
template clips overflow to the footer band rather than spilling over it, and
shares the same canvas/margin/footer/font constants as the SVG renderer so the
slide-1 preview matches the final render. Fonts use a Linux-friendly fallback
stack so PNG rasterization stays consistent when Helvetica is absent.

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
- `slug` names the output folder and file prefix.
Use the **real per-slide content**. No lorem ipsum.

## Workflow

### 0. Confirm folders
Check `linkedin/` exists (cwd-relative). If not, ask. Check `voice-tone/` if
tone consistency is expected; if missing, ask.
Resolve `SKILL_DIR` to this skill's own directory: project-local `.opencode/skills/carousel-builder` or global `~/.config/opencode/skills/carousel-builder`. Prefix all script and template paths below with `$SKILL_DIR`.
Probe export tooling up front: check whether `cairosvg` (SVG to PNG) and a headless browser (HTML to PNG via playwright or puppeteer) are available. Report which export formats this machine supports BEFORE rendering, so PNG limits are known now rather than discovered at the end.

### 1. Assemble slides JSON
**Voice compliance gate (before writing slide copy).** If `voice-tone/profile.md` (or raw `voice-tone/` samples) is present, scan the slide titles and bodies against its "Avoided Words & Phrases" and "Punctuation & Formatting Quirks". Auto-fix mechanical violations (em-dashes to periods or commas, banned punctuation) and report what changed. Flag judgment calls (hype words, AI-voice markers) for the user. Never emit a banned pattern. If no voice-tone exists, skip silently.

Write the slide copy into a JSON file at the canonical path
`linkedin/carousels/<slug>/slides.json`, following the schema above. If a
`slides.json` already exists at that path, check there first before asking the user to re-enter the copy.

### 2. Emit spec + preview slide 1 (review-first)
Design spec:
```
python3 $SKILL_DIR/scripts/spec.py \
  linkedin/carousels/<slug>/slides.json \
  --path linkedin/carousels/<slug> --render svg
```
SVG preview:
```
python3 $SKILL_DIR/scripts/render_svg.py \
  linkedin/carousels/<slug>/slides.json \
  --out linkedin/carousels/<slug> --only 1
```
HTML path (add `--template $SKILL_DIR/templates/slide-<theme>.html` for a themed look; omit for the default dark style):
```
python3 $SKILL_DIR/scripts/render_html.py \
  linkedin/carousels/<slug>/slides.json \
  --out linkedin/carousels/<slug> \
  --template $SKILL_DIR/templates/slide-neon.html \
  --only 1
```
**STOP and let the user review the preview + design spec before continuing.**

### 3. Render all slides (after approval)
Drop `--only 1` to render every slide:
```
python3 $SKILL_DIR/scripts/render_svg.py \
  linkedin/carousels/<slug>/slides.json --out linkedin/carousels/<slug>
```

### 4. Optional PNG export
SVG → PNG (degrades gracefully if `cairosvg` is missing):
```
python3 $SKILL_DIR/scripts/svg_to_png.py \
  linkedin/carousels/<slug>
```
If `cairosvg` is not installed, the script prints install/export instructions
and the SVGs remain valid output. HTML → PNG uses a headless browser
(playwright/puppeteer); optional, and `render_html.py` prints the hint.

## Scripts reference
- `scripts/spec.py`: reads slides JSON, prints design spec + per-slide
  auto-fit result (font sizes, line counts, overflow flags). `--path`,
  `--render`, `--json`, `--help`. Exit `3` if any slide overflows.
- `scripts/render_svg.py`: slides JSON → SVG files. Portrait 1080x1350,
  minimal palette, auto-fit font sizing with overflow warning (exit `3`).
  `--out`, `--only`, `--help`.
- `scripts/svg_to_png.py`: SVGs → PNGs via optional `cairosvg`. Never
  hard-fails; prints guidance if unavailable. `--out`, `--scale`, `--help`.
- `scripts/render_html.py`: slides JSON → HTML files from a template
  (`--template`, default `templates/slide.html`). `--out`, `--only`, `--help`.
- `templates/slide*.html`: self-contained 1080x1350 slide templates sharing
  the SVG renderer's constants (MARGIN 100, FOOTER_BAND 140); each clips
  overflow to the reserved footer band. Placeholders `{{TITLE}}`, `{{BODY}}`,
  `{{INDEX}}`, `{{TOTAL}}`, `{{FOOTER}}`. Themes: `slide.html` (default dark),
  `slide-glassmorphism.html`, `slide-neomorphism.html`, `slide-neon.html`,
  `slide-mario.html`, `slide-linkedin.html`, `slide-minimal-light.html`.
  Add a new theme by copying any of these and restyling. Keep the canvas,
  geometry, and placeholders identical.

All scripts use only the Python standard library for generation; `cairosvg`
and a headless browser are optional add-ons for PNG only.

## Conventions

These are shared assumptions so the content skills interoperate. Each skill
still works standalone; none of these require another skill to be present.
- **Folders** (all cwd-relative): `drafts/`, `linkedin/`, `medium/`,
  `archive/`, `voice-tone/`. Never auto-create; ask the user if missing.
- **Slug**: lowercase, hyphenated, derived from the working title. Reused as
  the filename stem across skills so a piece is traceable.
- **Filenames**: `drafts/<slug>.md`, `linkedin/<slug>-<type>.md`,
  `medium/<slug>-<type>.md`, carousels at `linkedin/carousels/<slug>/`.
- **Overwrite policy**: never silently overwrite an existing file. If the
  target exists, ask the user: overwrite, write a `-v2` (then `-v3`...)
  variant, or pick a new name.
- **Status values** (if a tracker file like `content-log.md` or `content-log.json` exists at cwd): `idea` -> `drafted` -> `reviewed` -> `posted` -> `archived`. If such a tracker exists, after writing or moving a file ASK the user in one line whether to update it to the new status. Absence of a tracker must never block the skill.
