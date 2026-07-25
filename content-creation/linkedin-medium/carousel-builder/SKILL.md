---
name: carousel-builder
description: Use when the user wants to turn carousel slide copy into actual rendered LinkedIn carousel image files, or wants carousel slide copy written from a source draft or rough idea. Accepts EITHER ready slide copy OR a draft/idea, authors the deck when copy is not provided, then renders it locally via a headless browser (Playwright/Chromium) into per-slide PNG files (square, portrait, or landscape) with typed slide layouts, four built-in themes plus a custom-theme path, bundled local fonts, and an automatic merged PDF. No image APIs or models.
---

# Carousel Builder

Turns a **typed carousel deck spec** into **actual rendered PNG slide files**
for LinkedIn, then **merges them into a single multi-page PDF**. Slides are
rendered locally from HTML/CSS through headless Chromium (Playwright) — one
element screenshot of a fixed-size canvas per slide. Pure local rendering: no
external image APIs, no image-generation models. Python tooling is managed with
`uv`.

## When to use
- The user has slide copy (or a deck spec) and wants postable slide images + a PDF.
- The user has a source draft or a rough idea/notes and wants a carousel built from it — this skill authors the deck spec itself when none is provided.
- Input can be a source draft at `drafts/<slug>.md`, a rough idea/notes, an existing `linkedin/carousels/<slug>/deck.yaml`, or a plain list of slide copy. If ready copy is not provided and no `deck.yaml` exists, the skill authors it before rendering. This skill is **standalone**.

## Output
1. **Per-slide PNG files** at `linkedin/carousels/<slug>/<format>/NN_<type>.png` — the primary output (retina 2x by default).
2. **A single combined PDF** at `linkedin/carousels/<slug>/<format>/<slug>.pdf` — one page per slide, generated automatically after the full render (unless `--no-pdf`).

## Prerequisites (one-time)
This skill requires **`uv`** and a local Chromium binary. It **never** falls back to pip/venv.
1. Check `uv --version`. **If `uv` is missing, STOP and ask the user to install it** (`curl -LsSf https://astral.sh/uv/install.sh | sh`, or `brew install uv`, or `pipx install uv`). Do not proceed without it.
2. From `$SKILL_DIR`, run once: `uv sync` then `uv run playwright install chromium`. After that, all rendering is fully local (no per-render network calls).
3. Fonts are **bundled locally** under `assets/fonts/` so rendering is deterministic across machines. Do not delete that folder — headless font rendering otherwise drifts between hosts.

## Folder rules (cwd-relative, never absolute)
All content folders resolve relative to the **current working directory** where opencode was launched.
- Carousel output goes under `linkedin/carousels/<slug>/`.
- **If `linkedin/` does NOT exist, STOP and ASK the user** how to proceed (create it? use a different path?). Never silently create the `linkedin/` tree.
- Read voice/brand tone from a `voice-tone/` folder (cwd-relative) if present, to keep wording/style consistent. If a `voice-tone/` folder is **expected but missing**, ask the user how to proceed rather than guessing.

Resolve `SKILL_DIR` to this skill's own directory: project-local `.opencode/skills/carousel-builder` or global `~/.config/opencode/skills/carousel-builder`. Run all `uv` commands with `$SKILL_DIR` as the working directory so the bundled fonts, templates, and themes resolve.

## Review-first (mandatory stop point)
Never run end-to-end automatically.
1. Emit a **design spec** with `--spec-only` (title, theme, format + canvas dims, slide count, bundled fonts, WCAG contrast report, and per-slide overflow-risk flags).
2. Render **only slide 1** as a preview (`--only 1`).
3. **STOP.** Show the spec + preview PNG path and let the user review/approve. If the spec reports an overflow risk on any slide, recommend shortening/splitting that slide's copy before proceeding.
4. Only after approval, render all slides (which also merges the PDF).

## Deck spec (content schema)
A single YAML (or JSON) file describes the whole carousel. Canonical path:
`linkedin/carousels/<slug>/deck.yaml`. It is validated against
`engine/deck_schema.json` before rendering; validation fails fast with the
slide index and offending field.

```yaml
meta:
  title: "My Carousel"       # required
  slug: my-carousel          # optional; derived from title if omitted
  format: portrait           # square | portrait | landscape (default portrait)
  theme: dark_navy           # a name in themes/, or a path to a custom theme .json
  footer: "@handle"          # optional; per-slide footer overrides this
slides:
  - type: title
    headline: "One bold claim"
    subheadline: "Optional supporting line."
```

### Slide types (required / optional fields)
Each `type` maps 1:1 to a template in `templates/`.

