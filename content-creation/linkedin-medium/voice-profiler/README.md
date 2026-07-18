# voice-profiler

Analyzes the user's writing samples in the cwd-relative `voice-tone/` folder **once** and distills them into a single reusable summary file, `voice-tone/profile.md`. Other content skills can then read this one profile so the user's voice stays consistent, instead of each skill re-deriving voice from raw samples and drifting apart over time.

---

## Trigger phrases

| Input | Example |
|---|---|
| Establish a voice profile | "capture my voice", "profile my voice", "set up my voice profile", "analyze my writing", "sound like me", "make you sound like me" |
| Voice/tone keywords | "voice", "tone", "style", "voice profile", "voice-tone" |
| Refresh an existing profile | "update my voice profile", "refresh my voice", "my style has changed" |

Run it **once** to establish the profile before a lot of content work, then refresh it whenever samples or voice change.

Do **not** use it to author content; it only profiles voice. Expanding an idea is `seed-expander`, drafting is `draft-builder`, LinkedIn writing is `linkedin-writer` and Medium writing is `medium-writer`, editing/variants is `editorial-reviewer`, carousels are `carousel-builder`, and step verification is `tutorial-verifier`. Those skills *consume* the profile; they do not produce it.

---

## What it does

- **Reads `voice-tone/` once.** Reads every file in the cwd-relative `voice-tone/` folder (except an existing `profile.md`, handled specially), covering two input kinds: **writing samples** (past posts/articles/drafts) and **explicit style-instruction files** (written-down rules the user has dropped in).
- **Treats instructions as ground truth.** Explicit style-instruction files are authoritative and folded into the profile as-is. They take precedence over patterns merely inferred from samples, which are treated as evidence.
- **Distills a single reusable profile.** Writes `voice-tone/profile.md`, framed explicitly at the top as **"guidance to adapt from"**, never a rigid template to copy verbatim.
- **Captures how the user writes.** Tone/register, POV/person, sentence rhythm and length, favored words/phrases, avoided words/phrases, structural habits (openings/closings/lists/questions), punctuation and formatting quirks, the verbatim explicit style instructions, and per-platform notes (LinkedIn vs Medium) when samples span platforms.
- **Flags confidence.** Under a **Notes & Uncertainties** section it calls out anything thin ("only 2 samples", "no Medium samples, LinkedIn notes only") so downstream consumers know how much to trust each part.
- **Asks if `voice-tone/` is missing or empty.** If the folder does not exist or has no usable samples/instructions, it STOPS and asks the user how to proceed (point to samples, paste them in chat, or skip). It never silently creates the folder or any file inside it.

---

## Optional / adaptive guidance: never a hard dependency

The `voice-tone/profile.md` this skill produces is **OPTIONAL** for every other skill:

- Skills that consume it use `profile.md` **if present** for a fast, consistent read of the voice.
- If `profile.md` is **absent**, those skills still work. They degrade gracefully to reading the raw samples in `voice-tone/` directly.

So running voice-profiler is a convenience/consistency optimization, not a dependency. Nothing breaks if it never runs. The profile is **adaptive guidance to adapt from**, applied to new content and platforms, not old text to reproduce.

---

## Profile contents

The generated `profile.md` uses these section headers:

| Section | Captures |
|---|---|
| **Tone & Register** | formal↔casual, warm↔blunt, playful↔serious, level of authority |
| **POV / Person** | first person, "we", second-person address to the reader |
| **Sentence Rhythm & Length** | short/punchy vs long/flowing, variation, fragment use |
| **Favored Words & Phrases** | signature vocabulary, recurring transitions, pet phrases |
| **Avoided Words & Phrases** | things never used or explicitly banned (hype words, clichés, jargon) |
| **Structural Habits** | hook style, closings/CTA, lists, headings, questions, one-line paragraphs, callbacks |
| **Punctuation & Formatting Quirks** | em-dashes, ellipses, parentheticals, emoji use, capitalization |
| **Explicit Style Instructions (authoritative)** | verbatim/faithfully summarized from instruction files |
| **Per-Platform Notes (LinkedIn / Medium)** | how the voice shifts per platform, or a note that samples are single-platform |
| **Notes & Uncertainties** | confidence flags for anything thin |

Each section is concise, actionable bullet guidance a downstream skill can apply, not prose essays.

---

## Review-first + no-silent-overwrite

1. Analyze `voice-tone/` and **draft** the profile in the chat.
2. **PRESENT** the drafted profile and ask for approval/edits. Iterate until approved.
3. Only **after approval**, write `voice-tone/profile.md`.
4. **Never overwrite an existing `profile.md` silently.** If one exists, read it, summarize what would change (added/removed/changed guidance), and ASK the user: **overwrite**, **keep existing**, or **merge** the new findings into the old profile.

---

## Inputs

| Input | Required | Description |
|---|---|---|
| `voice-tone/` folder | Yes | Cwd-relative folder holding writing samples and/or explicit style-instruction files |
| Writing samples | At least one usable input | Past posts/articles/drafts demonstrating the user's natural voice |
| Style-instruction files | Optional | Written-down rules; treated as authoritative and folded in verbatim |
| Approval | Yes | The drafted profile must be approved before `profile.md` is written |

---

## Outputs

- A drafted voice profile presented in chat for approval/edits.
- After approval: `voice-tone/profile.md`, the single shared, reusable voice reference downstream skills read when present.
- On a refresh where `profile.md` already exists: a diff/summary of proposed changes, then an overwrite / keep / merge decision applied.

---

## Limitations

- **Optional, never a dependency.** Every other skill works without `profile.md`, falling back to raw `voice-tone/` samples.
- **Review-first.** Always drafts in chat and requires approval before writing; never writes silently.
- **No silent overwrite.** An existing `profile.md` is never replaced without an explicit overwrite/keep/merge choice.
- **Never auto-creates `voice-tone/`.** If the folder is missing or empty, it stops and asks.
- **Guidance, not a template.** The profile describes habits to adapt from; it does not reproduce or lock in old text.
- **Confidence is only as good as the samples.** Thin input is flagged under Notes & Uncertainties rather than over-generalized.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global: available in all projects (Linux/macOS)
cp -r content-creation/linkedin-medium/voice-profiler ~/.config/opencode/skills/

# Per-project only
cp -r content-creation/linkedin-medium/voice-profiler .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse content-creation\linkedin-medium\voice-profiler "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/voice-profiler.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before the profiling task |

---

## Companion skills

A cross-cutting support skill for the LinkedIn/Medium content suite. Pipeline order: `seed-expander` -> `draft-builder` -> {`linkedin-writer`, `medium-writer`} -> {`carousel-builder`, `medium-imager`, `tutorial-verifier`} -> `editorial-reviewer`, with **`voice-profiler`** and `content-tracker` as cross-cutting support.

- **`draft-builder`**, **`linkedin-writer`**, **`medium-writer`**, **`editorial-reviewer`**, **`carousel-builder`**, **`tutorial-verifier`**: all read `voice-tone/profile.md` when present, and fall back to raw samples when absent
- **`seed-expander`**: expands a raw idea into structured angles/outline
- **`content-tracker`**: the other cross-cutting support skill; an optional pipeline tracker

`voice-profiler` improves consistency across the whole suite without ever becoming a hard dependency.
