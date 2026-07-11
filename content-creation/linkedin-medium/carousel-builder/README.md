# carousel-builder

Turns carousel slide copy (typically 8–12 slides) into **actual rendered image files** for LinkedIn, either per-slide **SVG files** or **HTML/CSS slides** at 1080x1350 portrait, using pure local rendering. No external image APIs, no image-generation models. Core generation is Python stdlib-only; PNG export is an optional add-on.

---

## Trigger phrases

| Input | Example |
|---|---|
| Render carousel copy | "turn this carousel into slide images", "make LinkedIn carousel images from this" |
| Themed look | "render these slides in neon / glassmorphism / LinkedIn brand style" |
| Handoff from copy | slides passed in from `platform-adapter`, or a plain list of slide copy provided directly |

This skill is **standalone**. A list of slide copy is enough to run it; it does not require `platform-adapter` to have run first.

Do **not** use it to write or adapt the slide copy itself (use `platform-adapter`, or `draft-builder`/`seed-expander` upstream), to verify tutorial code (use `tutorial-verifier`), or for a final editorial pass on wording (use `editorial-reviewer`).

---

## What it does

- **Two rendering paths, user chooses.** SVG (single built-in dark style) or HTML/CSS (multiple themes). Always asks which path the user prefers before rendering.
- **Review-first, never end-to-end.** Emits a design spec, renders only slide 1 as a preview, then STOPS for approval before rendering all slides.
- **Auto-fits every slide.** Steps font sizes down until title+body fit the safe area above the reserved footer band; warns and exits non-fatally when a slide still overflows so the copy can be shortened or split.
- **Reads from a canonical slides JSON** at `linkedin/carousels/<slug>/slides.json`, using real per-slide content (no lorem ipsum).
- **Optional PNG export** with graceful degradation. SVGs/HTML stay valid output even when the PNG rasterizer is absent.
- **Respects folder rules.** All paths are cwd-relative; never silently creates the `linkedin/` tree or guesses at a missing `voice-tone/` folder. It asks.

---

## Rendering paths

Ask which path the user prefers before rendering. If they want a specific look (glassmorphism, neon, brand colors, etc.), use the HTML path and pick the matching theme.

| Path | Script | Output | Themes | Optional PNG |
|---|---|---|---|---|
| **SVG** | `scripts/render_svg.py` | one `.svg` per slide | Single built-in dark style (no themes) | `scripts/svg_to_png.py` via `cairosvg` |
| **HTML/CSS** | `scripts/render_html.py` | one `.html` per slide | Multiple themes via `--template` | headless browser (playwright/puppeteer) |

Both paths share the same 1080x1350 canvas, MARGIN 100, FOOTER_BAND 140 geometry and font constants, so the slide-1 preview and auto-fit spec stay valid regardless of path or theme.

---

## Theme catalog (HTML path only)

All themes live in `templates/`, share the exact same canvas/geometry and the same `{{TITLE}}` `{{BODY}}` `{{FOOTER}}` `{{INDEX}}` `{{TOTAL}}` placeholders. Select one with `--template` (default = `slide.html`).

