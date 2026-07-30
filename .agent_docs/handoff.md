# Handoff Log

## Project Summary

`agent_skills` is a curated OpenCode agent-skills repository: a catalog of reusable, portable AI-agent skills (`SKILL.md` + `README.md` per skill) plus shareable agent and plugin definitions, with Python sync scripts that install everything into OpenCode (and IBM Bob) config dirs. Skills live under a categorized `skills/` tree: `skills/agent_session_management/` (2: init-session, end-session), `skills/content-creation/linkedin/` (2: linkedin-post-writer, linkedin-image-prompts), `skills/content-creation/Medium/` (empty), `skills/development/` (4: lean-coder, project-planner, repo-docs-publisher, ui-ux-designer), and `skills/learning/` (3: author-chapter, create-learning-repo, generate-practice-exam) — **11 skills total**. Agents live under `agents/orchestrator_mode_agents/` (`orchestrator.md` = primary/plan-only, `executor.md` = subagent that does+verifies a unit). Plugins live under `plugins/token_saving/` (`token-guard.ts`). `scripts/` holds five Python sync scripts (skills, agents, plugins to OpenCode; skills to Bob; `sync_all.py` orchestrates). The architecture is file-centric — pure Markdown/TypeScript content plus Python sync tooling, no build/CI/tests. Each `SKILL.md` frontmatter `name` must equal its leaf folder name; skills install by leaf name only (category path stripped). Global skills path: `~/.config/opencode/skills/`. No root `AGENTS.md`; this handoff is the sole cross-session context.

## Session Log

### Session: 2026-07-30 (current)
**Files touched:**

_agents/_
- `agents/orchestrator_mode_agents/{orchestrator.md,executor.md}` — read/understood as the delegation model (orchestrator plans-only/no edit-bash; executor does+verifies a unit, terse report) that all skill workflows were rewritten against.

_skills/ (content-creation/linkedin)_
- Merged `linkedin-post-reviewer` INTO `linkedin-post-writer` (one skill, two paths: WRITE + REVIEW/REFINE, shared 5-dimension rubric defined once); deleted the `linkedin-post-reviewer/` dir.
- `linkedin-image-prompts/` (SKILL.md + README.md) — updated cross-references to the merged writer skill.

_skills/ (all 11 SKILL.md rewritten to the delegation model)_
- Rewrote every SKILL.md so each workflow uses discrete units (Goal/scope, Inputs, Do, Self-verify, Report contract) plus explicit "STOP GATE (hand back)" markers: linkedin-post-writer, linkedin-image-prompts, lean-coder, project-planner, ui-ux-designer, repo-docs-publisher, create-learning-repo, author-chapter, generate-practice-exam, init-session, end-session. Several `reference/`/`references/` files had stale "Phase N" cross-refs updated to the new unit numbering.

_scripts/ + docs_
- `scripts/sync_opencode_skills.py`, `scripts/sync_bob_skills.py` — SKILLS lists updated 12→11 (removed the reviewer entry).
- `README.md`, `scripts/README.md` — skill count and cross-references updated 12→11.

_global installs_
- Synced all 11 skills into `~/.config/opencode/skills/` via `scripts/sync_opencode_skills.py`; removed the obsolete `linkedin-post-reviewer` from the global dir (12→11 there).

**Summary:** Large skills-repo refactor. Consolidated the two LinkedIn skills into one dual-path skill, then rewrote all 11 SKILL.md workflows to follow the orchestrator/executor delegation model (unit contracts + STOP GATEs), fixing stale reference cross-refs. Propagated the 12→11 skill-count change through both sync scripts and both READMEs, and pushed the result to the global OpenCode skills dir.

**Outcome:** Docs-only repo; verified by inspection + YAML frontmatter parse checks + a repo-wide grep confirming every SKILL.md carries the unit contracts (11/11). Global dir and sync script both show exactly 11 skills with the reviewer removed. No known unfinished edits; nothing committed to git.

### Session: 2026-07-29 (previous)
**Files touched:**

_scripts/_
- `scripts/sync_opencode_skills.py` — prefixed all 12 `SKILLS` entries with `skills/` to match the new layout.
- `scripts/sync_bob_skills.py` — same 12-entry `skills/` prefix change.
- `scripts/sync_opencode_agents.py` — repointed the agents source subdir from `agents/` to `agents/orchestrator_mode_agents/` (both the `Source:` print line and the loop `source_path`); destination unchanged (`~/.config/opencode/agent`).
- `scripts/sync_opencode_plugins.py` — repointed `plugins_dir` from `plugins/` to `plugins/token_saving/`; destination unchanged (`~/.config/opencode/plugin`).
- `scripts/README.md` — updated agent paths to `agents/orchestrator_mode_agents/{orchestrator,executor}.md` and the plugin glob to `plugins/token_saving/*.ts`; skill count (12) and destinations unchanged.

