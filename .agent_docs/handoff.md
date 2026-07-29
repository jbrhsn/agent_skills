# Handoff Log

## Project Summary

`agent_skills` is a curated collection of portable AI-agent skill files (`SKILL.md`) for OpenCode and IBM Bob, plus shareable OpenCode agents/plugins config and Python sync scripts. It was REORGANIZED this session: all skill categories now live under a top-level `skills/` dir — `skills/agent_session_management/` (2), `skills/content-creation/linkedin/` (3), `skills/content-creation/Medium/` (empty, no skills yet), `skills/development/` (4), `skills/learning/` (3) = 12 skills total. Agents now live under `agents/orchestrator_mode_agents/` (`orchestrator.md` + `executor.md`; `agents/README.md` stays at the top of `agents/`). Plugins now live under `plugins/token_saving/` (`token-guard.ts`; `plugins/README.md` stays at the top of `plugins/`). `scripts/` holds five Python sync scripts that install content to global config locations (OpenCode `~/.config/opencode/{skills,agent,plugin}`, Bob `~/.bob/skills`). The architecture is file-centric with no build system, CI, or tests — pure content (Markdown/TypeScript) plus Python sync scripts. Each skill's `SKILL.md` frontmatter `name` must match its leaf folder name. Skills are copied to global config by leaf folder name only (category path is stripped). There is NO AGENTS.md at the repo root — this handoff is the only persistent cross-session context.

## Session Log

### Session: 2026-07-29 (current)
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

### Session: 2026-07-29 — Global Agents/Plugins Sync + Script Fixes (previous)
**Files touched:**

_agents/_
- `agents/README.md` — added an `## opencode.json` section: agents are auto-discovered from the `agent/` dir (no `agent` block needed, matching the repo's own config), plus an optional inline `agent` override snippet and a restart-required note.

_plugins/_
- `plugins/README.md` — expanded the Configuration + Install/usage sections: a complete minimal `opencode.json` (full doc, matching the repo's live file), the tuple-vs-plain-string distinction, default 4000 vs override 8000, and a restart note.

_scripts/_
- `scripts/sync_opencode_agents.py` — CREATED. Syncs `agents/orchestrator.md` + `agents/executor.md` to `~/.config/opencode/agent/` (singular). Supports `--dry-run`, `OPENCODE_AGENTS` env override, excludes README, prints ✓/✗/⚠ + summary, exits nonzero on failure.
- `scripts/sync_opencode_plugins.py` — CREATED. Syncs all `plugins/*.ts` (glob, future-proof; currently just `token-guard.ts`) to `~/.config/opencode/plugin/` (singular). Supports `--dry-run`, `OPENCODE_PLUGINS` env override, excludes README/markdown.
- `scripts/sync_bob_skills.py` — FIXED. Replaced the fragile manual exclusion loop with a single `shutil.copytree(..., ignore=shutil.ignore_patterns(*EXCLUSIONS))` matching `sync_opencode_skills.py`, so exclusions now apply uniformly at all depths.
- `scripts/sync_all.py` — UPDATED. Added `sync_opencode_agents.py` + `sync_opencode_plugins.py` to the OpenCode path; exit codes wired in; docstring updated.
- `scripts/README.md` — UPDATED. Replaced the stale skill list with the correct 12 skills across 4 categories; added sections for the two new scripts; updated the `sync_all.py` section + verify steps.

_global installs_
- `~/.config/opencode/agent/{orchestrator.md,executor.md}` and `~/.config/opencode/plugin/token-guard.ts` — created via the new sync scripts (verified diff-identical to repo source).

**Summary:** Documented the `opencode.json` wiring in both the `agents/` and `plugins/` READMEs; created two new global-scope OpenCode sync scripts (agents + plugins) and wired them into `sync_all.py`; fixed a fragility bug in `sync_bob_skills.py`'s exclusion logic; refreshed the stale `scripts/README.md`; and installed the agents + plugins to global OpenCode scope.

**Outcome:** Agents + plugins live in global OpenCode config and verified diff-identical to source; all 5 sync scripts are `py_compile`-clean and pass `--dry-run`. Nothing committed to git that session.

## Open Items / Next Steps

- [ ] `scripts/sync_bob_skills.py` — Bob was NOT re-synced after the folder reorg + LinkedIn edits; run `python3 scripts/sync_bob_skills.py` to push all 12 skills (including the modified LinkedIn ones) to `~/.bob/skills/`.
- [ ] `skills/content-creation/Medium/` — empty category folder with no skills; add skill(s) here (each needs `SKILL.md` + `README.md`) and then add their `skills/content-creation/Medium/<name>` paths to the `SKILLS` lists in `scripts/sync_opencode_skills.py` and `scripts/sync_bob_skills.py`.

## Quick Reference

- **Skill folders (all under `skills/`):** `skills/agent_session_management/` (2), `skills/content-creation/linkedin/` (3: linkedin-post-writer, linkedin-image-prompts, linkedin-post-reviewer), `skills/content-creation/Medium/` (empty), `skills/development/` (4: lean-coder, project-planner, repo-docs-publisher, ui-ux-designer), `skills/learning/` (3: author-chapter, create-learning-repo, generate-practice-exam).
- **Agents dir:** `agents/orchestrator_mode_agents/{orchestrator.md,executor.md}` — source copies; `agents/README.md` documents `opencode.json` wiring (auto-discovered from the `agent/` dir).
- **Plugins dir:** `plugins/token_saving/token-guard.ts` — source copy; `plugins/README.md` documents `opencode.json` wiring.
- **Sync scripts:** `sync_opencode_skills.py`, `sync_bob_skills.py`, `sync_opencode_agents.py`, `sync_opencode_plugins.py`, and `sync_all.py` (runs all OpenCode syncs + Bob).
- **`SKILLS` list format:** full path from repo root, e.g. `skills/development/lean-coder`; the leaf segment becomes the installed folder name. Update these lists when adding/removing skills.
- **`sync_all.py` flags:** `--dry-run`, `--opencode-only`, `--bob-only`.
- **Env overrides:** `OPENCODE_SKILLS`, `BOB_SKILLS`, `OPENCODE_AGENTS`, `OPENCODE_PLUGINS`.
- **Verify a sync:** `python3 scripts/sync_all.py --dry-run` (expect 12 skills / 2 agents / 1 plugin / 12 Bob skills, 0 skipped); `python3 -m py_compile scripts/*.py` for syntax.
- **Global config locations:** OpenCode skills `~/.config/opencode/skills/`, agents `~/.config/opencode/agent/` (singular), plugins `~/.config/opencode/plugin/` (singular); Bob skills `~/.bob/skills/`.
- **opencode loads config only at startup** — restart opencode after changing any config, agent, or plugin file.
- **Skill template:** every skill needs `SKILL.md` (frontmatter `name` must match leaf folder name) + `README.md`.
- **LinkedIn skill conventions:** each of the 3 LinkedIn skills reads a user-supplied source file and writes its output (`linkedin_post.md`, `image_prompts.md`, `linkedin_post_revised.md`) in that same directory — never to a fixed folder.
- **No AGENTS.md** exists at the repo root — this handoff file is the only persistent cross-session context document.
- **Session continuity:** use `/init-session` at session start and `/end-session` at session end to restore/save context to `.agent_docs/handoff.md`.
