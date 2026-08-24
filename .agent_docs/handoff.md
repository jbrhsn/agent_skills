# Project Handoff

<!-- Managed by the end-session / init-session skills. Section order is fixed; the file is compacted on every write, not appended to. -->

## Project Snapshot

agent_skills: curated 11-skill distribution repo for OpenCode, IBM Bob, Google Antigravity, and Claude Code.
Skill organization: agent_session_management (2), learning (2), development (2), content-creation (5: Common 2, LinkedIn 1, Medium 2).
Key components: SKILL.md + README.md per skill, handoff.md compaction system, 3 agents (orchestrator, executor, ask).
Sync model: Lean Python sync system (`scripts/common.py` + per-platform scripts) to 4 platforms; agents to OpenCode only. Auto-discovery of skills from directory tree.

## Cumulative Learnings

- Shared helper module (`common.py`) + dynamic skill discovery (`Path.glob('**/SKILL.md')`) eliminates hardcoded lists and reduces multi-platform sync boilerplate by ~75% while keeping CLI backwards compatibility.
- Compaction on every write (never append) keeps handoff.md read cost bounded even on 100+ session projects.
- Claude Code on macOS uses `~/.claude/skills/{skill-name}/SKILL.md` for personal skills, with direct drop-in compatibility with OpenCode/Antigravity/Bob format.
- Evidence-backed ideation (velocity scoring, live sources) outperforms interview-driven brainstorm; users want signals, not questions.
- LinkedIn algorithm mechanics (dwell time, saves, substantive comments) differ materially from generic engagement; algorithm-informed rules yield better results.

## Last Session

- Removed medium-article-brainstorm and linkedin-image-prompts; added evidence-backed idea-research skill.
- Refined linkedin-post-writer with 2026 algorithm mechanics and anti-slop audit.
- Upgraded agent session management (init-session, end-session) with compaction and archiving.
- Synchronized and validated 11 skills and 3 agents across OpenCode, IBM Bob, and Antigravity.

## Current Session

**Date:** 2026-08-24
**Focus:** Claude Code support integration and lean-coder sync script refactoring

### Done
- Researched Claude Code on macOS: personal skills live in `~/.claude/skills/` and are 100% compatible with existing SKILL.md format.
- Implemented `scripts/sync_claude_skills.py` and integrated `--claude-only` into `scripts/sync_all.py`.
- Applied lean-coder skill across all sync scripts: created `scripts/common.py`, eliminated duplicate code, and switched to dynamic skill discovery (1003 → 255 total LOC, -74.5%).
- Updated documentation in `scripts/README.md`, `README.md`, and `AGENTS.md`.
- Verified dry-runs and executed live sync across all 4 platforms (OpenCode, IBM Bob, Antigravity, Claude Code).

### Decisions
- Auto-discover skills dynamically via glob in `common.py` rather than maintaining hardcoded arrays across 4 scripts.
- Keep each per-platform script independently executable with CLI flags and env overrides while delegating to `common.py`.

### Open Items
_None._
