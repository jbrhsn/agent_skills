# Project Handoff

<!-- Managed by the end-session / init-session skills. Section order is fixed; the file is compacted on every write, not appended to. -->

## Project Snapshot

agent_skills: curated 11-skill distribution repo for OpenCode, IBM Bob, Google Antigravity.
Skill organization: agent_session_management (2), learning (2), development (2), content-creation (5: Common 2, LinkedIn 1, Medium 2).
Key components: SKILL.md + README.md per skill, handoff.md compaction system, 3 agents (orchestrator, executor, ask).
Sync model: Python scripts to 3 platforms; agents to OpenCode only. Build: file-centric, no tests, verify by re-read/grep.

## Cumulative Learnings

- Skill removal requires updating 3 sync scripts (hardcoded SKILLS lists) — filesystem deletion alone silently leaves orphaned copies on platforms.
- Compaction on every write (never append) keeps handoff.md read cost bounded even on 100+ session projects.
- Evidence-backed ideation (velocity scoring, live sources) outperforms interview-driven brainstorm; users want signals, not questions.
- LinkedIn algorithm mechanics (dwell time, saves, substantive comments) differ materially from generic engagement; algorithm-informed rules yield better results.
- Voice inference (extract, not impose) is harder but more authentic than fixed persona; requires calibration checks.

## Last Session

- Removed obsolete skills (repo-docs-publisher, ui-ux-designer) and cleaned global platform folders.
- Wrote comprehensive README.md files for all learning + development skills.
- Updated root README.md to reflect accurate 11-skill count.
- Identified and began fixing hardcoded SKILLS lists in sync scripts.

## Current Session

**Date:** 2026-08-23
**Focus:** Skill refinement, documentation sync updates, comprehensive validation

### Done
- Removed 2 skills: medium-article-brainstorm (replaced by evidence-backed idea-research), linkedin-image-prompts (optional downstream, streamlines workflow)
- Added 1 new skill: idea-research (evidence-backed content ideas, velocity-scored, multi-platform, 91/100 rating)
- Refined linkedin-post-writer: 6-step workflow, 4 focused reference files, 2026 algorithm mechanics, anti-slop audit (91/100 rating)
- Enhanced agent_session_management skills: init-session and end-session significantly refined with robust scripts, compaction strategy, archive archiving (92/100 rating each)
- Updated README.md: removed old skill refs, added Common content section, clarified category breakdown (11 skills: 2+2+2+5)
- Updated scripts/README.md: corrected skill count (13→11), rewrote 'What Gets Synced' section
- Updated sync scripts: reflected 11-skill roster, removed hardcoded refs to deleted skills
- Final sync: 11 skills + 3 agents to all 3 platforms (OpenCode, Bob, Antigravity)
- Comprehensive validation: verified all 11 skills on all 3 platforms, file integrity, script presence, removed skills confirmed absent

### Decisions
- Remove image-prompts as separate skill: downstream optional workflow, better as user choice after post approval
- Consolidate to idea-research: live sources + velocity scoring better than interview-driven ideation
- Enhance session management: compaction + archive strategy solves multi-session context problem elegantly
- 11 skills is the right portfolio size: lean, focused, no dead weight

### Open Items
_None._
