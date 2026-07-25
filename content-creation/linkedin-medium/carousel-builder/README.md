# carousel-builder

Authors a typed carousel **deck spec** from a source draft or a rough idea when
none is provided, then renders it into **actual PNG slide files** for LinkedIn —
square, portrait, or landscape — and **merges them into a single multi-page
PDF**. Slides are rendered locally from HTML/CSS through headless Chromium
(Playwright): one element screenshot of a fixed-size canvas per slide. Ready
slide copy or an existing `deck.yaml` can also be passed in and rendered as-is.
No external image APIs, no image-generation models. Python tooling is managed
with `uv`; fonts are bundled locally for deterministic cross-machine rendering.

---

## Trigger phrases

| Input | Example |
|---|---|
| Author from a draft/idea | "turn this draft into a carousel", "make a LinkedIn carousel from this idea" |
| Render a deck spec | "render this deck.yaml", "turn this carousel into slide images" |
| Themed look | "render these slides in bold_gradient / mono_editorial" |
| Format | "make it square", "portrait carousel", "landscape version for cross-posting" |
| PDF deck | "combine my carousel into a PDF" |

This skill is **standalone**. A source draft, a rough idea, or a plain list of
slide copy is enough to run it. It authors the deck itself when none is
provided. Do **not** use it for full article drafting (use `draft-builder`),
idea expansion (`seed-expander`), tutorial code verification
(`tutorial-verifier`), or final editorial wording passes (`editorial-reviewer`).

---

## What it does

- **Authors a deck when none is provided** — 8–12 slides from a draft or idea, hook first, CTA last, each mapped to the best-fitting slide type. Ready copy / an existing `deck.yaml` is used as-is.
- **Eight typed slide layouts** — `title`, `comparison`, `quote`, `stat_grid`, `numbered_phase`, `process_loop`, `list_steps`, `cta`. Each is a self-contained HTML template driven by data.
- **Four built-in themes + a custom-theme path** — `dark_navy`, `minimal_light`, `bold_gradient`, `mono_editorial`, plus a documented token file you copy and edit.
- **Three formats** — square (1080×1080), portrait (1080×1350, default), landscape (1920×1080). LinkedIn carousels should be square/portrait; landscape is for single-image reuse.
- **Deterministic rendering** — headless Chromium with bundled local WOFF2 fonts (no system-font or web-font drift) at 2x for retina-quality PNGs.
- **Schema-validated deck spec** — validated against `engine/deck_schema.json`; fails fast with the slide index and offending field.
- **WCAG AA contrast check** — every theme's color tokens are checked (≥4.5:1 body, ≥3:1 large text); failures are warned loudly.
- **Overflow lint** — per-field character budgets per slide type warn when copy is likely to overflow (exit `3`).
- **Automatic combined PDF** — PNGs are merged into one PDF after the full render (opt out with `--no-pdf`).
- **Review-first** — emits a design spec + a slide-1 preview, then STOPS for approval before rendering everything.
- **Voice-compliance gate** — if a `voice-tone/` profile/samples exist, scans slide copy against them, auto-fixes mechanical violations, flags judgment calls. Skips silently if absent.
- **Respects folder rules** — cwd-relative; never silently creates `linkedin/` or guesses at a missing `voice-tone/`.

---

## Output

| File | Description |
|---|---|
| `linkedin/carousels/<slug>/<format>/NN_<type>.png` | One PNG per slide (primary output, retina 2x). |
| `linkedin/carousels/<slug>/<format>/<slug>.pdf` | Single multi-page PDF, produced automatically after the full render. |

---

## Deck spec

Canonical path: `linkedin/carousels/<slug>/deck.yaml` (JSON also accepted).

```yaml
meta:
  title: "My Carousel"
  slug: my-carousel        # optional; derived from title if omitted
  format: portrait         # square | portrait | landscape (default portrait)
  theme: dark_navy         # a name in themes/, or a path to a custom theme .json
  footer: "@handle"
slides:
  - type: title
    headline: "One bold claim"
    subheadline: "Optional supporting line."
  - type: cta
    headline: "Your close"
    action: "Follow for more"
```

See `SKILL.md` for the required/optional fields of all eight slide types and the
full CLI reference. A complete worked example lives at
`examples/example_deck.yaml` (exercises every slide type).

---

## Themes

| Theme | Look |
|---|---|
| `dark_navy` | Navy, green/coral accents, gradient bar (reference-deck palette). |
| `minimal_light` | Off-white, near-black, single accent, whitespace. |
| `bold_gradient` | Purple→magenta gradient, high contrast, punchy. |
| `mono_editorial` | Near-black, serif headline, one gold accent. |

