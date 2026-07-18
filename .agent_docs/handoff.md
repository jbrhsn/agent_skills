# Handoff Log

## Project Summary

`agent_skills` is a curated collection of portable AI-agent skill files (`SKILL.md`) for OpenCode and other coding/content assistants. The repo has no build system, dependencies, CI, or formal test suite; it is mostly Markdown content plus small standard-library Python helper scripts for skills that need executable behavior. The live categories are `learning/`, `agent_session_management/`, `development/`, and `content-creation/`. Key artifacts are each skill's `SKILL.md`, human-facing `README.md`, optional support folders (`reference/`, `references/`, `scripts/`, `templates/`), root `AGENTS.md` for authoritative local rules, and `.agent_docs/handoff.md` for session continuity.

Architecture is file-oriented: every skill is independently installable by copying its folder into `~/.config/opencode/skills/` or `.opencode/skills/`. Learning/session skills use `reference/`; development skills use `references/`; content-creation skills use `scripts/`, and `carousel-builder`/`medium-imager` also use SVG `templates/`. Critical constants: every skill requires `SKILL.md` + `README.md`; never add untested stubs; every phase of a multi-phase skill ends with an explicit confirmation gate; `AGENTS.md` is gitignored but authoritative; `medium-imager` treats `cairosvg` as required because PNG output is the Medium deliverable, while `carousel-builder` uses `cairosvg`/`Pillow` as optional PDF add-ons installed through `uv` after user confirmation.

## Session Log

### Session: 2026-07-18 (current)
**Files touched:**
- `content-creation/linkedin-medium/carousel-builder/` — updated `scripts/combine_pdf.py`, `SKILL.md`, and `README.md` so missing `cairosvg`/`Pillow` dependencies are handled through a user-confirmed `uv` `.venv` setup path; existing SVG/PDF migration files remain in the working tree.
- `tests/content-creation-e2e-broadcast-joins/` — created `.venv` with `uv`, installed `cairosvg` and `pillow`, and generated `carousel/broadcast-joins-vs-shuffle-joins.pdf` from the existing 8 SVG slides.
- `~/.config/opencode/skills/` — replaced/synced all 11 global `content-creation/linkedin-medium` skills from the repo using `rsync -a --delete --exclude '__pycache__/'`; checksum dry-run showed no remaining differences.
- `.agent_docs/handoff.md` — refreshed by this end-session run.

**Summary:** Created the requested carousel PDF with `uv` dependency management and updated `carousel-builder` so agents can ask for confirmation, then run `combine_pdf.py --install-missing` to create/reuse `.venv`, install `cairosvg pillow` through `uv`, and rerun PDF generation. Verified the updated script with `python3 -m py_compile` and a successful `--install-missing` PDF generation run. Copied/replaced the global content-creation skills and then verified global contents match the latest repo copies by checksum, excluding generated `__pycache__/` directories.

**Outcome:** Carousel PDF generation now works in the test workspace, the global OpenCode content skills are current with this repo, and the updated `carousel-builder` dependency behavior remains uncommitted in the repo working tree.

### Session: 2026-07-18 (previous)
**Files touched:**
- `tests/content-creation-e2e-broadcast-joins/` — added the user-provided Spark broadcast-vs-shuffle source sample, generated E2E outputs across drafts, LinkedIn, Medium, reviews, voice-tone, tracker log, tutorial verification blocks, carousel SVGs, Medium image SVGs, and wrote `FULL-E2E-EVALUATION.md`.
- `content-creation/linkedin-medium/carousel-builder/` — existing uncommitted SVG/PDF migration files remained in the working tree and were exercised by the E2E test; `spec.py`, `render_svg.py`, `combine_pdf.py`, and SVG templates were used.
- `content-creation/linkedin-medium/medium-imager/` — existing uncommitted new skill files remained in the working tree and were exercised by the E2E test; `spec.py`, `render_svg.py`, `svg_to_png.py`, and `suggest_from_draft.py` were used.
- `.agent_docs/handoff.md` — refreshed by this end-session run.

