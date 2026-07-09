---
name: end-session
description: Use when the user types /end-session or says "end session", "wrap up session", "create handoff", or "generate handoff". Generates or updates .agent_docs/handoff.md with a refreshed project summary, a rolling two-session action log inferred from recently modified files, and an open items section drawn from current session context.
---

# End Session — Handoff Generator

Follow these steps in order every time the skill activates. Do not skip steps.

---

## Step 1 — Get today's date and recent file activity

**Get today's date** (needed for the session log entry):

Detect the platform and run the appropriate command with the `bash` tool:

- **Linux / macOS:**
  ```bash
  date +%Y-%m-%d
  ```
- **Windows (PowerShell):**
  ```powershell
  Get-Date -Format 'yyyy-MM-dd'
  ```

**Get recently modified project files** (last 8 hours):

Again, detect the platform and use the appropriate command:

- **Linux / macOS:**
  ```bash
  git log --since="8 hours ago" --name-only --pretty=format: | sort -u | grep -v '^$'
  ```
  If the repo has no git history or the result is empty, fall back to:
  ```bash
  find . -not -path './.git/*' -newer .git/index -type f 2>/dev/null | sort
  ```

- **Windows (PowerShell):**
  ```powershell
  & "$env:USERPROFILE\.config\opencode\skills\end-session\get-session-context.ps1" -HoursBack 8 -Root "."
  ```
  The script outputs one line per file: `<timestamp>  <relative-path>`. Parse it as plain text — do not treat it as a table.

Use the `bash` tool for all commands. The file list is the primary signal for inferring what was worked on this session.

If the file list returns no results, retry with a 24-hour window (replace `8 hours ago` with `24 hours ago`, or `-HoursBack 24` on Windows). If still empty, note "No project files modified this session" in the session log.

---

## Step 2 — Read the existing handoff.md (if it exists)

Use the `Read` tool on `.agent_docs/handoff.md`.

- If it **succeeds**: read it in full. Extract the **Session Log** section — you need the most recent previous session entry to carry forward verbatim. The current session becomes the new top entry; the previous session becomes the second entry; drop anything older (rolling 2-session window).
- If it **fails / file not found**: this is first-time initialization. Write all sections from scratch. Use a richer project summary since there is no prior context.

---

## Step 3 — Survey the project structure

Use the `Read` tool on the workspace root directory and these subdirectories to understand current project state:
- Root level
- `src/` (if it exists)
- `notebooks/` (if it exists)
- `docs/` (if it exists)
- `tests/` (if it exists)

Also read `AGENTS.md` at the root — it contains authoritative project rules, exact names, and known gotchas that must feed into the Project Summary and Quick Reference sections.

Use the `Read` tool on other files only if the filename alone is insufficient to describe its purpose.

---

## Step 4 — Compose the new handoff.md content

Build the full file content with these four sections in order:

---

### 4a — Project Summary *(always re-generated)*

A concise 150–250 word overview covering:
- **What this project is** — purpose, business context
- **Key artifacts** — the most important files/folders and what they are
- **Architecture in one paragraph** — how the pieces fit together
- **Critical constants** — exact names/paths/values that must not be changed

Keep it tightly factual. No fluff.

---

### 4b — Session Log *(rolling 2-session window)*

Format as two dated entries, newest first. Use the date obtained in Step 1 for the current session.

```
## Session Log

### Session: <YYYY-MM-DD> (current)
**Files touched:** <relative paths from Step 1, grouped by folder>
**Summary:** <2–4 sentences describing what was accomplished, inferred from the files changed and conversation context>
**Outcome:** <one sentence — what state was the work left in>

### Session: <date> (previous)
<carry the previous session entry here verbatim — do not rewrite or summarise it>
```

If first-time initialization (no prior handoff.md), write only the current session entry and add a line: `*No prior session recorded.*`

---

### 4c — Open Items / Next Steps

**Strict rule:** Only include items a coding agent can execute directly in the next session. Apply this filter ruthlessly before writing any item.

**Include ONLY:**
- A specific file/section that was explicitly started this session but not finished
- A concrete technical decision that was deferred mid-session and is blocking further code/doc changes
- A specific file identified as needing a code or content change that was not yet touched

**Reject ALL of the following — do not write them even if they seem helpful:**
- Anything phrased as "consider", "verify", "review", "confirm", "check whether" — these are not coding tasks
- Review or approval steps
- Improvement ideas or feature suggestions not part of this session's scope
- Stakeholder, process, or human-action items
- Anything not directly traceable to unfinished work from this session's file changes

**Test each item before writing it:** Ask — "Can a coding agent open a file and make a change to resolve this?" If no, discard it.

If nothing passes the filter, write: `No open items from this session.`

Format as a checklist:
```
## Open Items / Next Steps
- [ ] <specific file> — <what exactly needs to be done>
```

---

### 4d — Quick Reference *(refresh each session)*

A compact cheat-sheet for the next coding agent. Pull from `AGENTS.md` (read in Step 3) for accuracy.

Cover:
- Key commands (`make test`, `make lint`, `uv run pytest`, etc.)
- Key file locations (main source, config files, notebooks, docs)
- Known gotchas (bare imports vs package imports, thread-safety patterns, Databricks globals, pre-commit hooks)

Limit to ~15 bullet points. Every item must be factually grounded in the actual project files — do not invent paths or commands.

---

## Step 5 — Write the file

Use the `Write` tool to write the complete composed content to `.agent_docs/handoff.md`.

The `Write` tool will create `.agent_docs/` automatically if it does not exist.

Always write the **complete** file — never partial updates.

---

## Step 6 — Confirm to the user

Reply with:
- Path written: `.agent_docs/handoff.md`
- Whether this was a first-time init or an update
- One-line summary of what was captured for this session (files touched + outcome)
- Reminder: "Start your next session with `/init-session` to restore this context."
