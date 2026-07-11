---
name: seed-expander
description: Use when the user gives a seed idea, topic, or rough thought and wants it expanded into multiple post-worthy LinkedIn/Medium content angles. Does thorough web research to enrich the seed, produces 8-10 tagged ideas, and on approval writes them as stub files into drafts/. Trigger on "expand this idea", "give me angles", "content ideas from", "seed idea".
---

# Seed Expander

Turn ONE user-provided seed idea into 8-10 distinct, post-worthy content angles for LinkedIn and Medium — grounded in fresh web research — then, on the user's confirmation, write the approved angles as stub draft files.

This skill NEVER generates ideas cold. The user always supplies the seed; the skill's job is research + expansion + angle-shaping.

## When to use
- User drops a raw thought, topic, project note, or link and wants ideas.
- User says: "expand this", "give me angles on X", "content ideas from these notes".

## Folder conventions (resolve relative to CWD)
All paths are relative to the current working directory where opencode was launched.
- `drafts/` — where approved idea stubs are written.
- `voice-tone/` — voice samples + style instructions (optional here; used to shape hooks).

If `drafts/` does not exist when you're about to write stubs, STOP and ask the user how to proceed (e.g. create it, use a different folder, or just print). Never silently create folders.

## Workflow

### 1. Intake the seed
Read the user's seed idea (bullets, paragraph, link, or messy note). If it's a link, fetch it. Ask one clarifying question only if the seed is truly ambiguous about domain or intent.

Ask the user (once) which goal weighting they want if unclear: **thought-leadership** vs **career-visibility** — both are valid and each idea will be tagged.

### 2. Thorough research
Do THOROUGH research (not a quick 2-3 fetch skim):
- Fetch multiple relevant, recent sources (news, docs, HN/Reddit discussions, primary sources).
- Cross-reference claims across sources; note points of debate or contrarian takes.
- Capture the URL + a one-line takeaway for each source you actually used.

### 3. Expand into angles
Produce **8-10 unique angles** from the seed. Each angle must include:
- **Hook** — one punchy line.
- **Angle type** — `thought-leadership` or `career-visibility`.
- **Suggested platform + content-type** drawn from the matrix below.
- **Why now** — the trending/research hook that makes it timely.
- **Sources** — the 1-3 research URLs backing it.

Make the angles genuinely distinct (different lens, audience, or format) — not 10 rewrites of one take.

#### Content-type matrix (pick per angle)
| Platform | Type | Length | Notes |
|---|---|---|---|
| LinkedIn | Short Post | 100-300 w | Hook-heavy, line-break formatted |
| LinkedIn | Long Post | 600-1200 w | Narrative, native feed |
| LinkedIn | Article | 1000+ w | Native publishing, headers/images |
| LinkedIn | Carousel | 8-12 slides | Image files (see carousel-builder) |
| Medium | Short Article | 3-5 min | Punchy, single-insight |
| Medium | Long Article | 8-12 min | Deep dive, multiple sections |
| Medium | Tutorial | varies | Code blocks, step-by-step |
| Medium | Listicle | varies | Numbered/structured list |

### 4. Review-first (mandatory stop)
Present all 8-10 angles to the user in a scannable list. STOP. Do not write anything yet.
Ask the user which angles to keep (all / a subset / none). Let them edit hooks or retag.

### 5. Write approved stubs (only after confirmation)
For each APPROVED angle, write a stub file to `drafts/` (after confirming the folder per the rules above).

Stub filename: `drafts/<short-slug>.md`. Stub contents:
```markdown
# <Working title>

**Status:** idea
**Platform / Type:** <e.g. LinkedIn Long Post>
**Angle:** <thought-leadership | career-visibility>
**Hook:** <the hook line>

## Why now
<the timeliness note>

## Research sources
- <url> — <one-line takeaway>
- <url> — <one-line takeaway>

## Raw notes / seed
<the user's original seed + any expansion notes>

## Draft
<!-- empty — hand off to draft-builder -->
```

Confirm to the user which files were written and their paths.

## Handoff
Approved stubs are consumed by `draft-builder`, which turns a chosen stub into a full source draft. This skill does NOT write the draft itself.

## Conventions

These are shared assumptions so the content skills interoperate. Each skill
still works standalone — none of these require another skill to be present.

- **Folders** (all cwd-relative): `drafts/`, `linkedin/`, `medium/`,
  `archive/`, `voice-tone/`. Never auto-create — ask the user if missing.
- **Slug**: lowercase, hyphenated, derived from the working title. Reused as
  the filename stem across skills so a piece is traceable.
- **Filenames**: `drafts/<slug>.md`, `linkedin/<slug>-<type>.md`,
  `medium/<slug>-<type>.md`, carousels at `linkedin/carousels/<slug>/`.
- **Overwrite policy**: never silently overwrite an existing file. If the
  target exists, ask the user: overwrite, write a `-v2` (then `-v3`...)
  variant, or pick a new name.
- **Status values** (if a tracker file like `content-log.md` or
  `content-log.json` exists at cwd): `idea` -> `drafted` -> `reviewed` ->
  `posted` -> `archived`. Updating the tracker is optional and best-effort;
  absence of a tracker must never block the skill.
