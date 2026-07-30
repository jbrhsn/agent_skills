# Handoff Log

## Project Progress (rolling summary)

`agent_skills` is a curated collection of reusable AI-agent **skills** for both OpenCode and IBM Bob. Each skill is a folder containing a `SKILL.md` (with YAML frontmatter whose `name` must equal the leaf folder name) plus usually a `README.md`, living under a categorized tree: `skills/agent_session_management/` (init-session, end-session), `skills/content-creation/Linkedin/` (linkedin-post-writer, linkedin-image-prompts), `skills/content-creation/Medium/` (medium-article-writer, medium-image-prompts), `skills/development/` (lean-coder, project-planner, repo-docs-publisher, ui-ux-designer), and `skills/learning/` (author-chapter, create-learning-repo, generate-practice-exam) — **13 skills total**. Agents live under `agents/orchestrator_mode_agents/` (orchestrator + executor); plugins under `plugins/token_saving/token-guard.ts`.

The architecture is file-centric: pure Markdown/TypeScript content installed by five Python sync scripts in `scripts/` (`sync_opencode_skills.py`, `sync_bob_skills.py`, `sync_opencode_agents.py`, `sync_opencode_plugins.py`, and `sync_all.py` which orchestrates). Critical constants: skills sync to **two destinations** — `~/.config/opencode/skills` and `~/.bob/skills`; each sync script carries a **hardcoded `SKILLS` list** that must include every skill dir (an unregistered skill is silently missed); skill dirs are addressed by their **leaf name** at the destination (category path stripped). There is no root `AGENTS.md`, no build, and no automated tests — skill edits are verified by careful re-read.

## Session Log

### Session: 2026-07-30 (current)
**Files touched:**

_skills/ (7 SKILL.md fixed for the chat-bloat anti-pattern)_
- `skills/development/project-planner/SKILL.md` — approval gates now point to the written `docs/0X-*.md` files + a short summary, not the doc body.
- `skills/learning/author-chapter/SKILL.md` — write draft to the target file before the U2 review gate; preserved "never overwrite pre-existing authored content" guardrail and mandatory U3 quality gate.
- `skills/learning/generate-practice-exam/SKILL.md` — write exam to a draft file at U4 with idempotent naming; U5/U6 update/finalize the same file in place; quality gate still mandatory.
- `skills/content-creation/Linkedin/linkedin-image-prompts/SKILL.md` — write `*_image_prompts.md` first, then the sanity-check gate shows counts/flags + file pointer (not the full prompt set).
- `skills/content-creation/Medium/medium-image-prompts/SKILL.md` — same inversion as the LinkedIn image-prompts skill.
- `skills/content-creation/Linkedin/linkedin-post-writer/SKILL.md` — (fixed earlier in session) WRITE path writes the `.md` draft before the review gate; REVIEW path writes `*_revised.md` before presenting; overwrite policy reconciled.
- `skills/content-creation/Medium/medium-article-writer/SKILL.md` — (fixed earlier in session) same inversion; REVIEW path writes `*_reviewed.md` before presenting.

_global installs_
- Ran `python3 scripts/sync_all.py` — synced 13/13 skills to both OpenCode and Bob, plus 2 agents + 1 plugin to OpenCode; verified the "do NOT paste the body" review-gate wording landed in both destinations.

**Summary:** Audited all 13 skills for a chat-bloat anti-pattern (drafting full content inline in chat for review instead of writing it to a file and pointing the user there). Inverted 7 skills to a "write-draft-to-file-first, then present only a short pointer + summary at the review gate, never paste the body" flow. Confirmed the other six skills (ui-ux-designer, repo-docs-publisher, lean-coder, create-learning-repo, end-session, init-session) were already compliant.

**Outcome:** All 7 fixes complete, verified by careful re-read (no automated tests in the repo), and synced 13/13 to both OpenCode and Bob. Nothing committed to git.

### Session: 2026-07-30 (previous)
**Files touched:**

