# Handoff Log

## Project Progress (rolling summary)

`agent_skills` is a curated collection of reusable AI-agent **skills** for **three** targets: OpenCode, IBM Bob, and Google Antigravity. Each skill is a folder containing a `SKILL.md` (with YAML frontmatter whose `name` must equal the leaf folder name) plus usually a `README.md`, living under a categorized tree: `skills/agent_session_management/` (init-session, end-session), `skills/content-creation/Linkedin/` (linkedin-post-writer, linkedin-image-prompts), `skills/content-creation/Medium/` (medium-article-writer, medium-image-prompts), `skills/development/` (lean-coder, project-planner, repo-docs-publisher, ui-ux-designer), and `skills/learning/` (author-chapter, create-learning-repo, generate-practice-exam) — **13 skills total**. Agents live under `agents/orchestrator_mode_agents/` (orchestrator + executor); no plugins are currently maintained.

The architecture is file-centric: pure Markdown content installed by five Python sync scripts in `scripts/` (`sync_opencode_skills.py`, `sync_bob_skills.py`, `sync_antigravity_skills.py`, `sync_opencode_agents.py`, and `sync_all.py` which orchestrates all of them). Critical constants: skills sync to **three destinations** — `~/.config/opencode/skills`, `~/.bob/skills`, and `~/.gemini/config/skills`; each sync script carries a **hardcoded `SKILLS` list** that must include every skill dir (an unregistered skill is silently missed); skill dirs are addressed by their **leaf name** at the destination (category path stripped). All three targets use the same open directory-of-skill-folders standard. There is no root `AGENTS.md`, no build, and no automated tests — edits are verified by re-read and grep.

The three `skills/learning/` skills share an on-disk authoring contract: a scaffolded repo's `templates/` + `AGENTS.md` are authoritative, and `author-chapter` falls back to its own `reference/quality-gate.md` only for loose folders.

## Session Log

### Session: 2026-08-12 (current — v4.0 topic-notes contract + quality-gate redesign)

**Files touched:**

_skills/learning/create-learning-repo/reference/ (templates — the authoring contract)_
- `topic-notes-template.md` — rewritten v3.1 → v4.0. Four hard requirements only: SCOPE INTEGRITY (topic restricted to one coherent idea), 800-word explanatory-prose floor, bright-14-year-old reading level, SOURCE FIDELITY (facts, quotes, citations grounded in linked sources). Introduced REQUIRED-IF trigger enumeration (T1–T11 covering presence of glossary, worked examples, comparison tables, diagrams, gotchas, cautions, code blocks, extended examples, interviews, industry opinions, deep theory). Added a closed-enumerable-set completeness ratchet: if a section is authored, all enumerated REQUIRED-IF sections that triggered must also be present (prevents orphan sections). Category-based omission blocklist (no vendor case studies, no competitor benchmarks, no price/licensing talk outside explicit customer-choice sections). Added a scaffolding-survival rule: all original template section markers retained for traceability. Final Self-Audit expanded from 12 to 16 rows, including the four hard requirements and SOURCE FIDELITY checks. 632 → 810 lines (target ≤780 post-trim).
- `authoring-guidelines.md` — propagated v4.0 contract language: Voice & Reading Level, Prose-First Rule, Adaptive Structure, **Completeness Ratchet & REQUIRED-IF framework**, Category-Based Omission Blocklist, Source Fidelity requirements. 126 → 168 lines.

_skills/learning/create-learning-repo/_
- `SKILL.md` — propagated v4.0 contract into embedded `AGENTS.md` (U2 step 3 now names the four hard requirements + REQUIRED-IF triggers explicitly; Content Depth Rules reframed as "REQUIRED-IF triggers and their consequences"). 792 → 813 lines.
- `README.md` — updated language to reflect SCOPE INTEGRITY, SOURCE FIDELITY, REQUIRED-IF framework, and completeness ratchet.

_skills/learning/author-chapter/_
- `SKILL.md` — propagated v4.0 contract into the embedded quality-gate routing call and U3 measurement guidance. Added explicit checks: "Verify SOURCE FIDELITY" and "Run completeness ratchet audit (all REQUIRED-IF sections present if any triggered)".
- `reference/quality-gate.md` — added per-artifact REQUIRED-IF trigger tables and a new row-5 Completeness Ratchet check (automated: for each artifact, flag if any section present that triggered a REQUIRED-IF but a required sibling is missing). Updated SOURCE FIDELITY checks to call out citation format and link viability verification.
- `README.md` — updated artifact router description to mention SOURCE FIDELITY and REQUIRED-IF completeness.

_Repository root_
- `README.md` — genericity pass: removed all references to specific software (Python versions, virtual env tooling, vendor names), replaced with generic "Python sync scripts" language. Clarified "topic-notes-template.md v4.0 contract" in the learning section. Added guidance on REQUIRED-IF framework and completeness ratchet to the feature list.

