# Handoff Log

## Project Summary

`agent_skills` is a curated collection of portable AI-agent skill files (`SKILL.md`) for OpenCode and IBM Bob, plus shareable OpenCode config. It contains 12 skills across four categories: `agent_session_management/` (2), `learning/` (3), `development/` (4), and `content-creation/linkedin/` (3). The top-level `agents/` dir holds an `orchestrator` (primary) + `executor` (subagent) pair (shareable source copies), and the top-level `plugins/` dir holds `token-guard.ts` (source copy). Both dirs have `README.md` files documenting how to wire them into `opencode.json` (added this session). A live `.opencode/` setup mirrors them for in-repo use: `.opencode/agents/`, `.opencode/plugin/token-guard.ts`, and `.opencode/opencode.json` (registers token-guard via the tuple form with `maxOutputChars` 8000; no `agent` block since agents are auto-discovered). NEW this session: the agents + plugins are now also installed to GLOBAL OpenCode scope at `~/.config/opencode/agent/` (`orchestrator.md`, `executor.md`) and `~/.config/opencode/plugin/` (`token-guard.ts`) — note the singular dir names; they are auto-discovered and require no global `opencode.jsonc` edit (the global token-guard runs at its default `maxOutputChars` 4000). `scripts/` holds Python sync scripts that install content to the global config locations. The architecture is file-centric with no build system, CI, or tests — pure content (Markdown/TypeScript) plus Python sync scripts. Each skill's `SKILL.md` frontmatter `name` must match its folder name.

## Session Log

### Session: 2026-07-29 — Global Agents/Plugins Sync + Script Fixes (current)
**Files touched:**

