---
name: init-session
description: Restore project memory and recent session context from .agent_docs/handoff.md when resuming work, recovering after context reset, or handling a request that assumes missing prior context.
---

# Init Session

Restore enough context to act on the user's request. The handoff contains project-wide memory, current work, and two earlier sessions; load it once rather than rediscovering the project or replaying it into chat.

## Python execution

Run Python scripts with `uv run`, including these helpers and project Python commands. Check `uv --version` before first use if availability is unknown. If uv is missing, explain that this workflow requires it, ask for confirmation to install it, and wait. After approval, use the official installation method appropriate to the system, verify `uv --version`, and continue. Honor existing explicit installation approval. If declined or unavailable, read the handoff with file tools and continue independent work; do not silently fall back to bare Python.

## Restore context

Resolve the helper from this skill's installed directory and pass the target project explicitly:

```bash
uv run /absolute/path/to/init-session/scripts/handoff_read.py --repo-root /absolute/project --format json
```

Read the project snapshot and cumulative learnings as durable memory, then the current session and two preceding sessions for concrete context. The helper returns done work, decisions, verification, and open items as well as historical summaries. Read referenced documents or archived snapshots only when the task needs details absent from the handoff. Avoid loading the archive wholesale.

Use `--open-only` for a request that only asks for the next tasks, or when full project memory is already in context. It is not a substitute for restoring missing context before implementation. A missing handoff is a normal first-session state; begin from the current project and request. A read error is different: report it and use accessible project evidence without inventing history.

The helper reports root rule files without printing their contents. Follow the host's instruction discovery rules, including applicable parent and nested instructions. Read applicable files not already loaded; do not reread known content just because a session started. Keep instruction files authoritative for working rules and use the handoff for project state.

Treat remembered state as historical evidence. Before acting, check the relevant files or status; reconcile contradictions with current evidence and the user's latest instructions. Do not require the user to reconfirm everything recorded in memory.

Give a brief recap if useful: latest outcome, relevant open work, and the next action. Continue work already requested or authorized. Ask what to pick up only when the user asked solely for a recap or there is no clear next task. A context reset does not end or replace the active objective.
