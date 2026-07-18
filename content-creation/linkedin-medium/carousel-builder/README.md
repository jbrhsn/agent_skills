# carousel-builder

Turns carousel slide copy (typically 8–12 slides) into **actual rendered SVG image files** for LinkedIn at 1080x1350 portrait, then **combines them into a single multi-page PDF** — using pure local rendering. No external image APIs, no image-generation models. Core generation is Python stdlib-only; the PDF combine step needs `cairosvg` + `Pillow` and, with user approval, can install them into a local `.venv` using `uv`.

---

## Trigger phrases

| Input | Example |
|---|---|
| Render carousel copy | "turn this carousel into slide images", "make LinkedIn carousel images from this" |
| Themed look | "render these slides in neon / glassmorphism / LinkedIn brand style" |
| PDF deck | "combine my carousel into a PDF", "give me one PDF of the slides" |
| Handoff from copy | slides passed in from `platform-adapter`, or a plain list of slide copy provided directly |

This skill is **standalone**. A list of slide copy is enough to run it; it does not require `platform-adapter` to have run first.

Do **not** use it to write or adapt the slide copy itself (use `platform-adapter`, or `draft-builder`/`seed-expander` upstream), to verify tutorial code (use `tutorial-verifier`), or for a final editorial pass on wording (use `editorial-reviewer`).

---

## What it does

- **SVG-only rendering with seven themes.** Every slide is a self-contained portrait SVG at 1080x1350. Themes cover default dark, glassmorphism, neomorphism, neon, Super Mario, LinkedIn brand, and minimal light.
- **Automatic combined PDF.** After the full render, the skill combines every SVG into one multi-page PDF at `linkedin/carousels/<slug>/<slug>.pdf`. Requires `cairosvg` + `Pillow`; without them the SVGs stay valid, and the agent asks before creating `.venv` with `uv` and installing dependencies.
- **Review-first, never end-to-end.** Emits a design spec, renders only slide 1 as a preview, then STOPS for approval before rendering all slides + PDF.
- **Auto-fits every slide.** Steps font sizes down until title+body fit the safe area above the reserved footer band; warns and exits non-fatally when a slide still overflows so the copy can be shortened or split.
- **Reads from a canonical slides JSON** at `linkedin/carousels/<slug>/slides.json`, using real per-slide content (no lorem ipsum).
- **Probes PDF tooling up front** (`cairosvg`, `Pillow`) and reports whether the final PDF step will succeed before rendering, so limits are known early rather than discovered at the end.
- **Runs a voice-compliance gate before writing slide copy.** If a `voice-tone/` profile or samples exist, it scans slide titles and bodies against the profile's avoided words/phrases and punctuation, auto-fixes mechanical violations, and flags judgment calls. Skips silently if no voice-tone exists.
- **Respects folder rules.** All paths are cwd-relative; never silently creates the `linkedin/` tree or guesses at a missing `voice-tone/` folder. It asks.

---

## Output

| File | Description |
|---|---|
| `linkedin/carousels/<slug>/<slug>-NN.svg` | One SVG per slide (primary output, always produced). |
| `linkedin/carousels/<slug>/<slug>.pdf` | Single multi-page PDF, one page per slide, produced automatically after full render when `cairosvg` + `Pillow` are available. |

---

## Theme catalog

All themes live in `templates/` as `.svg` files. They share the same 1080x1350 canvas and the same `{{TITLE_BLOCK}}` `{{BODY_BLOCK}}` `{{FOOTER}}` `{{COUNTER}}` `{{INDEX}}` `{{TOTAL}}` placeholders. Select one with `--template` (default = `slide.svg`).

