---
name: init-session
description: Use when the user types /init-session or says "start session", "load handoff", "restore context", or "what was I working on". It reads .agent_docs/handoff.md and loads the project summary, last-session log, and open items into the current session, then delivers a compact session-initialized briefing. Read-only — it never modifies files. If no handoff exists, it reports the path cleanly and stops rather than failing.
---

# Init Session — Context Loader

Restore full project context at the start of an agent session. Read the rolling handoff log written by the companion `end-session` skill, load its sections into working context, and deliver a tight briefing so work can resume immediately — without re-reading the whole codebase.

## When to use

- The user types `/init-session` or says "start session", "load handoff", "restore context", or "what was I working on".
- At the beginning of a work session where a prior `end-session` run should have left a handoff.
- Not for writing or updating the handoff — that is the companion **`end-session`** skill.

## Execution model

This skill runs **fully automatically as a single read-and-report pass — there is no routine STOP GATE.** It reads, loads, and reports without pausing for approval, because it writes nothing. The **one** conditional hand-back is Unit I5: if the handoff is clearly stale or internally ambiguous about where work stands, surface that and let the user decide before treating its open items as the work queue.

---

## Shared reference (defined once — units reference this, do not restate)

**Handoff file** — `.agent_docs/handoff.md`, relative to the workspace root. Written by the companion **`end-session`** skill. Rolling log retaining the last two sessions.

**Handoff sections** loaded by this skill:

- **Project Summary** — ground truth for what the project is, its key files, and its architecture.
- **Session Log** — what was done last session and the state it was left in.
- **Open Items / Next Steps** — concrete tasks carrying over; the starting work queue for this session.
- **Quick Reference** — key commands, file locations, known gotchas; applied while executing tasks.

**Project rules file** — `AGENTS.md` at the workspace root. Optional. Authoritative project rules (exact parameter names, table names, path casing, shell conventions, import patterns) that **take precedence over anything in the handoff if they conflict**. Internalize it — never echo it back to the user.

**Missing-content rule** — never error out on absent or malformed content. If the handoff file is missing, report cleanly and stop (Unit I1). If an individual section is missing or malformed, continue with what is available.

**Briefing output format** — the final structured message (Unit I4):

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

Keep it tight — orient quickly, never reproduce the full handoff.

---

## Workflow (units)

### Unit I1 — Locate & read the handoff
- **Goal/scope**: obtain the handoff content, or determine cleanly that it is absent.
- **Inputs**: the **Handoff file** path (shared reference).
- **Do**: read `.agent_docs/handoff.md`.
- **Self-verify**: confirm the file was found and its content is in hand.
  - If it **fails / file not found**: reply with `No handoff.md found at `.agent_docs/handoff.md`. Run `/end-session` at the end of a session to initialize it.` and **stop the whole skill here** — do not proceed to later units (per the shared missing-content rule).
- **Report contract**: `handoff: found & read` or `handoff: not found at .agent_docs/handoff.md — stopped, advised /end-session`.

### Unit I2 — Read project rules (AGENTS.md)
- **Goal/scope**: load authoritative project rules that override handoff content on conflict.
- **Inputs**: the **Project rules file** path (shared reference).
- **Do**: read `AGENTS.md` at the workspace root and internalize it. Do not echo it back to the user.
- **Self-verify**: confirm whether `AGENTS.md` was present and loaded; if absent, note that and continue (it is optional — missing-content rule).
- **Report contract**: `AGENTS.md: loaded (rules take precedence on conflict)` or `AGENTS.md: absent — continued`.

### Unit I3 — Internalize handoff sections
- **Goal/scope**: load the handoff's sections into working context as the session's ground truth and work queue.
- **Inputs**: the handoff content from I1; the **Handoff sections** list (shared reference).
- **Do**: load **Project Summary**, **Session Log**, **Open Items / Next Steps**, and **Quick Reference** into working context per their shared-reference roles. Apply AGENTS.md precedence from I2 wherever it conflicts with the handoff.
- **Self-verify**: confirm each expected section was actually located and loaded; note which (if any) were missing or malformed and continue with what is available (missing-content rule) — do not error out.
- **Report contract**: `sections loaded: <list present> | missing/malformed: <list or none>`.

### Unit I4 — Deliver the briefing
- **Goal/scope**: give the user a compact session-initialized orientation.
- **Inputs**: the internalized content from I3; the **Briefing output format** (shared reference).
- **Do**: reply using the Briefing output format — project one-liner, last-session summary with date, open-items checklist (write "None" if empty/absent), and one next-action line. Keep it tight; never reproduce the full handoff.
- **Self-verify**: confirm the briefing is populated from the loaded content (not placeholders) and that the open-items checklist matches the Open Items section loaded in I3.
- **Report contract**: `briefing delivered | open items: <N or None>`.

### Unit I5 — Stale/ambiguous handoff check (conditional STOP GATE)
- **Goal/scope**: catch a handoff that is clearly stale or internally ambiguous about where work stands before its open items are treated as the authoritative work queue.
- **Inputs**: the internalized content from I3 (dates, session log, open items).
- **Do**: judge whether the handoff is coherent and current. If it is clearly consistent, **no gate fires** — the skill has already completed at I4 and no hand-back is needed.
- **STOP GATE (hand back) — conditional**: fires **only** if the handoff is clearly stale (e.g. dated far in the past relative to the session) or internally contradictory (e.g. open items conflict with the session log). When it fires, surface the specific concern in one line and **hand control back** for the user to confirm how to proceed before the open items are used as the work queue. When it does not fire, state that explicitly and take no action.
- **Report contract**: `staleness/ambiguity: none — no gate` or `flagged: <one-line concern> | awaiting: user confirmation on how to proceed`.

---

## Companion skill

Use **`end-session`** at the end of every session to write the handoff (`.agent_docs/handoff.md`) that this skill reads.
