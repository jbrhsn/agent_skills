---
name: medium-image-prompts
description: Use when the user wants "image prompts for my Medium article", a "cover image for this Medium story", "visuals/illustrations for this Medium post", or a "featured image idea" — i.e. image-generation prompts for a finished Medium article. Produces one featured/cover image prompt plus one purposeful in-article visual prompt per major section that earns one (Medium is NOT a carousel platform), each with alt text, a caption including credit and the mandatory AI-disclosure line, and a rationale. Writes them to medium_image_prompts.md next to the source article. Does not render images — produces prompt text only.
---

# Medium Image Prompts

Generate image-generation prompts for a finished Medium article. Produces **prompt text only** — no image rendering, no API calls. The output is meant to be fed into whatever image-generation tool the user uses separately.

## When to use

- User has a finished article (typically `medium_article.md` or `medium_article_reviewed.md` from `medium-article-writer`) and wants visuals for it.
- User asks for "a cover image for this Medium story", "image prompts for my Medium article", "visuals/illustrations for this Medium post", or a "featured image idea".
- Not for actually rendering images — this skill produces prompts, not pixels.

## Input

A file path to the finished Medium article. If not given, ask. If the source directory contains exactly one obvious candidate (e.g. `medium_article.md` or `medium_article_reviewed.md`), propose it and confirm rather than asking from scratch.

## Output

`medium_image_prompts.md`, written in the **same directory as the source article file**. Never write to a fixed folder — always colocate.

**Overwrite policy**: never silently overwrite. If `medium_image_prompts.md` already exists, ask: overwrite, write `medium_image_prompts-v2.md`, or pick a new name.

---

## Why this format (verified Medium mechanics, retrieved 2026-07-30)

Grounded in Medium's official Using-images, Setting-a-featured-image, Read-time, Distribution Guidelines (updated 2026-06-29), and AI-content-policy help pages.

**Medium is NOT a carousel platform.** Unlike LinkedIn, a Medium article has (a) exactly **one featured/cover image** that gets pulled into the preview and social cards, and (b) **inline visuals placed at section breaks** inside the article body. So the decision is never "single hero vs carousel" — it is "one cover, plus how many purposeful in-article visuals the structure warrants, and where."

Why this shape wins on Medium:

- **Featured/cover image drives the card.** It's what gets pulled into the article preview + social cards; it's set via the featured-image picker (Shift+F). You set a **focal point** (Alt/Opt+click) so cropping stays clean across the homepage grid, feed cards, and social thumbnails — the same image is cropped to many aspect ratios, and a wrong/absent focal point produces bad crops. Full-width placement needs **≥1192px wide**; files up to 25MB; .JPG/.JPEG/.PNG/.GIF. Practical safe cover: **wide landscape, ~2:1 to 16:9, ≥1192px (ideally 1500px+)** so it survives every crop.
- **Curators reward purposeful, credited, captioned images** that "contribute to the story directly" — NOT decorative filler. Original/authentic visuals (your own photos, screenshots, charts, diagrams) signal first-hand experience and outperform generic stock. So every generated prompt targets a purposeful, contextual visual — not decoration.
- **Read-time effect.** Medium computes read time from word count (~265 WPM) **with an adjustment for images**, so meaningful images modestly increase displayed read time and the dwell signal. Another reason to place real visuals at section breaks — but filler is penalized, not rewarded.
- **AI-image disclosure is MANDATORY.** AI-generated images are allowed but **must be disclosed in the image caption**, e.g. "This image was created using an AI image creation program." Every prompt here is for an AI image generator, so every generated image needs that disclosure caption. Undisclosed AI erodes trust; undisclosed AI *writing* gets Network-only distribution — reinforce the disclosure habit.
- **Alt text + captions.** Medium natively supports alt text (accessibility + a curation quality signal) and captions (note: captions do not support italics). Every image should ship with short, descriptive alt text and a caption carrying credit + the AI-disclosure line.
- **In-article visual types that work best:** charts/diagrams, screenshots, and conceptual illustrations at section breaks. For code, prefer Medium's **native code blocks** over screenshots of code — they read better and are accessible/selectable. Place a visual roughly at each major section that genuinely needs one.

