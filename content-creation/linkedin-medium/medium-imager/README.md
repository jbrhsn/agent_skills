# medium-imager

Turns Medium article copy into **actual rendered image files**: one wide featured cover image (1500x750, Medium's recommended ratio) plus up to 10 in-article slide-style images (1600x900) — quote cards, key-takeaway callouts, stat/number highlights, and code snippet cards. Pure local SVG rendering, then a **required** rasterization pass to PNG via `cairosvg`, since Medium does not accept raw SVG uploads.

---

## Trigger phrases

| Input | Example |
|---|---|
| Cover image | "make a cover image for this Medium article", "generate a featured image" |
| In-article images | "turn these pull quotes into images", "make a stat card / callout image", "render a code snippet as an image" |
| Themed look | "render these in dark-code / editorial-serif / bold-magazine style" |
| Handoff from copy | image copy provided directly, or auto-suggested from an existing `medium/<slug>.md` draft |

This skill is **standalone**. A title plus a few image entries is enough to run it; it does not require any other skill to have run first, though it can read from an existing `medium/<slug>.md` draft to suggest copy.

Do **not** use it to write or adapt the article copy itself (use `draft-builder` or `medium-writer` upstream), to verify tutorial code (use `tutorial-verifier`), or for a final editorial pass on wording (use `editorial-reviewer`).

---

## What it does

- **Two canvases, five image types.** A wide cover (1500x750) plus a shared 1600x900 slide canvas rendered as quote / callout / stat / code cards depending on each item's `type`.
- **Five built-in themes.** `clean-minimal` (default), `editorial-serif`, `dark-code`, `bold-magazine`, `warm-sepia` — each theme ships one cover template + one slide template, shared across all four inner types.
- **Required PNG rasterization, not optional.** Unlike a "best-effort" PDF combine step, this skill treats `cairosvg` as required: Medium won't accept SVG uploads, so a run isn't considered done until PNGs exist. Missing `cairosvg` is a hard stop with install instructions — but on user approval it can be auto-installed via `uv` into a local `.venv` (the `--install-missing` path).
- **Review-first, never end-to-end.** Emits a design spec, renders + rasterizes only the cover and the first inner image as a preview, then STOPS for approval before rendering/rasterizing everything.
- **Auto-fits every image.** Steps font sizes down until title/quote/callout/stat/code content fits the safe area above the reserved footer band; warns and exits non-fatally when an item still overflows so the copy can be shortened or split.
- **Draft-aware.** If `medium/<slug>.md` exists, a helper script suggests cover title/subtitle, pull-quote, callout, and stat candidates parsed from the draft — but always surfaces them for the user to confirm/edit before anything is written.
- **Runs a voice-compliance gate before writing image copy.** If a `voice-tone/` profile or samples exist, it scans the cover title/subtitle and every text field except code against the profile's avoided words/phrases and punctuation, auto-fixes mechanical violations, and flags judgment calls. Skips silently if no voice-tone exists.
- **Respects folder rules.** All paths are cwd-relative; never silently creates the `medium/` tree or guesses at a missing `voice-tone/` folder. It asks.

---

## Output

| File | Description |
|---|---|
| `medium/images/<slug>/<slug>-cover.svg` + `.png` | Wide featured cover image, 1500x750 (PNG rasterized at 2x = 3000x1500). |
| `medium/images/<slug>/<slug>-NN-<type>.svg` + `.png` | One pair per inner image (quote/callout/stat/code), 1600x900 (PNG at 2x = 3200x1800). |
| `medium/images/<slug>/images.json` | The canonical copy source for the run. |

SVG source files are always kept alongside the PNGs — PNG is the upload-ready deliverable, SVG stays as editable source.

---

## Theme catalog

| Theme | Files | Look |
|---|---|---|
| Clean minimal (default) | `cover-clean-minimal.svg` / `slide-clean-minimal.svg` | Flat off-white, single blue accent block, geometric sans. |
| Editorial serif | `cover-editorial-serif.svg` / `slide-editorial-serif.svg` | Cream background, Georgia serif, thin black accent rule. |
| Dark code | `cover-dark-code.svg` / `slide-dark-code.svg` | Near-black, monospace, terminal green accent. Best for code-heavy pieces. |
| Bold magazine | `cover-bold-magazine.svg` / `slide-bold-magazine.svg` | High-contrast black/white sans, thick red accent rules. |
| Warm sepia | `cover-warm-sepia.svg` / `slide-warm-sepia.svg` | Warm tan background, soft brown accent, serif italics. |

Theme choice affects only the visual chrome; the design spec and auto-fit are theme-independent because themes only set fill/font-family/weight via inline `<style>` classes — the renderer sets geometry. Add a new theme by copying a `cover-*.svg` + `slide-*.svg` pair and restyling, keeping the canvas, geometry, class names, and placeholders identical.

---

## Review-first flow

Never runs end-to-end automatically. The mandatory stop point is:

1. During the folder-confirm step, probe `cairosvg` up front. It is **required** (not best-effort) — if missing, report the install command and ask the user whether to auto-install it via `uv` into a local `.venv` (`--install-missing`); if declined, stop.
2. Emit a **design spec** with `scripts/spec.py` (canvases, theme, image count, per-image auto-fit result incl. overflow warnings).
3. Render + rasterize **only the cover and the first inner image** as a preview (`--only cover`, `--only 1`).
4. **STOP.** Show the spec + preview PNG paths and let the user review/approve. If the spec reports overflow on any item, recommend shortening/splitting that item's copy first.
5. Only after approval, render every remaining image to SVG and rasterize all of them to PNG.

---

## images.json schema

Canonical path: `medium/images/<slug>/images.json`. `index`/`total` for inner images are auto-filled from array position. Do not include them.

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

Fields per type (all `footer` fields optional):

| Type | Required | Optional |
|---|---|---|
| `cover` | `title` | `subtitle`, `footer` |
| `quote` | `quote` | `attribution`, `footer` |
| `callout` | `text` | `label` (rendered as an uppercase kicker), `footer` |
| `stat` | `number`, `label` | `footer` |
| `code` | `code` (newlines preserved) | `language` (small badge, no syntax highlighting), `footer` |

Up to 10 entries in `images`. An entry missing a required field, or with an unrecognized `type`, should cause the agent to stop and ask the user to fix the copy before writing `images.json`. Use real per-item content, no lorem ipsum.

---

## Scripts

- `scripts/images.py`: shared schema loader/validator for `images.json` (not a CLI entry point; imported by spec.py and render_svg.py).
- `scripts/spec.py`: reads images.json, prints design spec + per-image auto-fit result (font sizes, line counts, overflow flags) for the cover and every inner image. Flags: `--path`, `--theme`, `--json`, `--help`. Exit `3` if any item overflows.
- `scripts/render_svg.py`: images.json → SVG files. Cover 1500x750, slides 1600x900, auto-fit font sizing per type with overflow warning (exit `3`). Flags: `--out`, `--theme`, `--only cover|N`, `--help`.
- `scripts/svg_to_png.py`: SVG → PNG via `cairosvg` (**required**, hard error with install hint if missing — no graceful degrade). Flags: `--only cover|N`, `--scale` (default `2.0`), `--install-missing` (uv creates `.venv` and installs `cairosvg` on user approval, then re-runs), `--help`.
- `scripts/suggest_from_draft.py`: parses an existing `medium/<slug>.md` for candidate cover title/subtitle, pull-quotes, callout sections, and bolded stats. Prints suggestions only, never writes files. Flags: `--json`, `--help`.
- `templates/cover-*.svg` / `templates/slide-*.svg`: self-contained 1500x750 / 1600x900 templates per theme (see theme catalog).

All scripts use only the Python standard library except `svg_to_png.py`, which requires `cairosvg` — the one required, non-optional dependency of this skill.

Script and template paths resolve under `$SKILL_DIR`, the skill's own directory (project-local `.opencode/skills/medium-imager` or global `~/.config/opencode/skills/medium-imager`). Commands in the skill are prefixed with `$SKILL_DIR/scripts/...` and templates are referenced by `--theme <name>` (resolved internally to `$SKILL_DIR/templates/cover-<name>.svg` / `slide-<name>.svg`).

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Cover + image copy | Yes | Title + up to 10 inner images as a plain list, auto-suggested from `medium/<slug>.md` (with mandatory confirmation), or entered manually; written into `medium/images/<slug>/images.json` |
| Theme (`--theme`) | Optional | One of the five theme names; defaults to `clean-minimal` |
| `medium/` folder | Yes | Must already exist (cwd-relative); the skill asks rather than creating it |
| `voice-tone/` folder | Optional | Read for wording/style consistency if present; asked about if expected but missing |
| `cairosvg` | **Required** | Needed to produce the PNG deliverable; the skill probes for it up front and stops with install instructions if missing, or auto-installs it via `uv` into a local `.venv` on user approval (`--install-missing`) |

---

## Outputs

- **Design spec** (from `spec.py`): canvases, theme, image count, and per-image auto-fit/overflow results.
- **Cover + inner image files** under `medium/images/<slug>/`: one `.svg` + `.png` pair per item.
- **Cover + image-1 preview PNGs** during the review stop point before full render.

---

## Limitations

- **Not fully automatic.** Always stops after the spec + cover/image-1 preview for approval before rendering everything.
- **PNG rasterization is required, not optional.** Without `cairosvg`, no PNGs are produced and the script hard-fails with install instructions — unlike carousel-builder's best-effort PDF combine, this is a genuine blocker since Medium needs PNG. On user approval, `cairosvg` can be auto-installed via `uv` into a local `.venv` (the `--install-missing` path) rather than installed by hand.
- **Overflowing items are warned, not auto-fixed.** If copy is too long at the smallest font size, the skill flags the item (exit `3`) and recommends shortening/splitting rather than spilling over the footer band.
- **No syntax highlighting for code cards.** Code snippets render as plain monospace text with an optional language badge; no keyword coloring.
- **Draft auto-suggestion is best-effort.** `suggest_from_draft.py` uses simple heuristics (H1/H2 headings, blockquotes, bolded numeric patterns) and may miss or mis-tag content; suggestions always require explicit user confirmation before being written.
- **Never auto-creates folders or overwrites files.** Asks the user if `medium/`/`voice-tone/` are missing, and offers overwrite / `-v2` variant / new name when a target exists.
- **Tracker updates are prompted, not automatic.** If a `content-log.md`/`content-log.json` tracker exists, the skill asks in one line whether to update it after writing; a missing tracker never blocks the skill.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global, available in all projects (Linux/macOS)
cp -r content-creation/linkedin-medium/medium-imager ~/.config/opencode/skills/

# Per-project only
cp -r content-creation/linkedin-medium/medium-imager .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse content-creation\linkedin-medium\medium-imager "$env:USERPROFILE\.config\opencode\skills\"
```

Required PNG dependency:

```bash
uv pip install cairosvg   # or: pip install cairosvg
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/medium-imager.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before the imaging task |

---

## Companion skills

Part of the LinkedIn/Medium content suite. Pipeline order: `seed-expander` → `draft-builder` → {`linkedin-writer`, `medium-writer`} → {`medium-imager`, `carousel-builder`, `tutorial-verifier`} → `editorial-reviewer`, with `voice-profiler` and `content-tracker` as cross-cutting support.

- **`seed-expander`**: expands a raw idea into an outline/angle
- **`draft-builder`**: turns the outline into a full draft
- **`medium-writer`**: produces the Medium article copy this skill sources cover/image text from
- **`carousel-builder`**: sibling skill producing LinkedIn carousel images instead of Medium article images
- **`tutorial-verifier`**: sibling downstream step; runs and verifies tutorial code blocks
- **`editorial-reviewer`**: final editorial pass on wording/structure
- **`voice-profiler`**: builds the `voice-tone/` guidance this skill reads for style consistency
- **`content-tracker`**: maintains the `content-log` status (`idea` → `drafted` → `reviewed` → `posted` → `archived`)