_skills/ (moved + LinkedIn edits)_
- Skill categories relocated under `skills/`; the three `skills/content-creation/linkedin/` skills (`linkedin-post-writer`, `linkedin-image-prompts`, `linkedin-post-reviewer`) were modified by the user, then synced to OpenCode.

**Summary:** Adapted all five sync scripts + `scripts/README.md` to the user's folder reorg (skills under `skills/`, agents under `agents/orchestrator_mode_agents/`, plugins under `plugins/token_saving/`). Then performed a real (non-dry-run) OpenCode skills sync to push the user's modified LinkedIn skills to `~/.config/opencode/skills/`.

**Outcome:** All scripts are `py_compile`-clean; `sync_all.py --dry-run` reports 12 OpenCode skills / 2 agents / 1 plugin / 12 Bob skills with 0 skipped. LinkedIn skills synced to OpenCode and verified diff-identical to source. Nothing committed to git; Bob was NOT re-synced this session.

## Open Items / Next Steps

No open items from this session.

## Quick Reference

- **Skill folders (all under `skills/`, 11 total):** `skills/agent_session_management/` (init-session, end-session), `skills/content-creation/linkedin/` (linkedin-post-writer, linkedin-image-prompts), `skills/content-creation/Medium/` (empty), `skills/development/` (lean-coder, project-planner, repo-docs-publisher, ui-ux-designer), `skills/learning/` (author-chapter, create-learning-repo, generate-practice-exam).
- **`linkedin-post-writer` is now dual-path:** WRITE (draft → `linkedin_post.md`) and REVIEW/REFINE (score + refine → `linkedin_post_revised.md`); the standalone `linkedin-post-reviewer` no longer exists.
- **All 11 SKILL.md workflows follow the delegation model:** discrete units with Goal/Inputs/Do/Self-verify/Report + explicit "STOP GATE (hand back)" markers.
- **Agents dir:** `agents/orchestrator_mode_agents/{orchestrator.md,executor.md}`; `agents/README.md` documents `opencode.json` wiring (auto-discovered from the `agent/` dir).
- **Plugins dir:** `plugins/token_saving/token-guard.ts`; `plugins/README.md` documents wiring.
- **Sync scripts:** `scripts/sync_opencode_skills.py`, `scripts/sync_bob_skills.py`, `scripts/sync_opencode_agents.py`, `scripts/sync_opencode_plugins.py`, and `scripts/sync_all.py` (runs all OpenCode syncs + Bob).
- **Sync all skills to OpenCode:** `python3 scripts/sync_opencode_skills.py` (add `--dry-run` to preview).
- **`sync_all.py` flags:** `--dry-run`, `--opencode-only`, `--bob-only`.
- **Env overrides:** `OPENCODE_SKILLS`, `BOB_SKILLS`, `OPENCODE_AGENTS`, `OPENCODE_PLUGINS`.
- **Syntax check:** `python3 -m py_compile scripts/*.py` (no test/lint suite in repo).
- **`SKILLS` list format:** full path from repo root, e.g. `skills/development/lean-coder`; the leaf segment becomes the installed folder name. Update these lists when adding/removing skills.
- **Global config locations:** OpenCode skills `~/.config/opencode/skills/`, agents `~/.config/opencode/agent/` (singular), plugins `~/.config/opencode/plugin/` (singular); Bob skills `~/.bob/skills/`.
- **Gotcha — sync does not auto-prune:** removing a skill from the repo does NOT delete it from the global dir; delete the obsolete global folder manually (as done for `linkedin-post-reviewer`).
- **Gotcha — restart required:** opencode loads config/agents/plugins/skills only at startup; restart after any change. Skills are auto-discovered from the `skills/` (or `agent/`) dir.
- **Skill template:** every skill needs `SKILL.md` (frontmatter `name` must match leaf folder name) + `README.md`.
- **No AGENTS.md** at the repo root — this handoff file is the only persistent cross-session context.
- **Session continuity:** `/init-session` at start, `/end-session` at end (reads/writes `.agent_docs/handoff.md`).