**Standalone reminder (state once in the output):** every image needs a **caption + credit**, and every **AI-generated image needs the AI-disclosure caption line**.

---

## Workflow — delegation-model units

The workflow is three self-contained units of work. Each unit lists its **goal/scope**, its **inputs**, the **self-verify** the doer runs before handing back, and the **report contract** (what it hands back). Do the units in order — each unit's report is the next unit's input. Unit 1 ends in a **hard hand-back gate** where control returns to the user.

---

### Unit 1 — Visual plan (HARD HAND-BACK GATE)

**Goal/scope:** Read the source article and propose the visual plan — the cover concept plus the list of in-article visuals (which sections, what each depicts, why each earns its place). State counts. Surface the reasoning and stop.

**Inputs:** File path to the finished article. If not given, ask. If the source directory contains exactly one obvious candidate (e.g. `medium_article.md` / `medium_article_reviewed.md`), propose it and confirm rather than asking from scratch.

**Do:** Read the article structure, then propose:

- **1 featured/cover image (always)** — a one-line concept tied to the article's core claim or hook.
- **N in-article visuals** — one per major section/beat that genuinely benefits from a visual (a chart/diagram, a screenshot, or a conceptual illustration at the section break). For each, name the section it sits at, what it depicts, and why it earns its place.

Recommend a sensible number: **roughly one visual per major section that needs one — do NOT force a visual onto every section.** Decorative-only filler is penalized by curators and does nothing for read-time, so leave a section imageless if no purposeful visual fits. State the counts explicitly (e.g. "Cover + 3 in-article visuals: Section 2 process diagram, Section 4 results chart, Section 6 screenshot").

**Self-verify:** Confirm the plan follows from the article's structure (sections named), that every proposed in-article visual is purposeful (not decorative filler), and that the cover concept ties to the article's core claim.

**⛔ HAND-BACK GATE:** Do NOT proceed to Unit 2. Hand back to the user and **wait for them to confirm or override** the plan (cover concept, visual count, and placements). This is a judgment call, not a hard rule — never silently pick.

**Report contract (hands back):**
- Source file used.
- Plan: cover concept (one line) + the list of in-article visuals (section, what it depicts, why it earns its place).
- Counts: "Cover + N in-article visuals."
- Explicit request: "Confirm or override this plan before I generate prompts."

---

### Unit 2 — Prompt generation

**Goal/scope:** Produce the full prompt set — the cover plus each confirmed in-article visual — to spec.

**Inputs:** The **user-confirmed plan** from Unit 1, and the source article.

**Do:** For the cover AND each confirmed in-article visual, write an entry with:

1. **Role/placement** — e.g. "Cover" / "Section 2 — the process diagram".
2. **Image-generation prompt** — a detailed prompt covering: composition/layout, subject matter or visual metaphor, style direction (e.g. minimal flat illustration, photo-real, clean data-viz, diagram), and color/mood direction.
   - **For the cover only, also specify:** a **wide landscape composition (~2:1 to 16:9)** suitable for cropping, a clear central **focal point** the crop can lock onto (so social/grid/feed crops stay clean), and a **≥1192px wide (ideally 1500px+)** resolution note.
   - Prefer purposeful visual types: charts/diagrams, screenshots, conceptual illustrations. For code, note that a **native code block reads better than a code screenshot**.
3. **Alt text** — a suggested short, descriptive alt-text line (accessibility + curation signal).
4. **Caption** — a suggested caption including a **credit**, and — because these are AI-generated — the **AI-disclosure line**, e.g. "This image was created using an AI image creation program." (No italics in captions.)
5. **Rationale** — one line on how the image contributes to the story directly (not decoration).

