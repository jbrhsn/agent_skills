---
name: end-session
description: Use when the user types /end-session or says "end session", "wrap up session", "create handoff", or "generate handoff". It writes or updates .agent_docs/handoff.md with a refreshed project summary, a rolling two-session action log inferred from recently modified files and conversation context, an open-items section drawn from the current session, and a quick-reference cheat-sheet. It runs fully automatically as a capture-and-write pass — no confirmation gate — and always writes the complete file rather than a partial update.
---

# End Session — Handoff Generator

Capture the state of an agent session into a high-signal handoff file so the companion `init-session` skill can restore it next time. Refresh the project summary, roll a two-session action log inferred from recently modified files and conversation context, filter open items down to directly-actionable work, and refresh a quick-reference cheat-sheet — then write the complete file.

## When to use

- The user types `/end-session` or says "end session", "wrap up session", "create handoff", or "generate handoff".
- At the end of a work session, to leave context for the next session.
- Not for reading or restoring a handoff — that is the companion **`init-session`** skill.

## Execution model

This skill runs **fully automatically as a single capture-and-write pass — there is NO STOP GATE.** It gathers signals, composes the file, writes it, and reports without pausing for approval, because it is a routine capture-and-write operation, not a destructive or ambiguous one. It always writes the **complete** handoff file (never a partial update), and it carries the prior session forward verbatim rather than overwriting session history — see the shared reference for the rolling rule.

---

## Shared reference (defined once — units reference this, do not restate)

**Handoff file** — `.agent_docs/handoff.md`, relative to the workspace root. Read by the companion **`init-session`** skill. The `Write` tool creates `.agent_docs/` automatically if it does not exist. Always write the **complete** file, never a partial update.

**Rolling two-session rule** — the Session Log retains exactly the last **two** sessions, newest first. On each run the current session becomes the new top entry, the most recent prior entry becomes the second entry, and **anything older than those two is dropped**. The previous session entry is carried forward **verbatim** — never rewritten or re-summarized. On first-time initialization (no prior handoff) only the current entry is written, followed by `*No prior session recorded.*`.

**Handoff sections** (composed in this order):

- **Project Summary** *(always re-generated)* — concise 150–250 word overview: what the project is (purpose/business context), key artifacts (most important files/folders and what they are), architecture in one paragraph, and critical constants (exact names/paths/values that must not change). Tightly factual, no fluff.
- **Session Log** *(rolling two-session window)* — two dated entries per the rolling rule (format in the file template below).
- **Open Items / Next Steps** — a filtered checklist per the **Open-items filter** below.
- **Quick Reference** *(refreshed each session)* — ~15-bullet cheat-sheet: key commands, key file locations, known gotchas. Every item factually grounded in actual project files — never invent paths or commands.

**Open-items filter** — apply ruthlessly before writing any item. Test each candidate: *"Can a coding agent open a file and make a change to resolve this?"* If no, discard it.

- **Include ONLY:** a specific file/section explicitly started this session but not finished; a concrete technical decision deferred mid-session that is blocking further code/doc changes; a specific file identified as needing a code/content change that was not yet touched.
- **Reject ALL of:** anything phrased as "consider / verify / review / confirm / check whether"; review or approval steps; improvement ideas or feature suggestions outside this session's scope; stakeholder/process/human-action items; anything not traceable to unfinished work from this session's file changes.
- If nothing passes, write: `No open items from this session.`

**Project rules file** — `AGENTS.md` at the workspace root. Optional. Feeds the Project Summary and Quick Reference with authoritative rules, exact names, and known gotchas. If absent, continue without it.

**Handoff file template**:

```markdown
# Handoff Log

## Project Progress (rolling summary)
<150–250 word overview: purpose, key files, architecture, critical constants>

## Session Log

### Session: <YYYY-MM-DD> (current)
**Files touched:** <relative paths from Unit E1, grouped by folder>
**Summary:** <2–4 sentences on what was accomplished, inferred from files changed + conversation context>
**Outcome:** <one sentence — what state the work was left in>

### Session: <date> (previous)
<carried verbatim from prior handoff — never rewritten>

## Open Items / Next Steps
- [ ] <specific file> — <what exactly needs to be done>

## Quick Reference
<~15-bullet cheat-sheet: key commands, file locations, gotchas>
```

**Platform-aware commands** (run with the `bash` tool where applicable):

- Today's date — Linux/macOS: `date +%Y-%m-%d`; Windows (PowerShell): `Get-Date -Format 'yyyy-MM-dd'`.
- Recently modified files (last 8 hours) — Linux/macOS: `git log --since="8 hours ago" --name-only --pretty=format: | sort -u | grep -v '^$'`, falling back to `find . -not -path './.git/*' -newer .git/index -type f 2>/dev/null | sort` when there is no git history or the result is empty. Windows (PowerShell): `& "$env:USERPROFILE\.config\opencode\skills\end-session\get-session-context.ps1" -HoursBack 8 -Root "."` (one line per file: `<timestamp>  <relative-path>` — parse as plain text, not a table).
- If the file list is empty, retry with a 24-hour window (`24 hours ago` / `-HoursBack 24`). If still empty, record "No project files modified this session" in the Session Log.

