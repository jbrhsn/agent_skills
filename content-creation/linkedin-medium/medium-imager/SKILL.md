---
name: medium-imager
description: Use when the user wants to turn Medium article copy into actual rendered cover + in-article image files: generates a wide featured cover image (1500x750) plus quote/callout/stat/code-snippet slide images (1600x900) locally as SVG, then rasterizes all of them to PNG (the actual Medium-uploadable asset) via cairosvg. No image APIs or models.
---

# Medium Imager

Turns Medium article copy into **actual rendered image files**: one wide
**cover image** (1500x750, Medium's featured-image ratio) plus up to 10
**in-article slide-style images** (1600x900) — quote cards, key-takeaway
callouts, stat/number highlights, and code snippet cards. Pure local SVG
rendering, then a **required** SVG->PNG rasterization pass, because Medium
does not accept raw SVG uploads. No external image APIs, no image-generation
models.

## When to use
- The user has (or wants help drafting) cover + in-article image copy for a
  Medium piece and wants postable PNG files.
- Copy can be provided as a plain list, read from an existing
  `medium/<slug>.md` draft (auto-suggested, never auto-written), or read from
  `medium/images/<slug>/images.json` if that file already exists. This skill
  is **standalone**: a title + a few image entries is enough to run it.

## Output
1. **Per-image SVG files** at `medium/images/<slug>/<slug>-cover.svg` and
   `medium/images/<slug>/<slug>-NN-<type>.svg` — kept as editable source.
2. **Per-image PNG files** at the same paths with `.png` — the actual
   Medium-uploadable deliverable, produced by rasterizing every SVG.

Unlike carousel-builder's optional PDF step, the PNG step here is
**required**, not best-effort: Medium does not accept SVG uploads, so a run
without PNGs is not "done". If `cairosvg` is missing, the rasterize step
prints install instructions and exits non-zero rather than degrading.

## Theme catalog
All themes live in `templates/` as pairs of `.svg` files: `cover-<theme>.svg`
(1500x750) and `slide-<theme>.svg` (1600x900, shared by all four inner image
types). Select one with `--theme` (default = `clean-minimal`).

| Theme | Cover / slide files | Look |
|---|---|---|
| Clean minimal (default) | `cover-clean-minimal.svg` / `slide-clean-minimal.svg` | Flat off-white, single blue accent block, geometric sans. |
| Editorial serif | `cover-editorial-serif.svg` / `slide-editorial-serif.svg` | Cream background, Georgia serif, thin black accent rule. |
| Dark code | `cover-dark-code.svg` / `slide-dark-code.svg` | Near-black, monospace, terminal green accent. Best for code-heavy pieces. |
| Bold magazine | `cover-bold-magazine.svg` / `slide-bold-magazine.svg` | High-contrast black/white sans, thick red accent rules. |
| Warm sepia | `cover-warm-sepia.svg` / `slide-warm-sepia.svg` | Warm tan background, soft brown accent, serif italics. |

The cover template has placeholders `{{TITLE_BLOCK}}` `{{SUBTITLE_BLOCK}}`
`{{FOOTER}}`. The slide template has one `{{CONTENT_BLOCK}}` placeholder that
`render_svg.py` fills differently per image `type` (quote/callout/stat/code),
plus `{{FOOTER}}` `{{COUNTER}}` `{{INDEX}}` `{{TOTAL}}`. Themes control
background, accent, and per-class fill/font-family/weight via inline
`<style>`; the renderer only sets text geometry so auto-fit stays
theme-independent. Add a new theme by copying a `cover-*.svg` +
`slide-*.svg` pair and restyling — keep canvas, geometry, class names, and
placeholders identical.

## Folder rules (cwd-relative, never absolute)
All folders resolve relative to the **current working directory** where
opencode was launched.
- Output goes under `medium/images/<slug>/`.
- **If `medium/` does NOT exist, STOP and ASK the user** how to proceed
  (create it? use a different path?). Never silently create the `medium/`
  folder tree.
- Read voice/brand tone from a `voice-tone/` folder (cwd-relative) if
  present, to keep wording/style consistent. If a `voice-tone/` folder is
  **expected but missing**, ask the user how to proceed rather than
  guessing.

## Review-first (mandatory stop point)
Never run end-to-end automatically.
1. Probe `cairosvg` up front (Step 0). It is **required** — if missing,
   report the install command and STOP; do not proceed to spec/render until
   resolved. SVG-only files are editable source, not completed Medium-ready
   output.
2. Emit a **design spec** with `scripts/spec.py` (canvases, theme, image
   count, and per-image auto-fit result incl. any overflow warnings).
3. Render **only the cover** (`--only cover`) and **only image 1**
   (`--only 1`) as SVG, then rasterize just those two to PNG.
4. **STOP.** Show the spec + preview PNG paths and let the user
   review/approve. If the spec reports overflow on any item, recommend
   shortening/splitting that item's copy before proceeding.
5. Only after approval, render all remaining images to SVG AND rasterize
   every SVG to PNG.

## Auto-fit & overflow
`render_svg.py` auto-fits every image: it steps font sizes down until the
content fits the safe area above the reserved footer band. If an item still
overflows at the smallest size, the script prints a WARNING naming the item
and exits `3` (non-fatal). Shorten the copy or split it. Fonts use a
Linux-friendly fallback stack so PNG rasterization stays consistent when
Helvetica/Georgia/Courier are absent.

## images.json schema
Canonical path: `medium/images/<slug>/images.json`. `index`/`total` for
inner images are auto-filled from array position. Do not include them.

```json
{
  "slug": "my-article",
  "cover": {
    "title": "How We Cut Deploy Time by 80%",
    "subtitle": "A practical guide to CI/CD pipeline optimization",
    "footer": "@handle"
  },
  "images": [
    {"type": "quote", "quote": "...", "attribution": "Jane Doe", "footer": "@handle"},
    {"type": "callout", "text": "...", "label": "Key takeaway", "footer": "@handle"},
    {"type": "stat", "number": "80%", "label": "reduction in deploy time", "footer": "@handle"},
    {"type": "code", "code": "def foo():\n    return 1", "language": "python", "footer": "@handle"}
  ]
}
```

**Fields per type** (all `footer` fields optional; blank renders without
attribution text — this is valid):
- `cover`: `title` (required), `subtitle` (optional), `footer` (optional)
- `quote`: `quote` (required), `attribution` (optional)
- `callout`: `text` (required), `label` (optional, rendered as an uppercase kicker)
- `stat`: `number` (required), `label` (required)
- `code`: `code` (required, newlines preserved), `language` (optional, shown as a small badge — no syntax highlighting)

**Limits:** up to 10 entries in `images`. **Field validation:** an entry
missing a required field for its `type`, or an unrecognized `type`, causes
`scripts/images.py` to raise and the agent should stop and ask the user to
supply/fix the missing content before writing `images.json`.

Use the **real per-item content**. No lorem ipsum.

## Workflow

### 0. Confirm folders + probe cairosvg
Check `medium/` exists (cwd-relative). If not, ask. Check `voice-tone/` if
tone consistency is expected; if missing, ask.
Resolve `SKILL_DIR` to this skill's own directory: project-local
`.opencode/skills/medium-imager` or global `~/.config/opencode/skills/medium-imager`.
Prefix all script and template paths below with `$SKILL_DIR`.
Probe `cairosvg` up front:
```
python3 -c "import cairosvg" 2>&1
```
If it's missing, report:
```
uv pip install cairosvg   # or: pip install cairosvg
```
Then, instead of only stopping, ASK the user whether to create a local
`.venv` with `uv` and install `cairosvg` now. Only on approval, run
`scripts/svg_to_png.py` with `--install-missing` (which creates `.venv` via
`uv`, installs `cairosvg`, then re-runs itself with the venv Python). If the
user declines, STOP — do not proceed past this point until resolved, since
PNG is the deliverable this skill considers "done" (unlike carousel-builder's
optional PDF step).

### 1. Assemble image copy
If `medium/<slug>.md` already exists, run the draft-suggestion helper and
present its output to the user for confirmation/edits — **never** write
`images.json` from these suggestions without an explicit user go-ahead:
```
python3 $SKILL_DIR/scripts/suggest_from_draft.py medium/<slug>.md
```
Otherwise ask the user directly for cover title/subtitle and each inner
image's copy.

**Voice compliance gate (before writing image copy).** If
`voice-tone/profile.md` (or raw `voice-tone/` samples) is present, scan the
cover title/subtitle and every inner image's text field **except `code`**
against its "Avoided Words & Phrases" and "Punctuation & Formatting Quirks".
Auto-fix mechanical violations (em-dashes to periods or commas, banned
punctuation) and report what changed. Flag judgment calls (hype words,
AI-voice markers) for the user. Never emit a banned pattern. If no
voice-tone exists, skip silently.

Write the copy into a JSON file at the canonical path
`medium/images/<slug>/images.json`, following the schema above. If an
`images.json` already exists at that path, check there first before asking
the user to re-enter the copy.

### 2. Emit spec + preview cover + image 1 (review-first)
Design spec (add `--theme <theme-name>` if a non-default theme is chosen):
```
python3 $SKILL_DIR/scripts/spec.py \
  medium/images/<slug>/images.json \
  --path medium/images/<slug> \
  --theme clean-minimal
```
SVG preview (same `--theme` value as the spec):
```
python3 $SKILL_DIR/scripts/render_svg.py \
  medium/images/<slug>/images.json \
  --out medium/images/<slug> \
  --theme clean-minimal \
  --only cover

python3 $SKILL_DIR/scripts/render_svg.py \
  medium/images/<slug>/images.json \
  --out medium/images/<slug> \
  --theme clean-minimal \
  --only 1
```
Rasterize just those two previews to PNG:
```
python3 $SKILL_DIR/scripts/svg_to_png.py medium/images/<slug> --only cover
python3 $SKILL_DIR/scripts/svg_to_png.py medium/images/<slug> --only 1
```
**STOP and let the user review the preview PNGs + design spec before
continuing.**

### 3. Render all images (after approval)
Drop `--only` to render every remaining image with the approved theme:
```
python3 $SKILL_DIR/scripts/render_svg.py \
  medium/images/<slug>/images.json \
  --out medium/images/<slug> \
  --theme clean-minimal
```

### 4. Rasterize all to PNG (automatic, required)
Immediately after Step 3 completes successfully, rasterize every SVG to PNG:
```
python3 $SKILL_DIR/scripts/svg_to_png.py medium/images/<slug>
```
Default scale is `2.0` (retina-sharp: cover renders at 3000x1500, slides at
3200x1800). If `cairosvg` is missing at this point, ASK the user for approval
and, if granted, rerun with `--install-missing` (which creates `.venv` via
`uv`, installs `cairosvg`, then re-runs itself):
```
python3 $SKILL_DIR/scripts/svg_to_png.py medium/images/<slug> --install-missing
```
If the user declines, the script exits `1` with install instructions — a hard
stop, not a soft degrade, since PNG is the deliverable.

## Scripts reference
- `scripts/images.py`: shared schema loader/validator for `images.json`
  (not a CLI entry point; imported by spec.py and render_svg.py).
- `scripts/spec.py`: reads images.json, prints design spec + per-image
  auto-fit result (font sizes, line counts, overflow flags) for the cover
  and every inner image. `--path`, `--theme`, `--json`, `--help`. Exit `3`
  if any item overflows.
- `scripts/render_svg.py`: images.json -> SVG files. Cover 1500x750, slides
  1600x900, auto-fit font sizing per type with overflow warning (exit `3`).
  `--out`, `--theme`, `--only cover|N`, `--help`.
- `scripts/svg_to_png.py`: SVG -> PNG via `cairosvg` (**required**, not
  optional — hard error with install hint if missing). `--only cover|N`,
  `--scale` (default `2.0`), `--install-missing` (uv creates `.venv` and
  installs `cairosvg` on user approval, then re-runs), `--help`.
- `scripts/suggest_from_draft.py`: parses an existing `medium/<slug>.md` for
  candidate cover title/subtitle, pull-quotes, callout sections, and bolded
  stats. Prints suggestions only — never writes files. `--json`, `--help`.
- `templates/cover-*.svg` / `templates/slide-*.svg`: self-contained
  1500x750 / 1600x900 templates per theme sharing the renderer's MARGIN/
  FOOTER_BAND constants. Add a new theme by copying a pair and restyling —
  keep canvas, geometry, `<style>` class names, and placeholders identical.

All scripts use only the Python standard library except `svg_to_png.py`,
which requires `cairosvg` (the one required, non-optional dependency of this
skill).

## Conventions

These are shared assumptions so the content skills interoperate. Each skill
still works standalone; none of these require another skill to be present.
- **Folders** (all cwd-relative): `drafts/`, `linkedin/`, `medium/`,
  `archive/`, `voice-tone/`. Never auto-create; ask the user if missing.
- **Slug**: lowercase, hyphenated, derived from the working title. Reused as
  the filename stem across skills so a piece is traceable.
- **Filenames**: `medium/<slug>-<type>.md` for the draft/article, images at
  `medium/images/<slug>/` with `<slug>-cover.{svg,png}` and
  `<slug>-NN-<type>.{svg,png}` per inner image.
- **Overwrite policy**: never silently overwrite an existing file. If the
  target exists, ask the user: overwrite, write a `-v2` (then `-v3`...)
  variant, or pick a new name.
- **Status values** (if a tracker file like `content-log.md` or
  `content-log.json` exists at cwd): `idea` -> `drafted` -> `reviewed` ->
  `posted` -> `archived`. If such a tracker exists, after writing images ASK
  the user in one line whether to update it to the new status. Absence of a
  tracker must never block the skill.