| Theme | Template file | Look |
|---|---|---|
| Default (dark) | `templates/slide.html` | Slate dark, cyan accent (matches the SVG renderer). |
| Glassmorphism | `templates/slide-glassmorphism.html` | Frosted translucent card over a colorful blurred gradient. |
| Neomorphism | `templates/slide-neomorphism.html` | Soft monochrome UI with extruded/inset dual shadows. |
| Neon | `templates/slide-neon.html` | Near-black cyberpunk with glowing pink/cyan text + grid. |
| Super Mario | `templates/slide-mario.html` | Sky blue, `?`-block gold accent, brick footer, chunky type. |
| LinkedIn | `templates/slide-linkedin.html` | Official LinkedIn blue (#0A66C2) on white, "in" mark. |
| Minimal light | `templates/slide-minimal-light.html` | Clean editorial serif on off-white, single rule. |

Theme choice affects only the HTML render; the design spec and auto-fit are theme-independent. Some themes rely on effects a headless browser renders best (glassmorphism's `backdrop-filter`, neon glows, Mario shadows). The `.html` files are always valid, and if a PNG rasterizer ignores an effect the layout/text still render. Add a new theme by copying any template and restyling, keeping the canvas, geometry, and placeholders identical.

---

## Review-first flow

Never runs end-to-end automatically. The mandatory stop point is:

1. Emit a **design spec** with `scripts/spec.py` (canvas, palette, font, slide count, per-slide auto-fit result incl. overflow warnings).
2. Render **only slide 1** as a preview (`--only 1`).
3. **STOP.** Show the spec + preview path and let the user review/approve. If the spec reports overflow on any slide, recommend shortening/splitting that slide's copy first.
4. Only after approval, render all slides and (optionally) export PNGs.

---

## Slides JSON schema

Canonical path: `linkedin/carousels/<slug>/slides.json`. `index`/`total` are auto-filled from array position. Do not include them.

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
- `footer` (string, optional, e.g. handle/CTA)
- `slug` names the output folder and file prefix.

Use real per-slide content, no lorem ipsum. If `platform-adapter` produced the copy it will have written it to this same path, so check there first.

---

## Scripts

- `scripts/spec.py`: reads slides JSON, prints design spec + per-slide auto-fit result (font sizes, line counts, overflow flags). Flags: `--path`, `--render`, `--json`, `--help`. Exit `3` if any slide overflows.
- `scripts/render_svg.py`: slides JSON → SVG files. Portrait 1080x1350, minimal palette, auto-fit font sizing with overflow warning (exit `3`). Flags: `--out`, `--only`, `--help`.
- `scripts/render_html.py`: slides JSON → HTML files from a template (`--template`, default `templates/slide.html`). Flags: `--out`, `--only`, `--help`.
- `scripts/svg_to_png.py`: SVGs → PNGs via optional `cairosvg`. Never hard-fails; prints install/export guidance if unavailable. Flags: `--out`, `--scale`, `--help`.
- `templates/slide*.html`: self-contained 1080x1350 slide templates (see theme catalog).

All scripts use only the Python standard library for generation. `cairosvg` and a headless browser are **optional** add-ons for PNG export only.

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Slide copy | Yes | 8–12 slides as a plain list or handed off from `platform-adapter`; written into `linkedin/carousels/<slug>/slides.json` |
| Rendering path | Yes | SVG or HTML/CSS, asked before rendering |
| Theme (`--template`) | HTML path only | One of the theme catalog templates; defaults to `slide.html` (dark) |
| `linkedin/` folder | Yes | Must already exist (cwd-relative); the skill asks rather than creating it |
| `voice-tone/` folder | Optional | Read for wording/style consistency if present; asked about if expected but missing |
| `cairosvg` / headless browser | Optional | Only for PNG export; SVG/HTML output stays valid without them |

---

## Outputs

- **Design spec** (from `spec.py`): canvas, palette, font, slide count, and per-slide auto-fit/overflow results.
- **Slide files** under `linkedin/carousels/<slug>/`: one `.svg` per slide (SVG path) or one `.html` per slide (HTML path).
- **Slide-1 preview** during the review stop point before full render.
- **Optional PNGs**: from `svg_to_png.py` (cairosvg) or a headless browser, when available.

---

## Limitations

- **Not fully automatic.** Always stops after the spec + slide-1 preview for approval before rendering all slides.
- **PNG export is optional and best-effort.** Without `cairosvg` (SVG path) or a headless browser (HTML path), only the `.svg`/`.html` files are produced; the scripts print guidance and never hard-fail.
- **Themes apply to the HTML path only.** The SVG path has a single built-in dark style.
- **Overflowing slides are warned, not auto-fixed.** If copy is too long at the smallest font size, the skill flags the slide (exit `3`) and recommends shortening/splitting rather than spilling over the footer band.
- **Never auto-creates folders or overwrites files.** Asks the user if `linkedin/`/`voice-tone/` are missing, and offers overwrite / `-v2` variant / new name when a target exists.

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

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/carousel-builder.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before the carousel task |

---

## Companion skills

Part of the LinkedIn/Medium content suite. Pipeline order: `seed-expander` → `draft-builder` → `platform-adapter` → {`carousel-builder`, `tutorial-verifier`} → `editorial-reviewer`, with `voice-profiler` and `content-tracker` as cross-cutting support.

- **`seed-expander`**: expands a raw idea into an outline/angle
- **`draft-builder`**: turns the outline into a full draft
- **`platform-adapter`**: adapts the draft into platform formats, including the carousel slide copy this skill renders
- **`tutorial-verifier`**: sibling downstream step; runs and verifies tutorial code blocks
- **`editorial-reviewer`**: final editorial pass on wording/structure
- **`voice-profiler`**: builds the `voice-tone/` guidance this skill reads for style consistency
- **`content-tracker`**: maintains the `content-log` status (`idea` → `drafted` → `reviewed` → `posted` → `archived`)
