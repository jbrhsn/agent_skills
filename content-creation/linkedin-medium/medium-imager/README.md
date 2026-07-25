# medium-imager

Renders **cover + in-article images** for Medium articles from a manual spec or automatic placement suggestion. Covers are 1200×680 (configurable ratio: wide/square/16:9), optionally with a photo-background layer and contrast scrim. In-article images (1400px fixed width, variable height) include: quote blocks, stat callouts, comparison tables, code cards with Pygments syntax highlighting, section dividers, and three diagram patterns. All rendered locally via headless Chromium (Playwright) with Jinja2 templates and JSON themes — no external image APIs or AI models.

---

## Trigger phrases

| Input | Example |
|---|---|
| Cover image | "make a cover image for this Medium article", "generate a featured image for..." |
| In-article images | "turn these quotes/stats into images", "render a code snippet as an image", "make a comparison table visual" |
| Themed look | "render these in editorial-serif / techdocs-mono style" |
| Automatic placement | "auto-suggest images from this draft", "what images would you put here?" |
| Handoff from copy | spec provided directly, or auto-suggested from an existing `medium/<slug>.md` draft |

This skill is **standalone**. A spec is enough; doesn't require other skills to have run first.

Do **not** use it for writing/adapting the article copy itself (use `draft-builder` or `medium-writer` upstream), verifying tutorial code (use `tutorial-verifier`), or final editorial polish (use `editorial-reviewer`).

---

## What it does

- **Two canvases, eight image types.** A cover (1200×680, configurable ratio with optional photo layer) plus inline images (1400px wide, variable height) as quote/stat/callout/code/diagram/divider/comparison cards.
- **Three built-in themes** — `clean_minimal` (default), `editorial_serif`, `techdocs_mono` — each with color tokens, font stack, and a Pygments syntax-highlighting style.
- **Automatic cover ratios.** Default 1.76:1 (wide, 1200×680); user can pick square (1:1) or 16:9 per article.
- **Optional photo-background layer on covers.** User supplies a local image path; it's applied as a background with a theme-defined scrim/gradient overlay for text legibility. No AI image generation.
- **Pygments syntax highlighting for code cards.** Language detection from fenced-code-block tags; unknown language falls back to plain text (still styled/boxed).
- **Review-first flow, never end-to-end.** Emits design spec, renders + rasterizes only cover as preview, then STOPS for approval.
- **Auto-placement from draft (with confidence tags).** Parses Markdown AST + YAML front-matter, suggests placement for detected headings/blockquotes/tables/code blocks/stats, tags each as high/low confidence, prints proposal for user confirmation.
- **Manual mode (YAML/JSON spec).** User provides explicit per-image specs; no guessing.
- **Draft-aware.** If `medium/<slug>.md` exists, auto-mode suggests structural elements from it.
- **Both modes available.** User chooses: "here's my spec" (manual) or "auto-detect from my draft" (auto, propose-then-confirm).
- **Respects folder rules.** All paths cwd-relative; never silently creates `medium/` tree or guesses at `voice-tone/`. Asks.

---

## Output

| File | Description |
|---|---|
| `medium/images/<slug>/cover.png` | Cover image, 1200×680 (PNG rasterized at 2x = 2400×1360). |
| `medium/images/<slug>/NN_<type>.png` | One per in-article image (1400×variable, PNG at 2x = 2800×variable). |

