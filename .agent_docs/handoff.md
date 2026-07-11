# Handoff Log

## Project Progress (rolling summary)

_Last updated: 2026-07-11_

**Current phase:** New `development/` skill category — evaluation, fixes, and documentation — **Status:** phase complete, uncommitted
**Now:** Repo has 5 commits visible on `main` (`HEAD` = `26dbb95`). A new `development/` category exists on disk with 4 skills (`lean-coder`, `project-planner`, `repo-docs-publisher`, `ui-ux-designer`), each with `SKILL.md` + `README.md` + a `references/` dir. This session evaluated all 4, applied fixes, wrote the 4 missing READMEs, and registered the category in `AGENTS.md`. **The entire `development/` tree is still untracked (`?? development/`) — nothing from this session is committed yet.**

**Project summary:** `agent_skills` is a curated collection of portable AI-agent skill files (`SKILL.md`) for OpenCode and other assistants. No build system, tests, or CI — pure Markdown. Three live categories: `learning/`, `agent_session_management/`, and now `development/`. Convention: one skill = `SKILL.md` (agent-facing) + `README.md` (human guide) + optional reference subdir (`reference/` singular in learning/session skills, `references/` plural in development skills). Handoff is the cross-session memory layer (`.agent_docs/handoff.md`), rolling 2-session window.

**Critical constants:**
- `AGENTS.md` is **gitignored** — it exists on disk, is edited/read normally, but never appears in `git status` and **cannot be committed** without first removing it from `.gitignore`. Do not attempt to `git add AGENTS.md` and expect it to stage.
- `development/` skills use `references/` (plural); `learning/`+`agent_session_management/` use `reference/` (singular). Match whichever the skill already uses.
- "Tested skills only" rule: skills must be exercised in a real session before commit.

**Progress so far:**
- Sessions 1–2 — Repo initialized, 3 skills scaffolded, evaluated, fixed. Commits `7773121`–`dc017c1`.
- Sessions 3–5 — Skills rearranged into `learning/` + `agent_session_management/`; naming revised. Commits `36cbeab`–`41799a1`.
- Session 6 (2026-07-09) — Created gitignored `AGENTS.md`; committed `.gitignore` agent-files block (`31275a1`).
- Session 7 (2026-07-09) — Quality audit + fixes: root README rewrite, 5 per-skill READMEs, phase gates, `end-session` Linux fallback. (Later folded into `26dbb95`.)
- Session 8 (2026-07-11) — New `development/` category evaluated, fixed, and documented (this session).

**Next up:** Commit the `development/` tree (the user requested a commit; it is not yet done).

---

## Session Log

### Session: 2026-07-11 (current) — Evaluate + fix `development/` skills

**Files touched:**
- `AGENTS.md` (gitignored — structure diagram, live-categories line, skill inventory table, install commands all extended for `development/`)
- `development/lean-coder/` — `SKILL.md` (Python section de-duplicated to point at `references/python-uv.md`), new `README.md`
- `development/project-planner/` — new `README.md`
- `development/repo-docs-publisher/` — `references/secrets-scan-checklist.md` (refreshed secret regexes), new `README.md`
- `development/ui-ux-designer/` — new `README.md`

**Summary:** Evaluated the 4 `development/` skills against the repo conventions and rated them (91/100). Fixed all identified issues: wrote the 4 missing per-skill `README.md` files (delegated to 4 parallel `general` subagents, matching the house style of existing READMEs); de-duplicated the inline Python/`uv` content in `lean-coder/SKILL.md` so it points to `references/python-uv.md` instead of restating it; refreshed the secret-detection regexes in `repo-docs-publisher/references/secrets-scan-checklist.md` (added `sk-proj-` OpenAI project keys, Google `AIza…`, and AWS secret-access-key patterns; removed the redundant old `sk-` line in both `rg` and `grep` blocks); and registered the whole `development/` category in `AGENTS.md`.

