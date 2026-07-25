# Handoff Log

## Project Summary

`agent_skills` is a curated collection of portable AI-agent skill files (`SKILL.md`) for OpenCode and other coding/content assistants. The repo has no build system, dependencies, CI, or formal test suite; it is mostly Markdown content plus small standard-library Python helper scripts for skills that need executable behavior. The live categories are `learning/`, `agent_session_management/`, `development/`, and `content-creation/`. Key artifacts are each skill's `SKILL.md`, human-facing `README.md`, optional support folders (`reference/`, `references/`, `scripts/`, `templates/`), root `AGENTS.md` for authoritative local rules, and `.agent_docs/handoff.md` for session continuity.

Architecture is file-oriented: every skill is independently installable by copying its folder into `~/.config/opencode/skills/` or `.opencode/skills/`. Learning/session skills use `reference/`; development skills use `references/`; content-creation skills use `scripts/`, and `carousel-builder`/`medium-imager` also use SVG `templates/`. Critical constants: every skill requires `SKILL.md` + `README.md`; never add untested stubs; every phase of a multi-phase skill ends with an explicit confirmation gate; `AGENTS.md` is authoritative. `content-creation/linkedin-medium/` now holds **10** skills. `medium-imager` treats `cairosvg` as required (PNG is the Medium deliverable) and now self-installs it via `uv` on user approval (`--install-missing`), mirroring `carousel-builder`'s optional-PDF pattern.

## Session Log

### Session: 2026-07-25 (current)
**Files touched:**
- `.agent_docs/handoff.md` — updated with new session entry and project context.
- `content-creation/linkedin-medium/draft-builder/` — read SKILL.md, README.md, claim_lint.py fixtures and test cases (TC1, TC2, TC3).
- `tests/draft-builder/` — reviewed regression test cases and fixture files.
- `~/.config/opencode/skills/` — synced all 19 skills from local repo (source of truth).

**Summary:** Successfully synced all 19 OpenCode skills from the local repository to the global `~/.config/opencode/skills/` directory with full verification. Created comprehensive sync verification report with SHA256 checksums confirming 100% content integrity (19/19 skills perfect match, 98 content files, 69 markdown + 32 supporting files). Source repository is now officially the authoritative master for all skills across all categories.

**Outcome:** Global skills directory updated and verified; all 19 skills (2 session management, 10 content creation, 4 development, 3 learning) now in production state with perfect content parity.

### Session: 2026-07-19 (previous)
**Files touched:**
- `~/.config/opencode/skills/*` — copied all 19 skills (10 content creation, 2 session management, 3 learning, 4 development) to the global OpenCode config path.
- `/home/jbrhsn/.gemini/config/skills/*` — copied all 19 skills to the global Antigravity config path.
- `/home/jbrhsn/.gemini/antigravity-ide/brain/2ecff6c1-156d-4059-a718-b1c8c5fb00b3/content_creation_skills_evaluation.md` — evaluated and compiled a detailed report of all 10 content creation skills.

**Summary:** Evaluated all 10 content creation skills in detail, confirming they are fully functional, review-first, local SVG-centric, and fact-linted. Created a comprehensive evaluation report. Copied all 19 custom repository skills (content-creation, session-management, learning, and development) to the global configuration paths for both OpenCode and Antigravity.

**Outcome:** Global install of all 19 repository skills completed and verified for both OpenCode and Antigravity; a detailed content-creation skills evaluation report artifact was written.

## Open Items / Next Steps

- [ ] `AGENTS.md` — create authoritative local agent behavior rules file (referenced in handoff but does not exist; should document skill naming conventions, test-before-commit policy, folder structure rules, critical paths).
- [ ] `agent_session_management/end-session/SKILL.md` (Step 1) — replace `find . -newer .git/index` with `find . -mmin -480` to handle repos with no commits; merge `git status --porcelain` to capture uncommitted session edits.
- [ ] `agent_session_management/end-session/SKILL.md` (Windows path) — derive `get-session-context.ps1` path from skill's own location instead of hardcoding `$env:USERPROFILE\.config\opencode\skills\end-session\`, enabling per-project installs.
- [ ] `agent_session_management/end-session/README.md` — fix "Handoff file structure" example: change `## Project Progress (rolling summary)` to `## Project Summary` to match actual SKILL.md output.

## Quick Reference

- No build/test/lint pipeline; git operations are the only formal developer commands.
- `.agent_docs/handoff.md` is the rolling session memory file; start next session with `/init-session`.
- Root categories: `agent_session_management/` (2 skills), `learning/` (3 skills), `development/` (4 skills), `content-creation/` (10 skills).
- Skill convention: every skill must have `SKILL.md` + `README.md`; support folders vary by category.
- Support folder names: `reference/` for learning/session skills, `references/` for development skills, `scripts/` and sometimes `templates/` for content-creation skills.
- `content-creation/linkedin-medium/` contains **10** skills: `seed-expander`, `draft-builder`, `carousel-builder`, `medium-imager`, `tutorial-verifier`, `editorial-reviewer`, `voice-profiler`, `content-tracker`, `linkedin-writer`, `medium-writer`.
- Canonical pipeline: `seed-expander → draft-builder → {linkedin-writer, medium-writer} → {carousel-builder, medium-imager, tutorial-verifier} → editorial-reviewer`, with `voice-profiler` + `content-tracker` cross-cutting.
- `linkedin-writer/reference/hook-writing-guide.md` and `medium-writer/reference/hook-writing-guide.md` are byte-identical; keep both in sync when editing either.
- `carousel-builder` authors carousel slide copy from draft/idea AND renders SVG + combined PDF; `cairosvg`/`Pillow` are optional PDF add-ons via `uv` (`combine_pdf.py --install-missing`) after user confirmation.
- `medium-imager` outputs Medium cover/card SVG source plus required PNG; `cairosvg` is required and self-installs via `uv` on approval (`svg_to_png.py --install-missing`, loop-guarded by `MEDIUM_IMAGER_UV_BOOTSTRAPPED`).
- Global sync command: `cp -r content-creation/linkedin-medium/<skill-name> ~/.config/opencode/skills/` (delete target first for clean replace; verify with `diff -r`).
- Use `python3 -m py_compile <script>` to syntax-check Python helpers; remove `__pycache__/` before committing.
- "Tested skills only" rule: never add or commit a skill stub without exercising it in a real session.
- Global `init-session`/`end-session` skills installed at `~/.config/opencode/skills/` and exposed as `/init-session` + `/end-session` commands in `~/.config/opencode/opencode.jsonc`.
- **Sync status:** All 19 skills successfully synced to `~/.config/opencode/skills/` (verified 2026-07-25, 100% checksum match).
