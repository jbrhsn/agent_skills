---
name: medium-imager
description: Use when the user wants to turn Medium article copy into actual rendered cover + in-article image files: generates a wide featured cover image (1200×680, with optional photo-background layer) plus in-article images (1400×variable: quote/stat/callout/code-snippet cards, comparison tables, section dividers, diagram flows) rendered locally via headless Chromium (Playwright) with Jinja2 templates, Pygments syntax highlighting, and JSON theme tokens. No external image APIs or models. Manual mode (YAML/JSON spec) or auto mode (propose placement from a draft, then render on confirmation).
---

# Medium Imager

Renders **actual cover + in-article images** for Medium articles from a spec or from auto-detected placement suggestions. Covers are 1200×680 (customizable ratio) with optional photo-background layer. In-article images (1400px fixed width, variable height) include: quote blocks, stat callouts, comparison tables, code cards with Pygments syntax highlighting, section dividers, and three diagram patterns (linear flow, 2-way branch, stage cycle). Renders locally via headless Chromium (Playwright) with Jinja2 templates and JSON themes — no external image APIs or AI models.

## When to use
- User has (or wants help drafting) cover + in-article image copy and wants postable PNG files.
- Input: manual spec (YAML/JSON), or a Markdown draft for automatic placement suggestion.
- This skill is **standalone** — a spec is enough; doesn't require other skills.

## Output
- **Cover PNG** at `medium/images/<slug>/<slug>-cover.png` (1200×680 @ 2x = 2400×1360 pixels).
- **In-article PNGs** at `medium/images/<slug>/<slug>-NN-<type>.png` (1400px wide, variable height @ 2x).
- Output directory defaults to `medium/images/<slug>/` (cwd-relative); ask before creating `medium/`.

## Prerequisites (one-time)
1. Check `uv --version`. If missing, **STOP and ask the user to install it** (`curl -LsSf https://astral.sh/uv/install.sh | sh`, or `brew install uv`, or `pipx install uv`). This skill never falls back to pip/venv.
2. From `$SKILL_DIR`, run once: `uv sync` then `uv run playwright install chromium`. After that, all rendering is fully local.
3. Fonts are bundled under `assets/fonts/` — do not delete; headless rendering otherwise drifts between machines.

## Folder rules (cwd-relative, never absolute)
- Output goes under `medium/images/<slug>/`.
- **If `medium/` does NOT exist, ASK the user** how to proceed. Never silently create the `medium/` tree.
- If tone/voice consistency is expected, check for `voice-tone/` folder (cwd-relative); if missing, ask.

Resolve `SKILL_DIR` to this skill's own directory: project-local `.opencode/skills/medium-imager` or global `~/.config/opencode/skills/medium-imager`.

## Review-first (mandatory stop point)
Never run end-to-end automatically.

1. Emit a **design spec** (title, theme, image count, per-image lint warnings, WCAG contrast report).
2. Render **only the cover** as a preview.
3. **STOP.** Show the spec + preview PNG and let the user review/approve. If spec reports overflow on any item, recommend shortening/splitting before proceeding.
4. Only after approval, render all remaining images.

## Operating modes

### Manual mode
User provides a spec file (YAML or JSON):
```bash
uv run python -m engine.render --spec medium/images/my-article/spec.yaml --spec-only
uv run python -m engine.render --spec medium/images/my-article/spec.yaml --only cover
uv run python -m engine.render --spec medium/images/my-article/spec.yaml
```

Spec schema: canonical path `medium/images/<slug>/spec.yaml` (or `.json`).
```yaml
meta:
  title: "How We Cut Latency by 80%"
  slug: cut-latency-80            # optional; derived from title if omitted
  theme: clean_minimal            # name in themes/, or path to custom .json
  cover:
    subtitle: "A practical guide to edge caching"
    ratio: wide                   # wide (default 1200×680) | square (1200×1200) | 16:9 (1280×720)
    photo: null                   # or path to local image for background layer

images:
  - type: stat_callout
    value: "80%"
    label: "latency reduction"
    context: "after edge caching"

  - type: quote_block
    quote: "Edge-first is how we think now."
    attribution: "Sarah Chen, VP Infra"

  - type: comparison_table
    title_left: "Before"
    title_right: "After"
    rows:
      - ["p99 latency", "800ms", "160ms"]
      - ["Cache hit", "12%", "94%"]

  - type: code_card
    language: python
    code: |
      def cached_fetch(key):
          ...

  - type: section_divider
    label: "Technical Details"

  - type: linear_flow
    steps: ["Step 1", "Step 2", "Step 3"]
```