_agents/_
- `agents/README.md` — added an `## opencode.json` section: agents are auto-discovered from the `agent/` dir (no `agent` block needed, matching the repo's own config), plus an optional inline `agent` override snippet and a restart-required note.

_plugins/_
- `plugins/README.md` — expanded the Configuration + Install/usage sections: a complete minimal `opencode.json` (full doc, matching the repo's live file), the tuple-vs-plain-string distinction, default 4000 vs override 8000, and a restart note.

_scripts/_
- `scripts/sync_opencode_agents.py` — CREATED. Syncs `agents/orchestrator.md` + `agents/executor.md` to `~/.config/opencode/agent/` (singular). Supports `--dry-run`, `OPENCODE_AGENTS` env override, excludes README, prints ✓/✗/⚠ + summary, exits nonzero on failure.
- `scripts/sync_opencode_plugins.py` — CREATED. Syncs all `plugins/*.ts` (glob, future-proof; currently just `token-guard.ts`) to `~/.config/opencode/plugin/` (singular). Supports `--dry-run`, `OPENCODE_PLUGINS` env override, excludes README/markdown.
- `scripts/sync_bob_skills.py` — FIXED. Replaced the fragile manual exclusion loop (`item.name.endswith(ext.lstrip("*"))`, applied only at the top level) with a single `shutil.copytree(..., ignore=shutil.ignore_patterns(*EXCLUSIONS))` matching `sync_opencode_skills.py`, so exclusions now apply uniformly at all depths. `SKILLS` list + destination unchanged.
- `scripts/sync_all.py` — UPDATED. Added `sync_opencode_agents.py` + `sync_opencode_plugins.py` to the OpenCode (non-`--bob-only`) path; exit codes wired in; docstring updated.
- `scripts/README.md` — UPDATED. Replaced the stale "19 skills"/deleted-skill list with the correct 12 skills across 4 real categories; added sections for the two new scripts; updated the `sync_all.py` section + verify steps to include `~/.config/opencode/agent/` and `~/.config/opencode/plugin/`.

_global installs_
- `~/.config/opencode/agent/{orchestrator.md,executor.md}` and `~/.config/opencode/plugin/token-guard.ts` — created via the new sync scripts (verified diff-identical to repo source).

**Summary:** Documented the `opencode.json` wiring in both the `agents/` and `plugins/` READMEs; created two new global-scope OpenCode sync scripts (agents + plugins) and wired them into `sync_all.py`; fixed a real fragility bug in `sync_bob_skills.py`'s exclusion logic; refreshed the stale `scripts/README.md`; and installed the agents + plugins to global OpenCode scope. NOTE: the `tarfile` bug claimed in the prior handoff was ALREADY gone — both skill scripts already used `shutil.copytree`, so no `tarfile` fix was needed.

**Outcome:** Agents + plugins now live in global OpenCode config and verified diff-identical to source; all 5 sync scripts are `py_compile`-clean and pass `--dry-run` (2 agents, 1 plugin, 12 skills each). Nothing committed to git this session.

### Session: 2026-07-29 — Agents/Plugins Docs + opencode.json (previous)
**Files touched:**
- `plugins/README.md` — created. Documents the top-level `plugins/` dir and its `token-guard.ts` plugin (head+tail truncation of `bash`/`webfetch` output, blocking whole-file/stream dump commands like `cat`/`tail`, terse compaction-summary prompt; configurable `maxOutputChars`, default 4000).
- `agents/README.md` — created. Documents the top-level `agents/` dir: the `orchestrator` (primary; edit/bash denied; delegates all work to executor subagents in parallel) + `executor` (subagent; edit allowed, dangerous bash gated to ask/deny, `steps: 20`; implements-then-verifies a unit of work) pair and how they work together.
- `.opencode/opencode.json` — created. Minimal valid opencode project config: `$schema` + a `plugin` array registering `./.opencode/plugin/token-guard.ts` via the tuple form with `{ "maxOutputChars": 8000 }`. No `agent` block (orchestrator/executor auto-discovered from `.opencode/agents/`).

**Summary:** Added README documentation for the repo's two new shareable OpenCode-config directories — top-level `agents/` (orchestrator + executor pair) and `plugins/` (`token-guard.ts`) — bringing them up to the same documented standard as the skills. Also created `.opencode/opencode.json` to wire the live in-repo setup, registering `token-guard.ts` via the tuple form with `maxOutputChars` overridden to 8000; the agents remain auto-discovered from `.opencode/agents/` so no `agent` block was needed. The top-level dirs are the source copies; `.opencode/` holds the live installed copies used within this repo.

**Outcome:** Two new READMEs and a valid `.opencode/opencode.json` are in place; config verified as valid JSON. Nothing committed to git yet this session.

## Open Items / Next Steps

- [ ] `content-creation/linkedin` skills — not yet synced to `~/.bob/skills/`; run `python3 scripts/sync_bob_skills.py` (or `sync_all.py`) to install them to Bob (they were only manually copied to `~/.config/opencode/skills/` previously).

## Quick Reference

- **Root skill folders:** `agent_session_management/` (2 skills), `learning/` (3), `development/` (4), `content-creation/linkedin/` (3: `linkedin-post-writer`, `linkedin-image-prompts`, `linkedin-post-reviewer`).
- **Top-level `agents/` dir:** the `orchestrator` (primary) + `executor` (subagent) pair — shareable source copies; its `README.md` now documents `opencode.json` wiring (agents auto-discovered from the `agent/` dir, optional inline `agent` override).
- **Top-level `plugins/` dir:** `token-guard.ts` (truncates `bash`/`webfetch` output, blocks whole-file/stream dumps, compaction-summary prompt) — shareable source copy; its `README.md` now documents `opencode.json` wiring.
- **`.opencode/opencode.json`:** registers `./.opencode/plugin/token-guard.ts` via the tuple form with `{ "maxOutputChars": 8000 }`; no `agent` block (agents auto-discovered from `.opencode/agents/`).
- **Global agent/plugin installs (NEW):** agents + plugins are now ALSO installed globally at `~/.config/opencode/agent/` (`orchestrator.md`, `executor.md`) + `~/.config/opencode/plugin/` (`token-guard.ts`) — singular dir names, auto-discovered, no global config edit; global token-guard runs at default `maxOutputChars` 4000.
- **Sync scripts:** `sync_opencode_skills.py`, `sync_bob_skills.py`, `sync_opencode_agents.py`, `sync_opencode_plugins.py`, and `sync_all.py` (runs all OpenCode syncs + Bob).
- **`sync_all.py` flags:** `--dry-run`, `--opencode-only`, `--bob-only`.
- **Env overrides:** `OPENCODE_SKILLS`, `BOB_SKILLS`, `OPENCODE_AGENTS`, `OPENCODE_PLUGINS`.
- **Sync scripts are now all working:** the `tarfile` bug was already gone (both skill scripts use `shutil.copytree`); the `sync_bob_skills.py` exclusion bug was fixed this session.
- **opencode loads config only at startup** — restart opencode after changing any config, agent, or plugin file for changes to take effect.
- **Skill template:** every skill needs `SKILL.md` (frontmatter `name` must match folder name) + `README.md`.
- **LinkedIn skill conventions:** each of the 3 `content-creation/linkedin/` skills reads a user-supplied source file and writes its output (`linkedin_post.md`, `image_prompts.md`, `linkedin_post_revised.md`) **in that same directory** — never to a fixed folder.
- **Global config locations:** OpenCode = `~/.config/opencode/skills/`, Bob = `~/.bob/skills/`.
- **Session continuity:** use `/init-session` at session start and `/end-session` at session end to restore/save context to `.agent_docs/handoff.md`.
- **No AGENTS.md exists** at the repo root — this handoff file is the only persistent cross-session context document.
