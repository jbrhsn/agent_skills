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
- Development skills should route by project domain and failure mode, keep implementation choices contextual, and treat production readiness as evidence-based rather than a universal checklist.
- Content-creation skills should distinguish evidence from voice and editorial judgment, make research and platform mechanics traceable, and avoid promising reach, ranking, or engagement from heuristic scores.
- Content research helpers use uv run, support dry-run previews, preserve partial failures and provenance, and avoid silently treating missing timestamps, failed pageviews, or unofficial sources as confirmed evidence.

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

**Focus:** Refine development and content-creation skills into flexible, production-grade guidance and close the session

### Done

- Reviewed and refined both development skills: lean-coder now covers web, data engineering, Web3, Android/iOS, and troubleshooting/debugging through adaptive domain references; project-planner now supports domain-aware planning and testing without rigid gates.
- Reviewed and refined all five content-creation skills: idea research, keyword research, LinkedIn posts, Medium articles, and Medium image prompts. Replaced fixed quotas and unsupported platform promises with contextual guidance, evidence/provenance handling, voice preservation, accessibility, and current policy-aware references.
- Hardened content research helpers: corrected installed-path resolution, stale-age and malformed-record handling, word-boundary matching, source-family grading, pageview failure semantics, dry-run support, argument validation, safe scaffolding, and uv-only environment setup.
- Added scripts/test_content_research.py with offline regression coverage for scoring, deduplication, dry-run behavior, scaffolding protections, helper failures, and provenance grading.
- Updated root and category documentation to describe the flexible workflows and evidence boundaries.

### Decisions

- Keep domain references as routing and calibration aids; agents may choose a lighter or deeper path based on project risk, evidence, user goals, and repository context.
- Treat heuristic research scores as prioritization signals only. Unknown, failed, unofficial, and inferred data remain explicitly labeled rather than being converted into certainty.
- Keep platform-specific mechanics current and sourced from official documentation where claims affect publishing, distribution, or policy; avoid universal timing, reach, CTR, tag, length, or image-count claims.
- Commit all current development and content skill changes together because they are the requested session outcome and no unrelated edits are present.

### Verification

- uv run --with pyyaml /Users/jbrhsn/.codex/skills/.system/skill-creator/scripts/quick_validate.py passed for all five content-creation skills and the revised development skills.
- uv run --no-project scripts/test_content_research.py: 13 tests passed.
- Ruby local-link check: 36 Markdown files checked; 51 local links resolve.
- git diff --check passed; bash -n passed for keyword helper and setup_env; keyword helper dry-run and setup_env checks passed.
- uv run scripts/sync_all.py --dry-run passed for all 11 skills. Actual sync was not run after these latest edits.

### Open Items

- [ ] Run an actual multi-platform sync with uv run scripts/sync_all.py --verify when ready; current changes are canonical and remain unsynced.
- [ ] Exercise the revised development and content skills in live platform sessions when practical; offline validation covers the helper behavior but not full editorial or agent interaction quality.
