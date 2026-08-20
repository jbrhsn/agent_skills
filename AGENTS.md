# AGENTS.md — agent_skills Repository Guide

This file is **not committed** (in `.gitignore`). It's for your session only.

---

## 1. Overview

**agent_skills** is a curated collection of 13 reusable workflow skills and agent definitions for AI coding agents on OpenCode, IBM Bob, and Google Antigravity. Edit and test skills locally in this repo, then sync to all three platforms via Python scripts. This is a distribution repo only — no per-project `opencode.json`.

---

## 2. Architecture

- **13 skills** in 4 categories: agent_session_management (2), learning (2), development (4), content-creation (5)
- **2 agent definitions** in `agents/orchestrator_mode_agents/`: `orchestrator.md` (primary, plans & delegates) and `executor.md` (subagent, implements & verifies)
- **6 sync scripts** in `scripts/`: master orchestrator `sync_all.py`, plus per-platform scripts
- **No per-project opencode.json** — agents auto-discover from `agents/` directory; skills from `skills/`

---

## 3. Skill Directory Structure

All skills live under `skills/{category}/{skill-name}/`:
- `SKILL.md` — agent-facing prompt with YAML frontmatter (`---` headers: available_skills, references, etc.)
- `README.md` — human-readable guide (optional but recommended)
- `reference/` or `references/` — templates, checklists, examples (optional)

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

See `agents/README.md` for full safety model and permission rules.

---

## 5. Sync Workflow

**Typical flow:**

1. Edit a skill in `skills/{category}/{skill-name}/SKILL.md` (or `README.md`)
2. Run `python3 scripts/sync_all.py --dry-run` to preview
3. Run `python3 scripts/sync_all.py` to sync to all platforms
4. Optional: `--opencode-only`, `--bob-only`, or `--antigravity-only` (mutually exclusive)

**Individual script sync:**
```bash
python3 scripts/sync_opencode_skills.py     # OpenCode skills only
python3 scripts/sync_opencode_agents.py     # OpenCode agents only  
python3 scripts/sync_bob_skills.py          # IBM Bob skills only
python3 scripts/sync_antigravity_skills.py  # Antigravity skills only
```

**Environment overrides:**
- `OPENCODE_SKILLS=~/.config/opencode/skills`
- `OPENCODE_AGENTS=~/.config/opencode/agent` (note: singular)
- `BOB_SKILLS=~/.bob/skills`
- `ANTIGRAVITY_SKILLS=~/.gemini/config/skills`

---

## 6. Destination Mappings

Where synced files land on each platform:

| Target | Skills Destination | Agents Destination |
|---|---|---|
| **OpenCode** | `~/.config/opencode/skills/{skill-name}/` | `~/.config/opencode/agent/{agent-name}.md` |
| **IBM Bob** | `~/.bob/skills/{skill-name}/` | — (not synced) |
| **Antigravity** | `~/.gemini/config/skills/{skill-name}/` | — (not synced) |

**Agents sync to OpenCode only** (orchestrator.md, executor.md → `~/.config/opencode/agent/`)

---

## 7. Important Constraints

**Antigravity destination caution:**
- `~/.gemini/config/` is **not skills-only**. It also contains `AGENTS.md`, `config.json`, `mcp_config.json`, `projects/`, `sidecars/`.
- **Never** delete or clear the entire `~/.gemini/config/` or `~/.gemini/config/skills/` directory.
- Only remove or replace individual skill folders within `skills/`.

**Excluded from sync** (saved ~2.5GB of artifacts):
- `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `node_modules/`, `.git/`, `.DS_Store`, `*.egg-info/`, `dist/`, `build/`, `tests/`

**Contributing:**
- Not open for contributions yet (solo curated collection)
- Issues welcome; see `CONTRIBUTING.md`

**Session-only files** (in `.gitignore`):
- `AGENTS.md` (this file) — your session guide, never committed
- `CLAUDE.md`, `.opencode/`, `.cursor/`, `.cursorrules`, `.github/copilot-instructions.md`

---

## 8. Typical Tasks & Commands

**Add a new skill:**
```bash
mkdir -p skills/{category}/{new-skill-name}
# Create SKILL.md with YAML frontmatter and prompt
# Create README.md with human-readable guide
# Add optional reference/ or references/ subdirectory
python3 scripts/sync_all.py --dry-run
python3 scripts/sync_all.py
```

**Test a skill locally before syncing:**
```bash
cp -r skills/{category}/{skill-name} ~/.config/opencode/skills/
# Test in OpenCode or project
```

**Verify sync completed:**
```bash
ls ~/.config/opencode/skills/ && ls ~/.bob/skills/ && ls ~/.gemini/config/skills/
```

**See what will be synced without applying:**
```bash
python3 scripts/sync_all.py --dry-run
```

**List all 14 skills by category:**
```bash
find skills -name "SKILL.md" | sed 's|.*/skills/||' | sed 's|/SKILL.md||' | sort
```

---

**Generated:** Session reference. For permanent docs, see `README.md`, `agents/README.md`, `scripts/README.md`.
