---
name: linkedin-image-prompts
description: Use when the user wants image-generation prompts for a LinkedIn post or article, wants to turn a post into a carousel, or asks for slide/visual ideas for a written piece. Decides between a single hero image and a multi-slide carousel based on content structure (or asks), then writes one detailed image-generation prompt per image/slide to image_prompts.md next to the source post. Does not render images — produces prompt text only.
---

# LinkedIn Image Prompts

Generate image-generation prompts for a finished LinkedIn post or article. Produces **prompt text only** — no image rendering, no API calls. The output is meant to be fed into whatever image-generation tool the user uses separately.

## When to use

- User has a finished post (typically `linkedin_post.md` from `linkedin-post-writer`) and wants visuals for it.
- User asks to "turn this into a carousel", "give me slide ideas", or "generate image prompts for this post".
- Not for actually rendering images or PDFs — this skill produces prompts, not pixels.

## Input

A file path to the finished post/article. If not given, ask. If the source directory contains exactly one obvious candidate (e.g. `linkedin_post.md`), you may propose it and confirm rather than asking from scratch.

## Output

`image_prompts.md`, written in the **same directory as the source post file**. Never write to a fixed folder — always colocate.

**Overwrite policy**: never silently overwrite. If `image_prompts.md` already exists, ask: overwrite, write `image_prompts-v2.md`, or pick a new name.

---

## Why carousels (2026 LinkedIn data)

Per 2026 engagement analysis, LinkedIn carousels/documents have the highest engagement rate of any format on the platform — roughly 585% better than text-only posts, ~3x images, ~3x video. The mechanism: carousels reward a reader who swipes, and each swipe is itself a dwell-time and interaction signal. A single strong hero image still helps dwell time on a short, single-insight post, but doesn't carry the same structural advantage. This is why format choice below is structure-driven, not arbitrary.

---

## Step 1 — Decide: single image or carousel

Read the post. Analyze its structure:

- **Recommend a carousel** if the post has 4+ distinct beats, steps, sections, or parallel points (a framework, a numbered list, a before/after/lessons arc, a multi-step process).
- **Recommend a single hero image** if the post is a short, single-insight piece with no natural multi-part structure.

State the recommendation and the one-line reason (e.g. "This post has 5 distinct steps — recommending a carousel"). **Ask the user to confirm or override** before generating prompts. Do not silently pick without surfacing the reasoning — this is a judgment call, not a hard rule.

---

## Step 2a — If carousel: slide breakdown

- **Slide count: 6–9.** Under 6 slides tends to feel thin for a swipe format; over 9 loses swipe-through completion. If the post's natural structure produces fewer or more beats, consolidate or split to land in this range — note when a beat had to be merged or split.
- **Slide 1 (cover)**: makes a promise and must be identifiable as the author's even in a fast feed skim (this is where visual branding consistency matters most). The cover's job is to make the swipe worth starting.
- **Middle slides**: strict **one idea per slide** — this is the single most common mistake to avoid. If a slide's prompt describes two ideas, split it into two slides.
- **Final slide**: a summary of the core takeaway plus a clear, specific call to action (what should the reader do next — follow, comment, save, visit a profile). Never end on a slide that just trails off.
- Prefer a **case-study or before/after arc** (problem → approach → result) when the source content supports it — this shape is proven to hold attention across the swipe better than a flat list.

For each slide, write:
1. Slide number and one-line role (e.g. "Slide 3 — the mistake").
2. **Text overlay content** — the exact short text (headline + supporting line, if any) that should appear on the slide. Keep overlay text short; the image is not a paragraph.
3. **Image-generation prompt** — a detailed prompt covering: composition/layout, subject matter or visual metaphor, style direction (e.g. minimal flat illustration, photo-real, abstract gradient background, icon-based), color/mood direction, and where the text overlay sits relative to the visual.
4. One-line rationale for why this slide/prompt supports the beat it represents.

## Step 2b — If single image: hero prompt

Write one detailed prompt for a cover/hero image reflecting the post's hook or core claim:
- Composition, subject/visual metaphor, style, color/mood, and any short text overlay (the hook line or a 3–5 word takeaway, not the full post).
- One-line rationale connecting the visual to the hook.

---

## Mobile-readability note

State once in the output: most LinkedIn viewing happens on a 6-inch phone screen, not a monitor — any text overlay described in a prompt must be large and high-contrast enough to read at that size. Flag any prompt where the overlay text is too long for this constraint.

---

## Output format (`image_prompts.md`)

```markdown
# Image Prompts — <post title / hook line>

**Format:** Carousel (N slides) | Single hero image
**Reasoning:** <one line>

## Slide 1 — Cover
**Overlay text:** ...
**Prompt:** ...
**Rationale:** ...

## Slide 2 — <role>
...

## Slide N — Summary / CTA
...
```

For a single image, use the same structure with one entry.

## Workflow

1. Read the source post. If not given, ask.
2. Decide carousel vs. single image per Step 1. State reasoning, confirm with user.
3. Generate the slide/image breakdown per Step 2a or 2b.
4. Present the full set of prompts to the user for a quick sanity check before writing (catches obvious mismatches early, but this is a lighter gate than the writer skill's review-first stop — no separate hook-selection step is needed here).
5. Write `image_prompts.md` next to the source file, applying the overwrite policy. Confirm the exact path.

## Handoff

This skill produces prompt text only. Rendering the prompts into actual images/slides is outside its scope — hand the file to whatever image-generation tool or workflow the user already uses.
