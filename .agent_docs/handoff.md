# Project Handoff

<!-- Managed by the end-session / init-session skills. Section order is fixed; the file is compacted on every write, not appended to. -->

## Project Snapshot

agent_skills is a curated distribution repository with 11 canonical skills under skills/, 3 base agent definitions under agents/, and the optional OpenCode search-internet plugin under plugins/. Canonical content syncs to OpenCode, IBM Bob, Antigravity, Claude Code, and Codex/ChatGPT through scripts/sync_all.py and platform-specific scripts. Python tooling uses PEP 723 and must run with uv run. Primary validation: uv run scripts/sync_all.py --dry-run; use --verify when destination harnesses are available. Skills flatten from category directories to destination skills/{name}/. Repository rules live in AGENTS.md; root README.md and category READMEs describe the public collection.

## Cumulative Learnings

- Treat skills as adaptable guidance: express outcomes, evidence, and safety constraints clearly while avoiding mandatory phases, arbitrary quotas, fixed formats, or stop conditions that reduce agent performance without a correctness reason.
- Keep canonical changes inside this repository and sync outward; never edit generated destination copies as repository work. Markdown prose remains unwrapped, one physical line per paragraph.
- create-learning-repo owns roadmap and scaffold structure; author-chapter consumes the scaffold frontmatter and Brief as its assignment. Preserve that metadata, replace scaffold prompts during authoring, and judge completeness against the brief rather than word counts.
- Learning depth, research, examples, assessment, and progression should scale to the topic, learner, stakes, and available evidence. Domain references provide options and calibration rather than compulsory checklists.
- Session helpers require uv. If uv is missing, ask before installing it; do not silently fall back to bare python. .agent_docs/handoff.md stores compact whole-project memory plus Current Session and two concrete prior sessions, rotating once per distinct session while checkpoints preserve the window.
- end-session saves memory and then creates a local Git commit for eligible session changes. Preserve unrelated edits and staging, respect ignored memory, skip empty commits, and do not push or amend unless separately requested.
- Sync verification compares canonical skill trees by SHA-256. Extra unknown destination directories are preserved and may cause destination-level verification warnings even when every canonical skill matches.

## Previous Session

- 2026-08-31 — Redesigned create-learning-repo around six files per chapter, profile-driven tier ladders, plan briefs with required purpose, and flexible depth/style guidance.
- Verified scaffold behavior and synchronized all canonical skills across the five supported platforms with parity checks.
- Identified the need for author-chapter to consume the new scaffold brief contract.

## Last Session

- 2026-08-31 — Redesigned author-chapter to consume create-learning-repo briefs, preserve frontmatter/Brief metadata, and teach through adaptable takeaway-first units.
- Added domain and file-type references, rewrote structure/checklist/examples/voice/pedagogy guidance, and aligned category and root documentation.
- Validated a craft-profile scaffold and synchronized all platforms. A full live authoring run remained untested at that point.

## Current Session

**Date:** 2026-09-19

**Focus:** Evaluate and refine learning and agent-session-management skills so they guide agents without unnecessarily restricting performance

### Done

- Reviewed and revised all skills/learning guidance and supporting references to replace rigid phases, quotas, caps, and bans with adaptive decision guidance while retaining useful quality and safety constraints.
- Reworked init-session and end-session so handoff.md acts as compact whole-project memory with Current Session plus two concrete prior sessions; added reliable rotation/checkpoint behavior, legacy handling, archive-on-write, payload validation, and task restoration.
- Standardized all Python instructions and helper execution on uv run, including the requirement to ask before installing uv when it is absent.
- Extended end-session to create a scoped local Git commit after memory is saved, including checkpoints, while preserving unrelated changes and ignored memory and avoiding push/amend behavior.
- Validated both session skills with skill-creator validation, exercised helper behavior in isolated tests, ran sync previews, and synchronized all 11 canonical skills and agents across configured platforms.
- All work is contained in commit 9b450660a7a62013ffa1999f8d52b27ab97c2966 (skills refinement set 1); main matches origin/main and the working tree was clean before this handoff write.

### Decisions

- Use flexible starting points and contextual judgment in skill prompts; reserve hard requirements for interoperability, correctness, security, explicit user constraints, or destructive actions.
- Keep Git operations agent-driven instead of placing them in handoff_write.py so commit scope, unrelated edits, hooks, and repository conventions can be assessed safely.
- Keep .agent_docs local when ignored; a valid end-session may therefore update memory without producing a new commit when project changes are already committed.

### Verification

- uv-based skill validation passed for init-session and end-session.
- Isolated helper tests passed for new-session rotation, repeated checkpoints, legacy handoffs, archiving, and archive-failure handling.
- uv run scripts/sync_all.py --dry-run passed after the source changes.
- uv run scripts/sync_all.py --verify synchronized all targets; every canonical skill passed SHA-256 parity. Claude Code also contains unknown directories .trash and synced, and Codex/ChatGPT contains the independently installed find-skills skill, so those destination-level checks reported extras while preserving them.

### Open Items

_None._
