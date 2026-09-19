# Project Handoff

<!-- Managed by the end-session / init-session skills. Section order is fixed; the file is compacted on every write, not appended to. -->

## Project Snapshot

agent_skills is a curated distribution repository with 13 canonical skills under skills/, 3 base agent definitions under agents/, and the optional OpenCode search-internet plugin under plugins/. Canonical content syncs to OpenCode, IBM Bob, Antigravity, Claude Code, and Codex/ChatGPT through scripts/sync_all.py and platform-specific scripts. Python tooling uses PEP 723 and must run with uv run. Primary validation: uv run scripts/sync_all.py --dry-run; use --verify when destination harnesses are available. Skills flatten from category directories to destination skills/{name}/. Repository rules live in AGENTS.md; root README.md and category READMEs describe the public collection.

## Cumulative Learnings

- Treat skills as adaptable guidance: express outcomes, evidence, and safety constraints clearly while avoiding mandatory phases, arbitrary quotas, fixed formats, or stop conditions that reduce agent performance without a correctness reason.
- Keep canonical changes inside this repository and sync outward; never edit generated destination copies as repository work. Markdown prose remains unwrapped, one physical line per paragraph.
- Session helpers require uv. If uv is missing, ask before installing it; do not silently fall back to bare Python. .agent_docs/handoff.md stores compact whole-project memory plus Current Session and two concrete prior sessions, rotating once per distinct session while checkpoints preserve the window.
- end-session saves memory and then creates a local Git commit for eligible session changes. Preserve unrelated edits and staging, respect ignored memory, skip empty commits, and do not push or amend unless separately requested.
- Sync verification compares canonical skill trees by SHA-256. Extra unknown destination directories are preserved and may cause destination-level verification warnings even when every canonical skill matches.
- Development skills route by project domain and failure mode; content skills distinguish evidence from voice and editorial judgment, make research and platform mechanics traceable, and avoid promising reach, ranking, or engagement from heuristic scores.
- The content-strategy skill is a platform-neutral superset of planning and idea research. It remains independent of writer skills and accepts optional handoffs; idea-research remains available for focused discovery and optional fetchers.
- Platform capability claims must be sourced and dated. X longer-post documentation has differing limits across publishing flows, so plans label account/client capability uncertainty rather than assuming a limit.

## Previous Session

- 2026-08-31: Redesigned author-chapter to consume create-learning-repo briefs, preserve frontmatter/Brief metadata, and teach through adaptable takeaway-first units. Added domain and file-type references, aligned documentation, validated a craft-profile scaffold, and synchronized all platforms.

## Last Session

- 2026-09-19: Added x-post-writer, a unified X skill for short, medium-length, long single posts, and threads. Added references for composition, X mechanics, handoffs, and writing notes. Researched official X documentation, exercised all four formats, corrected unsupported numerical claims, and passed validator, link/whitespace checks, and sync dry-run. Changes were not yet synced at session end.

## Current Session

**Date:** 2026-09-19

**Focus:** Create and verify a common content-strategy skill that integrates idea research for weekly and monthly LinkedIn, Medium, and X planning

### Done

- Created skills/content-creation/Common/content-strategy/SKILL.md with independent planning, integrated research, prioritization, calendar, feasibility, review, and handoff guidance.
- Added README.md, platform-planning.md, research-and-prioritization.md, calendar-schema.md, handoffs.md, and content-strategy-template.md.
- Updated root README.md, AGENTS.md, scripts/README.md, and content-creation/README.md from 12 to 13 skills and documented content-strategy handoffs. Updated x-post-writer to accept content_strategy.md context.
- Researched official LinkedIn analytics/scheduling, Medium distribution/publishing, and X post/thread/Article/view-count mechanics; recorded dated source links and capability limitations in the platform reference.
- Kept idea-research as a focused standalone skill for compatibility while making content-strategy a practical superset for calendar planning.
- Exercised the skill with an October cross-platform plan under a four-hour weekly budget and with a short LinkedIn plan restricted to supplied notes. The exercises caught capacity conflict, unsupported trending claims, date handling, source uncertainty, and unequal observation windows.

### Decisions

- Content-strategy produces content_strategy.md by convention and optional content_research.md; it plans and briefs but does not draft, publish, schedule, or modify accounts.
- No research fetcher scripts were duplicated into content-strategy; existing idea-research helpers remain optional and the strategy skill includes its own independent research method.
- Cross-platform adaptations count production effort separately even when research is shared. A calendar target is not evidence of a scheduled or published item.
- The session changes are one coherent content-strategy outcome and the x-post-writer handoff updates belong in the same commit.

### Verification

- uv run --with pyyaml /Users/jbrhsn/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/content-creation/Common/content-strategy: passed.
- uv run scripts/sync_all.py --dry-run: passed; all five platform syncs discover 13 skills and make no writes.
- Ruby checks: 14 changed/new Markdown files checked, 55 local links resolve, and no trailing whitespace; git diff --check passed.
- Independent planning exercises completed for cross-platform October content and a constrained LinkedIn week. Publishing performance, account scheduling, and live analytics remain untested.

### Open Items

- [ ] Run uv run scripts/sync_all.py --verify when ready to apply the new skill to all destinations; current changes remain canonical and unsynced.
- [ ] Review the new skill and decide whether to perform the requested multi-platform sync in a later session.
