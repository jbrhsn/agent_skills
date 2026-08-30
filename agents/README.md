# Agents

Canonical per-mode agent definitions — a Markdown file with YAML frontmatter (mode + permissions) followed by the agent's prompt body, written for **OpenCode** and always synced there.

| Agent | Mode | Role |
|---|---|---|
| [**orchestrator**](./orchestrator_mode_agents/orchestrator.md) | `primary` | Decomposes a request and delegates every unit of work to executors |
| [**executor**](./orchestrator_mode_agents/executor.md) | `subagent` | Implements, runs, and verifies one unit end-to-end |
| [**ask**](./ask_mode_agents/ask.md) | `primary` | Read-only conversational exploration |

## The safety model

The orchestrator/executor pair splits power deliberately:

- **orchestrator** — `edit: deny`, `bash: deny`, `task: {"*": deny, executor: allow}`. It plans and delegates, nothing else. It may `read`/`grep`/`glob` enough to scope work, but not read files end-to-end — an executor will read what it needs.
- **executor** — `edit: allow`, `bash: {"*": allow}` with destructive patterns behind `ask` (`rm -rf`, `git push`, `git reset --hard`, `git clean`, `git checkout -- `/`git restore`, `git branch -D`, `curl|`/`wget|`, `| sh`/`| bash`, `sudo`, `chmod -R`, `dd`, `mkfs`) and a fork bomb at `deny`. It also stays inside its assigned file scope so parallel executors can't collide.
- **ask** — read-only end to end: no edit, no bash, no delegation. When asked to act, it says so plainly and offers what it *can* do, pointing at orchestrator mode for the rest.

Each has `steps: 20` (`ask`: 10).

## How they work together

1. The orchestrator splits the request into **independent units** — fewer, larger units beat many small ones; split further only when it buys real parallelism.
2. It dispatches them to executors — **in parallel** when independent (≤4 concurrent, in waves beyond that), sequentially when dependent. Every task is self-contained: goal, the files already identified while planning, an explicit scope boundary that never overlaps a concurrent executor, and how to verify.
3. Each executor implements its unit, **verifies it itself** (tests, build, lint, or diff inspection — by inspection against the stated requirements if the repo has no tooling), and returns **only** a terse summary: files changed, what was verified and the result, pass/fail. Never raw logs, output, or diffs.
4. On failure the orchestrator sends a targeted follow-up describing the specific problem, not the whole log.

Neither ever reports "done" without an executor having actually checked. An executor approaching its step limit reports honest partial progress instead.

Coding work is gated on the [`lean-coder`](../skills/development/lean-coder/) skill: `executor.md` mandates loading it before writing, editing, reviewing, or debugging code. Skills are referenced **by name**, never by repo path — the path doesn't exist once the agent file is synced elsewhere.

## Cross-platform

| Platform | What it gets |
|---|---|
| **OpenCode** | All three, verbatim, plus any plugin overlays → `~/.config/opencode/agent/` |
| **Claude Code** | `executor.md` only, translated to Claude Code's subagent schema → `~/.claude/agents/`. `orchestrator`/`ask` are `mode: primary`, and Claude Code's own top-level session is that equivalent, governed by `CLAUDE.md` |
| **Antigravity** | [`ANTIGRAVITY_AGENTS.md`](./ANTIGRAVITY_AGENTS.md) — a separate hand-authored source, *not* a translation of the three above. Antigravity has one global instructions file per workspace, so it carries the same execution/verification standards as standing rules → `~/.gemini/config/AGENTS.md` |
| **IBM Bob** | Not synced — its custom-agent config format isn't documented publicly enough to target confidently |
| **Codex / ChatGPT** | Not synced — its subagents use TOML config layers rather than this Markdown agent schema, and repository guidance is discovered from `AGENTS.md`. Skills only |

## Install

```bash
uv run scripts/sync_opencode_agents.py             # → ~/.config/opencode/agent/
uv run scripts/sync_opencode_agents.py --dry-run   # preview
uv run scripts/sync_all.py                         # all platforms, agents + skills
```

Set `OPENCODE_AGENTS` to target somewhere else (e.g. a per-project `.opencode/agent/`). `README.md` is never synced. See [`scripts/README.md`](../scripts/README.md).

### Plugin overlays

These three are the **base** definitions and are what syncs by default. A plugin (see [`plugins/`](../plugins/)) may ship *overlays* extending them — adding a permission and appending a `## Capability: <plugin>` section — plus net-new agents of its own. Overlays merge in memory at sync time; files in this directory are never modified.

```bash
uv run scripts/sync_opencode_agents.py --plugins search-internet --verify
uv run scripts/sync_opencode_agents.py --plugins search-internet \
    --print-composed orchestrator     # inspect the merged result, write nothing
```

A plugin's tool is available to **every** agent unless explicitly denied, so an overlay that denies it on `orchestrator` is part of the safety model above — which is why runtime files and overlays always install together.

### Manual copy

```bash
cp agents/orchestrator_mode_agents/orchestrator.md \
   agents/orchestrator_mode_agents/executor.md \
   agents/ask_mode_agents/ask.md \
   ~/.config/opencode/agent/      # or .opencode/agent/ for one project
```

## opencode.json

Agents in `agent/` are **auto-discovered** — no `opencode.json` entry is needed. Add an `agent` block only to override an auto-discovered agent or define one inline:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "executor": { "mode": "subagent", "permission": { "edit": "allow", "bash": "ask" } }
  }
}
```

> **Restart required.** OpenCode loads config only at startup — restart after changing any agent file or `opencode.json`.
