# medium-writer

Takes a source draft, rough notes, or a raw idea and produces a posting-ready Medium article with deep platform craft applied: title and subtitle engineering, four-type hook selection, read-ratio-aware pacing, emotional arc writing, pull quote placement, and a 7-section structure matched to the content type. Produces Short Articles (700–1,000 words), Long Articles (1,300–1,800 words), Tutorials, and Listicles. Built around Medium's distribution mechanic, which rewards completion (read ratio) over clicks — the opposite of LinkedIn.

---

## Trigger phrases

| Input | Example |
|---|---|
| Write a Medium article | "write a Medium article about X", "turn this into a Medium post" |
| Medium version of a draft | "Medium version", "make this go viral on Medium" |
| Sharpen an existing article | "improve this Medium article", "make the title stronger" |

Do **not** use it for LinkedIn posts (use `linkedin-writer`), carousel image rendering (use `carousel-builder`), tutorial code verification (use `tutorial-verifier`), or generating raw ideas (use `seed-expander`).

---

## What it does

- **Detects content type.** Reads the input and recommends Short Article, Long Article, Tutorial, or Listicle based on substance. States the reasoning in one line, then asks for confirmation before writing. Never silently defaults to a type.
- **Matches voice (mandatory).** Reads `voice-tone/profile.md` if present — specifically the `### Medium` subsection — then falls back to raw samples. If `voice-tone/` does not exist, stops and asks how to proceed.
- **Engineers 10 title variants + 3 subtitles.** Before any body work, generates 10 numbered titles (pushing past the generic first instincts), marks the top 2–3, generates 3 subtitle variants for the top title, then stops for the user to pick both. Nothing is drafted until title AND subtitle are selected.
- **Engineers 4 hook variants.** After title/subtitle confirmation, generates one hook per type (Observational, Narrative, Rhetorical, Authority), applies the aloud test to each, marks the top 1–2, then stops for the user to choose. Body drafting does not begin until a hook is selected.
- **Drafts the full piece with craft rules applied.** Names the target emotion (one word) before drafting, selects the right section structure, applies read-ratio pacing, pull quotes at correct intervals, section-end pulls, specificity rules, and an emotional arc that delivers on the title's promise.
- **Self-audits before showing the draft.** Runs 8 internal checks (title format, subtitle format, hook quality, length match, paragraph density, emotion anchor, title-to-content honesty, pull quote presence) and fixes all flagged items before presenting to the user.
- **Review-first (mandatory stop).** Presents the draft plus audit results and target emotion, then stops. Nothing is written until the user approves.
- **Persists after approval.** Runs a voice compliance gate (scans against `voice-tone/profile.md` avoided words/phrases and punctuation quirks, auto-fixes mechanical violations, flags judgment calls), then writes the file at the correct path.

---

## Medium craft rules applied

| Rule | Key mechanic |
|---|---|
| Title engineering | 10 variants written; first-person + specific stake outperforms generic advice; one promise not three; Title Case, no ending period |
| Subtitle engineering | Under ~15 words; does a different job than the title (title = hook, subtitle = context/stakes); proper "T" icon formatting |
| Opening hook (4 types) | Observational (plain specific fact), Narrative (mid-action drop), Rhetorical (silent-yes question), Authority (claim + specific detail); pick by writing all four, cut three |
| Length and pacing | Decided before drafting (3–5 min for personal/opinion; 6–8 min for deep dive); cut redundant paragraphs in second pass; one idea per paragraph; section endings pull forward |
| Formatting for the eye | Break every 3–5 sentences; 1 pull quote per 400–500 words; subheaders mark real structural shifts only; Title Case main headers, Sentence case sub-headers |
| Writing toward a specific emotion | Name one target emotion before drafting (not "informed"); reverse-engineer from ending; turn abstractions into a single concrete moment; sadness needs a second beat |
| Headline-to-content honesty | Reread title + subtitle + final section back-to-back after drafting; ending must deliver the title's promise; no hollow curiosity-gap framing |

---

## Workflow

