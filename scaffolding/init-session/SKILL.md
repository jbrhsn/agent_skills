---
name: init-session
description: Use when starting a new work session on any project. Reads the handoff log, README, and AGENTS.md to rebuild full context — then produces a concise briefing. Read-only for project code; only writes to .gitignore to exclude agent reference files.
---

# init-session

## When to use this skill

Trigger on any request that matches:
- "start a new session"
- "init session"
- "reload context"
- "what's the project state?"
- "where did we leave off?"
- "catch me up on this project"
- `/init-session` (as a slash command)

Do NOT trigger if the user is asking to make code changes, run builds, or author content — this skill is read-only orientation only.

---

## Core Principles

1. **Read before acting.** Never make code changes, run tests, or commit during this skill. Orientation only.
2. **Three docs first.** Most sessions can be resumed from `.agent_docs/handoff.md`, `README.md`, and `AGENTS.md` alone. Do not escalate to git or filesystem checks unless the three docs disagree.
3. **Aligned docs are enough.** When the three baseline docs tell a consistent story, trust them — do not verify every path on disk "just to be thorough."
4. **Escalate only on conflict.** If the docs disagree, use git and targeted Glob/Read calls to find the truth, then flag every discrepancy explicitly.
5. **Concise briefing.** The output is a short operational summary, not a wall of text.

---

## Phase 0 — Intake

No intake questions needed. Begin immediately.

If the user provides `$ARGUMENTS` (e.g. a focus area like "pick up where we left off on the auth module"), treat it as an optional focus hint and incorporate it into the briefing.

---

## Phase 1 — Read the Three Baseline Docs

**Read all three in parallel** (they are independent):

1. **Handoff log** — `.agent_docs/handoff.md`
   - Common alternates: `HANDOFF.md`, `PROGRESS.md`, `docs/handoff.md`, `.handoff/`
   - Focus on: the `## Project Progress (rolling summary)` block at the top, and the most recent detailed entry
   - Skim earlier detailed entries only if needed for continuity

2. **README** — `README.md` at repo root
   - Focus on: project overview, described directory layout, any current-state claims

3. **Agent/contributor conventions** — `AGENTS.md` (canonical)
   - Common alternates to also check: `CONTRIBUTING.md`, `.cursorrules`, `CLAUDE.md`
   - Focus on: locked-in rules, non-negotiable constraints, any filesystem manifest (`What actually exists` sections)

If any of the three is missing or empty: note it explicitly and proceed directly to Phase 2 (escalation).

---

## Phase 2 — Alignment Check

Run this checklist against the three docs. All checks must pass for the docs to be "aligned":

| Check | What to verify |
|---|---|
| Handoff vs. AGENTS.md manifest | Does the handoff's `Now` / `Progress so far` describe a repo whose files match AGENTS.md's file list? |
| README layout vs. AGENTS.md manifest | Does the directory tree in README match AGENTS.md's manifest? |
| Handoff `Next up` vs. README/AGENTS.md | Is the queued next action still coherent given what the other docs describe? |
| Rolling summary vs. newest detailed entry | Do they tell the same story about current project state? |
| Explicit stale flags | If AGENTS.md (or handoff) marks another doc as stale, that counts as alignment — the conflict is documented. |

**If every check passes → aligned.** Go directly to Phase 4 (produce the briefing). Do NOT run git commands or verify paths on disk.

**If any check fails → not aligned.** Continue to Phase 3.

---

## Phase 3 — Escalation (only when docs disagree)

Trust the repository over any doc. Run read-only commands only:

```bash
git status --short
git log --oneline -10
git diff --stat
```

Use Glob/Read/Grep to verify specific paths that the docs disagreed about. Do not scan the whole tree — target only the disputed claims.

Flag every discrepancy in the "Open issues / cautions" section of the briefing: which doc is wrong and what the repo actually shows.

---

## Phase 4 — Update .gitignore for Agent Reference Files

Ensure agent reference files are excluded from version control:

1. Check if `.gitignore` exists at the repo root. If not, create it.
2. For each agent reference file that exists in the repo, add it to `.gitignore` if not already present:
   - `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `CONTRIBUTING.md` (if agent-specific)
3. Format in `.gitignore`:
   ```
   # Agent reference files (auto-maintained by init-session)
   AGENTS.md
   CLAUDE.md
   .cursorrules
   ```
4. Do not commit or push this change — leave it for the user to approve.

---

## Phase 5 — Produce the Briefing

Output the briefing in this exact structure:

```markdown
### Overall progress
- <2–4 bullets distilled from the handoff rolling summary: phase-by-phase / milestone progress so far>
- <Note if reconstructed because the summary block was absent>

### Project state
- <current phase/milestone, overall status, what exists vs. not — 1–3 bullets>

### Last session recap
- <what the most recent detailed handoff entry says was done>
- <note if no handoff exists>

### Open issues / cautions
- <unresolved issues, OPEN items, or doc discrepancies>
- <if docs were aligned: "Docs aligned — no discrepancies found.">

### Recommended next steps
1. <highest-priority next action, from the rolling summary's "next up">
2. <next>
3. <next>

### Awaiting your direction
- <ask the user which next step to start, or confirm the focus from $ARGUMENTS>

### Context-load footnote
- <"aligned: 3 docs only" OR "escalated: 3 docs + git + <specific verifications>">
```

---

## Constraints

- **Read-only for project code.** Do not edit app/project files, run builds, tests, or commit/push/stash/amend.
- **Write-only to `.gitignore`.** Phase 4 may create or append to `.gitignore`. Do not commit this change.
- **Do not pre-emptively verify paths.** When docs are aligned, they are the source of truth — no additional filesystem checks.
- **No code changes.** If the user also asks for a code change in the same message, acknowledge it but defer until after orientation is complete.

---

## Adapting to Other Agents

This skill was authored for **OpenCode** (`SKILL.md` format with frontmatter).
To use it with other platforms:

| Platform | How to adapt |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into your project's `CLAUDE.md` under a `## Session Management` section. |
| **Cursor** | Paste the content (below frontmatter) into `.cursor/rules/init-session.mdc`, set rule type to `Agent Requested`. |
| **GitHub Copilot** | Add the content to `.github/copilot-instructions.md` under a `## Session Start Workflow` heading. |
| **ChatGPT / Claude (web)** | Paste the full content below the frontmatter as your first message, then describe the project. |

---

## Reference: directory layout for this skill

```
agent_skills/
└── scaffolding/
    └── init-session/
        ├── SKILL.md      ← this file (OpenCode primary format)
        └── README.md     ← human-readable guide for this skill
```
