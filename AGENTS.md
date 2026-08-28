# AGENTS.md — agent_skills Repository Guide

Working guide for agents operating in this repo. Committed — keep it accurate.

---

## 1. Overview

**agent_skills** is a curated collection of reusable workflow skills and agent definitions for AI coding agents on OpenCode, IBM Bob, Google Antigravity, and Claude Code. Edit and test skills locally in this repo, then sync to all platforms via Python scripts. This is a distribution repo only — no per-project `opencode.json`.

---

## 2. Architecture

- **11 skills** in 4 categories: agent_session_management (2), learning (2), development (2), content-creation (5)
- **3 base agent definitions**: `agents/orchestrator_mode_agents/` holds `orchestrator.md` (primary, plans & delegates) and `executor.md` (subagent, implements & verifies); `agents/ask_mode_agents/` holds `ask.md` (primary, read-only)
- **1 optional plugin** in `plugins/`: `search-internet` (OpenCode only, opt-in via `--plugins`)
- **Sync scripts** in `scripts/`: master `sync_all.py`, per-platform scripts, plus `plugins.py` (composition engine) and `common.py` (shared helpers)
- **No per-project opencode.json** — agents auto-discover from `agents/`; skills from `skills/`; plugins from `plugins/*/plugin.json`

---

## 3. Skill Directory Structure

All skills live under `skills/{category}/{skill-name}/`:
- `SKILL.md` — agent-facing prompt with YAML frontmatter (`name`, `description`)
- `README.md` — human-readable guide (optional but recommended)
- `references/`, `assets/`, `scripts/` — optional: guides the skill loads on demand,
  templates it writes from, stdlib-only Python it runs

Example: `skills/development/lean-coder/SKILL.md`

---

## 4. Agent Definitions

**Orchestrator** (`agents/orchestrator_mode_agents/orchestrator.md`):
- Mode: `primary` (main entry point)
- Never edits files, never runs bash — only reads, plans, and delegates
- Parallelizes independent work to executor subagents (≤4 concurrent)
- Verifies each executor's self-contained summary before accepting

**Executor** (`agents/orchestrator_mode_agents/executor.md`):
- Mode: `subagent` (implements work units)
- Has edit + bash access; gates dangerous commands (`rm -rf`, `git push`, etc.) behind `ask`
- Implements, runs tests/builds, verifies itself, reports terse summary
- Never pastes raw logs; only structured result (files changed, verification type, pass/fail)
- Mandated to load the `lean-coder` skill before writing, editing, reviewing, or debugging code

**Ask** (`agents/ask_mode_agents/ask.md`):
- Mode: `primary` (read-only entry point)
- No edit, bash, or delegation — searches and reads, cites `path/to/file:line`

See `agents/README.md` for the full safety model and permission rules.

---

## 5. Sync Workflow

**Always run via `uv run`** — the scripts carry PEP 723 headers (they need `pyyaml`).

**Typical flow:**

1. Edit a skill in `skills/{category}/{skill-name}/SKILL.md` (or `README.md`)
2. Run `uv run scripts/sync_all.py --dry-run` to preview
3. Run `uv run scripts/sync_all.py --verify` to sync and verify SHA-256 parity
4. Optional: `--opencode-only`, `--bob-only`, `--antigravity-only`, or `--claude-only` (mutually exclusive)

**Plugins (OpenCode only, opt-in):**
```bash
uv run scripts/sync_all.py --list-plugins                       # what's available
uv run scripts/sync_all.py --plugins search-internet --verify   # install + assert resolved config
uv run scripts/sync_all.py                                      # omit flag = uninstall, files pruned
```
`--plugins` drives both the runtime file and the agent overlays — never install one
without the other (see §7). `--verify` shells out to `opencode debug agent` and checks
each agent's resolved permissions match what was composed.

**Individual script sync:**
```bash
uv run scripts/sync_opencode_skills.py       # OpenCode skills
uv run scripts/sync_opencode_agents.py       # OpenCode agents (accepts --plugins, --verify)
uv run scripts/sync_opencode_plugins.py      # OpenCode plugin runtime (accepts --plugins)
uv run scripts/sync_claude_skills.py         # Claude Code skills
uv run scripts/sync_claude_agents.py         # Claude Code subagents (executor only, translated)
uv run scripts/sync_antigravity_skills.py    # Antigravity skills
uv run scripts/sync_antigravity_agents.py    # Antigravity ~/.gemini/config/AGENTS.md (full overwrite)
uv run scripts/sync_bob_skills.py            # IBM Bob skills
```

**Inspect a composed agent without writing anything:**
```bash
uv run scripts/sync_opencode_agents.py --plugins search-internet --print-composed orchestrator
```

**Environment overrides:**
- `OPENCODE_SKILLS=~/.config/opencode/skills`
- `OPENCODE_AGENTS=~/.config/opencode/agent` (note: singular)
- `OPENCODE_PLUGINS=~/.config/opencode/plugin` (note: singular)
- `CLAUDE_SKILLS=~/.claude/skills`
- `CLAUDE_AGENTS=~/.claude/agents`
- `ANTIGRAVITY_SKILLS=~/.gemini/config/skills`
- `ANTIGRAVITY_AGENTS=~/.gemini/config/AGENTS.md` (a file, not a directory)
- `BOB_SKILLS=~/.bob/skills`