PNG is the final deliverable (Medium doesn't accept SVG). All files are uploaded-ready out of the box.

---

## Image types

| Type | Required | Optional | Looks like |
|---|---|---|---|
| `cover` | — | `subtitle`, `photo` (path), `ratio` (wide/square/16:9) | Featured image with centered title + optional subtitle. Photo layer optional. |
| `section_divider` | — | `label` | Accent bar + section heading (visual break). |
| `stat_callout` | `value`, `label` | `context` | Big number + description (e.g. "80% latency reduction"). |
| `quote_block` | `quote` | `attribution` | Blockquote + speaker. |
| `comparison_table` | `title_left`, `title_right`, `rows` | — | Side-by-side table (before/after, A/B). |
| `code_card` | `code` | `language` | Code snippet with Pygments syntax highlighting. |
| `linear_flow` | `steps` | — | 2–6 steps → → → (horizontal flow). |
| `branch_2way` | `left_label`, `right_label`, `left_items`, `right_items` | — | Two columns: left (negatives), right (positives). |
| `stage_cycle` | `stages` | — | 2–4 stages in circular loop. |

---

## Theme catalog

| Theme | Look |
|---|---|
| Clean minimal (default) | Off-white background, Space Grotesk heading, blue accent, clean sans body. |
| Editorial serif | Cream bg, IBM Plex Serif heading, brown/gold accent, editorial/premium feel. |
| Techdocs mono | Terminal-dark (near-black), green/red accents, monospace-friendly, code-first. |

**Custom themes:** copy `themes/_custom_template.json`, edit colors/fonts/pygments_style, set `meta.theme: path/to/my-theme.json`. All 7 color keys required. Font families must match bundled folders under `assets/fonts/`. Add a new font by dropping `.woff2` files in `assets/fonts/<Family Name>/`.

---

## Review-first flow

Never runs end-to-end automatically:

1. During folder confirm, probe `uv`. If missing, STOP + ask user to install.
2. Emit **design spec** (images, theme, per-image auto-fit/overflow results, WCAG contrast report).
3. Render + rasterize **only the cover** as a preview PNG.
4. **STOP.** Show spec + preview PNG. Let user review/approve. If spec flags overflow on any item, recommend shortening/splitting.
5. Only after approval, render all remaining images.

---

## Spec schema (manual mode)

Canonical path: `medium/images/<slug>/spec.yaml` (or `.json`).

```yaml
meta:
  title: "How We Cut Latency by 80%"
  slug: cut-latency-80
  theme: clean_minimal
  cover:
    subtitle: "A practical guide to edge caching"
    ratio: wide               # wide | square | 16:9
    photo: null               # or path to local image

images:
  - type: stat_callout
    value: "80%"
    label: "latency reduction"

  - type: quote_block
    quote: "We went edge-first."
    attribution: "Sarah Chen"

  - type: code_card
    language: python
    code: |
      def fetch(key):
          ...
```

Use real per-item content, no lorem ipsum. Up to 10 images per spec.

---

## Auto-mode placement detection

Parses Markdown AST + optional YAML front-matter. Detection rules (all tagged high/low confidence):

- **Cover** (high): from front-matter title or H1.
- **Section dividers** (high): before each H2/H3.
- **Quote blocks** (high): Markdown blockquotes.
- **Comparison tables** (high): Markdown tables.
- **Code cards** (high): fenced code blocks (kept as Medium native by default; explicit image only on request).
- **Stat callouts** (low/high): standalone % / "X of Y" / large numbers.
- **Diagrams** (low): only if explicit ` ```diagram ` / ` ```mermaid ` blocks.

All suggestions are shown to user for confirmation before rendering — nothing silently wrong-placed.

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Cover + image copy | Yes | Spec (manual mode) or draft (auto mode). |
| Theme (`--theme`) | Optional | One of the three built-in names; defaults to `clean_minimal`. |
| `medium/` folder | Yes | Must exist (cwd-relative). Skill asks rather than creating. |
| `voice-tone/` folder | Optional | Read for consistency if present; asked about if expected but missing. |
| `uv` on PATH | **Required** | Must be installed (one-time check). |

---

## Outputs

- **Design spec** (from `--spec-only`): canvas, theme, image count, per-image auto-fit/overflow, WCAG contrast report.
- **Cover + in-article PNGs** under `medium/images/<slug>/`: one `.png` per item.
- **Cover-only preview PNG** during the review stop point.

---

## Limitations

- **Not fully automatic.** Always stops after spec + cover preview for approval before rendering all.
- **PNG rasterization is required, not optional.** Without `uv` + Chromium, no PNGs and script hard-fails (unlike carousel-builder's best-effort PDF) — Medium requires PNGs, not SVG.
- **Overflowing items are warned, not auto-fixed.** If copy is too long at smallest font size, flagged (exit `3`) — user shortens/splits.
- **Pattern-based diagrams only.** Diagrams are linear_flow, branch_2way, stage_cycle; not a general engine. Anything more complex is flagged for manual spec.
- **Auto-placement is heuristic.** Regex-based stat detection; edge cases may not trigger. All suggestions shown to user for confirmation — nothing guessed wrong silently.
- **Code cards default to native.** Fenced code blocks are kept as Medium's native block by default (copy-paste-friendly). Image rendering only on explicit request.
- **Pygments quality depends on language tags.** Missing/unsupported tags fall back to plain text (still styled, no coloring).
- **Font determinism depends on `assets/fonts/`.**Never delete; headless Chromium otherwise substitutes and drifts between machines.
- **Requires `uv` + Chromium (~150MB, one-time).** Skill hard-stops if `uv` is missing; never falls back to pip.
- **Never auto-creates folders or overwrites files.** Asks if `medium/` missing; offers overwrite / `-v2` / new name when target exists.
- **Tracker updates are prompted, not automatic.** If `content-log.md`/`content-log.json` exists, asks whether to update; missing tracker never blocks.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global (Linux/macOS):
cp -r content-creation/linkedin-medium/medium-imager ~/.config/opencode/skills/

# Per-project:
cp -r content-creation/linkedin-medium/medium-imager .opencode/skills/

# Windows (PowerShell):
Copy-Item -Recurse content-creation\linkedin-medium\medium-imager "$env:USERPROFILE\.config\opencode\skills\"
```

One-time setup:
```bash
cd ~/.config/opencode/skills/medium-imager  # (or .opencode/skills/...)
uv sync && uv run playwright install chromium
```

---

## Companion skills

Part of the LinkedIn/Medium content suite. Pipeline order: `seed-expander` → `draft-builder` → {`linkedin-writer`, `medium-writer`} → {`medium-imager`, `carousel-builder`, `tutorial-verifier`} → `editorial-reviewer`, with `voice-profiler` and `content-tracker` as cross-cutting support.

- **`medium-writer`**: produces the Medium article copy this skill sources image text from.
- **`carousel-builder`**: sibling skill producing LinkedIn carousel images (independent theme set, Playwright engine).
- **`tutorial-verifier`**: downstream step; runs and verifies code blocks.
- **`editorial-reviewer`**: final editorial pass on wording/structure.
- **`voice-profiler`**: builds the `voice-tone/` guidance this skill reads for style consistency.
- **`content-tracker`**: maintains content-log status (`idea` → `drafted` → `reviewed` → `posted` → `archived`).
