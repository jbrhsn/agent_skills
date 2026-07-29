---
name: init-session
description: Use when the user types /init-session or says "start session", "load handoff", "restore context", or "what was I working on". Reads .agent_docs/handoff.md and loads project context, last session summary, and open items into the current session.
---

# Init Session — Context Loader

Follow these steps in order every time the skill activates.

---

## Step 1 — Read handoff.md

Use the `Read` tool on `.agent_docs/handoff.md`.

- If it **fails / file not found**: reply with "No handoff.md found at `.agent_docs/handoff.md`. Run `/end-session` at the end of a session to initialize it." Stop here.
- If it **succeeds**: proceed to Step 2.

---

## Step 2 — Read AGENTS.md

Use the `Read` tool on `AGENTS.md` at the workspace root. This contains authoritative project rules (exact parameter names, table names, path casing, shell conventions, import patterns) that take precedence over anything in handoff.md if they conflict. Internalize it — do not echo it back to the user.

---

## Step 3 — Internalize the handoff content

From the handoff.md, load these sections into working context:

- **Project Summary** — treat as ground truth for what this project is, its key files, and its architecture
- **Session Log** — understand what was done last session and what state it was left in
- **Open Items / Next Steps** — these are the concrete coding tasks carrying over; treat them as the starting work queue for this session
- **Quick Reference** — key commands, file locations, known gotchas; apply these when executing tasks this session

If any section is missing or malformed, continue with what is available — do not error out.

---

## Step 4 — Confirm to the user

Reply with this structured briefing:

```
## Session Initialized

**Project:** <one-line description from the Project Summary>

**Last session (<date>):** <one or two sentences — what was accomplished and what state it was left in>

**Open items carrying over:**
- [ ] <item>
- [ ] <item>
(write "None" if the list was empty or absent)

**Ready.** <one sentence on the logical next action based on open items, or last session outcome if no open items>
```

Keep it tight — orient quickly, do not reproduce the full handoff.md. The user is ready to work.
