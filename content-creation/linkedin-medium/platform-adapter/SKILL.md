---
name: platform-adapter
description: Use when the user has a source draft and wants platform-specific versions for LinkedIn and/or Medium. Reshapes one neutral draft into the right content-type from the matrix (LinkedIn short/long/article/carousel-copy, Medium short/long/tutorial/listicle), adapts voice per platform, and writes into linkedin/ and medium/. Trigger on "adapt for LinkedIn", "make a Medium version", "format this for posting".
---

# Platform Adapter

Take one platform-neutral source draft and reshape it into platform- and type-specific versions for LinkedIn and/or Medium, following the content-type matrix. Voice adapts per platform.

## When to use
- User has a source draft (from `draft-builder` or their own) and wants posting-ready versions.
- User says: "make a LinkedIn version", "turn this into a Medium deep dive", "give me both".

## Folder conventions (resolve relative to CWD)
- `drafts/`: source drafts read from here.
- `linkedin/`: LinkedIn versions written here.
- `medium/`: Medium versions written here.
- `voice-tone/`: voice samples + style instructions.

If `linkedin/` or `medium/` is needed but missing, STOP and ask the user how to proceed. Never silently create folders.

### Voice handling
Read `voice-tone/` if present and adapt. If a needed voice-tone folder is expected but missing, ask the user how to proceed. Voice adapts by **content type AND platform** (see tone rules below).

## Content-type matrix
| Platform | Type | Length | Notes |
|---|---|---|---|
| LinkedIn | Short Post | 100-300 w | Hook-heavy, line-break formatted |
| LinkedIn | Long Post | 600-1200 w | Narrative, native feed, no images |
| LinkedIn | Article | 1000+ w | Native publishing, headers/images |
| LinkedIn | Carousel | 8-12 slides | Slide copy + JSON schema output |
| Medium | Short Article | 3-5 min | Punchy, single-insight |
| Medium | Long Article | 8-12 min | Deep dive, multiple sections |
| Medium | Tutorial | varies | Code blocks, step-by-step (blocks labeled unverified) |
| Medium | Listicle | varies | Numbered/structured list |

## Platform tone rules
- **LinkedIn**: more direct, personal, first-person; short punchy lines with deliberate line breaks and whitespace; strong scroll-stopping hook in the first 1-2 lines; scannable.
- **Medium**: more considered and essayistic; real subheadings; longer paragraphs allowed; title + subtitle + section structure.

## Workflow

### 1. Read the source draft + confirm expected outputs
Read the source draft. Before generating anything, ASK the user what outputs they expect and STOP for their answer. Do not assume. Surface the concrete deliverables this skill supports:
- **LinkedIn**: Short Post, Long Post, Article, and/or Carousel copy (any mix).
- **Medium**: Short Article, Long Article, Tutorial, and/or Listicle (any mix).
- **Both platforms**, or just one.

For each chosen target, determine the content-type:
- Detect the best-fit type from the draft's substance (a step-by-step with code → Tutorial; a numbered structure → Listicle; a single sharp insight → Short; a layered argument → Long/Article).
- If the type is ambiguous, ASK rather than guess.
- For **LinkedIn**, you MUST present the 2-3 format menu (Short Post, Long Post, Carousel outline) and get an explicit selection from the user BEFORE generating any LinkedIn file. Do not default to a single format.

### 2. Produce the versions
- Reshape the SAME core idea per platform. Do not write a different piece; re-cut the source draft.
- Apply the platform tone rules and the matrix constraints (length, formatting).
- **LinkedIn Short/Long**: apply line-break/scannability formatting.
- **LinkedIn Article / Medium Long**: add headers/subheadings.
- **LinkedIn Carousel**: output slide COPY as structured slides (title + body + optional footer per slide, 8-12 slides). Also emit the slides as JSON to `linkedin/carousels/<slug>/slides.json` so they can be rendered separately:
  ```json
  {"slug":"<slug>","slides":[{"title":"...","body":"...","footer":"@handle"}]}
  ```
  The JSON is the complete carousel deliverable from this skill. Image rendering is out of scope.
- **Medium Tutorial**: structure with steps + fenced code blocks. Label every code block `# unverified` in a comment — do NOT claim code is verified. Code execution is out of scope for this skill.

### 3. Review-first (mandatory stop)
Present all generated versions/options. STOP. Let the user pick, tweak, or reject before anything is written.

### 4. Persist (after approval)
**Voice compliance gate (before any content file write).** If `voice-tone/profile.md` (or raw `voice-tone/` samples) is present, scan the generated text against its "Avoided Words & Phrases" and "Punctuation & Formatting Quirks" sections. Auto-fix mechanical violations (em-dashes to periods or commas, banned punctuation) and report what you changed. Flag judgment-call violations (hype words, AI-voice markers, cliches) for the user rather than silently rewriting. Never emit a pattern the profile bans. If no voice-tone exists, skip this silently.

- LinkedIn versions → `linkedin/<slug>-<type>.md`
- Medium versions → `medium/<slug>-<type>.md`
- Carousel slide JSON → `linkedin/carousels/<slug>/slides.json`

Confirm the written paths.

## Conventions

These are shared assumptions so the content skills interoperate. Each skill
still works standalone. None of these require another skill to be present.

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
