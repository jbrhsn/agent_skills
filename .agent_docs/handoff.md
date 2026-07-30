# Handoff Log

## Project Summary

`agent_skills` is a curated OpenCode agent-skills repository: a catalog of reusable, portable AI-agent skills (`SKILL.md` + `README.md` per skill) plus shareable agent and plugin definitions, with Python sync scripts that install everything into OpenCode (and IBM Bob) config dirs. Skills live under a categorized `skills/` tree: `skills/agent_session_management/` (2: init-session, end-session), `skills/content-creation/linkedin/` (2: linkedin-post-writer, linkedin-image-prompts), `skills/content-creation/Medium/` (2: medium-article-writer, medium-image-prompts), `skills/development/` (4: lean-coder, project-planner, repo-docs-publisher, ui-ux-designer), and `skills/learning/` (3: author-chapter, create-learning-repo, generate-practice-exam) — **13 skills total**. Agents live under `agents/orchestrator_mode_agents/` (`orchestrator.md` = primary/plan-only, `executor.md` = subagent that does+verifies a unit). Plugins live under `plugins/token_saving/` (`token-guard.ts`). `scripts/` holds five Python sync scripts (skills, agents, plugins to OpenCode; skills to Bob; `sync_all.py` orchestrates); the sync scripts carry a HARDCODED `SKILLS` list that must be edited when skills are added/removed. The architecture is file-centric — pure Markdown/TypeScript content plus Python sync tooling, no build/CI/tests. Each `SKILL.md` frontmatter `name` must equal its leaf folder name; skills install by leaf name only (category path stripped). Global skills path: `~/.config/opencode/skills/`. No root `AGENTS.md`; this handoff is the sole cross-session context.

## Session Log

### Session: 2026-07-30 (current)
**Files touched:**

_skills/ (content-creation/Medium — NEW)_
- `skills/content-creation/Medium/medium-article-writer/SKILL.md` — new dual-path skill (WRITE + REVIEW/SCORE) mirroring linkedin-post-writer: shared 5-dimension /100 rubric grounded in Medium's Distribution Guidelines, AI-content policy, and Partner Program mechanics; units W1–W6 and R1–R6; guardrails against fabricating earnings figures and the "about Medium = Network-only" trap. Outputs `medium_article.md` / `medium_article_reviewed.md`.
- `skills/content-creation/Medium/medium-image-prompts/SKILL.md` — new skill mirroring linkedin-image-prompts but adapted to Medium's non-carousel model (1 featured/cover + N purposeful in-article visuals); featured-image focal-point/≥1192px guidance, mandatory AI-image caption-disclosure, credit+caption+alt-text per image. Outputs `medium_image_prompts.md`.

_scripts/ + docs_
- `scripts/sync_opencode_skills.py`, `scripts/sync_bob_skills.py` — added the two Medium skill paths to the hardcoded `SKILLS` lists (11→13).
- `scripts/README.md` — "11 skills"→"13 skills"; added "Content Creation (Medium)" category line.

_global installs_
- Synced all 13 skills to `~/.config/opencode/skills/` and `~/.bob/skills/` (both: 13 synced, 0 skipped); verified both Medium `SKILL.md` files landed on disk in both targets.

**Summary:** Researched Medium monetization/hooks/structure/images (4 parallel research passes), then created two new Medium content-creation skills mirroring the LinkedIn pair — a dual-path `medium-article-writer` and a `medium-image-prompts`. Registered both in the two sync scripts' hardcoded SKILLS lists, updated the scripts README count 11→13, and synced to both OpenCode and Bob global dirs.

**Outcome:** Docs-only additions, verified by frontmatter/name checks and on-disk confirmation in both global dirs (13/13, 0 skipped). Note the repo `README.md` skill table was NOT yet updated to list the two Medium skills or bump its counts. User still needs to restart opencode to load the new skills. Nothing committed to git.

### Session: 2026-07-30 (previous)
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

## Open Items / Next Steps
- [ ] `README.md` (repo root) — the Skills table under "### Content Creation" still lists only the two LinkedIn skills and describes content-creation as LinkedIn-only; add a Medium subsection (or rows) for `medium-article-writer` and `medium-image-prompts`, and update the install-commands block and the support-dir table to include `content-creation/Medium/`.

## Quick Reference

- **Skill folders (all under `skills/`, 13 total):** `skills/agent_session_management/` (init-session, end-session), `skills/content-creation/linkedin/` (linkedin-post-writer, linkedin-image-prompts), `skills/content-creation/Medium/` (medium-article-writer, medium-image-prompts), `skills/development/` (lean-coder, project-planner, repo-docs-publisher, ui-ux-designer), `skills/learning/` (author-chapter, create-learning-repo, generate-practice-exam).
- **Medium skills mirror the LinkedIn pair:** `medium-article-writer` is dual-path (WRITE → `medium_article.md`; REVIEW/SCORE → `medium_article_reviewed.md`); `medium-image-prompts` produces 1 cover + N in-article visual prompts → `medium_image_prompts.md`. Both self-contained (Medium research baked in).
- **`linkedin-post-writer` is dual-path:** WRITE (`linkedin_post.md`) + REVIEW/REFINE (`linkedin_post_revised.md`).
- **All 13 SKILL.md workflows follow the delegation model:** discrete units with Goal/Inputs/Do/Self-verify/Report + explicit "STOP GATE (hand back)" markers.
- **Agents dir:** `agents/orchestrator_mode_agents/{orchestrator.md,executor.md}`.
- **Plugins dir:** `plugins/token_saving/token-guard.ts`.
- **GOTCHA — sync scripts have a HARDCODED `SKILLS` list:** adding a skill requires editing the list in BOTH `scripts/sync_opencode_skills.py` and `scripts/sync_bob_skills.py` (a plain sync will silently miss unregistered skills). Format: full path from repo root, e.g. `skills/content-creation/Medium/medium-article-writer`; leaf segment becomes the installed folder name.
- **Sync all skills to OpenCode:** `python3 scripts/sync_opencode_skills.py` (add `--dry-run` to preview). Bob: `python3 scripts/sync_bob_skills.py`.
- **`sync_all.py` flags:** `--dry-run`, `--opencode-only`, `--bob-only`.
- **Env overrides:** `OPENCODE_SKILLS`, `BOB_SKILLS`, `OPENCODE_AGENTS`, `OPENCODE_PLUGINS`.
- **Syntax check:** `python3 -m py_compile scripts/*.py` (no test/lint suite in repo).
- **Global config locations:** OpenCode skills `~/.config/opencode/skills/`, agents `~/.config/opencode/agent/` (singular), plugins `~/.config/opencode/plugin/` (singular); Bob skills `~/.bob/skills/`.
- **Gotcha — sync does not auto-prune:** removing a skill from the repo does NOT delete it from the global dir; delete the obsolete global folder manually.
- **Gotcha — restart required:** opencode loads config/agents/plugins/skills only at startup; restart after any change.
- **Skill template:** every skill needs `SKILL.md` (frontmatter `name` must match leaf folder name) + `README.md`. NOTE: the two new Medium skills currently have SKILL.md only (no README.md yet).
- **No AGENTS.md** at the repo root — this handoff file is the only persistent cross-session context.
- **Session continuity:** `/init-session` at start, `/end-session` at end (reads/writes `.agent_docs/handoff.md`).
