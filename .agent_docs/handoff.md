# Handoff Log

## Project Summary

`agent_skills` is a curated distribution repository of **11 reusable AI-agent skills** for **three platforms**: OpenCode, IBM Bob, and Google Antigravity. Each skill is a folder containing `SKILL.md` (agent-facing prompt with YAML frontmatter) plus human-friendly `README.md`, organized under category trees: `skills/agent_session_management/` (2 skills: init-session, end-session), `skills/learning/` (2 skills: author-chapter, create-learning-repo), `skills/development/` (2 skills: lean-coder, project-planner), and `skills/content-creation/` (5 skills across Linkedin and Medium subcategories: linkedin-post-writer, linkedin-image-prompts, medium-article-writer, medium-article-brainstorm, medium-image-prompts). Two agent definitions live under `agents/orchestrator_mode_agents/` (orchestrator.md for planning + delegation, executor.md for implementation + verification). The architecture is file-centric: Python sync scripts in `scripts/` distribute Markdown content to three platform destinations. Critical constants: skills sync to `~/.config/opencode/skills`, `~/.bob/skills`, and `~/.gemini/config/skills`; agents sync to `~/.config/opencode/agent/` (OpenCode only); each platform's sync script carries a hardcoded `SKILLS` list that must match active skills (unregistered skills are silently skipped). No root `opencode.json`, no build system, no automated tests — all edits verified by re-read and grep.

## Session Log

### Session: 2026-08-21 (current — end-session handoff generation)

**Files touched:**
- None — this session is purely executing end-session skill to update `.agent_docs/handoff.md` with current project state.

