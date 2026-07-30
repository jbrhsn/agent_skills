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

## Workflow — delegation-model units

The workflow is three self-contained units of work. Each unit lists its **goal/scope**, its **inputs**, the **self-verify** the doer runs before handing back, and the **report contract** (what it hands back). Do the units in order — each unit's report is the next unit's input. Two units end in a **hand-back gate** where control returns to the user.

---

### Unit 1 — Format decision (HARD HAND-BACK GATE)

**Goal/scope:** Read the source post and decide, from its structure, whether it wants a multi-slide carousel or a single hero image. Surface the reasoning and stop.

**Inputs:** File path to the finished post/article. If not given, ask. If the source directory contains exactly one obvious candidate (e.g. `linkedin_post.md`), propose it and confirm rather than asking from scratch.

**Do:** Analyze the post's structure:

- **Recommend a carousel** if the post has 4+ distinct beats, steps, sections, or parallel points (a framework, a numbered list, a before/after/lessons arc, a multi-step process).
- **Recommend a single hero image** if the post is a short, single-insight piece with no natural multi-part structure.

State the recommendation and the one-line reason (e.g. "This post has 5 distinct steps — recommending a carousel").

**Self-verify:** Confirm the recommendation actually follows from the post's structure (beat count named), and that the reason is one line.

**⛔ HAND-BACK GATE:** Do NOT proceed to Unit 2. Hand back to the user and **wait for them to confirm or override** the format. This is a judgment call, not a hard rule — never silently pick.

**Report contract (hands back):**
- Source file used.
- Recommended format (carousel / single hero image) + one-line reason (beat count).
- Explicit request: "Confirm or override before I generate prompts."

---

### Unit 2 — Slide / image breakdown

**Goal/scope:** Produce the full per-slide (carousel) or single-image prompt set to spec.

**Inputs:** The **user-confirmed format** from Unit 1, and the source post.

**Do — if carousel (2a):**

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

**Do — if single image (2b):**

Write one detailed prompt for a cover/hero image reflecting the post's hook or core claim:
- Composition, subject/visual metaphor, style, color/mood, and any short text overlay (the hook line or a 3–5 word takeaway, not the full post).
- One-line rationale connecting the visual to the hook.

**Self-verify (doer runs this itself before reporting):**
- **One idea per slide** — no middle slide's prompt describes two ideas; if it does, split it.
- **Slide count in range** — carousel lands at 6–9 slides; note any beat merged/split to get there.
- **Cover + final slide rules met** — cover makes a promise and is brand-identifiable; final slide is takeaway + specific CTA (not a trail-off).
- **Mobile-readability** — every overlay text is short and high-contrast enough to read on a 6-inch phone; flag any overlay that's too long.

**Report contract (to Unit 3):**
- Format + slide count.
- The full prompt set (overlay text + prompt + rationale per slide/image) — this is an **internal handoff to Unit 3 for writing to file**, not to be surfaced to the user in chat.
- Self-verify result: pass, or the specific items flagged (over-long overlay, merged/split beat).

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

---

### Unit 3 — Sanity check + persist

**Goal/scope:** Write the prompt set to disk first, then present a short summary + file pointer for a quick sanity check.

**Inputs:** The full prompt set and self-verify result from Unit 2; the source file's directory.

**Do:**
1. **Write `image_prompts.md` FIRST**, next to the source file, applying the overwrite policy for a pre-existing file from a prior run (never silently overwrite: offer overwrite, `image_prompts-v2.md`, or a new name).
2. **Present ONLY a short summary + the file path** for a quick sanity check (catches obvious mismatches early): format (carousel N slides / single hero), slide/image count, and any prompts flagged for mobile-readability risk. **Do NOT paste the full prompt set into chat** — point the user to the written file to review. This is a **lighter gate** than the writer skill's review-first stop — no separate hook-selection step is needed here.
3. Ask for a quick confirm or revisions. **On revision, re-edit the file in place and re-point** to it (in-place updates don't re-trigger the overwrite prompt; the prior-run-file overwrite policy applies only to the first write).

**Self-verify (doer runs this itself before reporting):**
- The written file matches the output-format block above (Format + Reasoning header, one entry per slide/image with Overlay text / Prompt / Rationale).
- The mobile-readability note appears once in the output.
- The file was colocated with the source (not a fixed folder), and the overwrite policy was honored.

**Report contract (hands back to user):**
- Wrote `<exact path>` first, then presented a summary for confirm (full prompt set not pasted into chat).
- Format + slide/image count.
- Any prompts flagged for mobile-readability risk.
- Pass, or the specific issue flagged.

---

## Handoff

This skill produces prompt text only. Rendering the prompts into actual images/slides is outside its scope — hand the file to whatever image-generation tool or workflow the user already uses.

If the user later revises the post via `linkedin-post-writer`'s built-in review/refine path (which produces `linkedin_post_revised.md`), that refined file can be fed back through Unit 1 to regenerate visuals.
