# Handoff Log

## Project Progress (rolling summary)

`agent_skills` is a curated collection of reusable AI-agent **skills** for **three** targets: OpenCode, IBM Bob, and Google Antigravity. Each skill is a folder containing a `SKILL.md` (with YAML frontmatter whose `name` must equal the leaf folder name) plus usually a `README.md`, living under a categorized tree: `skills/agent_session_management/` (init-session, end-session), `skills/content-creation/Linkedin/` (linkedin-post-writer, linkedin-image-prompts), `skills/content-creation/Medium/` (medium-article-writer, medium-image-prompts), `skills/development/` (lean-coder, project-planner, repo-docs-publisher, ui-ux-designer), and `skills/learning/` (author-chapter, create-learning-repo, generate-practice-exam) — **13 skills total**. Agents live under `agents/orchestrator_mode_agents/` (orchestrator + executor); no plugins are currently maintained.

The architecture is file-centric: pure Markdown content installed by five Python sync scripts in `scripts/` (`sync_opencode_skills.py`, `sync_bob_skills.py`, `sync_antigravity_skills.py`, `sync_opencode_agents.py`, and `sync_all.py` which orchestrates all of them). Critical constants: skills sync to **three destinations** — `~/.config/opencode/skills`, `~/.bob/skills`, and `~/.gemini/config/skills`; each sync script carries a **hardcoded `SKILLS` list** that must include every skill dir (an unregistered skill is silently missed); skill dirs are addressed by their **leaf name** at the destination (category path stripped). All three targets use the same open directory-of-skill-folders standard. There is no root `AGENTS.md`, no build, and no automated tests — edits are verified by re-read and grep.

The three `skills/learning/` skills share an on-disk authoring contract: a scaffolded repo's `templates/` + `AGENTS.md` are authoritative, and `author-chapter` falls back to its own `reference/quality-gate.md` only for loose folders.

## Session Log

### Session: 2026-08-11 (current — sync + Antigravity support)
**Files touched:**

_scripts/_
- `sync_antigravity_skills.py` — **NEW** (executable). Near drop-in copy of `sync_bob_skills.py`. Destination `~/.gemini/config/skills`, overridable via a new `ANTIGRAVITY_SKILLS` env var. Reuses the same 13-item `SKILLS` list and `EXCLUSIONS` verbatim. Per-skill `rmtree`→`copytree` only; the docstring and an inline comment both record that the parent dir must never be cleaned. Standard library only.
- `sync_all.py` — added `--antigravity-only`; the three `*-only` flags are now an argparse `add_mutually_exclusive_group()` (passing two exits 2); each target runs if no only-flag was passed OR its own flag was; added the Antigravity invocation so a plain run syncs all three targets; docstring lists all three destinations and the new env var; help text updated.
- `README.md` — documented the new script, its destination and env override, the three-target `sync_all.py` behaviour and new flag, and added a troubleshooting note that `~/.gemini/config/` holds sibling Gemini config so only individual skill folders may ever be removed.

**Summary:** Synced the previous session's `skills/learning/` redesign to the global dirs. Ran a dry run first (13/13 clean at both existing targets), then the real `sync_all.py`. The user also asked for Antigravity, which had zero support in the repo — researched it, confirmed the app is installed at `/Applications/Antigravity IDE.app` and that per the official docs it uses the **same directory-of-skill-folders standard** as OpenCode (global dir `~/.gemini/config/skills/`, `SKILL.md` with YAML frontmatter required, `name` optional), so a mirrored sync script was the correct approach rather than a concatenated single instructions file. Wrote the script, registered it in the orchestrator, and updated the scripts README.

**Outcome:** **13/13 skills installed at all three destinations**, plus 2 agents to `~/.config/opencode/agent/`. Verified by checking real artifacts rather than trusting the scripts' own success output: at each destination, `chapter-intro-template.md` and `chapter-podcast-template.md` present, the deleted `chapter-notes-template.md` correctly absent, `topic-notes-template.md` contains `PHASE 0` (proves the newest v3.1 procedure landed, not a stale copy), and `quality-gate.md` contains `Gate —` (proves the split per-artifact rubrics landed). Gemini sibling files confirmed intact post-sync (`AGENTS.md`, `config.json`, `mcp_config.json`, `projects/`, `sidecars/`). `python3 -m py_compile scripts/*.py` clean; all flag permutations tested. Antigravity already held a byte-identical manual copy, so that sync was idempotent — it is now scripted and repeatable. The plugins sub-script reports 0 files, which is expected. **Nothing committed to git.**