### Auto mode (propose placement from draft)
User provides a Markdown draft; the skill parses it, suggests image placements (with confidence tags), and waits for confirmation before rendering:
```bash
uv run python -m engine.render --draft article.md --auto
```

Placement detection (all tagged `high`/`low` confidence):
- **Cover** (high): from YAML front-matter `title` or H1.
- **Section dividers** (high): before each H2/H3.
- **Quote blocks** (high): from Markdown blockquotes.
- **Comparison tables** (high): from Markdown tables.
- **Code cards** (high): from fenced code blocks (kept as Medium native by default; request image explicitly).
- **Stat callouts** (low/high): from standalone percentage/large-number claims.
- **Diagrams** (low): only if explicitly marked (` ```diagram ` / ` ```mermaid `) or via suggestions.

The proposal is printed for the user to review/edit; user approves and the skill renders with the confirmed spec.

## Image types (required/optional fields)

| Type | Required | Optional | Notes |
|---|---|---|---|
| `cover` (generated once) | — | `subtitle`, `photo` (path), `ratio` | Safe zone centered both axes; photo + scrim layer optional. |
| `section_divider` | — | `label` | Visual break between sections. |
| `stat_callout` | `value`, `label` | `context` | Large number + description. |
| `quote_block` | `quote` | `attribution` | Blockquote with optional speaker. |
| `comparison_table` | `title_left`, `title_right`, `rows` | — | Rows are `[[feature, left, right], ...]`. |
| `code_card` | `code` | `language` | Pygments syntax highlighting; lang detection optional. |
| `linear_flow` | `steps` | — | 2–6 horizontal steps with arrows. |
| `branch_2way` | `left_label`, `right_label`, `left_items`, `right_items` | — | Two-column A/B or before/after. |
| `stage_cycle` | `stages` | — | 2–4 stages in a circular loop. |

## Theme reference

Themes are JSON token files in `themes/`. Built-ins:

| Theme | Look |
|---|---|
| `clean_minimal` (default) | Off-white, Space Grotesk heading, blue accent, clean sans body. |
| `editorial_serif` | Cream bg, IBM Plex Serif heading, brown/gold accents, editorial feel. |
| `techdocs_mono` | Dark terminal (near-black), green/red accents, monospace-friendly. |

**Create a custom theme:** copy `themes/_custom_template.json`, edit the tokens (colors, fonts, pygments_style, decoration), and set `meta.theme` to its path (e.g. `theme: ./my-theme.json`).

All 7 color keys are required; fonts.heading/body must match a bundled family under `assets/fonts/` (Space Grotesk, IBM Plex Sans, IBM Plex Serif, Inter, Manrope). To add your own font, drop `.woff2` files in `assets/fonts/<Family Name>/`.

`--spec-only` run prints a WCAG AA contrast report (≥4.5:1 body, ≥3:1 large text); a failing theme is warned about loudly, not blocked.

## Workflow

### 0. Confirm prerequisites & folders
Check `uv --version` (STOP + ask if missing). Ensure one-time `uv sync` + `uv run playwright install chromium` is done. Check `medium/` exists; if not, ask. Check `voice-tone/` if expected; if missing, ask.

### 1. Assemble the spec (manual) or draft (auto)
**Manual:** user provides a spec file or describes it to you; you write `medium/images/<slug>/spec.yaml`.
**Auto:** user provides a draft `.md` file. You run the auto-placement engine, print the proposal, and wait for confirmation/edits.

### 2. Emit spec + preview cover (review-first)
From `$SKILL_DIR`:
```bash
uv run python -m engine.render --spec <cwd>/medium/images/<slug>/spec.yaml --spec-only
uv run python -m engine.render --spec <cwd>/medium/images/<slug>/spec.yaml --only cover --out <cwd>/medium/images/<slug>
```

**STOP and let the user review the preview PNG + spec before continuing.** If spec flags an overflow risk, recommend shortening/splitting.

