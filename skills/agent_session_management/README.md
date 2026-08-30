# Agent Session Skills

Two paired skills that carry project context across agent sessions in OpenCode, Claude Code, Codex/ChatGPT, Antigravity, IBM Bob, or any harness that loads `SKILL.md` files.

```
end-session/    -> writes .agent_docs/handoff.md when you stop work
init-session/   -> reads it back when you start
```

| Skill | Fires when | Produces |
|---|---|---|
| [**init-session**](./init-session/README.md) | "catch me up", "resume", "where did we leave this", or you start giving instructions that assume context the agent doesn't have | A five-second recap: what last session ended with, open items verbatim, and only the learnings that bear on them |
| [**end-session**](./end-session/README.md) | "wrap up", "done for today", "checkpoint this", or a context compaction is about to land | `.agent_docs/handoff.md`, compacted not appended, plus the outgoing session archived under `.agent_docs/archive/` |

## Install

From this repo, the sync script handles every platform:

```bash
uv run scripts/sync_all.py            # every skill in the repo, all five platforms
```

Or copy both folders into wherever your harness looks for skills:

| Harness | Path |
|---|---|
| Claude Code | `~/.claude/skills/` (per-repo: `<repo>/.claude/skills/`) |
| OpenCode | `~/.config/opencode/skills/` (per-repo: `<repo>/.opencode/skills/`) |
| Codex / ChatGPT | `~/.agents/skills/` |
| Antigravity | `~/.gemini/config/skills/` |
| IBM Bob | `~/.bob/skills/` |

```bash
cp -r end-session init-session ~/.claude/skills/
```

Requires Python 3.8+. No third-party packages.

## What gets created in your repo

```
.agent_docs/
├── handoff.md              # compacted every write — this is what gets read
└── archive/
    └── session-<ts>.md     # full detail of every past session
```

## The design in one line

`handoff.md` is **compacted on every write, never appended to** — Snapshot + deduped Learnings + a 3-5 bullet Last Session + the current session — so its read cost stays roughly flat no matter how many sessions a project accumulates. Everything trimmed goes to `archive/`, where it costs nothing until you deliberately open it.

`init-session` reports which of `AGENTS.md` / `CLAUDE.md` exist but does **not** print them, since Claude Code already auto-loads `CLAUDE.md`; the agent reads them only when they are not already in context.

## Committing

Commit `.agent_docs/handoff.md` if you want handoffs shared across machines or teammates. To keep them local, add to `.gitignore`:

```
.agent_docs/
```

Committing `handoff.md` while ignoring `archive/` is a reasonable middle ground.

## Scripts

Both are usable standalone:

```bash
python init-session/scripts/handoff_read.py --format text     # human-readable recap
python init-session/scripts/handoff_read.py --open-only       # just the next tasks
python end-session/scripts/handoff_write.py --input p.json --dry-run
```

They locate the repo root by walking up for `.git` or `.agent_docs`, so they work from any subdirectory. A missing handoff exits 0 — a first session is not an error.
