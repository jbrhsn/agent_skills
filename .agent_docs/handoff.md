# Handoff Log

## Project Progress (rolling summary)

_Last updated: 2026-07-17_

**Current phase:** `content-creation/linkedin-medium/` skill suite — deep evaluation cycle (3 test runs), bug fixes, and SKILL.md design-gap fixes — **Status:** all fixes applied, NOT yet committed.

**Now:** `HEAD` = `7be9ca6` on `main`. Working tree has **20 modified files** (staged as M) — all changes from this session are uncommitted. The `content-creation/linkedin-medium/` category now has 11 skills (original 8 + `hooks-drafter`, `linkedin-writer`, `medium-writer` added in a prior session). This session ran three full evaluation passes with parallel subagents, identified and fixed 8 script bugs + 15 SKILL.md design gaps (v1 report), verified all fixes via re-test (v2 report, Databricks DLT anchor), ran a full end-to-end pipeline test in third-person voice (v3 test, Databricks cost optimization), and fixed 5 additional issues surfaced by that test.

**Project summary:** `agent_skills` is a curated collection of portable AI-agent skill files (`SKILL.md`) for OpenCode and other assistants. No build system, tests, or CI — pure Markdown plus stdlib-only Python helpers. Four live categories: `learning/`, `agent_session_management/`, `development/`, `content-creation/`. Convention: one skill = `SKILL.md` + `README.md` + optional support dir. `content-creation/linkedin-medium/` uses `scripts/` (and `templates/` for `carousel-builder`) instead of `reference/`. Handoff is the cross-session memory layer, rolling 2-session window. `AGENTS.md` at repo root is gitignored.

**Critical constants:**
- `AGENTS.md` is **gitignored** — exists on disk, never stages. `git check-ignore AGENTS.md` confirms.
- Support-dir naming: `reference/` (learning + session), `references/` (development), `scripts/`+`templates/` (content-creation).
- Scripts are stdlib-only Python. `cairosvg` + headless browser are optional PNG add-ons (degrade gracefully).
- `track.py` flag placement: `--json` is a **subparser flag**, not global — use `track.py list --json`, not `--json list` (fixed this session).
- `verify.py` exit codes: 0 pass, 1 fail/refused, 2 usage error, 3 unknown (cluster-only module or no runtime).
- "Tested skills only" rule: skills must be exercised before commit.

**Progress so far:**
- Sessions 1–5 — Repo initialized; `learning/` + `agent_session_management/` scaffolded. Commits `7773121`–`41799a1`.
- Sessions 6–7 (2026-07-09) — Gitignored `AGENTS.md`; quality audit + READMEs + phase gates. `26dbb95`.
- Session 8 (2026-07-11) — `development/` evaluated, fixed, committed (`8cdaad0`).
- Session 9 (2026-07-11) — `content-creation/linkedin-medium/` (8 skills) evaluated + fixed + committed (`7e21e80`).
- Prior to this session — `hooks-drafter`, `linkedin-writer`, `medium-writer` added (commits up to `7be9ca6`).
- **Session 10 (2026-07-17, this session)** — Full evaluation cycle on all 11 skills; 8 script bugs + 15+5 SKILL.md gaps fixed; three test repos produced under `tests/`. All changes uncommitted.

**Next up:** Commit all 20 modified files. Suggested message: `"fix(content-creation): evaluation-driven bug fixes and design-gap patches across 11 skills"`. Then optionally `git push`.

---

## Session Log

### Session: 2026-07-17 (current) — Full evaluation + fix cycle for all 11 content-creation skills

