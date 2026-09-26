# init-session

Restores project memory, the latest work, and two previous sessions from `.agent_docs/handoff.md`. Pair with [end-session](../end-session/README.md). Use when resuming a project, recovering context, or handling a request that assumes missing prior knowledge.

Follow [SKILL.md](SKILL.md) for the workflow. The agent gives a brief relevant recap and continues authorized work; loading context does not require an extra approval round.

```bash
uv run --python /absolute/project/.venv/bin/python python /absolute/path/to/init-session/scripts/handoff_read.py --repo-root /absolute/project --format json
uv run --python /absolute/project/.venv/bin/python python /absolute/path/to/init-session/scripts/handoff_read.py --repo-root /absolute/project --format text
uv run --python /absolute/project/.venv/bin/python python /absolute/path/to/init-session/scripts/handoff_read.py --repo-root /absolute/project --open-only
```

Resolve the script from the installed skill location and run it through the target project's `.venv` with `uv run`. The helper finds a project root by walking up for `.git` or `.agent_docs` when `--repo-root` is omitted. It requires Python 3.8+ via uv and no third-party libraries. If uv is absent, request confirmation before installing it; file tools can read the memory without running Python.

JSON includes `snapshot`, `learnings`, `previous_session`, `last_session`, `current_session`, and `additional_memory`. Historical sessions are Markdown strings so both summaries and concrete legacy records survive. Current session includes date, focus, done work, decisions, verification, open items and completed checkboxes. Text output presents the same working context. `--open-only` selects current open tasks; use it when full memory is already known or the user only wants the task list.

The helper reports root instruction-file paths and approximate token costs without injecting their contents. The agent follows applicable instruction discovery, avoids reading files already loaded, and checks current project evidence before acting on historical state. Archives are counted, not loaded automatically.

A missing handoff is normal and exits 0. An unreadable handoff is reported as an error rather than mistaken for a fresh project. Legacy handoffs without Previous Session remain readable. Project-wide open work is maintained by the writer's agent, not inferred by this reader from older sessions.