---

## Workflow (units)

### Unit E1 — Gather date & recent file activity
- **Goal/scope**: establish today's date and the list of files worked on this session — the primary signal for inferring the session summary.
- **Inputs**: the **Platform-aware commands** (shared reference).
- **Do**: run the date command and the recent-modified-files command for the detected platform, applying the 8h→24h fallback and the empty-result handling from the shared reference.
- **Self-verify**: confirm a date string was obtained and a file list (or an explicit "no files modified this session" determination) is in hand.
- **Report contract**: `date: <YYYY-MM-DD> | modified files: <N or "none — 24h window empty">`.

### Unit E2 — Read existing handoff & extract prior session
- **Goal/scope**: obtain the current handoff so the prior session can be carried forward, or determine this is a first-time init.
- **Inputs**: the **Handoff file** path and **Rolling two-session rule** (shared reference).
- **Do**: `Read` `.agent_docs/handoff.md`. If it exists, extract the most recent Session Log entry to carry forward **verbatim** as the "previous" entry. If it does not exist, treat this as first-time initialization (write a richer Project Summary; the log will carry only the current entry plus `*No prior session recorded.*`).
- **Self-verify**: confirm whether the handoff was found; if found, confirm the prior session entry was captured verbatim for carry-forward; if absent, confirm first-time-init mode is set.
- **Report contract**: `existing handoff: found — prior session captured` or `existing handoff: absent — first-time init`.

### Unit E3 — Survey project structure & rules
- **Goal/scope**: understand current project state well enough to compose an accurate Project Summary and Quick Reference.
- **Inputs**: the **Project rules file** path (shared reference); the workspace tree.
- **Do**: `Read` the workspace root and the key subdirectories that exist (`src/`, `notebooks/`, `docs/`, `tests/`). `Read` `AGENTS.md` at the root if present — it feeds authoritative names, rules, and gotchas into the Project Summary and Quick Reference. `Read` individual files only when the filename alone does not convey purpose.
- **Self-verify**: confirm the root and existing key subdirectories were surveyed, and note whether `AGENTS.md` was present and folded in (absent is fine — continue).
- **Report contract**: `surveyed: root + <subdirs present> | AGENTS.md: <loaded | absent>`.

### Unit E4 — Compose the four handoff sections
- **Goal/scope**: build the complete handoff content in memory before writing.
- **Inputs**: E1 (date + files), E2 (prior session + init mode), E3 (survey + AGENTS.md); the **Handoff sections**, **Rolling two-session rule**, **Open-items filter**, and **Handoff file template** (shared reference).
- **Do**: compose all four sections in order per the template — regenerate the **Project Summary**; build the **Session Log** as the current entry (files grouped by folder, 2–4 sentence summary inferred from files + conversation, one-line outcome) plus the prior entry carried forward per the rolling rule (or the first-time-init line); build **Open Items / Next Steps** by applying the Open-items filter; refresh the **Quick Reference** (~15 bullets, all grounded in real files).
- **Self-verify**:
  - Confirm all four sections are present and populated (not placeholders).
  - Confirm the **Session Log holds exactly the rolling two-session window** — current entry newest, at most one prior entry, anything older dropped, prior entry unchanged verbatim (or, on first-time init, only the current entry plus `*No prior session recorded.*`).
  - Confirm every Open Item passes the Open-items filter ("can a coding agent open a file and make this change?"); if none pass, the section reads `No open items from this session.`
- **Report contract**: `sections composed: 4 | session log entries: <1 (init) | 2> | open items: <N | none>`.

### Unit E5 — Write the handoff file
- **Goal/scope**: persist the composed content as the complete handoff.
- **Inputs**: the composed content from E4; the **Handoff file** path (shared reference).
- **Do**: use the `Write` tool to write the **complete** composed content to `.agent_docs/handoff.md` (the tool creates `.agent_docs/` if needed). Never write a partial update.
- **Self-verify**: confirm the file exists at `.agent_docs/handoff.md` and contains all four sections in order, with the Session Log matching the rolling two-session window composed in E4.
- **Report contract**: `wrote: .agent_docs/handoff.md (complete) | mode: <first-time init | update>`.

### Unit E6 — Confirm to the user
- **Goal/scope**: report what was captured and point to the companion skill.
- **Inputs**: results of E1–E5.
- **Do**: reply with the path written (`.agent_docs/handoff.md`), whether this was a first-time init or an update, a one-line summary of what was captured (files touched + outcome), and the reminder: "Start your next session with `/init-session` to restore this context."
- **Self-verify**: confirm the confirmation reflects the actual write result from E5 (path, mode, session captured).
- **Report contract**: `confirmed: path + <init|update> + session summary + /init-session reminder`.

---

## Companion skill

Use **`init-session`** at the start of every session to restore the context this skill writes to `.agent_docs/handoff.md`.
