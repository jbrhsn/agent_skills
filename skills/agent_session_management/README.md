# Agent Session Skills

Two paired skills preserve compact project memory across agent sessions and context resets.

| Skill | Purpose |
|---|---|
| [init-session](init-session/README.md) | Restore project facts, recent decisions, verification and open work; continue the user's task |
| [end-session](end-session/README.md) | Save durable project memory, the current session and two previous sessions; create a local Git commit for session changes |

`.agent_docs/handoff.md` is a compact, maintained memory for the entire project. It holds purpose, architecture, important paths, durable decisions and lessons, current project-wide open work, and concrete recent session records. Older recorded snapshots live in `.agent_docs/archive/` and are read only when needed. This preserves useful context without reloading a growing transcript every session.

The agent selects and deduplicates memory; the helpers handle reading, rotation, archiving and writing. Roughly 1,000–2,000 tokens is a useful starting target, not a limit that discards important context. Repeated checkpoints preserve the two previous sessions. Existing four-section handoffs are compatible with the new five-section format.

After saving memory, end-session commits relevant session changes, including at checkpoints, unless the user requests otherwise. The agent handles Git separately from the memory helper, respects ignored memory and unrelated edits, and reports the commit hash or blocker. It does not push automatically.

All Python scripts run through `uv run`. If uv is missing, the agent asks for confirmation before installation, verifies the installation, then proceeds. It can use file tools while installation is pending or declined. Helpers require Python 3.8+ and only the standard library.

Edit canonical skills here and preview distribution with:

```bash
uv run scripts/sync_all.py --dry-run
```

Use the repository's sync workflow to install into supported harnesses. Resolve helper paths from the installed skill directory and use `--repo-root` to select the target project. Keep or share `.agent_docs/` according to project conventions; neither skill changes ignore rules automatically.