**Files touched:**
- `content-creation/linkedin-medium/draft-builder/scripts/claim_lint.py` — B1 (study stopword guard), B2 (bare-number ≤10 suppression), B3 (inline backtick span stripping), B4 (line-level limitation documented)
- `content-creation/linkedin-medium/carousel-builder/scripts/spec.py` — B5 (`--json` path now exits 3 on overflow)
- `content-creation/linkedin-medium/carousel-builder/templates/slide-{glassmorphism,linkedin,mario,minimal-light,neomorphism,neon}.html` — B6 (CSS comment placeholder pollution removed from 6/7 templates)
- `content-creation/linkedin-medium/content-tracker/scripts/track.py` — B7 (`--json` moved to subparsers), G14 (`archive` subcommand added)
- `content-creation/linkedin-medium/tutorial-verifier/scripts/verify.py` — B8 (`eval` denylist tightened; NI-7 cluster-only `ModuleNotFoundError` reclassified as UNKNOWN not FAIL)
- `content-creation/linkedin-medium/voice-profiler/SKILL.md` — G1 (contradictory-sample guidance), G2 (ISO date format), G3 (min sample count)
- `content-creation/linkedin-medium/seed-expander/SKILL.md` — G4 (angle distribution), G5 (overwrite in Step 5), G6 (research minimum 4 sources)
- `content-creation/linkedin-medium/draft-builder/SKILL.md` — G7 (`--section` vs `--whole-file` guidance)
- `content-creation/linkedin-medium/editorial-reviewer/SKILL.md` — G8 (AI-voice fallback), G9 (length check), G10 (preserve claim markers); B4 (non-interactive note)
- `content-creation/linkedin-medium/carousel-builder/SKILL.md` — G15 (JSON field validation)
- `content-creation/linkedin-medium/hooks-drafter/SKILL.md` — G12 cross-ref to linkedin/medium-writer; B5 (third-person Story-in-motion claim note)
- `content-creation/linkedin-medium/linkedin-writer/SKILL.md` — G11 (voice-tone soft gate), G12 (hooks-drafter cross-ref), B3 (pre-publish marker cleanup), B4 (non-interactive note)
- `content-creation/linkedin-medium/platform-adapter/SKILL.md` — B3 (pre-publish marker cleanup), B4 (non-interactive note)
- `content-creation/linkedin-medium/medium-writer/SKILL.md` — G11, G12, G13 (pull-quote Short Article exclusion), B1 (third-person title rule), B4 (non-interactive note)
- `content-creation/linkedin-medium/tutorial-verifier/SKILL.md` — B2 (HTTP API snippet guidance)
- `tests/EVALUATION-REPORT.md` — v1 evaluation report (8 bugs + 15 gaps, collection 8.5/10)
- `tests/EVALUATION-REPORT-V2.md` — v2 re-evaluation report (Databricks DLT anchor, collection 8.7/10, all fixes confirmed)
- `tests/content-creation-test/` — v1 test repo (22 files, code-review-bullets anchor)
- `tests/content-creation-test-v2/` — v2 test repo (26 files, DLT data quality anchor)
- `tests/content-creation-test-v3/` — v3 test repo (22 files, Databricks cost optimization, third-person voice)

**Summary:** Ran three sequential evaluation passes on all 11 `content-creation/linkedin-medium/` skills using parallel subagents. V1 test (code-review-bullets anchor) identified 8 confirmed script bugs and 15 SKILL.md design gaps. All 23 issues were fixed via 9 targeted subagents. V2 re-test (Databricks DLT anchor) confirmed all 8 script bugs and 15 gaps resolved; scored the collection 8.7/10 (+0.2 from v1); surfaced 9 new lower-priority issues including NI-7 (cluster-only `ModuleNotFoundError`). NI-7 was fixed immediately (verify.py `CLUSTER_ONLY_MODULES` set + reclassification to UNKNOWN). V3 full end-to-end pipeline test (Databricks cost optimization, third-person voice, all 11 skills sequential) scored 8.5/10 and surfaced 5 more issues (B1–B5); all 5 fixed via 3 parallel subagents.

**Outcome:** 20 files modified, all verified working. All fixes committed-ready but **NOT yet committed**. Working tree is clean except for the 20 modified tracked files.

---

### Session: 2026-07-11 (previous) — Evaluate + fix + commit `content-creation/linkedin-medium` skills