_skills/ (content-creation/Medium — NEW)_
- `skills/content-creation/Medium/medium-article-writer/SKILL.md` — new dual-path skill (WRITE + REVIEW/SCORE) mirroring linkedin-post-writer: shared 5-dimension /100 rubric grounded in Medium's Distribution Guidelines, AI-content policy, and Partner Program mechanics; units W1–W6 and R1–R6; guardrails against fabricating earnings figures and the "about Medium = Network-only" trap. Outputs `medium_article.md` / `medium_article_reviewed.md`.
- `skills/content-creation/Medium/medium-image-prompts/SKILL.md` — new skill mirroring linkedin-image-prompts but adapted to Medium's non-carousel model (1 featured/cover + N purposeful in-article visuals); featured-image focal-point/≥1192px guidance, mandatory AI-image caption-disclosure, credit+caption+alt-text per image. Outputs `medium_image_prompts.md`.

_scripts/ + docs_
- `scripts/sync_opencode_skills.py`, `scripts/sync_bob_skills.py` — added the two Medium skill paths to the hardcoded `SKILLS` lists (11→13).
- `scripts/README.md` — "11 skills"→"13 skills"; added "Content Creation (Medium)" category line.

_global installs_
- Synced all 13 skills to `~/.config/opencode/skills/` and `~/.bob/skills/` (both: 13 synced, 0 skipped); verified both Medium `SKILL.md` files landed on disk in both targets.

**Summary:** Researched Medium monetization/hooks/structure/images (4 parallel research passes), then created two new Medium content-creation skills mirroring the LinkedIn pair — a dual-path `medium-article-writer` and a `medium-image-prompts`. Registered both in the two sync scripts' hardcoded SKILLS lists, updated the scripts README count 11→13, and synced to both OpenCode and Bob global dirs.

**Outcome:** Docs-only additions, verified by frontmatter/name checks and on-disk confirmation in both global dirs (13/13, 0 skipped). Note the repo `README.md` skill table was NOT yet updated to list the two Medium skills or bump its counts. User still needs to restart opencode to load the new skills. Nothing committed to git.

## Open Items / Next Steps
No open items from this session.

## Quick Reference

- **Sync everything:** `python3 scripts/sync_all.py` — syncs 13 skills to both OpenCode + Bob, plus agents + plugins to OpenCode. Flags: `--dry-run`, `--opencode-only`, `--bob-only`.
- **Per-target scripts:** `scripts/sync_opencode_skills.py`, `scripts/sync_bob_skills.py`, `scripts/sync_opencode_agents.py`, `scripts/sync_opencode_plugins.py`.
- **OpenCode skills destination:** `~/.config/opencode/skills/`. **Bob skills destination:** `~/.bob/skills/`.
- **OpenCode agents/plugins destinations:** `~/.config/opencode/agent/` (singular) and `~/.config/opencode/plugin/` (singular).
- **Env overrides:** `OPENCODE_SKILLS`, `BOB_SKILLS`, `OPENCODE_AGENTS`, `OPENCODE_PLUGINS`.
- **Skills live at:** `skills/<category>/.../<name>/SKILL.md` — 13 total across agent_session_management, content-creation/Linkedin, content-creation/Medium, development, learning.
- **GOTCHA — use `python3`, not `python`:** `python` is not on PATH in this environment.
- **GOTCHA — hardcoded `SKILLS` list:** adding a new skill requires adding its full repo-root path to the `SKILLS` array in BOTH `scripts/sync_opencode_skills.py` AND `scripts/sync_bob_skills.py`; unregistered skills are silently skipped. The leaf segment becomes the installed folder name.
- **GOTCHA — case of the LinkedIn category dir is `Linkedin`** (capital L, lowercase rest) as referenced in the sync scripts' SKILLS paths.
- **GOTCHA — sync does not auto-prune:** removing a skill from the repo does NOT delete it from the global dir; delete the obsolete global folder manually.
- **GOTCHA — restart required:** opencode loads config/agents/plugins/skills only at startup; restart after any change.
- **Chat-pointer discipline (established this session):** skills write drafts to files, then present only a pointer + short summary at review/approval gates — **never paste the draft body into chat**. Applies to writer/planner/authoring/exam/image-prompt skills.
- **No automated tests/lint/build:** verify skill edits by re-read; optional syntax check `python3 -m py_compile scripts/*.py`.
- **Skill template:** each skill needs `SKILL.md` (frontmatter `name` must match leaf folder name); most also carry a `README.md`.
- **No root `AGENTS.md`:** this handoff file is the sole persistent cross-session context.
- **Session continuity:** `/init-session` at start, `/end-session` at end (reads/writes `.agent_docs/handoff.md`).