**Custom theme:** copy `themes/_custom_template.json`, edit the tokens, and set
`meta.theme` to its path. All 7 color keys are required; fonts must match a
bundled family (`Inter`, `Space Grotesk`, `Manrope`, `IBM Plex Sans`,
`IBM Plex Serif`). Run `--spec-only` to see the contrast report.

---

## Usage

Run from the skill directory (`$SKILL_DIR`) so bundled fonts/templates/themes resolve.

```bash
# One-time setup
uv sync
uv run playwright install chromium

# Review-first: spec + slide-1 preview (STOP here for approval)
uv run python -m engine.render --deck path/to/deck.yaml --spec-only
uv run python -m engine.render --deck path/to/deck.yaml --only 1 --out path/to/linkedin/carousels/<slug>

# Full render + automatic PDF (after approval)
uv run python -m engine.render --deck path/to/deck.yaml --out path/to/linkedin/carousels/<slug>
```

| Option | Effect |
|---|---|
| `--deck PATH` | Deck spec (`.yaml`/`.json`). Required. |
| `--theme NAME\|PATH` | Override `meta.theme`. |
| `--format {square,portrait,landscape}` | Override `meta.format`. |
| `--out DIR` | Output root. |
| `--only N` | Render only slide N (skips PDF). |
| `--scale F` | deviceScaleFactor (default 2.0). |
| `--spec-only` | Print spec + contrast + lint, no render. |
| `--no-pdf` | Skip PDF merge. |

Exit codes: `0` ok · `1` deck/theme error · `2` `uv` missing · `3` rendered with overflow warnings.

---

## Structure

```
carousel-builder/
├── SKILL.md               # trigger conditions, usage, slide/theme/format reference
├── pyproject.toml         # uv-managed deps: playwright, jinja2, pyyaml, jsonschema, img2pdf
├── engine/
│   ├── render.py          # CLI entrypoint
│   ├── layout_engine.py   # Jinja2 fill, format presets, font-face, icons, overflow lint
│   ├── theme_loader.py    # load + validate theme tokens
│   ├── contrast_check.py  # WCAG AA contrast validation
│   └── deck_schema.json   # deck + 8-slide-type JSON schema
├── templates/             # _base.html + one HTML per slide type
├── themes/                # 4 built-in themes + _custom_template.json
├── assets/
│   ├── fonts/             # bundled OFL/Apache WOFF2 (do NOT remove) + licenses
│   └── icons/             # flat/line SVG icon set
├── examples/example_deck.yaml
└── output/                # gitignored render target
```

**Adding a slide type:** add `templates/<type>.html` (extends `_base.html`) and a
matching `oneOf` entry in `engine/deck_schema.json`. No core engine changes.

---

## Limitations

- **No photorealistic/isometric illustrations** — code-only rendering uses a bundled flat/line SVG icon set; 3D/AI art is out of scope.
- **Font determinism depends on `assets/fonts/`** — do not delete it or headless rendering drifts across machines.
- **Requires `uv` + a one-time Chromium download (~150MB)** — the skill hard-stops if `uv` is missing and never falls back to pip.
- **Overflow is warned, not auto-fixed** — long copy is flagged (exit `3`); shorten or split.
- **Landscape is not a native LinkedIn carousel size** — use square/portrait for carousels.
- **Review-first, never end-to-end** — always stops after the spec + slide-1 preview.
- **Never auto-creates folders or overwrites files** — asks about missing `linkedin/`/`voice-tone/`; offers overwrite / `-v2` / new name.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global, available in all projects (Linux/macOS)
cp -r content-creation/linkedin-medium/carousel-builder ~/.config/opencode/skills/

# Per-project only
cp -r content-creation/linkedin-medium/carousel-builder .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse content-creation\linkedin-medium\carousel-builder "$env:USERPROFILE\.config\opencode\skills\"
```

Then, once, from inside the copied skill directory:

```bash
uv sync
uv run playwright install chromium
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/carousel-builder.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before the carousel task |

---

## Companion skills

Part of the LinkedIn/Medium content suite. Pipeline order: `seed-expander` →
`draft-builder` → {`linkedin-writer`, `medium-writer`} → {`carousel-builder`,
`medium-imager`, `tutorial-verifier`} → `editorial-reviewer`, with
`voice-profiler` and `content-tracker` as cross-cutting support.

- **`seed-expander`**: expands a raw idea into an outline/angle
- **`draft-builder`**: turns the outline into a full draft
- **`linkedin-writer`**: writes LinkedIn post copy from a draft
- **`tutorial-verifier`**: sibling downstream step; runs and verifies tutorial code
- **`editorial-reviewer`**: final editorial pass on wording/structure
- **`voice-profiler`**: builds the `voice-tone/` guidance this skill reads
- **`content-tracker`**: maintains the `content-log` status
