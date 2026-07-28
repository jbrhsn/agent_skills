# linkedin-post-reviewer

Score a finished LinkedIn post across 5 algorithm-aligned dimensions and produce one refined version that fixes the flagged weaknesses. This skill scores and rewrites in place — it does not produce multiple stylistic variants.

---

## Trigger phrases

| Input | Example |
|---|---|
| Review/score request | "review this LinkedIn post", "score this for virality", "how shareable is this" |
| Refinement request | "refine this post", "tighten this up" |

Works on any pasted text or file, not only output from `linkedin-post-writer`.

---

## What it does

Scores the piece out of 100 across 5 dimensions (20 pts each), each grounded in a specific 2026 LinkedIn ranking mechanic rather than generic writing advice:

| Dimension | What it checks | Why it matters |
|---|---|---|
| Hook strength | Fold test on the first 1–3 lines, tension/specificity | Determines whether the post gets read past "see more" |
| Structure & scannability | One-idea-per-line, paragraph caps | Phone-first reading behavior |
| Specificity & save-worthiness | Real detail, reusable frameworks | Saves drive ~5x the reach of a like — highest-leverage dimension |
| Engagement design | Closing-question quality, no bait phrasing | Comments carry ~2x reach of likes; bait is actively suppressed |
| Platform mechanics | No body links, no AI-voice crutch phrases, hashtag discipline | Body links tank dwell time, a core ranking signal |

After scoring, it produces **one refined version** addressing every flagged weakness, plus an itemized list of what changed and why, tied back to the specific dimension improved.

---

## Input

A file path to the finished post. If not given, ask. Pasted text also works — the skill will ask where to write the output since there's no source directory.

## Output

`linkedin_post_revised.md`, written in the **same directory as the source file**, containing (in order): the score table, the refined post, and the itemized change list. Never silently overwrites — offers overwrite, `-v2`, or a new name.

---

## Workflow

1. **Intake** — read the source post.
2. **Diagnose** — one-line strong/weak note per dimension.
3. **Score** — /20 per dimension, summed to /100.
4. **Refine** — produce one version fixing every flagged weakness; flag (don't invent) anything needing information not in the source.
5. **Itemize** — list each change with its rationale, tied to a dimension.
6. **Present** — lightweight confirm; another pass treats the refined version as new input.
7. **Write** — `linkedin_post_revised.md`, confirmed path.

---

## Limitations

- Produces exactly one refined version per pass, not multiple stylistic options.
- Will not fabricate specific facts/numbers to raise the specificity score — flags the gap instead.
- No voice-profile matching — refines toward the rubric, not a personal style guide.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global — available in all projects (Linux/macOS)
cp -r content-creation/linkedin/linkedin-post-reviewer ~/.config/opencode/skills/

# Per-project only
cp -r content-creation/linkedin/linkedin-post-reviewer .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse content-creation\linkedin\linkedin-post-reviewer "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a named section |
| **Cursor** | Paste into `.cursor/rules/linkedin-post-reviewer.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your opening message |

---

## Companion skills

- **`linkedin-post-writer`** — produces the original `linkedin_post.md`.
- **`linkedin-image-prompts`** — can generate visuals from the refined `linkedin_post_revised.md`.
