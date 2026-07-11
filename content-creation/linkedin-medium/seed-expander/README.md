# seed-expander

Turns ONE user-provided seed idea into 8-10 distinct, post-worthy content angles for LinkedIn and Medium, grounded in fresh web research. On the user's confirmation, it writes the approved angles as stub draft files. It never generates ideas cold. The user always supplies the seed; the skill's job is research, expansion, and angle-shaping.

---

## Trigger phrases

| Input | Example |
|---|---|
| Expand a seed | "expand this idea", "expand this" |
| Ask for angles | "give me angles", "give me angles on X" |
| Ideas from notes | "content ideas from these notes", "seed idea" |
| A raw thought or link | A dropped paragraph, project note, or URL to riff on |

Do **not** use it to write the actual draft (use `draft-builder`), to reshape a draft into LinkedIn/Medium versions (use `platform-adapter`), or to render carousel images (use `carousel-builder`). This skill stops at approved idea stubs and hands off to `draft-builder`.

---

## What it does

- **Intakes the seed.** Reads the user's raw thought, bullets, paragraph, project note, or link. If the seed is a link, it fetches it. Asks one clarifying question only if the seed is truly ambiguous about domain or intent.
- **Confirms goal weighting.** Asks once (if unclear) whether the user wants **thought-leadership** or **career-visibility** weighting. Both are valid, and each idea is tagged.
- **Does thorough research.** Not a quick 2-3 fetch skim: fetches multiple relevant, recent sources (news, docs, HN/Reddit discussions, primary sources), cross-references claims across sources, notes points of debate or contrarian takes, and captures the URL plus a one-line takeaway for each source actually used. If sources are unreachable or gated, it reports which ones failed and never presents placeholder or invented sources as if researched.
- **Expands into 8-10 distinct angles.** Each angle includes a **Hook** (one punchy line), an **Angle type** (`thought-leadership` or `career-visibility`), a **Suggested platform + content-type** from the matrix, a **Why now** timeliness hook, and the 1-3 **Sources** backing it. Angles are genuinely distinct (different lens, audience, or format), not 10 rewrites of one take.
- **Review-first (mandatory stop).** Presents all angles in a scannable list and stops. Nothing is written until the user picks which angles to keep (all / a subset / none) and optionally edits hooks or retags.
- **Runs a voice-compliance gate before writing.** If a `voice-tone/` profile or samples exist, it scans generated hooks and copy against the profile's avoided words/phrases and punctuation rules, auto-fixes mechanical violations (banned punctuation), and flags judgment calls (hype words, AI-voice markers) for you. Skips silently if no voice-tone exists.
- **Writes approved stubs.** For each approved angle, writes a stub file to `drafts/` after confirming the folder exists. Never silently creates folders.

---

## Content-type matrix

Each angle is tagged with a suggested platform and content-type drawn from this matrix:

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

---

## Workflow

| Step | What happens |
|---|---|
| **1. Intake the seed** | Read/fetch the seed; ask one clarifying question only if truly ambiguous; confirm goal weighting once if unclear |
| **2. Thorough research** | Fetch multiple recent sources, cross-reference claims, capture URL + one-line takeaway per source used |
| **3. Expand into angles** | Produce 8-10 distinct angles, each with Hook, Angle type, Platform + type, Why now, Sources |
| **4. Review-first (stop)** | Present all angles in a scannable list and stop; user keeps all/subset/none and may edit |
| **5. Write approved stubs** | After confirmation, write each approved angle as `drafts/<slug>.md`; confirm the written paths: runs the voice-compliance gate before writing |

Each written stub follows a fixed structure: working title, `**Status:** idea`, platform/type, angle tag, hook, `## Why now`, `## Research sources`, `## Raw notes / seed`, and an empty `## Draft` section to hand off to `draft-builder`.

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Seed idea | Yes | A raw thought, bullets, paragraph, project note, or link the user wants expanded |
| Goal weighting | Optional | `thought-leadership` vs `career-visibility`; asked once if unclear |
| `drafts/` folder | For writing stubs | Must exist before stubs are written; the skill asks how to proceed if missing |
| `voice-tone/` folder | Optional | Voice samples + style instructions used to shape hooks |

---

## Outputs

- **A scannable list of 8-10 angles** presented for review, each with hook, angle type, suggested platform/type, why-now, and sources.
- **Approved idea stubs** written to `drafts/<slug>.md` (only after confirmation), each pre-populated with title, status, platform/type, hook, why-now, research sources, raw notes, and an empty `## Draft` section.
- **A confirmation** of which files were written and their paths.

---

## Limitations

- **Never generates ideas cold.** The user must supply the seed; the skill only researches, expands, and shapes angles.
- **Never silently creates folders.** If `drafts/` is missing when about to write stubs, it stops and asks how to proceed.
- **Never overwrites silently.** If a target file exists, it asks the user to overwrite, write a `-v2`/`-v3` variant, or pick a new name.
- **Stops at stubs.** It does not write the draft body. That is `draft-builder`'s job.
- **Tracker updates are prompted, not automatic.** If a `content-log.md`/`content-log.json` tracker exists, the skill asks in one line whether to update it after writing; a missing tracker never blocks the skill.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global: available in all projects (Linux/macOS)
cp -r content-creation/linkedin-medium/seed-expander ~/.config/opencode/skills/

# Per-project only
cp -r content-creation/linkedin-medium/seed-expander .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse content-creation\linkedin-medium\seed-expander "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/seed-expander.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before the content task |

---

## Companion skills

`seed-expander` is the first stage of the LinkedIn/Medium content pipeline: **seed-expander → draft-builder → platform-adapter → {carousel-builder, tutorial-verifier} → editorial-reviewer**, with `voice-profiler` and `content-tracker` as cross-cutting support.

- **`draft-builder`**: consumes an approved stub and turns it into a full source draft (the next stage)
- **`platform-adapter`**: reshapes a source draft into LinkedIn/Medium versions
- **`carousel-builder`**: renders carousel slide copy into image files
- **`tutorial-verifier`**: runs and verifies code in tutorial drafts
- **`editorial-reviewer`**: produces edited variants of a version
- **`voice-profiler`**: builds the `voice-tone/` profile used to shape hooks
- **`content-tracker`**: tracks each piece's status across the pipeline