**Files touched:**
- `AGENTS.md` (gitignored — structure diagram, live-categories line, `scripts/`/`templates/` note, skill inventory table +8 rows, "One skill =" convention, install commands all extended for `content-creation/`)
- `content-creation/linkedin-medium/*/README.md` — 8 new READMEs (seed-expander, draft-builder, platform-adapter, carousel-builder, tutorial-verifier, editorial-reviewer, voice-profiler, content-tracker)
- `content-creation/linkedin-medium/draft-builder/scripts/claim_lint.py` — attribution detector now captures the subject and skips common sentence openers via `ATTRIBUTION_STOPWORDS`
- `content-creation/linkedin-medium/tutorial-verifier/scripts/verify.py` — failed/unavailable dependency installs now surface "DEPENDENCY INSTALL FAILED" instead of silently degrading to static

**Summary:** Evaluated the 8-skill LinkedIn/Medium content pipeline and rated it 88/100. Fixed all identified gaps: wrote 8 missing per-skill READMEs; refined `claim_lint.py`; made `verify.py` surface failed dependency installs honestly; registered the whole category in `AGENTS.md`; cleaned up `.pyc`.

**Outcome:** All fixes complete, verified, and committed as `7e21e80` (30 files, 4317 insertions). `AGENTS.md` edits on disk but excluded (gitignored). Commit was local-only at that point.

---

## Open Items / Next Steps

- [ ] `content-creation/linkedin-medium/` — commit the 20 modified files: `git add content-creation/linkedin-medium/ tests/EVALUATION-REPORT.md tests/EVALUATION-REPORT-V2.md && git commit -m "fix(content-creation): evaluation-driven bug fixes and design-gap patches across 11 skills"`
- [ ] After commit — optionally `git push` to publish

---

## Quick Reference

- **No build/test/lint pipeline** — git operations are the only meaningful commands.
- **`AGENTS.md` is gitignored** — edit/read normally, never stages. `git check-ignore AGENTS.md` confirms.
- **Repo layout:** `learning/`, `agent_session_management/`, `development/`, `content-creation/` at root; `.agent_docs/handoff.md` = session memory; `tests/` = evaluation test repos.
- **Skill structure:** `SKILL.md` + `README.md` + optional support dir. `reference/` (learning/session), `references/` (development), `scripts/`+`templates/` (content-creation).
- **11 live content-creation skills:** `seed-expander`, `draft-builder`, `platform-adapter`, `carousel-builder`, `tutorial-verifier`, `editorial-reviewer`, `voice-profiler`, `content-tracker`, `hooks-drafter`, `linkedin-writer`, `medium-writer`.
- **Pipeline order:** `voice-profiler` → `seed-expander` → `draft-builder` → [`hooks-drafter`] → `linkedin-writer` / `medium-writer` / `platform-adapter` → [`carousel-builder`, `tutorial-verifier`] → `editorial-reviewer`; `content-tracker` cross-cutting.
- **Key scripts:** `claim_lint.py` (exit 0/1/2), `verify.py` (exit 0/1/2/3; 3 = UNKNOWN/cluster-only), `track.py` (add/update/list/archive/render), `spec.py`+`render_svg.py`+`render_html.py`+`svg_to_png.py`.
- **`track.py` flag placement:** `--json` is per-subparser — `track.py list --json` ✓, NOT `--json list`.
- **`verify.py` cluster-only packages:** `pyspark`, `delta`, `databricks`, `dlt`, `mlflow`, `torch`, `jax` → `STATUS: UNKNOWN (exit 3)`, not FAIL.
- **Lint a draft stub section only:** `python3 .../claim_lint.py drafts/<slug>.md --section Draft`
- **Verify scripts:** `python3 -m py_compile <script>` to syntax-check. Clean `__pycache__/` before committing.
- **Install a skill:** `cp -r content-creation/linkedin-medium/<skill> ~/.config/opencode/skills/` (global) or `.opencode/skills/` (per-project).
- **"Tested skills only" rule** — exercise a skill in a real session before committing it.
- **Current `HEAD`:** `7be9ca6`. Working tree: 20 modified files, uncommitted.
- **Restore this context next session with `/init-session`.**