| Theme | Template file | Look |
|---|---|---|
| Default (dark) | `templates/slide.svg` | Slate dark, cyan accent. |
| Glassmorphism | `templates/slide-glassmorphism.svg` | Frosted translucent card over a blurred colorful gradient. |
| Neomorphism | `templates/slide-neomorphism.svg` | Soft monochrome UI with extruded/inset dual shadows. |
| Neon | `templates/slide-neon.svg` | Near-black cyberpunk with glowing pink/cyan text + grid. |
| Super Mario | `templates/slide-mario.svg` | Sky blue, `?`-block gold accent, brick footer, chunky type. |
| LinkedIn | `templates/slide-linkedin.svg` | Official LinkedIn blue (#0A66C2) on white, "in" mark. |
| Minimal light | `templates/slide-minimal-light.svg` | Editorial serif on off-white, single accent rule. |

Theme choice affects only the visual chrome; the design spec and auto-fit are theme-independent because themes only set fill/font-family/weight via inline `<style>` classes (`title`, `body`, `footer`) — the renderer sets geometry. Add a new theme by copying any template and restyling, keeping the canvas, geometry, class names, and placeholders identical.

---

## Review-first flow

Never runs end-to-end automatically. The mandatory stop point is:

1. During the folder-confirm step, probe the PDF tooling (`cairosvg`, `Pillow`) and report whether the combined PDF step will succeed.
2. Emit a **design spec** with `scripts/spec.py` (canvas, template, slide count, per-slide auto-fit result incl. overflow warnings).
3. Render **only slide 1** as a preview (`--only 1`).
4. **STOP.** Show the spec + preview path and let the user review/approve. If the spec reports overflow on any slide, recommend shortening/splitting that slide's copy first.
5. Only after approval, render all slides and automatically combine them into the single PDF.

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
- `slug` names the output folder, per-slide file prefix, and the combined PDF name.

Use real per-slide content, no lorem ipsum. If `platform-adapter` produced the copy it will have written it to this same path, so check there first.

---

## Scripts

- `scripts/spec.py`: reads slides JSON, prints design spec + per-slide auto-fit result (font sizes, line counts, overflow flags). Flags: `--path`, `--template`, `--json`, `--help`. Exit `3` if any slide overflows.
- `scripts/render_svg.py`: slides JSON → SVG files. Portrait 1080x1350, auto-fit font sizing with overflow warning (exit `3`). Flags: `--out`, `--template`, `--only`, `--help`.
- `scripts/combine_pdf.py`: SVGs → single multi-page PDF via `cairosvg` + `Pillow` (both optional). Prints `uv` install guidance if unavailable; with user approval, `--install-missing` creates `.venv`, installs `cairosvg pillow`, and reruns the combine step. Flags: `--out`, `--scale`, `--install-missing`, `--help`.
- `templates/slide*.svg`: self-contained 1080x1350 slide templates (see theme catalog).

All scripts use only the Python standard library for SVG generation. `cairosvg` and `Pillow` are **optional** add-ons for the PDF combine step only and should be installed with `uv` when needed.

Script and template paths resolve under `$SKILL_DIR`, the skill's own directory (project-local `.opencode/skills/carousel-builder` or global `~/.config/opencode/skills/carousel-builder`). Commands in the skill are prefixed with `$SKILL_DIR/scripts/...` and `$SKILL_DIR/templates/...`.

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Slide copy | Yes | 8–12 slides as a plain list or handed off from `platform-adapter`; written into `linkedin/carousels/<slug>/slides.json` |
| Theme (`--template`) | Optional | One of the seven theme templates; defaults to `slide.svg` (dark) |
| `linkedin/` folder | Yes | Must already exist (cwd-relative); the skill asks rather than creating it |
| `voice-tone/` folder | Optional | Read for wording/style consistency if present; asked about if expected but missing |
| `cairosvg` + `Pillow` | Optional | Only for the combined PDF; SVG output stays valid without them; install through `uv` after confirmation |

---

## Outputs

- **Design spec** (from `spec.py`): canvas, template, slide count, and per-slide auto-fit/overflow results.
- **Slide files** under `linkedin/carousels/<slug>/`: one `.svg` per slide.
- **Slide-1 preview** during the review stop point before full render.
- **Combined PDF** at `linkedin/carousels/<slug>/<slug>.pdf` when `cairosvg` + `Pillow` are available.

---

## Limitations

- **Not fully automatic.** Always stops after the spec + slide-1 preview for approval before rendering all slides.
- **PDF combine is optional but supported.** Without `cairosvg` (rasterizer) and `Pillow` (PDF writer), only the `.svg` files are produced until the user approves `uv` dependency setup.
- **Overflowing slides are warned, not auto-fixed.** If copy is too long at the smallest font size, the skill flags the slide (exit `3`) and recommends shortening/splitting rather than spilling over the footer band.
- **SVG effect fidelity varies.** Themes with heavy effects (glassmorphism blur, neon glow, Mario textures) render natively in modern viewers and rasterize fine through cairosvg. Very old rasterizers may ignore some filters; the layout/text still render.
- **Never auto-creates folders or overwrites files.** Asks the user if `linkedin/`/`voice-tone/` are missing, and offers overwrite / `-v2` variant / new name when a target exists.
- **Tracker updates are prompted, not automatic.** If a `content-log.md`/`content-log.json` tracker exists, the skill asks in one line whether to update it after writing; a missing tracker never blocks the skill.

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

Optional PDF dependencies:

```bash
uv venv .venv
uv pip install --python .venv/bin/python cairosvg pillow
```

Or let the script do the same after user confirmation:

```bash
python3 content-creation/linkedin-medium/carousel-builder/scripts/combine_pdf.py linkedin/carousels/<slug> --install-missing
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
