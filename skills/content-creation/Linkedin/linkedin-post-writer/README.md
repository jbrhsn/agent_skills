# linkedin-post-writer

Turn a source draft, notes file, or rough bullet points into a posting-ready LinkedIn post — or take a finished post and score + refine it for virality. Both jobs live in one skill, expressed as delegation-model units of work (each with a clear goal, explicit inputs, a self-verify step, an explicit hand-back stop gate where relevant, and a terse report contract). All craft is grounded in how LinkedIn's algorithm ranks content in 2026 — hook engineering for the "see more" fold, scroll-first body structure, no-link-in-body dwell-time protection, and engagement-bait avoidance — not generic copywriting advice.

---

## Two paths

- **WRITE path** — source notes/draft/points into a posting-ready `linkedin_post.md`, behind mandatory review gates.
- **REVIEW/REFINE path** — a finished post scored out of 100 across 5 dimensions and rewritten once into `linkedin_post_revised.md` with an itemized change list.

---

## Trigger phrases

| Path | Example |
|---|---|
| WRITE | "write a LinkedIn post from this", "turn these notes into a LinkedIn post", "draft a LinkedIn post" |
| WRITE (raw) | User pastes bullets/ideas directly and asks for a LinkedIn post |
| REVIEW/REFINE | "review this LinkedIn post", "score this for virality", "how shareable is this", "refine this post" |

Not for Medium, X/Twitter, or other platforms. Not for carousel/image generation — see `linkedin-image-prompts`, meant to run after this skill.

---

## What it does

**WRITE path**
- **Locates the source.** Requires a file path (or pasted text); asks if none is given. Never guesses a folder to read from.
- **Detects content type.** Short Post (100–300w), Long Post (600–1200w), or Article (1000–2500w+) — auto-detected, stated with one-line reasoning, confirmed before drafting.
- **Hook engineering (mandatory gate).** Generates 5 hook variants — Contrarian, Curiosity gap/number-contrast, Confession, Mid-scene, Problem-naming — applying the cold-read test and exact-number specificity. Stops and hands back for the user to pick or mix before drafting the body.
- **Narrative frame selection.** Picks the frame (Before→After→Bridge, Mistake→Realization→Shift, Challenge→Action→Result, Contrarian stance) that fits the real content.
- **Body craft.** One idea per line, 1–3 line paragraphs, specificity over vague nouns, zero body links, no engagement-bait phrasing, a sharp non-generic closing question, no em-dashes.
- **Self-audits before showing the user** against the shared 5 dimensions, fixing flagged items once.
- **Review-first stop.** Presents the full draft + audit results and hands back for approval before writing any file.

**REVIEW/REFINE path**
- Scores the post out of 100 across 5 dimensions (20 pts each), each grounded in a specific 2026 ranking mechanic — the same mechanics the WRITE path produces and self-audits, defined once and shared.
- Produces **one refined version** fixing every flagged weakness (never multiple stylistic variants), re-checking the rubric against its own refined output before finalizing.
- Emits an itemized change list, each tied to the dimension it improves; flags anything it can't fix for lack of source information rather than inventing facts.

---

## Shared rubric / mechanics (defined once)

Both paths reference one shared definition of the 5 dimensions — no duplication:

| Dimension | What it checks | Why it matters |
|---|---|---|
| Hook strength | Fold test on the first 1–3 lines, tension/specificity | Determines whether the post gets read past "see more" |
| Structure & scannability | One-idea-per-line, paragraph caps, no em-dashes | Phone-first reading behavior |
| Specificity & save-worthiness | Real detail, reusable frameworks | Saves drive ~5x the reach of a like — highest-leverage dimension |
| Engagement design | Closing-question quality, no bait phrasing | Comments carry ~2x reach of likes; bait is actively suppressed |
| Platform mechanics | No body links, no AI-voice crutch phrases, hashtag discipline | Body links tank dwell time, a core ranking signal |

LinkedIn's 2026 ranking is semantic and relevance-over-recency; saves drive roughly 5x the reach of a like, comments about 2x, dwell time is a major passive signal, and engagement bait is actively suppressed rather than rewarded. Every craft rule and rubric dimension traces back to one of these mechanics.

---

## Input

A file path (any text format) — notes/draft/points for the WRITE path, or a finished post for the REVIEW/REFINE path. If missing, the skill asks before doing anything else. Pasted text works too, but then the skill asks where to write the output since there's no source directory.

## Output

- **WRITE path** — `linkedin_post.md`.
- **REVIEW/REFINE path** — `linkedin_post_revised.md`, containing (in order): the score table, the refined post, then the itemized change list.

Both are written in the **same directory as the source file** — never a fixed `linkedin/` or `drafts/` folder. Neither silently overwrites an existing file; each offers overwrite, a `-v2` variant, or a new name.

---

## Workflow (delegation-model units)

Each unit is self-contained: a goal/scope, explicit inputs, a self-verify step, an explicit hand-back stop gate where the doer must return control, and a terse report contract.

**WRITE path**
1. **W1 Intake & type selection** — read source, detect type. **Stop gate:** confirm type.
2. **W2 Hook engineering** — 5 variants. **Stop gate:** hand back for pick/mix.
3. **W3 Draft** — frame + body + 3 closing-question candidates + hashtags; runs W4 before reporting.
4. **W4 Self-audit** — 5-dimension PASS/FLAGGED check, fixed once (runs inside W3).
5. **W5 Review-first** — **Stop gate:** show draft + audit, hand back for approval; nothing written yet.
6. **W6 Persist** — write `linkedin_post.md`, confirm the exact path.

**REVIEW/REFINE path**
1. **R1 Intake** — read the finished post.
2. **R2 Diagnose & score** — per-dimension diagnostic + /20 each, summed to /100.
3. **R3 Refine** — one refined version; re-checks the rubric against its own output.
4. **R4 Itemize changes** — every flag accounted for as change or explicit not-fixed note.
5. **R5 Present & confirm** — **Stop gate (lightweight):** show score + refined + changes; another pass re-runs R2–R4.
6. **R6 Write** — write `linkedin_post_revised.md` (score → refined → changes), confirm the path.

---

## Limitations

- Requires a source file or pasted text; does not generate a post from nothing.
- REVIEW/REFINE produces exactly one refined version per pass, not multiple stylistic options.
- Will not fabricate specific facts/numbers to raise the specificity score — flags the gap instead.
- Does not generate images/carousels — hand off to `linkedin-image-prompts`.
- No voice-profile matching — writes/refines toward the rubric, in a neutral, direct professional voice.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global — available in all projects (Linux/macOS)
cp -r content-creation/linkedin/linkedin-post-writer ~/.config/opencode/skills/

# Per-project only
cp -r content-creation/linkedin/linkedin-post-writer .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse content-creation\linkedin\linkedin-post-writer "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a named section |
| **Cursor** | Paste into `.cursor/rules/linkedin-post-writer.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your opening message |

---

## Companion skills

- **`linkedin-image-prompts`** — generates carousel/hero-image prompts from the post this skill writes or refines (`linkedin_post.md` or `linkedin_post_revised.md`).