**Self-verify (doer runs this itself before reporting):**
- **Every image is purposeful** — no decorative-only filler; each earns its place from the article's content.
- **Cover meets guidance** — wide landscape (~2:1 to 16:9), explicit focal point, ≥1192px note present.
- **Every entry has all four attachments** — alt text + caption (with credit) + the AI-disclosure line + rationale.
- **Code handled right** — where the visual is code, native-code-block preference is noted rather than defaulting to a text/code screenshot.

**Report contract (to Unit 3):**
- Counts: cover + N in-article visuals.
- The full prompt set, passed internally to Unit 3 for writing (Role/Placement + Prompt + Alt text + Caption + Rationale per image) — this is an internal handoff, not something to paste to the user in chat.
- Self-verify result: pass, or the specific items flagged.

---

## Output format (`medium_image_prompts.md`)

```markdown
# Image Prompts — <article title>

**Set:** Cover + N in-article visuals
**Reasoning:** <one line — how the visuals map to the article's structure>

> Reminder: every image needs a caption + credit. Every AI-generated image
> needs an AI-disclosure caption line, e.g. "This image was created using an
> AI image creation program."

## Cover — Featured image
**Prompt:** <composition/layout; subject or visual metaphor; style; color/mood; WIDE LANDSCAPE ~2:1–16:9; set a focal point for clean cropping; render ≥1192px wide (ideally 1500px+)>
**Alt text:** ...
**Caption:** <credit> · This image was created using an AI image creation program.
**Rationale:** ...

## Section 2 — <what it depicts>
**Prompt:** ...
**Alt text:** ...
**Caption:** <credit> · This image was created using an AI image creation program.
**Rationale:** ...

## Section N — <what it depicts>
...
```

---

### Unit 3 — Sanity check + persist

**Goal/scope:** Write the prompt set to disk first (as a draft), then present a short summary + file pointer for a quick sanity check.

**Inputs:** The full prompt set and self-verify result from Unit 2; the source file's directory.

**Do:**
1. Write `medium_image_prompts.md` **next to the source file first**, applying the overwrite policy (never silently overwrite: if a file already exists from a prior run, offer overwrite, `medium_image_prompts-v2.md`, or a new name).
2. Present ONLY a **short summary + the file path** for a quick sanity check (catches obvious mismatches early): the counts (cover + N in-article visuals) and any entries flagged (e.g. a section where no purposeful visual fit). **Do NOT paste the full prompt set into chat** — point the user to the written file to review. Ask for a quick confirm or revisions. This is a **lighter gate** than the Unit 1 plan stop.
3. On revision, **re-edit the file in place and re-point** the user to it (in-place updates don't re-trigger the overwrite prompt; the prior-run-file overwrite policy still applies only to the first write).

**Self-verify (doer runs this itself before reporting):**
- The written file matches the output-format block above (Set + Reasoning header, one entry per image with Role/Placement / Prompt / Alt text / Caption / Rationale).
- The **caption + credit** requirement and the **AI-disclosure** reminder appear in the output (the standalone reminder block is present, and every caption carries the disclosure line).
- The cover entry carries the resolution / ratio / focal-point guidance.
- The file was colocated with the source (not a fixed folder), and the overwrite policy was honored.

**Report contract (hands back to user):**
- Wrote `<exact path>` first, then presented a summary for confirm.
- Counts: cover + N in-article visuals.
- Any entries flagged (e.g. a section where no purposeful visual fit).
- Explicit note that the full prompt set is in the file (not pasted here) — user reviews it there.
- Pass, or the specific issue flagged.

---

## Handoff

This skill produces prompt text only. Rendering the prompts into actual images is outside its scope — hand the file to whatever image-generation tool the user already uses. Remind the user, when they publish, to set the cover via the featured-image picker (Shift+F), set the focal point (Alt/Opt+click), and add the alt text + caption (with credit + AI-disclosure line) to every image on Medium.

If the user later revises the article via `medium-article-writer`'s review path (which produces `medium_article_reviewed.md`), that revised file can be fed back through Unit 1 to regenerate the visual plan.
