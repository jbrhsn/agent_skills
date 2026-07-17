---
name: editorial-reviewer
description: Use when the user asks to review, edit, polish, tighten, or generate variants of a finished LinkedIn post or Medium article. Runs a structured editorial pass and returns 2-3 labeled edited variants for the user to choose, mix, or reject. Never auto-approves or replaces their text.
---

# Editorial Reviewer

Run a finished piece, a LinkedIn post/article or a Medium article, through a structured editorial review and return **2-3 edited variants** for the user to choose from. This skill is **review-first**: it presents options, then STOPS. The user picks, mixes, or rejects. Nothing is written until they choose.

## When to use

- User pastes finished text or points to a file and wants it reviewed, edited, polished, tightened, or sharpened.
- User wants alternate angles ("make it more contrarian", "tighter hook", "give me variants").

It works standalone on any pasted text or file.

## Folder conventions (cwd-relative)

All folders resolve relative to the **current working directory** where opencode launched:

- `linkedin/`: LinkedIn posts/articles
- `medium/`: Medium articles
- `drafts/`: in-progress pieces
- `archive/`: retired versions
- `voice-tone/`: voice/tone reference material

**Never auto-create folders.** If a folder needed to write the chosen version is missing, ASK THE USER how to proceed (create it, pick another location, or skip writing).

## Voice handling

- If `voice-tone/` exists (cwd-relative), read it to judge **voice authenticity** and to keep edits sounding like the user.
- Adapt to the content and the target platform.
- If a voice-tone folder is expected but missing, ask the user how to proceed rather than guessing.

## Review dimensions

Evaluate every piece against these five dimensions, and make different variants emphasize different ones:

1. **Hook strength**: does the opening earn the next line?
2. **Clarity / tightness**: cut filler, tighten phrasing, sharpen the point.
3. **Contrarian angle**: is there a sharper, more differentiated take?
4. **Voice authenticity**: does it still sound like the user (per `voice-tone/`)? If `voice-tone/` is absent, audit against a baseline list of known AI-voice markers instead: "delve into", "it's worth noting", "crucial", "in today's fast-paced world", "let's explore", "game-changer", "leverage" (as a verb). Flag any present. Explicitly scan each variant against the profile's "Avoided Words & Phrases" and "Punctuation & Formatting Quirks". Auto-fix mechanical bans (em-dashes, banned punctuation) and flag judgment calls (hype words, AI-voice markers).
5. **Scannability**: is it easy to skim on the target platform?

## Workflow

### 1. Intake + detect platform/type
Read the pasted text or file. Detect the platform:
- **LinkedIn** cues: short punchy post, first-person, no subheadings.
- **Medium** cues: long-form, subheadings/sections, article structure.

If the platform is unclear, ASK before proceeding.

### 2. Analyze against the 5 dimensions
Give a brief diagnostic: what's strong, what's weak, per dimension. Keep it short.

### 3. Produce 2-3 labeled variants
Default to 2-3 variants (honor a specific count if the user requests one). Number them clearly and give each a short editorial-angle label, e.g.:

For each variant, verify it respects platform length constraints: LinkedIn posts should be 100–1,200 words (Short: 100–300, Long: 600–1,200); Medium articles should be 700–1,800 words. Flag any variant outside its platform's range with a one-line note.

- **Variant 1 - Tighter hook:** rewrites the opening for immediate pull.
- **Variant 2 - More contrarian:** pushes a sharper, differentiated take.
- **Variant 3 - Safer / more polished:** cleaner, lower-risk, broadly shareable.

Under each variant include a one-line diagnostic: **what changed and why** (which dimensions it emphasizes). Also include a `voice check:` line per variant reporting `passed`, `N auto-fixed`, or `M flagged` against the profile's Avoided list.

### 4. Mechanical / formatting pass (per platform)
- **LinkedIn:** short lines, generous whitespace, strong first 1-2 lines, scannable line breaks. No dense paragraphs.
- **Medium:** clear subheadings, logical section structure, readable paragraph length.

Apply the appropriate pass to each variant so they're platform-ready.

### 5. Mandatory review-first STOP
Present all variants and diagnostics, then STOP and ask the user to choose, mix, or reject. Do **not** pick for them. Do **not** write anything yet.
If running non-interactively (e.g. in a batch pipeline or scripted run), document this gate as "skipped — auto-proceeding with output as drafted" and continue; do not silently omit the gate from the output log.

### 6. Write the chosen version
Only after the user picks:
- **Voice compliance gate (before write).** If `voice-tone/profile.md` (or raw `voice-tone/` samples) is present, scan the chosen text against its "Avoided Words & Phrases" and "Punctuation & Formatting Quirks". Auto-fix mechanical violations (em-dashes to periods or commas, banned punctuation) and report what changed. Flag judgment-call violations for the user. Never emit a banned pattern. If no voice-tone exists, skip silently.
- Preserve any `[source: ...]`, `[UNVERIFIED]`, and `[personal]` claim markers from the source text through to the written file. Do not strip them during editing.
- Confirm the target: `linkedin/` or `medium/` (cwd-relative).
- If the folder is missing, ASK how to proceed. Never silently create it.
- Write the chosen (or mixed) version and confirm the exact path back to the user.

## Iteration

This skill can be run repeatedly. After the user picks a variant, they can ask for another pass to refine it further. Treat the chosen version as the new input and generate fresh variants.

If the user states a standing style rule during review (for example "never use em-dashes"), offer to persist it to `voice-tone/profile.md` so every skill inherits it. Do not write the profile without the user's confirmation.

## Configurable count

Default is 2-3 variants. If the user asks for a specific number (e.g. "give me 4"), honor it.

## Conventions

These are shared assumptions so the content skills interoperate. Each skill
still works standalone: none of these require another skill to be present.

- **Folders** (all cwd-relative): `drafts/`, `linkedin/`, `medium/`,
  `archive/`, `voice-tone/`. Never auto-create: ask the user if missing.
- **Slug**: lowercase, hyphenated, derived from the working title. Reused as
  the filename stem across skills so a piece is traceable.
- **Filenames**: `drafts/<slug>.md`, `linkedin/<slug>-<type>.md`,
  `medium/<slug>-<type>.md`, carousels at `linkedin/carousels/<slug>/`.
- **Overwrite policy**: never silently overwrite an existing file. If the
  target exists, ask the user: overwrite, write a `-v2` (then `-v3`...)
  variant, or pick a new name.
- **Status values** (if a tracker file like `content-log.md` or
  `content-log.json` exists at cwd): `idea` -> `drafted` -> `reviewed` ->
  `posted` -> `archived`. If such a tracker exists, after writing or moving a
  file ASK the user in one line whether to update it to the new status.
  Absence of a tracker must never block the skill.
