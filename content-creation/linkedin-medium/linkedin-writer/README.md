# linkedin-writer

Takes a source draft, rough notes, or a raw idea and produces a posting-ready LinkedIn piece with deep platform craft applied: hook engineering, scroll-optimized body structure, narrative framing, specificity rules, a sharp closing question, and human-voice checks. Produces Short Posts (100–300 words), Long Posts (600–1200 words), and Articles (1000–2500 words). Built around the mechanics of how LinkedIn actually renders, truncates, and distributes posts.

---

## Trigger phrases

| Input | Example |
|---|---|
| Write a LinkedIn post | "write a LinkedIn post about X", "turn this into a LinkedIn post" |
| LinkedIn version of a draft | "LinkedIn version", "make this shareable on LinkedIn" |
| Sharpen an existing post | "improve this LinkedIn post", "make this hook stronger" |

Do **not** use it for Medium articles (use `medium-writer`), carousel copy or image rendering (use `carousel-builder`), or generating raw ideas (use `seed-expander`).

---

## What it does

- **Detects content type.** Reads the input and recommends Short Post, Long Post, or Article based on substance. States the reasoning in one line, then asks for confirmation before writing. Never silently defaults to a type.
- **Matches voice (mandatory).** Reads `voice-tone/profile.md` if present — specifically the `### LinkedIn` subsection — then falls back to raw samples. If `voice-tone/` does not exist, stops and asks how to proceed.
- **Engineers 5 hook variants.** Before drafting the body, generates one hook per mode (Contrarian, Curiosity gap, Number+contrast, Confession, Mid-scene), applies the cold-read test to each, and stops for the user to choose. Nothing is written until a hook is selected.
- **Drafts the full piece with craft rules applied.** One idea per line, 1–3 line paragraph cap, scroll momentum, correct narrative frame, specificity pass, 3 closing question candidates, no URLs in the body.
- **Self-audits before showing the draft.** Runs 7 internal checks (hook fold test, line density, specificity scan, crutch-phrase scan, throat-clearing scan, link discipline, closing question quality) and fixes all flagged items before presenting to the user.
- **Review-first (mandatory stop).** Presents the draft plus audit results, then stops. Nothing is written until the user approves.
- **Persists after approval.** Runs a voice compliance gate (scans against `voice-tone/profile.md` avoided words/phrases and punctuation quirks, auto-fixes mechanical violations, flags judgment calls), then writes the file at the correct path.

---

## LinkedIn craft rules applied

| Rule | Mechanics |
|---|---|
| Hook | Written last; 5 variants (contrarian, curiosity gap, number+contrast, confession, mid-scene); cold-read tested; exact numbers not round ones; throat-clearing deleted |
| Fold awareness | First 1–3 lines under ~200 chars; cut must land at unresolved tension, not a full stop |
| Body density | One idea per line; 1–3 line paragraph max; blank line between every paragraph |
| Scroll momentum | Each short paragraph ends on a slightly incomplete thought |
| Narrative frame | Before→After→Bridge / Mistake→Realization→Shift / Challenge→Action→Result / Contrarian stance — chosen to match what actually happened |
| Specificity | Vague nouns replaced with real textured detail; "only you could write this" test applied per paragraph |
| Closing question | Not yes/no; not "Thoughts?"; 3 candidates drafted, safest deleted |
| Human voice | Coffee test (read aloud); crutch-phrase hunt; one deliberate rule break; one rough edge kept |
| Links | No URLs in body; link goes in first comment after publishing |

---

## Workflow

| Step | What happens |
|---|---|
| **1. Intake + type selection** | Read input; recommend type with one-line reasoning; STOP for confirmation |
| **2. Hook engineering** | Generate 5 labeled hook variants; mark top 1–2; STOP for user to pick |
| **3. Draft** | Select narrative frame (stated); write body with all craft rules; 3 closing question candidates |
| **4. Self-audit** | Run 7 checks internally; fix all FLAGGED items; only then proceed |
| **5. Review-first (stop)** | Present draft + audit report + frame note; iterate until approved; no file written |
| **6. Persist** | Voice compliance gate; write file at correct path; confirm path; ask about tracker update |

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Source content | Yes | `drafts/<slug>.md`, pasted draft, rough notes, or a raw idea |
| `voice-tone/` folder | Yes (or explicit opt-out) | `profile.md` or raw samples; skill stops and asks if missing |
| `linkedin/` folder | For persistence | Target write folder; skill asks how to proceed if missing |
| Content type | Optional | Short Post / Long Post / Article; skill recommends if not provided |

---

## Outputs

- **5 labeled hook variants** with the top 1–2 marked, before the body is drafted.
- **A posting-ready LinkedIn piece** in the chosen format with all craft rules applied.
- **Self-audit report** (7 checks: PASS or FLAGGED with fixes made).
- **The persisted file** at `linkedin/<slug>-short.md`, `linkedin/<slug>-long.md`, or `linkedin/<slug>-article.md`.

---

## Limitations

- **Short Posts, Long Posts, Articles only.** Carousel copy is out of scope — use `carousel-builder` (it authors and renders carousel slides).
- **Not a Medium skill.** Use `medium-writer` for Medium.
- **Requires a voice signal.** If `voice-tone/` is absent, the skill stops and asks rather than inventing a voice.
- **Hook step is mandatory.** The body is not drafted until a hook variant is selected — this is by design, not skippable.
- **Never silently creates folders or overwrites files.** Asks how to proceed in both cases.
- **Tracker updates are prompted, not automatic.** If a `content-log.json` tracker exists, the skill asks in one line whether to update it; a missing tracker never blocks the skill.
- **Link placement is the user's responsibility.** The skill removes URLs from the body and tells the user to add the link as a first comment after publishing; it cannot post to LinkedIn on their behalf.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global, available in all projects (Linux/macOS)
cp -r content-creation/linkedin-medium/linkedin-writer ~/.config/opencode/skills/

# Per-project only
cp -r content-creation/linkedin-medium/linkedin-writer .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse content-creation\linkedin-medium\linkedin-writer "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/linkedin-writer.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before the content task |

---

## Companion skills

`linkedin-writer` sits between `draft-builder` and `editorial-reviewer` in the LinkedIn branch of the pipeline: **seed-expander → draft-builder → {linkedin-writer, medium-writer} → {carousel-builder, medium-imager, tutorial-verifier} → editorial-reviewer**, with `voice-profiler` and `content-tracker` as cross-cutting support.

- **`seed-expander`**: generates approved angle stubs; `draft-builder` builds them into source drafts
- **`draft-builder`**: produces the platform-neutral source draft this skill reads
- **`carousel-builder`**: authors and renders carousel slide copy into image files (this skill does not produce carousel copy)
- **`editorial-reviewer`**: produces 2–3 edited variants of the finished post for a final polish pass
- **`medium-writer`**: the Medium counterpart to this skill; for both LinkedIn and Medium, run this skill and `medium-writer`
- **`voice-profiler`**: builds the `voice-tone/` profile this skill reads for voice matching
- **`content-tracker`**: tracks each piece's status (`idea` → `drafted` → `reviewed` → `posted` → `archived`) across the pipeline
