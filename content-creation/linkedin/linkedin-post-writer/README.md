# linkedin-post-writer

Turn a source draft, notes file, or rough bullet points into a posting-ready LinkedIn post. Applies platform craft grounded in how LinkedIn's algorithm ranks content in 2026 — hook engineering for the "see more" fold, scroll-first body structure, no-link-in-body dwell-time protection, and engagement-bait avoidance — with a mandatory review gate before anything is written.

---

## Trigger phrases

| Input | Example |
|---|---|
| Draft to post | "Turn these notes into a LinkedIn post", "write a LinkedIn post from this file" |
| Raw points | User pastes bullets/ideas directly and asks for a LinkedIn post |

Not for Medium, X/Twitter, or other platforms. Not for carousel/image generation — see `linkedin-image-prompts`, meant to run after this skill.

---

## What it does

- **Locates the source.** Requires a file path from the user; asks if none is given. Never guesses a folder to read from.
- **Detects content type.** Short Post (100–300w), Long Post (600–1200w), or Article (1000–2500w+) — auto-detected from the source substance, stated with one-line reasoning, and confirmed with the user before drafting.
- **Hook engineering (mandatory gate).** Generates 5 hook variants — Contrarian, Curiosity gap/number-contrast, Confession, Mid-scene, Problem-naming — applying the cold-read test and exact-number specificity. Stops and waits for the user to pick or mix before drafting the body.
- **Narrative frame selection.** Picks the frame (Before→After→Bridge, Mistake→Realization→Shift, Challenge→Action→Result, Contrarian stance) that fits the real content, never the reverse.
- **Body craft.** One idea per line, 1–3 line paragraphs, specificity over vague nouns, zero links in the body (dwell-time protection), no engagement-bait phrasing, a sharp non-generic closing question.
- **Self-audits before showing the user** — hook fold test, line density, specificity, crutch-phrase scan, link discipline, engagement-bait scan, closing-question quality — fixing flagged items once.
- **Review-first stop.** Presents the full draft + audit results and waits for approval before writing any file.

## Why these specific rules

LinkedIn's 2026 ranking is semantic and relevance-over-recency; saves drive roughly 5x the reach of a like, comments about 2x, dwell time is a major passive signal, and engagement bait is actively suppressed rather than rewarded. Every craft rule in this skill traces back to one of these mechanics — not generic copywriting advice.

---

## Input

A file path to source notes/draft/points (any text format). If missing, the skill asks before doing anything else. Pasted text works too, but then the skill asks where to write the output since there's no source directory.

## Output

`linkedin_post.md`, written in the **same directory as the source file** — never a fixed `linkedin/` or `drafts/` folder. Never silently overwrites an existing file; offers overwrite, `-v2`, or a new name instead.

---

## Workflow

1. **Intake + type selection** — read the source, detect/confirm content type.
2. **Hook engineering** — 5 variants presented, mandatory stop for the user's pick.
3. **Draft** — frame selection, body craft, 3 closing-question candidates, hashtags.
4. **Self-audit** — 7-point PASS/FLAGGED check, fixed once before showing the user.
5. **Review-first stop** — full draft + audit shown, waits for approval/edits.
6. **Persist** — writes `linkedin_post.md`, confirms the exact path.

---

## Limitations

- Requires a source file or pasted text; does not generate a post from nothing.
- Does not generate images/carousels — hand off to `linkedin-image-prompts`.
- Does not score or produce alternate variants of an already-finished post — hand off to `linkedin-post-reviewer`.
- No voice-profile matching — writes in a neutral, direct professional voice.

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

- **`linkedin-image-prompts`** — generates carousel/hero-image prompts from the post this skill writes.
- **`linkedin-post-reviewer`** — scores and refines a finished post for virality.