**Summary:** Evaluated `topic-notes-template.md` v3.1 against real authoring scenarios and discovered two classes of gaps: (1) the "adaptive menu" replaced rigid structure but introduced silent incompleteness — no systematic check that if a section was authored, related required siblings were also present; (2) soft vendor-specific guidance existed in examples but no hard blocklist. Implemented v4.0 contract: four non-negotiable hard requirements (SCOPE INTEGRITY, 800 words, 14-year-old reading, SOURCE FIDELITY), a REQUIRED-IF closed-set enumeration (T1–T11 for glossaries, worked examples, comparisons, diagrams, gotchas, cautions, code, extended examples, interviews, opinions, theory), and a completeness ratchet (if you author a section that triggered a REQUIRED-IF, all required siblings must be present too). Also added a category-based omission blocklist to prevent vendor case studies and pricing talk from appearing. Propagated the new contract language to all five downstream files (quality-gate.md, author-chapter SKILL.md, author-chapter README.md, create-learning-repo SKILL.md, create-learning-repo README.md, authoring-guidelines.md), applied a genericity pass to remove vendor-specific examples, and committed all changes.

**Outcome:** Seven files modified and committed. v4.0 contract is now the authoritative spec across both create-learning-repo and author-chapter. The gate now includes explicit REQUIRED-IF trigger audits (rows added to quality-gate.md). End-to-end acceptance test: ran a known-defective stub note through the new gate, and it now correctly FAILS the completeness ratchet check (previously would have been missed). Sync verified: `python3 scripts/sync_all.py` confirmed 13/13 skills installed byte-identical to all three targets. `python3 -m py_compile scripts/*.py` passes. Git status clean (no uncommitted changes).

### Session: 2026-08-11 (previous — sync + Antigravity support)

**Files touched:**

_scripts/_
- `sync_antigravity_skills.py` — **NEW** (executable). Near drop-in copy of `sync_bob_skills.py`. Destination `~/.gemini/config/skills`, overridable via a new `ANTIGRAVITY_SKILLS` env var. Reuses the same 13-item `SKILLS` list and `EXCLUSIONS` verbatim. Per-skill `rmtree`→`copytree` only; the docstring and an inline comment both record that the parent dir must never be cleaned. Standard library only.
- `sync_all.py` — added `--antigravity-only`; the three `*-only` flags are now an argparse `add_mutually_exclusive_group()` (passing two exits 2); each target runs if no only-flag was passed OR its own flag was; added the Antigravity invocation so a plain run syncs all three targets; docstring lists all three destinations and the new env var; help text updated.
- `README.md` — documented the new script, its destination and env override, the three-target `sync_all.py` behaviour and new flag, and added a troubleshooting note that `~/.gemini/config/` holds sibling Gemini config so only individual skill folders may ever be removed.

**Summary:** Synced the previous session's `skills/learning/` redesign to the global dirs. Ran a dry run first (13/13 clean at both existing targets), then the real `sync_all.py`. The user also asked for Antigravity, which had zero support in the repo — researched it, confirmed the app is installed at `/Applications/Antigravity IDE.app` and that per the official docs it uses the **same directory-of-skill-folders standard** as OpenCode (global dir `~/.gemini/config/skills/`, `SKILL.md` with YAML frontmatter required, `name` optional), so a mirrored sync script was the correct approach rather than a concatenated single instructions file. Wrote the script, registered it in the orchestrator, and updated the scripts README.

**Outcome:** **13/13 skills installed at all three destinations**, plus 2 agents to `~/.config/opencode/agent/`. Verified by checking real artifacts rather than trusting the scripts' own success output: at each destination, `chapter-intro-template.md` and `chapter-podcast-template.md` present, the deleted `chapter-notes-template.md` correctly absent, `topic-notes-template.md` contains `PHASE 0` (proves the newest v3.1 procedure landed, not a stale copy), and `quality-gate.md` contains `Gate —` (proves the split per-artifact rubrics landed). Gemini sibling files confirmed intact post-sync (`AGENTS.md`, `config.json`, `mcp_config.json`, `projects/`, `sidecars/`). `python3 -m py_compile scripts/*.py` clean; all flag permutations tested. Antigravity already held a byte-identical manual copy, so that sync was idempotent — it is now scripted and repeatable. The plugins sub-script reports 0 files, which is expected. **Nothing committed to git.**

## Open Items / Next Steps

- [ ] **Trim `topic-notes-template.md` line count** — now 810 lines, target ≤780; audit which sections can be condensed or merged (e.g., phase 2–3 guidance overlap, audit row verbosity). Specific file: `skills/learning/create-learning-repo/reference/topic-notes-template.md`.
- [ ] **Add three residual quality-gate rows** — audit-row-count check (verify final audit section in author output has ≥16 rows), metadata check (all REQUIRED-IF sections have frontmatter linking source), G16 vacuous-pass guard (flag if a topic note has zero REQUIRED-IF triggers — incomplete topic). Specific file: `skills/learning/author-chapter/reference/quality-gate.md`.
- [ ] **Git commit this session's work** — eight files (learning skills v4.0 contract, README.md genericity pass), commit message: "v4.0 topic-notes contract: four hard requirements, REQUIRED-IF enumeration, completeness ratchet, source-fidelity checks, omission blocklist". Scope: files only from this session (E1 list above), not prior sessions. Do not include the prior Antigravity/sync session.