| Step | What happens |
|---|---|
| **1. Intake + type selection** | Read input; recommend type with one-line reasoning; STOP for confirmation |
| **2. Title + subtitle engineering** | Generate 10 labeled title variants; mark top 2–3; generate 3 subtitle variants; STOP for user to pick title AND subtitle |
| **3. Hook engineering** | Generate 4 labeled hook variants (one per type); mark top 1–2; STOP for user to select. Body not drafted until hook is chosen |
| **4. Draft** | State target emotion (one word); select structure (stated); write body with all craft rules; closing delivers emotion + title promise |
| **5. Self-audit** | Run 8 checks internally; fix all FLAGGED; only then proceed |
| **6. Review-first (stop)** | Present draft + audit report + emotion target + structure note; iterate until approved; no file written |
| **7. Persist** | Voice compliance gate; write file at correct path; confirm path; ask about tracker update |

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Source content | Yes | `drafts/<slug>.md`, pasted draft, rough notes, or a raw idea |
| `voice-tone/` folder | Yes (or explicit opt-out) | `profile.md` or raw samples; skill stops and asks if missing |
| `medium/` folder | For persistence | Target write folder; skill asks how to proceed if missing |
| Content type | Optional | Short Article / Long Article / Tutorial / Listicle; skill recommends if not provided |

---

## Outputs

- **10 labeled title variants** with top 2–3 marked, plus **3 subtitle variants**, before any body work.
- **4 labeled hook variants** (one per type) with top 1–2 marked, before the body is drafted.
- **A posting-ready Medium article** in the chosen format with all craft rules applied and a named emotional arc.
- **Self-audit report** (8 checks: PASS or FLAGGED with fixes made, plus target emotion and structure note).
- **The persisted file** at `medium/<slug>-short.md`, `medium/<slug>-long.md`, `medium/<slug>-tutorial.md`, or `medium/<slug>-listicle.md`.

---

## Limitations

- **Short Articles, Long Articles, Tutorials, Listicles only.** No LinkedIn output — use `linkedin-writer` for that.
- **No code verification.** Tutorial code blocks are written but not run — use `tutorial-verifier` after this skill for that step.
- **Requires a voice signal.** If `voice-tone/` is absent, the skill stops and asks rather than inventing a voice.
- **Title + subtitle step is mandatory.** Body drafting does not begin until both are selected — this is by design, not skippable.
- **Hook step is mandatory.** The body is not drafted until a hook variant is selected — also by design.
- **Never silently creates folders or overwrites files.** Asks how to proceed in both cases.
- **Tracker updates are prompted, not automatic.** If a `content-log.json` tracker exists, the skill asks in one line whether to update it; a missing tracker never blocks the skill.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global, available in all projects (Linux/macOS)
cp -r content-creation/linkedin-medium/medium-writer ~/.config/opencode/skills/

# Per-project only
cp -r content-creation/linkedin-medium/medium-writer .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse content-creation\linkedin-medium\medium-writer "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/medium-writer.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before the content task |

---

## Companion skills

`medium-writer` sits between `draft-builder` and `editorial-reviewer` in the Medium branch of the pipeline: **seed-expander → draft-builder → {linkedin-writer, medium-writer} → {carousel-builder, medium-imager, tutorial-verifier} → editorial-reviewer**, with `voice-profiler` and `content-tracker` as cross-cutting support.

- **`seed-expander`**: generates approved angle stubs; `draft-builder` builds them into source drafts
- **`draft-builder`**: produces the platform-neutral source draft this skill reads
- **`linkedin-writer`**: the LinkedIn counterpart to this skill; for both LinkedIn and Medium, run this skill and `linkedin-writer`
- **`tutorial-verifier`**: runs and verifies code blocks from Tutorial-type output before publishing
- **`editorial-reviewer`**: produces 2–3 edited variants of the finished article for a final polish pass
- **`voice-profiler`**: builds the `voice-tone/` profile this skill reads for voice matching
- **`content-tracker`**: tracks each piece's status (`idea` → `drafted` → `reviewed` → `posted` → `archived`) across the pipeline
