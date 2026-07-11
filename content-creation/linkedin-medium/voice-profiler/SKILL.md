---
name: voice-profiler
description: Use when the user wants to analyze their writing samples and distill a reusable voice profile so their voice, tone, and style stay consistent across skills. Reads voice-tone/ samples once and writes voice-tone/profile.md. Trigger on "voice", "tone", "style", "voice profile", "voice-tone", "analyze my writing", "sound like me", "capture my voice", "profile my voice".
---

# Voice Profiler

Analyze the user's existing writing samples in the CWD-relative `voice-tone/` folder ONCE and distill them into a single reusable summary file: `voice-tone/profile.md`. Other skills (`draft-builder`, `platform-adapter`, `editorial-reviewer`, `tutorial-verifier`, `carousel-builder`) can then read this one profile so the user's voice stays consistent, instead of each skill independently re-deriving voice from raw samples and drifting apart over time.

The profile is **adaptive guidance to adapt from**, never a rigid template to copy verbatim.

## Standalone by design
This skill works entirely on its own. It does not require any other skill to be present or run.

The `voice-tone/profile.md` it produces is **OPTIONAL** for every other skill:
- Skills that consume it use `profile.md` **if present** for a fast, consistent read of the voice.
- If `profile.md` is **absent**, those skills must still work. They degrade gracefully to reading the raw samples in `voice-tone/` directly.

So running voice-profiler is a convenience/consistency optimization, not a dependency. Nothing breaks if it never runs.

## When to use
- Run it **once** to establish the voice profile before doing a lot of content work.
- **Refresh** it whenever the user's samples or voice change (new samples added, style has evolved, updated style-instruction files dropped in `voice-tone/`).
- Trigger phrases: "analyze my writing", "capture / profile my voice", "make you sound like me", "set up my voice profile", "update my voice profile".

## How it reads `voice-tone/` (resolve relative to CWD)
`voice-tone/` holds two kinds of inputs, both of which are read:
1. **Writing samples**: past posts/articles/drafts that demonstrate the user's natural voice.
2. **Explicit style-instruction files**: any file where the user has written down rules ("avoid hype words", "always open with a question", "use British spelling", etc.). These are authoritative and are folded into the profile as-is; they take precedence over patterns merely inferred from samples.

Read every file in `voice-tone/` (except an existing `profile.md`, which is handled specially, see review-first). Treat instruction files as ground truth and samples as evidence.

## Ask-if-missing rule (never create silently)
If `voice-tone/` does not exist, or exists but contains no usable samples/instructions, **STOP and ASK** the user how to proceed. Offer:
- point to where the samples live,
- paste some samples/style rules directly into the chat, or
- skip profiling for now.

Never silently create the `voice-tone/` folder or any file inside it.

## What the profile captures (adaptive, not rigid)
The profile describes *how the user tends to write* so another skill can adapt those habits to new content and platforms, not reproduce old text. Capture:

- **Tone / register**: formal↔casual, warm↔blunt, playful↔serious, level of authority.
- **POV / person**: first person? "we"? second-person address to the reader?
- **Sentence rhythm & length habits**: short punchy vs long flowing, variation patterns, fragment use.
- **Favored words & phrases**: signature vocabulary, recurring transitions, pet phrases.
- **Avoided words & phrases**: things the user never uses or explicitly bans (hype words, clichés, jargon).
- **Structural habits**: how they open (hook style) and close (takeaway/CTA), use of lists, headings, questions, one-line paragraphs, callbacks.
- **Punctuation quirks**: em-dashes, ellipses, parentheticals, emoji use, capitalization habits.
- **Explicit style instructions**: verbatim / faithfully summarized from instruction files in `voice-tone/`, marked as authoritative.
- **Per-platform notes**: if samples span LinkedIn vs Medium (or others), note how the voice shifts per platform (LinkedIn line breaks + hooks, Medium longer-form subheads, etc.). If samples are single-platform or platform-agnostic, say so instead of inventing distinctions.

Frame the whole document as **"guidance to adapt from,"** explicitly, at the top.

## Review-first + no-silent-overwrite (mandatory)
1. Analyze `voice-tone/` and **draft** the profile in the chat.
2. **PRESENT** the drafted profile to the user and ask for approval / edits. Iterate until approved.
3. Only **after approval**, write `voice-tone/profile.md`.
4. **Never overwrite an existing `profile.md` silently.** If one already exists:
   - read it, summarize what would change (a diff/summary of added, removed, and changed guidance), and
   - ASK the user which they want: **overwrite**, **keep existing**, or **merge** the new findings into the old profile.

## Structure of the generated `profile.md`
The written profile follows these section headers:

```markdown
# Voice Profile

> Guidance to adapt from, not a template to copy verbatim.
> Adapt these habits to the specific content and platform.

_Sources analyzed: <files in voice-tone/>. Last updated: <date>._

## Tone & Register
## POV / Person
## Sentence Rhythm & Length
## Favored Words & Phrases
## Avoided Words & Phrases
## Structural Habits (openings, closings, lists, questions)
## Punctuation & Formatting Quirks
## Explicit Style Instructions (authoritative)
## Per-Platform Notes
### LinkedIn
### Medium
## Notes & Uncertainties
```

Keep each section concise and actionable: bullet guidance a downstream skill can apply, not prose essays. Under **Notes & Uncertainties**, flag anything thin (e.g. "only 2 samples", "no Medium samples, LinkedIn notes only") so consumers know the confidence level.

## Handoff
Once approved and written, `voice-tone/profile.md` becomes the shared voice reference. Downstream skills read it when present and fall back to raw `voice-tone/` samples when it is absent, so this skill improves consistency without ever becoming a hard dependency.