### Session: 2026-08-11 (previous — learning-skills redesign)
**Files touched:**

_skills/learning/create-learning-repo/reference/ (templates — the authoring contract)_
- `topic-notes-template.md` — rewritten v2.0 → v3.0 → v3.1. Rigid 11-section order and all fixed counts removed; now a 17-entry **menu of suggested sections**. Three hard requirements only: Coverage Plan, 800-word explanatory-prose floor, bright-14-year-old reading level. 44-row audit replaced by a 12-row evidence-bearing Final Self-Audit. v3.1 added a 7-phase authoring procedure, `HOW TO MEASURE` recipes, and a coverage-mapping worked example. 690 → 632 lines.
- `chapter-intro-template.md` — **NEW.** For `00-intro.md`: topic map with relative links, plus a "How the Topics Connect" section (prose using DEPENDS ON / MOTIVATES / CONTRASTS / EXTENDS) that is the reason the file exists. 7-phase procedure, pairwise connection-map method, bicycle-maintenance worked example, evidence-bearing self-check. 399 lines.
- `chapter-podcast-template.md` — **NEW.** For `99-podcast.md`: two-speaker transcript with a locked `**Host:**` / `**Expert:**` convention, one segment per topic, compliant-vs-non-compliant dialogue illustrations. 7-phase procedure, per-topic segment inventory, countable dialogue checks. Zero code fences in the transcript body by rule. 425 lines.
- `authoring-guidelines.md` — rewritten. The backwards voice guidance ("not a textbook", "assume the reader knows the prerequisites") deleted; replaced by a headline Voice & Reading Level section, Prose-First Rule, Adaptive Structure, Completeness backstop, per-artifact guidance, and an explicit Authoring Order. 86 → 126 lines.
- `chapter-notes-template.md` — **DELETED.** The old rigid template, superseded by `topic-notes-template.md`.

_skills/learning/create-learning-repo/_
- `SKILL.md` — 631 → 792 lines. New per-chapter layout in the tree/manifest/naming table; U0 intent-logic branch deleted (aux files now unconditional); **U2 gained a 9-step topic-decomposition procedure** with a bread-baking worked example; embedded `AGENTS.md` fully rewritten (9 adaptive Content Depth Rules replacing the count-based ones, plus a new Authoring Order section); U5/U6 tails updated; `TodoWrite` threshold 30 → 20; added a HOW TO RUN orientation block and consolidated STOP CONDITIONS.
- `README.md` — updated: five per-chapter artifact types, unconditional aux files, adaptive structure, derived-artifact authoring order.

_skills/learning/author-chapter/_
- `SKILL.md` — 236 → ~500 lines. Added an **artifact-type router** (filename → topic note / chapter intro / podcast / interview-prep / thought-leadership), a **sibling-readiness gate** that hard-refuses to author a derived artifact over stubs, and a **derived-content mode** where intro/podcast skip live research and synthesise only from sibling notes. Drifted inline depth numbers deleted in favour of the on-disk contract. Added orientation block, numbered steps in U0–U4, mechanical U3 measurement methods, STOP CONDITIONS, and a worked run.
- `reference/quality-gate.md` — 89 → 201 lines. One rubric split into **five per-artifact gates** plus a filename→rubric routing table, universal rules, and an artifact-keyed deterministic-checks table.
- `README.md` — updated for the router, the refusal, and the derived mode.

_skills/learning/generate-practice-exam/_
- `SKILL.md` — reconciled with adaptive notes: extraction now targets **content roles, not exact heading names** (no heading is guaranteed to exist); added source-eligibility rules (numbered topic notes primary; `00-intro.md`/`99-podcast.md` secondary and never sole grounding; interview-prep and thought-leadership excluded). Content-only grounding rule left intact.

