# end-session

Writes a high-signal handoff file at the end of an agent session. Captures a rolling project summary, a dated session entry (inferred from recently modified files and conversation context), and a filtered list of open items for the next agent to act on.

---

## Trigger phrases

| Input | Example |
|---|---|
| Slash command | `/end-session` |
| Natural language | "end session", "wrap up session", "create handoff", "generate handoff" |

---

## What it does

1. **Gets the current date** — platform-aware: uses `date +%Y-%m-%d` on Linux/macOS or `Get-Date` on Windows.
2. **Reads recent file activity** — uses `git log` (Linux/macOS) or the bundled `get-session-context.ps1` (Windows) to identify what was worked on in the last 8 hours. Falls back to 24 hours if empty.
3. **Reads the existing handoff** (if present) — extracts the previous session entry to carry forward verbatim, maintaining the rolling 2-session window.
4. **Surveys the project structure** — reads the root directory and key subdirectories; reads `AGENTS.md` for authoritative project rules.
5. **Composes the full handoff file** — four sections: Project Summary, Session Log, Open Items, Quick Reference.
6. **Writes `.agent_docs/handoff.md`** — creates the `.agent_docs/` directory automatically if needed.
7. **Confirms** — reports the path, whether this was an init or update, and what was captured.

---

## Workflow

Six sequential steps, no confirmation gates (it is a capture-and-write operation):

```
Step 1 — Get date + recent file activity
Step 2 — Read existing handoff.md (if any)
Step 3 — Survey project structure + AGENTS.md
Step 4 — Compose the four handoff sections
Step 5 — Write .agent_docs/handoff.md
Step 6 — Confirm to user
```

---

## Handoff file structure

```markdown
# Handoff Log

## Project Progress (rolling summary)
<150–250 word project overview: purpose, key files, architecture, critical constants>

## Session Log

### Session: YYYY-MM-DD (current)
**Files touched:** ...
**Summary:** ...
**Outcome:** ...

### Session: YYYY-MM-DD (previous)
<carried verbatim from prior handoff — never rewritten>

## Open Items / Next Steps
- [ ] <specific file> — <what exactly needs to be done>

## Quick Reference
<~15 bullet cheat-sheet: key commands, file locations, gotchas>
```

---

## Open items filter

The skill applies a strict filter to open items — only items that a coding agent can directly execute in the next session are included:

**Included:**
- A file that was started but not finished this session
- A concrete technical decision deferred mid-session that blocks further changes
- A specific file identified as needing a change that was not yet touched

**Excluded:**
- "Consider", "verify", "review", "check whether" items
- Feature ideas or improvement suggestions outside this session's scope
- Human-action, process, or stakeholder items

---

## Inputs

| Input | Required | Description |
|---|---|---|
| `.agent_docs/handoff.md` | No | If present, the previous session entry is extracted and carried forward. If absent, the skill initializes from scratch. |
| `AGENTS.md` | No | If present, feeds the Project Summary and Quick Reference sections. |
| Conversation context | Yes | Used to infer session summary and open items alongside the file list. |

---

## Outputs

**`.agent_docs/handoff.md`** — written or updated with the full four-section structure.

---

## Limitations

- **File activity inference is heuristic.** The skill infers what was done from recently modified files and conversation context — it does not have a perfect record of every change made.
- **Rolling 2-session window.** Entries older than two sessions are dropped. Use git history for older context.
- **PowerShell script is Windows-global-path only.** `get-session-context.ps1` is hardcoded to `$env:USERPROFILE\.config\opencode\skills\end-session\`. Update the path if installing per-project or on a non-standard location. On Linux/macOS the skill uses `git log` automatically.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global — available in all projects (Linux/macOS)
cp -r agent_session_management/end-session ~/.config/opencode/skills/

# Per-project only
cp -r agent_session_management/end-session .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse agent_session_management\end-session "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a named section |
| **Cursor** | Paste into `.cursor/rules/end-session.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your opening message |

---

## Companion skill

Use **`init-session`** at the start of every session to restore the context this skill writes.
