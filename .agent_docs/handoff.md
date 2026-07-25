# Handoff Log

## Project Summary

`agent_skills` is a curated collection of portable AI-agent skill files (`SKILL.md`) for OpenCode and other coding/content assistants. The repo has no build system, dependencies, CI, or formal test suite; it is mostly Markdown content plus small standard-library Python helper scripts for skills that need executable behavior. The live categories are `learning/`, `agent_session_management/`, `development/`, and `content-creation/`. Key artifacts are each skill's `SKILL.md`, human-facing `README.md`, optional support folders (`reference/`, `references/`, `scripts/`, `templates/`), root `AGENTS.md` for authoritative local rules, and `.agent_docs/handoff.md` for session continuity.

Architecture is file-oriented: every skill is independently installable by copying its folder into `~/.config/opencode/skills/` or `.opencode/skills/`. Learning/session skills use `reference/`; development skills use `references/`; content-creation skills use `scripts/`, and `carousel-builder`/`medium-imager` also use SVG `templates/`. Critical constants: every skill requires `SKILL.md` + `README.md`; never add untested stubs; every phase of a multi-phase skill ends with an explicit confirmation gate; `AGENTS.md` is authoritative. `content-creation/linkedin-medium/` now holds **10** skills. `medium-imager` treats `cairosvg` as required (PNG is the Medium deliverable) and now self-installs it via `uv` on user approval (`--install-missing`), mirroring `carousel-builder`'s optional-PDF pattern.

## Session Log

### Session: 2026-07-19 (current)
**Files touched:**
- `~/.config/opencode/skills/*` — copied all 19 skills (10 content creation, 2 session management, 3 learning, 4 development) to the global OpenCode config path.
- `/home/jbrhsn/.gemini/config/skills/*` — copied all 19 skills to the global Antigravity config path.
- `/home/jbrhsn/.gemini/antigravity-ide/brain/2ecff6c1-156d-4059-a718-b1c8c5fb00b3/content_creation_skills_evaluation.md` — evaluated and compiled a detailed report of all 10 content creation skills.

**Summary:** Evaluated all 10 content creation skills in detail, confirming they are fully functional, review-first, local SVG-centric, and fact-linted. Created a comprehensive evaluation report. Copied all 19 custom repository skills (content-creation, session-management, learning, and development) to the global configuration paths for both OpenCode and Antigravity.

**Outcome:** Global install of all 19 repository skills completed and verified for both OpenCode and Antigravity; a detailed content-creation skills evaluation report artifact was written.

### Session: 2026-07-19 (previous)
**Files touched:**
- `~/.config/opencode/skills/init-session/` — copied skill folder from `agent_session_management/init-session/` (global install).
- `~/.config/opencode/skills/end-session/` — copied skill folder from `agent_session_management/end-session/` (global install); includes `SKILL.md`, `README.md`, `get-session-context.ps1`.
- `~/.config/opencode/opencode.jsonc` — added `command` entries `init-session` and `end-session` whose templates instruct the model to invoke the respective skill (typed as `/init-session`, `/end-session`).
- Repo `agent_session_management/*` — read only for evaluation; no in-repo edits this session.

**Summary:** Evaluated the `init-session` and `end-session` skills (structure, trigger wiring, round-trip against the repo's own `handoff.md`), then installed both globally by copying to `~/.config/opencode/skills/`, and registered `/init-session` and `/end-session` slash commands in the global `opencode.jsonc`. Confirmed the skills are discovered (present in `available_skills`) and clarified they are model-invoked, not built-in slash commands. Identified four concrete skill-file fixes (README section-name drift, hardcoded Windows script path, uncommitted-work blind spot, fragile `find` fallback) but did not apply them.

**Outcome:** Global install + two commands configured and validated (`opencode.jsonc` parses as JSON); no files inside the `agent_skills` repo were modified this session.

## Open Items / Next Steps
- [ ] `README.md` — add `medium-imager` to the Content Creation skills table to ensure it is documented alongside other content creation skills.
- [ ] `agent_session_management/end-session/README.md` — fix the "Handoff file structure" example: the section is `## Project Summary`, not `## Project Progress (rolling summary)`, to match SKILL.md output and the produced file.
- [ ] `agent_session_management/end-session/SKILL.md` (and README) — derive `get-session-context.ps1` path from the skill's own location instead of hardcoding `$env:USERPROFILE\.config\opencode\skills\end-session\`, so per-project installs work.
- [ ] `agent_session_management/end-session/SKILL.md` Step 1 — merge committed + uncommitted signals (e.g. `git status --porcelain` + `find -mmin -480`) instead of using `git log` and only falling back when empty, so uncommitted session edits are captured.
- [ ] `agent_session_management/end-session/SKILL.md` Step 1 fallback — replace `find . -newer .git/index` with `find . -mmin -480` (the former errors when the repo has no commits).

## Quick Reference
- No build/test/lint pipeline; git operations are the only formal developer commands.
- `AGENTS.md` is authoritative for local agent behavior; read it at session start (note: repo currently has no `AGENTS.md` despite references to it).
- `.agent_docs/handoff.md` is the rolling session memory file; start next session with `/init-session`.
- Root categories: `agent_session_management/`, `learning/`, `development/`, `content-creation/`.
- Skill convention: every skill must have `SKILL.md` + `README.md`; support folders vary by category.
- Support folder names: `reference/` for learning/session skills, `references/` for development skills, `scripts/` and sometimes `templates/` for content-creation skills.
- `content-creation/linkedin-medium/` now contains **10** skills: `seed-expander`, `draft-builder`, `carousel-builder`, `medium-imager`, `tutorial-verifier`, `editorial-reviewer`, `voice-profiler`, `content-tracker`, `linkedin-writer`, `medium-writer` (`platform-adapter` removed).
- Canonical pipeline: `seed-expander → draft-builder → {linkedin-writer, medium-writer} → {carousel-builder, medium-imager, tutorial-verifier} → editorial-reviewer`, with `voice-profiler` + `content-tracker` cross-cutting.
- `linkedin-writer/reference/hook-writing-guide.md` and `medium-writer/reference/hook-writing-guide.md` are intentionally byte-identical; keep both in sync when editing either.
- `carousel-builder` now authors carousel slide copy from a draft/idea AND renders SVG + combined PDF; `cairosvg`/`Pillow` are optional PDF add-ons via `uv` (`combine_pdf.py --install-missing`) after user confirmation.
- `medium-imager` outputs Medium cover/card SVG source plus required PNG; `cairosvg` is required and now self-installs via `uv` on approval (`svg_to_png.py --install-missing`, loop-guarded by `MEDIUM_IMAGER_UV_BOOTSTRAPPED`).
- `medium-imager` commands center on `scripts/spec.py`, `scripts/render_svg.py`, `scripts/svg_to_png.py`, and `scripts/suggest_from_draft.py`.
- Sync a content skill globally with `cp -r content-creation/linkedin-medium/<skill-name> ~/.config/opencode/skills/` (delete the target first for a clean replace; verify with `diff -r`).
- Use `python3 -m py_compile <script>` to syntax-check Python helpers and remove `__pycache__/` before committing.
- "Tested skills only" rule: never add or commit a skill stub that has not been exercised in a real session.
- Global `init-session`/`end-session` skills are installed at `~/.config/opencode/skills/` and exposed as `/init-session` + `/end-session` commands in `~/.config/opencode/opencode.jsonc`.