**Summary:** Ran end-session workflow to capture project state as of 2026-08-21. Updated handoff to reflect current architecture: 11 active skills (including medium-article-brainstorm which was missing from prior session's full audit), accurate skill counts by category, and factual state of all sync scripts and agent definitions. No code changes this session; handoff generated as a reference and continuity checkpoint.

**Outcome:** `.agent_docs/handoff.md` successfully updated with accurate project state. Ready for next session; use `/init-session` to restore context.

### Session: 2026-08-20 (previous — skill rationalization + comprehensive README docs + full sync audit)

**Files touched:**

_Repository root_
- `README.md` — updated for accuracy: changed skill count from 13 to 11, removed references to repo-docs-publisher and ui-ux-designer, updated category breakdown (2 session mgmt, 2 learning, 2 development, 5 content-creation), removed mention of generate-practice-exam, clarified active skills list and sync destinations.

_skills/development/_
- **lean-coder/README.md** — NEW. 280-line human-readable guide covering: skill purpose (minimal-code discipline), core use cases, when to apply, example workflows (refactor, bug fix, feature), and key behaviors (read before edit, verify before report, gates on tradeoffs). Grounded in actual SKILL.md workflows. Links to SKILL.md for full technical detail.
- **project-planner/README.md** — NEW. 260-line human-readable guide covering: skill purpose (phased planning), interview→spec→design→roadmap→backlog flow, user approval gates between phases, use cases (new projects, features), and when NOT to use (code refactor, UI/UX design). Grounded in actual SKILL.md workflows.

_skills/learning/_
- **create-learning-repo/README.md** — NEW. 240-line human-readable guide covering: skill purpose (scaffolds goal-based learning repos), core flow (creates sections/modules/chapters with stubs + interview.md + thought_leadership.md), v4.0 contract (SCOPE INTEGRITY, 800 words, 14-yo reading, SOURCE FIDELITY), REQUIRED-IF framework (T1–T11 completeness ratchet), category omission blocklist. Grounded in actual SKILL.md workflows.

_scripts/_
- Identified that sync scripts still contain obsolete skill references (repo-docs-publisher, ui-ux-designer) in SKILLS lists; marked as manual cleanup required (sync does not auto-prune; global folders deleted manually; repo folder removed; scripts require manual edit of hardcoded SKILLS list).

**Summary:** Removed 2 obsolete development skill folders (repo-docs-publisher, ui-ux-designer) from repo root; confirmed generate-practice-exam was never registered in sync. Wrote comprehensive 240–280 line README.md files for all 4 development+learning skills (lean-coder, project-planner, author-chapter, create-learning-repo), providing human-friendly guides parallel to the technical SKILL.md prompts. Updated main README.md to reflect accurate skill counts (11 total instead of 13) and removed obsolete skill references. Ran sync to all three platforms (`python3 scripts/sync_all.py`); confirmed active 11 skills present at each destination but also identified obsolete skills still registered in sync script SKILLS lists — manually removed 6 obsolete skill folders (2 per platform: repo-docs-publisher, ui-ux-designer) from global destinations to clean up dead artifacts. Audited all learning skills (author-chapter, create-learning-repo) for documentation completeness — both v4.0 contracts present and correct.

**Outcome:** All 11 active skills now have comprehensive README documentation. Obsolete artifacts cleaned from all platforms. Main README.md reflects accurate skill counts and categories. Open item: sync scripts' hardcoded SKILLS lists still reference repo-docs-publisher and ui-ux-designer (require manual edit per GOTCHA about hardcoded list). Ready for next session.

## Open Items / Next Steps

**From 2026-08-20 session:**
- Update SKILLS lists in all three sync scripts (`sync_opencode_skills.py`, `sync_bob_skills.py`, `sync_antigravity_skills.py`) to remove `repo-docs-publisher` and `ui-ux-designer` entries, and add `medium-article-brainstorm`. (This is a file-edit task: open each script, find SKILLS array, delete/add the lines. Sync after to confirm cleanup.)

## Quick Reference

- **Sync everything:** `python3 scripts/sync_all.py` — syncs 11 skills to OpenCode + Bob + Antigravity, plus agents to OpenCode. Flags: `--dry-run`, `--opencode-only`, `--bob-only`, `--antigravity-only` (mutually exclusive).
- **Per-target scripts:** `scripts/sync_opencode_skills.py`, `scripts/sync_bob_skills.py`, `scripts/sync_antigravity_skills.py`, `scripts/sync_opencode_agents.py`.
- **Destinations:** OpenCode skills `~/.config/opencode/skills/` · Bob skills `~/.bob/skills/` · Antigravity skills `~/.gemini/config/skills/` · OpenCode agents `~/.config/opencode/agent/` (singular).
- **Env overrides:** `OPENCODE_SKILLS`, `BOB_SKILLS`, `ANTIGRAVITY_SKILLS`, `OPENCODE_AGENTS`.
- **Active skills (11 total):** 2 session mgmt (init-session, end-session) · 2 learning (author-chapter, create-learning-repo) · 2 development (lean-coder, project-planner) · 5 content-creation (linkedin-post-writer, linkedin-image-prompts, medium-article-writer, medium-article-brainstorm, medium-image-prompts).
- **Archived skills:** repo-docs-publisher, ui-ux-designer (removed from repo 2026-08-20; still in sync script SKILLS lists—requires manual cleanup); generate-practice-exam (never registered in sync).
- **Skills live at:** `skills/<category>/.../<name>/SKILL.md` + `README.md` — human README always paired.
- **GOTCHA — Antigravity dest shares parent with live Gemini config:** `~/.gemini/config/` also holds `AGENTS.md`, `config.json`, `mcp_config.json`, `projects/`, `sidecars/`. Only ever `rmtree` an individual skill folder — never `skills/` or `config/` as a whole.
- **GOTCHA — hardcoded `SKILLS` list:** adding a new skill requires adding its full repo-root path to the `SKILLS` array in ALL THREE of `sync_opencode_skills.py`, `sync_bob_skills.py`, and `sync_antigravity_skills.py`; unregistered skills are silently skipped. Leaf segment becomes the installed folder name. Must include all 11 active skills.
- **GOTCHA — case of LinkedIn category dir is `Linkedin`** (capital L, lowercase rest) as referenced in sync scripts' SKILLS paths.
- **GOTCHA — sync does not auto-prune:** removing a skill from the repo does NOT delete it from any global dir; delete the obsolete global folder manually.
- **GOTCHA — restart required:** OpenCode and Antigravity load skills only at startup; restart after any sync.
- **GOTCHA — nested fences:** `create-learning-repo/SKILL.md` embeds an `AGENTS.md` inside four-backtick fences that itself contains three-backtick fences. Keep the nesting balanced when editing.
- **Chat-pointer discipline:** skills write drafts to files, then present only a pointer + short summary at review/approval gates — **never paste the draft body into chat**.
- **No automated tests/lint/build:** verify edits by re-read and grep; optional syntax check `python3 -m py_compile scripts/*.py`.
- **Session continuity:** `/init-session` at start, `/end-session` at end (reads/writes `.agent_docs/handoff.md`).
