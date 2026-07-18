# Handoff Log

## Project Summary

`agent_skills` is a curated collection of portable AI-agent skill files (`SKILL.md`) for OpenCode and other coding/content assistants. The repo has no build system, dependencies, CI, or formal test suite; it is mostly Markdown content plus small standard-library Python helper scripts for skills that need executable behavior. The live categories are `learning/`, `agent_session_management/`, `development/`, and `content-creation/`. Key artifacts are each skill's `SKILL.md`, human-facing `README.md`, optional support folders (`reference/`, `references/`, `scripts/`, `templates/`), root `AGENTS.md` for authoritative local rules, and `.agent_docs/handoff.md` for session continuity.

Architecture is file-oriented: every skill is independently installable by copying its folder into `~/.config/opencode/skills/` or `.opencode/skills/`. Learning/session skills use `reference/`; development skills use `references/`; content-creation skills use `scripts/`, and `carousel-builder`/`medium-imager` also use SVG `templates/`. Critical constants: every skill requires `SKILL.md` + `README.md`; never add untested stubs; every phase of a multi-phase skill ends with an explicit confirmation gate; `AGENTS.md` is authoritative. `content-creation/linkedin-medium/` now holds **10** skills (`platform-adapter` was removed). `medium-imager` treats `cairosvg` as required (PNG is the Medium deliverable) and now self-installs it via `uv` on user approval (`--install-missing`), mirroring `carousel-builder`'s optional-PDF pattern.

## Session Log

### Session: 2026-07-18 (current)
**Files touched:**
- `content-creation/linkedin-medium/carousel-builder/` — `SKILL.md` + `README.md` extended so the skill AUTHORS 8–12 slides of carousel copy from a draft/idea (not just renders provided copy); all platform-adapter references removed.
- `content-creation/linkedin-medium/medium-imager/` — `scripts/svg_to_png.py` gained a `--install-missing` flag (uv creates `.venv`, installs `cairosvg`, re-execs, guarded by `MEDIUM_IMAGER_UV_BOOTSTRAPPED`); `SKILL.md` + `README.md` updated to probe-then-ask-then-install.
- `content-creation/linkedin-medium/linkedin-writer/` + `medium-writer/` — `README.md`/`SKILL.md` repointed carousel copy to `carousel-builder` and both-platform work to running both writers; hook-writing-guide.md files marked as intentional byte-identical duplicates.
- `content-creation/linkedin-medium/{draft-builder,seed-expander,tutorial-verifier,editorial-reviewer,voice-profiler,content-tracker}/README.md` — cross-references and pipeline diagrams updated to the new canonical pipeline.
- `content-creation/linkedin-medium/platform-adapter/` — DELETED (`SKILL.md` + `README.md`).
- `AGENTS.md`, `README.md` — inventory tables, repo tree, install block, pipeline blurb updated; AGENTS.md gained the intentional-duplication convention note.
- `.agent_docs/handoff.md` — refreshed by this end-session run.

**Summary:** Evaluated all `content-creation/linkedin-medium` skills, then acted on four decisions: (1) marked the duplicated hook guide as intentional in both files + `AGENTS.md`; (2) added a `uv` self-install flow to `medium-imager/svg_to_png.py` mirroring `carousel-builder`; (3) folded LinkedIn carousel-copy authoring into `carousel-builder`; (4) removed `platform-adapter` and repointed every reference to the writer skills. Work was orchestrated via parallel subagents partitioned by file ownership. Verified repo-wide `platform-adapter` refs are zero (excluding this handoff), all scripts run, the edited script compiles, and the `--install-missing` path created a venv + produced a PNG end-to-end.

**Outcome:** Repo now has 10 linkedin-medium skills; all changes synced to `~/.config/opencode/skills/` (per-skill `diff -r` clean, `platform-adapter` removed globally). Changes remain uncommitted in the working tree.

### Session: 2026-07-18 (previous)
**Files touched:**
- `tests/content-creation-e2e-broadcast-joins/` — added the user-provided Spark broadcast-vs-shuffle source sample, generated E2E outputs across drafts, LinkedIn, Medium, reviews, voice-tone, tracker log, tutorial verification blocks, carousel SVGs, Medium image SVGs, and wrote `FULL-E2E-EVALUATION.md`.
- `content-creation/linkedin-medium/carousel-builder/` — existing uncommitted SVG/PDF migration files remained in the working tree and were exercised by the E2E test; `spec.py`, `render_svg.py`, `combine_pdf.py`, and SVG templates were used.
- `content-creation/linkedin-medium/medium-imager/` — existing uncommitted new skill files remained in the working tree and were exercised by the E2E test; `spec.py`, `render_svg.py`, `svg_to_png.py`, and `suggest_from_draft.py` were used.
- `.agent_docs/handoff.md` — refreshed by this end-session run.