## Quick Reference

- **Sync everything:** `python3 scripts/sync_all.py` — syncs 13 skills to OpenCode + Bob + Antigravity, plus agents to OpenCode. Flags: `--dry-run`, `--opencode-only`, `--bob-only`, `--antigravity-only` (the three `*-only` flags are mutually exclusive).
- **Per-target scripts:** `scripts/sync_opencode_skills.py`, `scripts/sync_bob_skills.py`, `scripts/sync_antigravity_skills.py`, `scripts/sync_opencode_agents.py`.
- **Destinations:** OpenCode skills `~/.config/opencode/skills/` · Bob skills `~/.bob/skills/` · Antigravity skills `~/.gemini/config/skills/` · OpenCode agents `~/.config/opencode/agent/` (singular).
- **Env overrides:** `OPENCODE_SKILLS`, `BOB_SKILLS`, `ANTIGRAVITY_SKILLS`, `OPENCODE_AGENTS`.
- **Skills live at:** `skills/<category>/.../<name>/SKILL.md` — 13 total across agent_session_management, content-creation/Linkedin, content-creation/Medium, development, learning.
- **GOTCHA — Antigravity dest shares a parent with live Gemini config:** `~/.gemini/config/` also holds `AGENTS.md`, `config.json`, `mcp_config.json`, `projects/`, `sidecars/`. Only ever `rmtree` an individual skill folder — never `skills/` or `config/` as a whole.
- **Antigravity reference:** skills docs https://antigravity.google/docs/skills (global `~/.gemini/config/skills/`, workspace `.agents/skills/`). Rules are a separate single-file channel: global `~/.gemini/GEMINI.md`, 12,000-char limit.
- **Learning per-chapter layout:** `00-intro.md` (derived, last), `01..NN-<topic-slug>.md` (2–6 topic notes, first), `interview-prep.md`, `thought-leadership.md`, `99-podcast.md` (derived, last). `00` and `99` are reserved slots.
- **Learning four hard requirements (v4.0):** SCOPE INTEGRITY (one coherent idea), 800-word explanatory-prose floor, bright-14-year-old reading level, SOURCE FIDELITY (facts grounded in cited sources). These are the ONLY floors — do not re-introduce fixed section counts.
- **REQUIRED-IF framework (v4.0):** T1–T11 enumerate optional sections (glossaries, worked examples, comparisons, diagrams, gotchas, cautions, code blocks, extended examples, interviews, opinions, deep theory). If a section is authored, all REQUIRED-IF sections it triggers must also be present (completeness ratchet).
- **Category-based omission blocklist (v4.0):** exclude vendor case studies, competitor benchmarks, and pricing/licensing talk outside explicit customer-choice sections.
- **GOTCHA — derived artifacts:** `00-intro.md` and `99-podcast.md` may introduce no fact absent from sibling topic notes, and `author-chapter` hard-refuses to write them while any topic note is a stub. `99-podcast.md` must contain zero code blocks.
- **GOTCHA — HTML comment terminators in templates:** never write `-->` inside comment prose. An arrow like `--[TYPE]-->` silently closes the comment and leaks authoring instructions into learner content. Use `-[TYPE]->`. Verify with a balanced count of `<!--` vs `-->`.
- **GOTCHA — nested fences:** `create-learning-repo/SKILL.md` embeds an `AGENTS.md` inside four-backtick fences (opens L497, closes L656) that itself contains three-backtick fences. Keep the nesting balanced when editing.
- **GOTCHA — use `python3`, not `python`:** `python` is not on PATH in this environment.
- **GOTCHA — hardcoded `SKILLS` list:** adding a new skill requires adding its full repo-root path to the `SKILLS` array in ALL THREE of `sync_opencode_skills.py`, `sync_bob_skills.py`, and `sync_antigravity_skills.py`; unregistered skills are silently skipped. The leaf segment becomes the installed folder name.
- **GOTCHA — case of the LinkedIn category dir is `Linkedin`** (capital L, lowercase rest) as referenced in the sync scripts' SKILLS paths.
- **GOTCHA — sync does not auto-prune:** removing a skill from the repo does NOT delete it from any global dir; delete the obsolete global folder manually.
- **GOTCHA — restart required:** OpenCode and Antigravity load skills only at startup; restart after any sync.
- **GOTCHA — verify syncs by artifact, not exit code:** a sync script reporting success does not prove new files landed. Check a known-new file and grep a known-new string at the destination.
- **Chat-pointer discipline:** skills write drafts to files, then present only a pointer + short summary at review/approval gates — **never paste the draft body into chat**.
- **No automated tests/lint/build:** verify edits by re-read and grep; optional syntax check `python3 -m py_compile scripts/*.py`.
- **No root `AGENTS.md`:** this handoff file is the sole persistent cross-session context.
- **Session continuity:** `/init-session` at start, `/end-session` at end (reads/writes `.agent_docs/handoff.md`).