**Summary:** Ran a subagent-based end-to-end evaluation of all 11 skills under `content-creation/linkedin-medium/` using the supplied Spark broadcast-joins vs shuffle-joins article. The workflow generated a voice profile, 8 idea/draft stubs, claim-linted draft content, content tracker state, LinkedIn and Medium outputs, editorial review artifacts, statically validated tutorial snippets, carousel SVGs, Medium image SVGs, and a consolidated evaluation report. Verification included `claim_lint.py`, `track.py`, `carousel-builder` spec/render checks, `medium-imager` spec/render checks, and `python3 -m py_compile` for helper scripts; PNG export failed as designed because `cairosvg` is not installed.

**Outcome:** E2E evaluation artifacts and findings are captured in `tests/content-creation-e2e-broadcast-joins/FULL-E2E-EVALUATION.md`; no skill source fixes were applied during this evaluation pass, and the prior uncommitted `carousel-builder` plus `medium-imager` work remains in the working tree.

## Open Items / Next Steps
- [ ] `content-creation/linkedin-medium/medium-writer/SKILL.md` and `content-creation/linkedin-medium/medium-writer/README.md` — define language-specific unverified-code labeling for SQL/text blocks and fix the README typo that says the skill is LinkedIn-only.
- [ ] `content-creation/linkedin-medium/tutorial-verifier/scripts/verify.py` and `content-creation/linkedin-medium/tutorial-verifier/SKILL.md` — add SQL static-validation support and explicit Spark physical-plan/text-block handling.
- [ ] `content-creation/linkedin-medium/medium-imager/scripts/suggest_from_draft.py` — improve stat extraction for plain numeric phrases like `40 minutes instead of 4`, `400 GB`, `50 GB`, `6 MB`, `8 GB`, and `100-500MB`.
- [ ] `content-creation/linkedin-medium/content-tracker/scripts/track.py` and `content-creation/linkedin-medium/content-tracker/README.md` — make active/archive listing semantics explicit, enforce `posted -> archived` unless forced, and escape Markdown table cells.
- [ ] `content-creation/linkedin-medium/draft-builder/scripts/claim_lint.py` — add optional support for `<cite ...>` markers or document marker-contract-only behavior more explicitly.
- [ ] `content-creation/linkedin-medium/linkedin-writer/README.md`, `content-creation/linkedin-medium/linkedin-writer/SKILL.md`, `content-creation/linkedin-medium/medium-writer/README.md`, and `content-creation/linkedin-medium/medium-writer/SKILL.md` — align missing `voice-tone/` behavior between README and skill instructions.

## Quick Reference
- No build/test/lint pipeline; git operations are the only formal developer commands.
- `AGENTS.md` is gitignored but authoritative for local agent behavior; read it at session start and do not expect it to stage.
- `.agent_docs/handoff.md` is the rolling session memory file; start next session with `/init-session`.
- Root categories: `agent_session_management/`, `learning/`, `development/`, `content-creation/`.
- Skill convention: every skill must have `SKILL.md` + `README.md`; support folders vary by category.
- Support folder names: `reference/` for learning/session skills, `references/` for development skills, `scripts/` and sometimes `templates/` for content-creation skills.
- `content-creation/linkedin-medium/` currently contains 11 skills: `seed-expander`, `draft-builder`, `platform-adapter`, `carousel-builder`, `medium-imager`, `tutorial-verifier`, `editorial-reviewer`, `voice-profiler`, `content-tracker`, `linkedin-writer`, `medium-writer`.
- Install/sync content skills globally with `rsync -a --delete --exclude '__pycache__/' content-creation/linkedin-medium/<skill-name>/ ~/.config/opencode/skills/<skill-name>/`.
- `carousel-builder` outputs LinkedIn carousel SVG files and combines to PDF with `cairosvg` + `Pillow`; if missing, ask the user before running `combine_pdf.py --install-missing` to create/reuse `.venv` with `uv`.
- `medium-imager` outputs Medium cover/card SVG source plus required PNG files; `cairosvg` is required for completion.
- `medium-imager` commands center on `scripts/spec.py`, `scripts/render_svg.py`, `scripts/svg_to_png.py`, and `scripts/suggest_from_draft.py`.
- E2E evaluation artifacts for the Spark broadcast/shuffle sample live under `tests/content-creation-e2e-broadcast-joins/`, with the consolidated report at `FULL-E2E-EVALUATION.md` and carousel PDF at `carousel/broadcast-joins-vs-shuffle-joins.pdf`.
- Use `python3 -m py_compile <script>` to syntax-check Python helpers and remove `__pycache__/` before committing.
- "Tested skills only" rule: never add or commit a skill stub that has not been exercised in a real session.