**Summary:** Ran a subagent-based end-to-end evaluation of all 11 skills under `content-creation/linkedin-medium/` using the supplied Spark broadcast-joins vs shuffle-joins article. The workflow generated a voice profile, 8 idea/draft stubs, claim-linted draft content, content tracker state, LinkedIn and Medium outputs, editorial review artifacts, statically validated tutorial snippets, carousel SVGs, Medium image SVGs, and a consolidated evaluation report. Verification included `claim_lint.py`, `track.py`, `carousel-builder` spec/render checks, `medium-imager` spec/render checks, and `python3 -m py_compile` for helper scripts; PNG export failed as designed because `cairosvg` is not installed.

**Outcome:** E2E evaluation artifacts and findings are captured in `tests/content-creation-e2e-broadcast-joins/FULL-E2E-EVALUATION.md`; no skill source fixes were applied during this evaluation pass, and the prior uncommitted `carousel-builder` plus `medium-imager` work remains in the working tree.

## Open Items / Next Steps
- [ ] Repo working tree — commit this session's changes (10 modified files, 2 deleted `platform-adapter/` files) once reviewed; remove any `__pycache__/` before committing.
- [ ] `content-creation/linkedin-medium/tutorial-verifier/scripts/verify.py` and `content-creation/linkedin-medium/tutorial-verifier/SKILL.md` — add SQL static-validation support and explicit Spark physical-plan/text-block handling.
- [ ] `content-creation/linkedin-medium/medium-imager/scripts/suggest_from_draft.py` — improve stat extraction for plain numeric phrases like `40 minutes instead of 4`, `400 GB`, `50 GB`, `6 MB`, `8 GB`, and `100-500MB`.
- [ ] `content-creation/linkedin-medium/content-tracker/scripts/track.py` and `content-creation/linkedin-medium/content-tracker/README.md` — make active/archive listing semantics explicit, enforce `posted -> archived` unless forced, and escape Markdown table cells.
- [ ] `content-creation/linkedin-medium/draft-builder/scripts/claim_lint.py` — add optional support for `<cite ...>` markers or document marker-contract-only behavior more explicitly.

## Quick Reference
- No build/test/lint pipeline; git operations are the only formal developer commands.
- `AGENTS.md` is authoritative for local agent behavior; read it at session start.
- `.agent_docs/handoff.md` is the rolling session memory file; start next session with `/init-session`.
- Root categories: `agent_session_management/`, `learning/`, `development/`, `content-creation/`.
- Skill convention: every skill must have `SKILL.md` + `README.md`; support folders vary by category.
- Support folder names: `reference/` for learning/session skills, `references/` for development skills, `scripts/` and sometimes `templates/` for content-creation skills.
- `content-creation/linkedin-medium/` now contains **10** skills: `seed-expander`, `draft-builder`, `carousel-builder`, `medium-imager`, `tutorial-verifier`, `editorial-reviewer`, `voice-profiler`, `content-tracker`, `linkedin-writer`, `medium-writer` (`platform-adapter` removed this session).
- Canonical pipeline: `seed-expander → draft-builder → {linkedin-writer, medium-writer} → {carousel-builder, medium-imager, tutorial-verifier} → editorial-reviewer`, with `voice-profiler` + `content-tracker` cross-cutting.
- `linkedin-writer/reference/hook-writing-guide.md` and `medium-writer/reference/hook-writing-guide.md` are intentionally byte-identical; keep both in sync when editing either.
- `carousel-builder` now authors carousel slide copy from a draft/idea AND renders SVG + combined PDF; `cairosvg`/`Pillow` are optional PDF add-ons via `uv` (`combine_pdf.py --install-missing`) after user confirmation.
- `medium-imager` outputs Medium cover/card SVG source plus required PNG; `cairosvg` is required and now self-installs via `uv` on approval (`svg_to_png.py --install-missing`, loop-guarded by `MEDIUM_IMAGER_UV_BOOTSTRAPPED`).
- `medium-imager` commands center on `scripts/spec.py`, `scripts/render_svg.py`, `scripts/svg_to_png.py`, and `scripts/suggest_from_draft.py`.
- Sync a content skill globally with `cp -r content-creation/linkedin-medium/<skill-name> ~/.config/opencode/skills/` (delete the target first for a clean replace; verify with `diff -r`).
- Use `python3 -m py_compile <script>` to syntax-check Python helpers and remove `__pycache__/` before committing.
- "Tested skills only" rule: never add or commit a skill stub that has not been exercised in a real session.