| Type | Required | Optional | Looks like |
|---|---|---|---|
| `title` | `headline` | `subheadline`, `kicker` | Hook slide: big headline, accent bar. Use for slide 1. |
| `comparison` | `title_left`, `title_right`, `items_left`, `items_right` | `heading` | Two columns — left = crosses (negative), right = checks (positive). |
| `quote` | `quote` | `attribution` | Large quotation mark + statement + attribution. |
| `stat_grid` | `heading`, `primary` `{label,value,detail?}` | `secondary[] {label,value,detail?}` (≤6) | One big stat + a grid of secondary stats. |
| `numbered_phase` | `number`, `title`, `body` | `icon`, `callout_label`, `callout_body` | Big number + heading + body + optional accent callout box. |
| `process_loop` | `heading`, `steps[] {label,detail?}` (2–4) | — | Numbered step cards presented as a repeating loop. |
| `list_steps` | `heading`, `items` | `style` (`check`\|`bullet`\|`number`, default `check`) | Checklist / bullet / numbered list. |
| `cta` | `headline` | `subtext`, `action` | Closing call-to-action with an action pill + arrow. Use for the last slide. |

`icon` values map to `assets/icons/` names: `check, cross, arrow, arrow-down, badge, doc, gear, chart, bolt, target, shield, quote`. Icons inline as SVG and recolor per theme automatically.

Use the **real per-slide content**. No lorem ipsum. The overwrite policy applies: never silently overwrite an existing `deck.yaml` or PNG — ask to overwrite, write a `-v2` variant, or pick a new name.

## Theme reference
Themes are pure data (JSON token files) in `themes/`. Built-ins:

| Theme | Look |
|---|---|
| `dark_navy` | Navy background, green/coral accents, gradient accent bar (replicates the reference deck). |
| `minimal_light` | Off-white, near-black text, single green accent, generous whitespace. |
| `bold_gradient` | Saturated purple→magenta gradient, high contrast, punchy. |
| `mono_editorial` | Near-black with a serif headline (IBM Plex Serif) and one gold accent — "premium newsletter". |

**Create a custom theme:** copy `themes/_custom_template.json`, edit the tokens, and set `meta.theme` to its path (e.g. `theme: ./my-theme.json`). All 7 color keys are required; `fonts.heading`/`fonts.body` must match a bundled family folder under `assets/fonts/` (`Inter`, `Space Grotesk`, `Manrope`, `IBM Plex Sans`, `IBM Plex Serif`). To add your own font, drop its `.woff2` files in `assets/fonts/<Family Name>/`. The `--spec-only` run prints a WCAG AA contrast report (≥4.5:1 body, ≥3:1 large text); a failing theme is warned about loudly, not blocked.

## Format reference
| Format | Pixels (1x) | Use |
|---|---|---|
| `square` | 1080×1080 | Safe, widely supported LinkedIn carousel. |
| `portrait` | 1080×1350 | **Default.** Most feed space, generally highest engagement. |
| `landscape` | 1920×1080 | **Not a native LinkedIn carousel size.** Provided for single-image reuse / cross-posting (blog headers, X). |

**LinkedIn rule:** for an actual swipeable carousel upload, every slide must be the **same size** — use `square` or `portrait`. Mixing sizes causes LinkedIn to pad/crop. Landscape is for repurposing individual slides, not for a carousel.

## Workflow

### 0. Confirm prerequisites & folders
Check `uv --version` (STOP + ask if missing). Ensure the one-time `uv sync` + `uv run playwright install chromium` has been done. Check `linkedin/` exists (cwd-relative); if not, ask. Check `voice-tone/` if tone consistency is expected; if missing, ask.

### 1. Author or assemble the deck spec
**Author it if it wasn't provided.** If the user did NOT provide ready copy and no `deck.yaml` exists at `linkedin/carousels/<slug>/deck.yaml`, author the deck from the source draft (`drafts/<slug>.md`) or the rough idea/notes:
- Produce **8–12 slides**, one clear idea per slide.
- Slide 1 = a strong **hook** (`title`, one bold claim, no logo dump).
- Last slide = a **CTA** (`cta`).
- Map ideas to the most fitting slide `type` (comparison, stat_grid, numbered_phase, process_loop, list_steps, quote).
- Set `meta.format` (default portrait) and `meta.theme`.

If ready copy or an existing `deck.yaml` was provided, use it directly and skip authoring.

**Voice compliance gate (before writing copy).** If `voice-tone/profile.md` (or raw `voice-tone/` samples) is present, scan the slide text against its "Avoided Words & Phrases" and "Punctuation & Formatting Quirks". Auto-fix mechanical violations (em-dashes to periods/commas, banned punctuation) and report what changed. Flag judgment calls (hype words, AI-voice markers). Never emit a banned pattern. If no voice-tone exists, skip silently.

If you authored the deck, **present it for review and get approval before rendering** (same review-first gate as Step 2).

Write the deck to `linkedin/carousels/<slug>/deck.yaml`. If one already exists there, check it first before re-authoring.