**Outcome:** All fixes complete and verified on disk, but **uncommitted** — `git status` shows only `?? development/`. The user then asked to commit; `git status`/`git log`/gitignore were inspected and it was confirmed `AGENTS.md` is gitignored (so it can't be included), and the commit itself was not yet run.

### Session: 2026-07-09 (previous) — Quality audit fixes + per-skill READMEs

**Phase:** Quality fixes + documentation
**Status:** phase complete

#### Current state
- Root `README.md` fully rewritten — accurate paths, all 5 skills, correct install commands
- `AGENTS.md` updated — repo structure diagram, conventions, install commands all current
- 5 per-skill `README.md` files created (init-session, end-session, create-learning-repo, author-chapter, generate-practice-exam)
- `end-session/SKILL.md` — Step 1 now platform-aware (Linux/macOS + Windows branches)
- `author-chapter/SKILL.md` — Phase 2 now ends with an explicit confirmation gate
- `generate-practice-exam/SKILL.md` — Phase 0 and Phase 2 now end with explicit confirmation gates
- Handoff trimmed to rolling 2-session window

#### Completed this session
- **Root `README.md` rewrite:** replaced stale `Scaffolding` category with `Session Management` + `Learning`; skills table lists all 5 skills with correct relative paths; install commands split into `agent_session_management/` and `learning/` variants.
- **`AGENTS.md` update:** structure diagram shows `README.md` in every skill folder; conventions updated; install commands cover both prefixes.
- **`end-session/SKILL.md` Step 1 fix:** platform-detecting branches — Linux/macOS uses `date`/`git log`/`find`; Windows uses `Get-Date` and the `.ps1` script.
- **Phase gate additions:** `author-chapter` Phase 2; `generate-practice-exam` Phase 0 and Phase 2.
- **5 per-skill READMEs created.**

#### Decisions / rationale
- **Per-skill README convention adopted;** `AGENTS.md` convention updated accordingly.
- **Phase gates added only where user review provides real value.**
- **`AGENTS.md` gitignored — unchanged** by user request.

---

## Open Items / Next Steps

- [ ] Repo root — commit the new `development/` tree. Run `git add development/ && git commit -m "feat: add development skills (lean-coder, project-planner, repo-docs-publisher, ui-ux-designer) with READMEs"`. Note: `AGENTS.md` edits from this session **cannot** be included (gitignored) — do not try to stage it.

---

## Quick Reference

- **No build/test/lint pipeline** — git operations are the only meaningful commands.
- **`AGENTS.md` is gitignored** — edit/read it normally, but it never stages or commits. `git check-ignore AGENTS.md` returns it.
- **Repo layout:** `learning/`, `agent_session_management/`, `development/` categories at root; `.agent_docs/handoff.md` = session memory.
- **Skill structure:** `SKILL.md` + `README.md` + optional refs. `development/` uses `references/` (plural); others use `reference/` (singular).
- **`development/` skills:** `lean-coder` (broad coding; `/review-diff`, `/audit-repo`), `project-planner` (`/plan-project`, spec→design→roadmap→backlog under `docs/`), `repo-docs-publisher` (README/publish docs, secrets scan first), `ui-ux-designer` (`/design-ux` → `docs/ux-design.md`).
- **Install a skill (from repo root):** `cp -r development/<skill> ~/.config/opencode/skills/` (global) or `.opencode/skills/` (per-project); Windows: `Copy-Item -Recurse development\<skill> "$env:USERPROFILE\.config\opencode\skills\"`.
- **Commit pending work:** `git add development/ && git commit -m "..."`.
- **Secrets scan reference:** `development/repo-docs-publisher/references/secrets-scan-checklist.md` (now covers `sk-proj-`, `AIza…`, AWS secret keys).
- **"Tested skills only" rule** — exercise a skill in a real session before committing it.
- **Current `HEAD`:** `26dbb95`. Only `?? development/` is untracked/uncommitted.
- **Restore this context next session with `/init-session`.**
