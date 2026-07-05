---
name: end-session
description: Use when ending a work session. Writes a high-signal handoff to .agent_docs/handoff.md — a rolling project summary plus a detailed session entry — so the next agent or session can resume without loss of context.
---

# end-session

## When to use this skill

Trigger on any request that matches:
- "end session"
- "wrap up"
- "write a handoff"
- "save my progress"
- "log what we did today"
- "I'm done for today"
- `/end-session` (as a slash command)

Do NOT trigger if the user is asking to continue working, commit code, or push changes — this skill writes the handoff only; it does not commit or push.

---

## Core Principles

1. **Evidence-based.** Ground every claim in git output and file inspection from this session — never paraphrase from memory alone.
2. **Rolling summary is always rewritten.** The `## Project Progress (rolling summary)` block is refreshed every session so it always reflects current state. It never grows unbounded.
3. **Detailed entries are append-only.** Never edit or delete previous session entries. Add the new one above older ones.
4. **Strict next-action sourcing.** Every item in `Next up` or `Recommended next steps` must come from pending work observed this session OR explicit user direction. Never infer or pad.
5. **No commits.** This skill writes `.agent_docs/handoff.md` only. It does not commit, push, stash, or amend.

---

## Phase 0 — Intake

No questions needed. Begin immediately.

If the user provides `$ARGUMENTS` (e.g. session notes or a summary of decisions), incorporate them only if they don't conflict with repository evidence.

---

## Phase 1 — Read the Existing Handoff

Read `.agent_docs/handoff.md`:
- If the directory `.agent_docs/` does not exist, create it.
- If the file does not exist or is empty, initialize it with just: `# Handoff Log`
- Read the existing `## Project Progress (rolling summary)` block — use it as the base for the refreshed summary.
- Read the most recent detailed entry — use it for continuity.

---

## Phase 2 — Inspect the Repository

Run these commands to ground the handoff in evidence:

```bash
git status --short
git diff --stat
git diff
git log --oneline -10
```

Use Read/Grep to inspect specific changed files as needed to confirm intent and summarize accurately.

Do NOT commit, amend, stash, rebase, or push.

---

## Phase 3 — Write the Updated Handoff

The updated file must always follow this layout:

```markdown
# Handoff Log

## Project Progress (rolling summary)

_Last updated: <YYYY-MM-DD>_

**Current phase:** <phase> — **Status:** <in progress | phase complete | blocked>
**Now:** <1 line: what state the project is in right now>

**Progress so far:**
- Phase 1 — <one-line status / what's done>
- Phase 2 — <one-line status / what's done>
- <compress older sessions into one-liners>

**Next up:** <single highest-priority next action. Write `_None — awaiting user direction._` if nothing qualifies.>

---

<newest detailed entry>
<older detailed entries — never edited>
```

### Rolling summary rules
- **Rewrite** the summary block in place every session — do not append to it.
- Keep it short: aim for ≤ 12 lines.
- Compress older phase detail into one-liners as the project progresses.
- `Next up` must come from pending work or explicit user direction only.

### Detailed entry format

```markdown
## <YYYY-MM-DD> — <short session title>

**Phase:** <phase name or "Unknown (inferred)">
**Status:** <in progress | phase complete | blocked>

### Current state
- <1–3 bullets: where the project stands at the end of this session>

### Completed this session
- <specific, verifiable work completed — mention files, modules, commands, or behavior changes>

### Decisions / rationale
- <important decisions made and why>

### Issues encountered
- <issue> → <resolution or current status>
- <issue> → OPEN

### Guidance for next agent
- <practical instruction, warning, assumption, or pattern to preserve>
- <things that were tried and should not be retried blindly>

### Recommended next steps
_Sourced only from pending work in this session or explicit user direction._
1. <highest-priority next action>
2. <next action>
```

### Next-actions sourcing rule (strict)

Only include items in `Next up` / `Recommended next steps` from:
1. **Pending work in this session** — uncommitted changes, deferred tasks, open issues, partially-completed items
2. **Explicit user direction given during this session**

**Do NOT:**
- Copy forward next-up items from the previous summary unless they are genuinely still pending
- Synthesize next actions from the project's roadmap or your own judgment about "what comes next"
- Pad the list to reach 3 items — one item is fine, zero items is fine (`_None — awaiting user direction._`)

---

## Phase 4 — Confirm

Print a one-line confirmation:
```
Handoff written: rolling summary updated to "<current status>"; session entry logged for <YYYY-MM-DD>.
```

Do not commit or push unless the user explicitly asks.

---

## Constraints

- **Write only to `.agent_docs/handoff.md`.** Do not edit any project code files.
- **No commits.** Never commit, push, stash, or amend as part of this skill.
- **Append-only for detailed entries.** Never edit or delete any previous session entry.
- **Rewrite the rolling summary.** It is refreshed, not appended to.
- **Evidence first.** Run git inspection before writing — do not paraphrase from memory.

---

## Adapting to Other Agents

This skill was authored for **OpenCode** (`SKILL.md` format with frontmatter).
To use it with other platforms:

| Platform | How to adapt |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into your project's `CLAUDE.md` under a `## Session End Workflow` section. |
| **Cursor** | Paste the content (below frontmatter) into `.cursor/rules/end-session.mdc`, set rule type to `Agent Requested`. |
| **GitHub Copilot** | Add the content to `.github/copilot-instructions.md` under a `## Session End Workflow` heading. |
| **ChatGPT / Claude (web)** | Paste the full content below the frontmatter as your first message, then say "end my session". |

---

## Reference: directory layout for this skill

```
agent_skills/
└── scaffolding/
    └── end-session/
        ├── SKILL.md      ← this file (OpenCode primary format)
        └── README.md     ← human-readable guide for this skill
```