> OpenCode's docs say `agents/` and `plugins/` (plural), but 1.18.23 reads the
> **singular** paths above. Verified empirically — don't "fix" these.

---

## 6. Destination Mappings

Where synced files land on each platform:

| Target | Skills | Agents | Plugins |
|---|---|---|---|
| **OpenCode** | `~/.config/opencode/skills/{skill}/` | `~/.config/opencode/agent/{agent}.md` — all 3, composed | `~/.config/opencode/plugin/{file}.js` |
| **Claude Code** | `~/.claude/skills/{skill}/` | `~/.claude/agents/executor.md` — translated | — |
| **Antigravity** | `~/.gemini/config/skills/{skill}/` | `~/.gemini/config/AGENTS.md` — one flat file | — |
| **IBM Bob** | `~/.bob/skills/{skill}/` | — | — |

**Plugins are OpenCode-only.** OpenCode agents are composed at sync time: base agents
from `agents/*/*.md`, plus overlays from any plugin named in `--plugins`. Composed
files exist only at the destination — never written back into the repo.

**Claude Code** gets only `mode: subagent` agents (today, just `executor`); its own
top-level session is the `primary` equivalent, governed by `CLAUDE.md`. Its subagent
frontmatter has no per-command bash permission map, so `executor`'s allow/ask/deny
gates become a plain-language note in the body.

**Antigravity** has no per-mode agent files — `agents/ANTIGRAVITY_AGENTS.md` is a
separate hand-authored source (not a translation) copied verbatim, overwriting the
destination in full.

**Bob** gets skills only — its custom-agent config format isn't publicly documented
enough to target confidently.

---

## 7. Important Constraints

**Shared config destination caution:**
- `~/.gemini/config/` and `~/.claude/` are **not** skills-only. They contain settings, session states, history, projects, and other tool configs.
- **Never** delete or clear the entire `~/.gemini/config/` or `~/.claude/` directories.
- Only remove or replace individual skill folders within `skills/`.
- Plugin/agent pruning is manifest-scoped: each destination carries a
  `.agent_skills_manifest.json` listing only files this tooling wrote, and prune touches
  nothing else. Don't replace this with a directory wipe.

**Plugin tools are allow-by-default:**
- A tool registered by an OpenCode plugin is available to **every** agent unless a
  permission explicitly denies it (verified on 1.18.23).
- So a plugin's runtime file and its agent overlays must install together — otherwise
  the orchestrator silently gains a tool it was designed to delegate instead.
- `--plugins` enforces this by driving both syncs; the standalone plugin script warns.
- Two plugins setting the same frontmatter key to different values is a **hard error**,
  not a last-one-wins merge. Resolve it in the overlays.

**Excluded from sync** (`EXCLUSIONS` in `scripts/common.py`):
- `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `node_modules/`, `.git/`, `.DS_Store`, `*.egg-info/`, `dist/`, `build/`

**Contributing:**
- Not open for contributions yet (solo curated collection)
- Issues welcome; see `CONTRIBUTING.md`

**Skills are referenced by name, never by path:**
- Anything that gets synced out (agent files, `ANTIGRAVITY_AGENTS.md`) must say
  "load the `lean-coder` skill", not `skills/development/lean-coder/SKILL.md`.
- Skills flatten to `skills/{name}/` at every destination — the category subfolder
  is gone, and the destination tree is unrelated to whatever project the agent runs in.

**Local-only files** (in `.gitignore`):
- `.agent_docs/`, `.opencode/`, `.cursor/`, `.cursorrules`, `.github/copilot-instructions.md`

---

## 8. Typical Tasks & Commands

**Add a new skill:**
```bash
mkdir -p skills/{category}/{new-skill-name}
# Create SKILL.md with YAML frontmatter and prompt
# Create README.md with human-readable guide
# Add optional reference/ or references/ subdirectory
uv run scripts/sync_all.py --dry-run
uv run scripts/sync_all.py
```

**Add a new plugin:** see `plugins/README.md` — write `plugin.json`, put the tool in
`plugin/`, and add an overlay per base agent whose permissions must change.

**Test a skill locally before syncing:**
```bash
cp -r skills/{category}/{skill-name} ~/.config/opencode/skills/
# Test in OpenCode or project
```

**Verify sync completed:**
```bash
uv run scripts/sync_all.py --verify   # SHA-256 parity check across all platforms
opencode debug agent orchestrator     # resolved permissions + tools map
```

**See what will be synced without applying:**
```bash
uv run scripts/sync_all.py --dry-run
```

**List all skills by category:**
```bash
find skills -name "SKILL.md" | sed 's|.*/skills/||' | sed 's|/SKILL.md||' | sort
```

---

**Generated:** Session reference. For permanent docs, see `README.md`, `agents/README.md`, `scripts/README.md`.