### 2. Emit spec + preview slide 1 (review-first)
Run from `$SKILL_DIR`:
```
uv run python -m engine.render --deck <cwd>/linkedin/carousels/<slug>/deck.yaml --spec-only
uv run python -m engine.render --deck <cwd>/linkedin/carousels/<slug>/deck.yaml --only 1 --out <cwd>/linkedin/carousels/<slug>
```
Pass the deck and `--out` as absolute or correctly-relative paths since the command runs from `$SKILL_DIR`. **STOP and let the user review the preview + spec before continuing.** If the spec flags an overflow risk, recommend shortening/splitting first.

### 3. Render all slides + PDF (after approval)
Drop `--only 1`:
```
uv run python -m engine.render --deck <cwd>/linkedin/carousels/<slug>/deck.yaml --out <cwd>/linkedin/carousels/<slug>
```
This writes `NN_<type>.png` for every slide into `<slug>/<format>/` and automatically merges them into `<slug>/<format>/<slug>.pdf`. Override with `--theme`, `--format`, `--scale`, or `--no-pdf` as needed.

## CLI reference (`engine/render.py`)
`uv run python -m engine.render --deck <path> [options]`

| Option | Effect |
|---|---|
| `--deck PATH` | Deck spec (`.yaml` or `.json`). **Required.** |
| `--theme NAME\|PATH` | Override `meta.theme` (built-in name or custom `.json` path). |
| `--format {square,portrait,landscape}` | Override `meta.format`. |
| `--out DIR` | Output root (default: skill's `output/`). Point at `linkedin/carousels/<slug>`. |
| `--only N` | Render only slide N (1-based); skips PDF. For the slide-1 preview. |
| `--scale F` | deviceScaleFactor (default `2.0` = retina). |
| `--spec-only` | Print the design spec + contrast + overflow lint and exit without rendering. |
| `--no-pdf` | Skip the automatic PNG→PDF merge. |

Exit codes: `0` ok, `1` deck/theme error, `2` `uv` missing, `3` rendered but with overflow-risk warnings.

## Engine layout
- `engine/render.py` — CLI orchestrator (uv check → validate → theme+contrast → Playwright screenshots → PDF).
- `engine/layout_engine.py` — Jinja2 fill, format presets, `@font-face` from bundled fonts, icon inlining, overflow lint.
- `engine/theme_loader.py` — load/validate theme tokens; run contrast check.
- `engine/contrast_check.py` — WCAG AA contrast ratios.
- `engine/deck_schema.json` — JSON schema for the deck + all 8 slide types.
- `templates/_base.html` + one `<type>.html` per slide type — Jinja2/HTML/CSS templates.
- `themes/*.json` — 4 built-in themes + `_custom_template.json`.
- `assets/fonts/` — bundled OFL/Apache WOFF2 fonts (**do not remove**). `assets/icons/` — flat/line SVG icons.
- `examples/example_deck.yaml` — worked example exercising all 8 slide types.

**Adding a new slide type:** add `templates/<type>.html` (extend `_base.html`) and a matching `oneOf` entry in `engine/deck_schema.json`. No core engine changes needed.

## Known limitations
- **No photorealistic/isometric illustrations.** The code-only approach uses a bundled flat/line SVG icon set; 3D/AI-style art is out of scope. Set expectations accordingly.
- **Font determinism depends on `assets/fonts/`.** Never delete it; headless Chromium otherwise substitutes system fonts and rendering drifts between machines.
- **Requires `uv` + a one-time Chromium download** (~150MB). The skill hard-stops if `uv` is missing rather than falling back to pip.
- **Overflow is auto-scaled to fit (no clipping).** Long copy is flagged in the spec as an overflow *risk* (exit `3`). During rendering, content is automatically scaled down to a minimum of **0.7x** to guarantee everything fits within the safe zone — text becomes smaller but rendering never clips. Shorten or split flagged slides if the scaled-down size looks too small.
- **Landscape is not a real LinkedIn carousel size** — use square/portrait for carousels.
- **Never auto-creates folders or overwrites files.** Asks if `linkedin/`/`voice-tone/` are missing; offers overwrite / `-v2` / new name when a target exists.

## Conventions
Shared assumptions so the content skills interoperate. Each works standalone.
- **Folders** (all cwd-relative): `drafts/`, `linkedin/`, `medium/`, `archive/`, `voice-tone/`. Never auto-create; ask if missing.
- **Slug**: lowercase, hyphenated, derived from the working title; reused as the filename stem across skills.
- **Filenames**: `drafts/<slug>.md`, `linkedin/<slug>-<type>.md`, carousels at `linkedin/carousels/<slug>/` with `deck.yaml`, `<format>/NN_<type>.png` per slide, and `<format>/<slug>.pdf`.
- **Overwrite policy**: never silently overwrite. Offer overwrite, a `-v2` (then `-v3`…) variant, or a new name.
- **Status values** (if a `content-log.md`/`content-log.json` tracker exists at cwd): `idea` → `drafted` → `reviewed` → `posted` → `archived`. If a tracker exists, after writing/moving a file ASK the user in one line whether to update it. Absence of a tracker must never block the skill.