**Summary:** Evaluated the three `skills/learning/` skills against four user objectives (prose-first teenager-readable notes with adaptive structure; multiple topic notes per chapter; a per-chapter `intro.md` authored last; a conversational `podcast.md`) and scored them 27/100 — objectives 3 and 4 were entirely unimplemented and objective 2 was contradicted in four places. Then implemented the full redesign: a new five-artifact per-chapter layout (`00-intro.md`, `01..NN-<topic-slug>.md`, `interview-prep.md`, `thought-leadership.md`, `99-podcast.md`), an adaptive menu-based topic-note template replacing the rigid one, two new derived-artifact templates, and per-artifact quality gates. Finally did a second pass embedding explicit phased procedures, measurement recipes, evidence-bearing audit rows, and STOP CONDITIONS across all five files so small (7B–30B) models can follow steps instead of inferring process.

**Outcome:** All edits complete and verified by grep + targeted re-read: zero stale `chapter-notes-template` / `notes.md` references, zero vendor/technology leakage, balanced HTML comments (12/12 intro, 11/11 podcast), balanced four-backtick fence nesting in the embedded `AGENTS.md` (opens L497, closes L656), and podcast transcript body confirmed free of code fences. One real bug caught and fixed: the connection-map arrow notation `--[TYPE]-->` was prematurely closing HTML comments (5 occurrences), which would have leaked authoring instructions into learner-facing content. No end-to-end execution test was run — correctness is inspection-verified only.

## Open Items / Next Steps
- [ ] `README.md` (repo root) — three defects: the skill table omits the two `content-creation/Medium/` skills; the install paths are missing the `skills/` prefix (it says `cp -r learning/create-learning-repo` where the dir is `skills/learning/create-learning-repo`); and it documents only OpenCode, with no mention of the Bob or Antigravity destinations. The Learning section descriptions are also stale relative to the five-artifact redesign.
- [ ] `skills/learning/create-learning-repo/SKILL.md` and `skills/learning/author-chapter/SKILL.md` — the "Portability" tables at the end of both files list Claude Code / Cursor / Copilot / ChatGPT but not Antigravity, which is now a first-class sync target using the same `SKILL.md` standard. Add it.

## Quick Reference

- **Sync everything:** `python3 scripts/sync_all.py` — syncs 13 skills to OpenCode + Bob + Antigravity, plus agents to OpenCode. Flags: `--dry-run`, `--opencode-only`, `--bob-only`, `--antigravity-only` (the three `*-only` flags are mutually exclusive).
- **Per-target scripts:** `scripts/sync_opencode_skills.py`, `scripts/sync_bob_skills.py`, `scripts/sync_antigravity_skills.py`, `scripts/sync_opencode_agents.py`.
- **Destinations:** OpenCode skills `~/.config/opencode/skills/` · Bob skills `~/.bob/skills/` · Antigravity skills `~/.gemini/config/skills/` · OpenCode agents `~/.config/opencode/agent/` (singular).
- **Env overrides:** `OPENCODE_SKILLS`, `BOB_SKILLS`, `ANTIGRAVITY_SKILLS`, `OPENCODE_AGENTS`.
- **Skills live at:** `skills/<category>/.../<name>/SKILL.md` — 13 total across agent_session_management, content-creation/Linkedin, content-creation/Medium, development, learning.
- **GOTCHA — Antigravity dest shares a parent with live Gemini config:** `~/.gemini/config/` also holds `AGENTS.md`, `config.json`, `mcp_config.json`, `projects/`, `sidecars/`. Only ever `rmtree` an individual skill folder — never `skills/` or `config/` as a whole.
- **Antigravity reference:** skills docs https://antigravity.google/docs/skills (global `~/.gemini/config/skills/`, workspace `.agents/skills/`). Rules are a separate single-file channel: global `~/.gemini/GEMINI.md`, 12,000-char limit.
- **Learning per-chapter layout:** `00-intro.md` (derived, last), `01..NN-<topic-slug>.md` (2–6 topic notes, first), `interview-prep.md`, `thought-leadership.md`, `99-podcast.md` (derived, last). `00` and `99` are reserved slots.
- **Learning three hard requirements:** Coverage Plan; 800-word explanatory-prose floor; bright-14-year-old reading level. These are the ONLY floors — do not re-introduce fixed section counts.
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