### 3. Render all images (after approval)
Drop `--only cover` to render every image:
```bash
uv run python -m engine.render --spec <cwd>/medium/images/<slug>/spec.yaml --out <cwd>/medium/images/<slug>
```

Override with `--theme`, `--scale` (default 2.0 = retina) as needed.

## CLI reference (`engine/render.py`)
`uv run python -m engine.render [options]`

| Option | Effect |
|---|---|
| `--spec PATH` | Manual spec (`.yaml` or `.json`). |
| `--draft PATH --auto` | Auto-placement mode (parse draft, propose, wait for confirmation). |
| `--theme NAME\|PATH` | Override spec's `meta.theme`. |
| `--out DIR` | Output root (default: `medium/images/<slug>`). |
| `--only cover\|N` | Render only cover or image N (1-based); skips later images. |
| `--scale F` | deviceScaleFactor (default `2.0` = retina). |
| `--spec-only` | Print design spec + contrast report and exit without rendering. |

Exit codes: `0` ok, `1` spec/theme error, `2` `uv` missing, `3` rendered but with overflow-risk warnings.

## Engine layout
- `engine/render.py` — CLI orchestrator (uv check → validate → theme+contrast → Playwright screenshots).
- `engine/layout_engine.py` — Jinja2 fill, cover ratios, font-face CSS, inline width/height, overflow lint.
- `engine/theme_loader.py` — load/validate JSON themes; contrast check.
- `engine/contrast_check.py` — WCAG AA contrast ratios.
- `engine/draft_parser.py` — Markdown parsing + optional YAML front-matter extraction.
- `engine/placement_engine.py` — confidence-tagged placement proposal generation.
- `engine/code_highlight.py` — Pygments wrapper for syntax highlighting.
- `engine/spec_schema.json` — JSON schema for the spec.
- `templates/_base.html` + one per image type — Jinja2/HTML/CSS templates (in `templates/`).
- `themes/*.json` — 3 built-in themes + `_custom_template.json`.
- `assets/fonts/` — bundled OFL/Apache WOFF2 fonts. `assets/icons/` — flat/line SVG icons.
- `examples/example_article.md` — worked example with front-matter and mixed image types.

## Known limitations
- **Pattern-based diagrams only.** Diagrams are 3 simple patterns (linear flow, 2-way branch, stage cycle); not a general-purpose diagram engine. Anything more complex must be manually specified or flagged for custom design.
- **Auto-placement is heuristic.** Stat/diagram detection uses simple regex patterns; edge cases and complex prose structures may not be detected. All auto-mode suggestions are shown to the user for confirmation before rendering — nothing is silently placed wrong.
- **Code cards default to Medium native.** Code fences are detected but kept as Medium's native block by default (copy-paste-friendly). Explicit `code_card` images are generated only when requested.
- **Pygments quality depends on language tags.** If a fenced code block lacks a language tag or tags an unsupported language, Pygments falls back to plain text rendering (still styled, just no syntax coloring).
- **Font determinism depends on `assets/fonts/`.**  Never delete it; headless Chromium otherwise substitutes system fonts and rendering drifts between machines.
- **Requires `uv` + one-time Chromium download** (~150MB). Hard-stops if `uv` is missing rather than falling back to pip.
- **Overflow is warned, not auto-fixed.** Long copy is flagged (exit `3`); shorten or split the image.
- **Never auto-creates folders or overwrites files.** Asks if `medium/` is missing; offers overwrite / `-v2` / new name when a target exists.

## Conventions
Shared assumptions so content skills interoperate. Each works standalone.
- **Folders** (cwd-relative): `drafts/`, `medium/`, `linkedin/`, `archive/`, `voice-tone/`. Never auto-create; ask if missing.
- **Slug**: lowercase, hyphenated, derived from title; reused as filename stem across skills.
- **Filenames**: `medium/images/<slug>/spec.yaml`, `<slug>-cover.png`, `<slug>-NN-<type>.png` per image.
- **Overwrite policy**: never silently overwrite. Offer overwrite, a `-v2` (then `-v3`…) variant, or a new name.
- **Status** (if `content-log.md`/`content-log.json` exists at cwd): `idea` → `drafted` → `reviewed` → `posted` → `archived`. If tracker exists, ask 1-liner whether to update after writing. Absence of tracker never blocks.
