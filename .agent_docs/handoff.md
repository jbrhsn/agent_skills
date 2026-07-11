# Handoff Log

## Project Progress (rolling summary)

_Last updated: 2026-07-11_

**Current phase:** New `content-creation/linkedin-medium/` skill category — evaluation, fixes, documentation, and commit — **Status:** phase complete, committed
**Now:** `HEAD` = `7e21e80` on `main` (not yet pushed). The `content-creation/linkedin-medium/` category is committed: 8 skills (`seed-expander`, `draft-builder`, `platform-adapter`, `carousel-builder`, `tutorial-verifier`, `editorial-reviewer`, `voice-profiler`, `content-tracker`), each with `SKILL.md` + `README.md`, plus stdlib-only `scripts/` and (for `carousel-builder`) 7 HTML `templates/`. This session evaluated the suite (88/100), fixed two scripts, wrote the 8 missing READMEs, registered the category in `AGENTS.md`, removed `__pycache__` cruft, and committed everything except the gitignored `AGENTS.md`.

**Project summary:** `agent_skills` is a curated collection of portable AI-agent skill files (`SKILL.md`) for OpenCode and other assistants. No build system, tests, or CI — pure Markdown plus a few stdlib-only Python helpers. Four live categories: `learning/`, `agent_session_management/`, `development/`, and `content-creation/`. Convention: one skill = `SKILL.md` (agent-facing) + `README.md` (human guide) + optional support dir. Learning/session skills use `reference/` (singular); development skills use `references/` (plural); `content-creation/linkedin-medium/` skills use `scripts/` (and `templates/` for `carousel-builder`) instead. Handoff is the cross-session memory layer (`.agent_docs/handoff.md`), rolling 2-session window.

**Critical constants:**
- `AGENTS.md` is **gitignored** — it exists on disk, is edited/read normally, but never appears in `git status` and **cannot be committed** without first removing it from `.gitignore`. Do not attempt to `git add AGENTS.md` and expect it to stage.
- Support-dir naming differs by category: `reference/` (learning + session), `references/` (development), `scripts/`+`templates/` (content-creation). Match whichever the skill already uses.
- `content-creation` scripts are standard-library Python only; `cairosvg` and a headless browser are OPTIONAL PNG-only add-ons that degrade gracefully.
- "Tested skills only" rule: skills must be exercised in a real session before commit.

**Progress so far:**
- Sessions 1–5 — Repo initialized; skills scaffolded/rearranged into `learning/` + `agent_session_management/`. Commits `7773121`–`41799a1`.
- Session 6–7 (2026-07-09) — Gitignored `AGENTS.md`; quality audit + per-skill READMEs + phase gates + `end-session` Linux fallback. Folded into `26dbb95`.
- Session 8 (2026-07-11) — `development/` category evaluated, fixed, documented, committed (`8cdaad0`).
- Session 9 (2026-07-11) — `content-creation/linkedin-medium/` evaluated, fixed, documented, committed (`7e21e80`) (this session).

**Next up:** Optionally `git push` (commit `7e21e80` is local-only). No other open work from this session.

---

## Session Log

### Session: 2026-07-11 (current) — Evaluate + fix + commit `content-creation/linkedin-medium` skills

**Files touched:**
- `AGENTS.md` (gitignored — structure diagram, live-categories line, `scripts/`/`templates/` note, skill inventory table +8 rows, "One skill =" convention, install commands all extended for `content-creation/`)
- `content-creation/linkedin-medium/*/README.md` — 8 new READMEs (seed-expander, draft-builder, platform-adapter, carousel-builder, tutorial-verifier, editorial-reviewer, voice-profiler, content-tracker)
- `content-creation/linkedin-medium/draft-builder/scripts/claim_lint.py` — attribution detector now captures the subject and skips common sentence openers via `ATTRIBUTION_STOPWORDS` (fewer false positives; still catches named sources like "Gartner estimates")
- `content-creation/linkedin-medium/tutorial-verifier/scripts/verify.py` — failed/unavailable dependency installs (Python + JS) now surface "DEPENDENCY INSTALL FAILED (deps NOT installed) — snippet was NOT executed" instead of silently degrading to static
- Removed `carousel-builder/scripts/__pycache__/` cruft (already gitignored)

**Summary:** Evaluated the 8-skill LinkedIn/Medium content pipeline and rated it 88/100. Fixed all identified gaps: wrote the 8 missing per-skill READMEs (delegated to 3 parallel `general` subagents, matching the `lean-coder` house style, with correct `content-creation/linkedin-medium/<skill>` install paths); refined `claim_lint.py` to reduce attribution over-flagging; made `verify.py` surface failed dependency installs honestly; registered the whole category in `AGENTS.md`; and cleaned up the committed `.pyc`. All scripts byte-compile and pass a functional smoke test (claim_lint FAIL/PASS, verify python PASS + shell REFUSED, spec, tracker).

**Outcome:** All fixes complete, verified, and **committed** as `7e21e80` (30 files, 4317 insertions). `AGENTS.md` edits are on disk but excluded from the commit (gitignored). Commit is local-only — not yet pushed.

### Session: 2026-07-11 (previous) — Evaluate + fix `development/` skills

**Files touched:**
- `AGENTS.md` (gitignored — structure diagram, live-categories line, skill inventory table, install commands all extended for `development/`)
- `development/lean-coder/` — `SKILL.md` (Python section de-duplicated to point at `references/python-uv.md`), new `README.md`
- `development/project-planner/` — new `README.md`
- `development/repo-docs-publisher/` — `references/secrets-scan-checklist.md` (refreshed secret regexes), new `README.md`
- `development/ui-ux-designer/` — new `README.md`

**Summary:** Evaluated the 4 `development/` skills against repo conventions and rated them (91/100). Fixed all identified issues: wrote the 4 missing per-skill READMEs (4 parallel `general` subagents); de-duplicated the inline Python/`uv` content in `lean-coder/SKILL.md` so it points to `references/python-uv.md`; refreshed the secret-detection regexes in `repo-docs-publisher/references/secrets-scan-checklist.md` (added `sk-proj-`, Google `AIza…`, AWS secret-key patterns); registered the `development/` category in `AGENTS.md`.

**Outcome:** All fixes complete and verified; committed in the following session as `8cdaad0` ("development skills added"). `AGENTS.md` excluded (gitignored).

---

## Open Items / Next Steps

No open items from this session. (Optional, not a coding task: `git push` to publish local commit `7e21e80`.)

---

## Quick Reference

- **No build/test/lint pipeline** — git operations are the only meaningful commands; scripts are stdlib-only Python.
- **`AGENTS.md` is gitignored** — edit/read it normally, but it never stages or commits. `git check-ignore AGENTS.md` returns it.
- **Repo layout:** `learning/`, `agent_session_management/`, `development/`, `content-creation/` categories at root; `.agent_docs/handoff.md` = session memory.
- **Skill structure:** `SKILL.md` + `README.md` + optional support dir. `reference/` (learning/session), `references/` (development), `scripts/`+`templates/` (content-creation).
- **`content-creation/linkedin-medium/` pipeline:** `seed-expander` → `draft-builder` → `platform-adapter` → {`carousel-builder`, `tutorial-verifier`} → `editorial-reviewer`, with `voice-profiler` + `content-tracker` as cross-cutting support.
- **Key scripts:** `draft-builder/scripts/claim_lint.py` (claim-integrity gate; exit 0/1/2), `tutorial-verifier/scripts/verify.py` (isolated code verify; exit 0/1/2/3; NOT a security sandbox), `content-tracker/scripts/track.py` (add/update/list/render), `carousel-builder/scripts/{spec,render_svg,render_html,svg_to_png}.py`.
- **Verify scripts:** `python3 -m py_compile <script>` to syntax-check; they run with plain `python3`. Clean up any `__pycache__/` before committing (gitignored, but `spec.py` imports `render_svg` and regenerates it).
- **Install a skill (from repo root):** `cp -r content-creation/linkedin-medium/<skill> ~/.config/opencode/skills/` (global) or `.opencode/skills/` (per-project); Windows: `Copy-Item -Recurse content-creation\linkedin-medium\<skill> "$env:USERPROFILE\.config\opencode\skills\"`.
- **"Tested skills only" rule** — exercise a skill in a real session before committing it.
- **Current `HEAD`:** `7e21e80` (local-only, unpushed). Working tree clean.
- **Restore this context next session with `/init-session`.**
