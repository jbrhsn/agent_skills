# Project Handoff

<!-- Managed by the end-session / init-session skills. Section order is fixed; the file is compacted on every write, not appended to. -->

## Project Snapshot

agent_skills is a curated distribution repository with 15 canonical skills under skills/, 3 base agent definitions under agents/, and the optional OpenCode search-internet plugin under plugins/. Canonical content syncs to OpenCode, IBM Bob, Antigravity, Claude Code, and Codex/ChatGPT through scripts/sync_all.py and platform-specific scripts. Python tooling uses PEP 723 and must run with uv run. Primary validation: UV_CACHE_DIR=/private/tmp/agent-skills-uv-cache uv run scripts/sync_all.py --dry-run; use --verify when destination harnesses are available. Skills flatten from category directories to destination skills/{name}/. Repository rules live in AGENTS.md; root README.md and category READMEs describe the public collection.

## Cumulative Learnings

- Treat skills as adaptable guidance: express outcomes, evidence, and safety constraints clearly while avoiding mandatory phases, arbitrary quotas, fixed formats, or stop conditions that reduce agent performance without a correctness reason.
- Keep canonical changes inside this repository and sync outward; never edit generated destination copies as repository work. Markdown prose remains unwrapped, one physical line per paragraph.
- Session helpers require uv. If uv is missing, ask before installing it; do not silently fall back to bare Python. .agent_docs/handoff.md stores compact whole-project memory plus Current Session and two concrete prior sessions, rotating once per distinct session while checkpoints preserve the window.
- end-session saves memory and then creates a local Git commit for eligible session changes. Preserve unrelated edits and staging, respect ignored memory, skip empty commits, and do not push or amend unless separately requested.
- Skill destinations are shared. Sync records only its own folders in .agent_skills_skills_manifest.json, prunes only folders in that manifest, and verifies all canonical skill trees by SHA-256 without failing for user-installed folders. Duplicate flattened skill names are rejected.
- Development skills route by project domain and failure mode; content skills distinguish evidence from voice and editorial judgment, make research and platform mechanics traceable, and avoid promising reach, ranking, or engagement from heuristic scores.
- The content-strategy skill is a platform-neutral superset of planning and idea research. It remains independent of writer skills and accepts optional handoffs; idea-research remains available for focused discovery and optional fetchers.
- Platform capability claims must be sourced and dated. X longer-post documentation has differing limits across publishing flows, so plans label account/client capability uncertainty rather than assuming a limit.
- LinkedIn, X, and Medium writers use a five-proposal hook-and-structure review for new drafts and substantial rewrites, research comparable performance evidence, recommend a faithful direction, and wait for author confirmation before producing their two output files.
- content-fact-checker replaces evidence-preserving-refinement. It improves claim reliability and attribution without changing the author's core message, opinions, voice, or tone. Remotion infographics needs an approved or delegated visual direction before it renders a project, MP4, and exact-final-frame hero PNG.

## Previous Session

- 2026-09-19: Added x-post-writer for short, medium-length, and long single posts plus threads, with composition, X mechanics, handoff, and publishing-note references. Exercised all formats, corrected unsupported numerical claims, and passed validation, local-link checks, and sync dry-run.

## Last Session

- 2026-09-19: Created and exercised the independent content-strategy skill for weekly and monthly LinkedIn, Medium, and X planning. It integrates research, prioritization, feasibility, calendar, and writer handoffs while retaining idea-research as a focused standalone skill. Current-session deployment resolved its pending live sync.

## Current Session

**Date:** 2026-09-20

**Focus:** Refine the content-creation skill suite, align its documentation and synchronization, then deploy it to all supported harnesses.

### Done

- Refined LinkedIn, Medium, and X writers so new drafts and substantial rewrites compare five hook-and-structure proposals against web research, recommend a preserving direction, obtain author confirmation, and then write paired post/article and publishing-note files.
- Renamed evidence-preserving-refinement to content-fact-checker and expanded its claim-level web-research, revision, attribution, and unresolved-claim workflow.
- Expanded remotion-infographics with researched retention guidance, six style variants, theme/palette confirmation, a local remotion-infographic workspace, MP4 plus final-frame PNG delivery, and rendering verification.
- Updated root, content-creation, and sync READMEs; added missing READMEs for content-fact-checker and remotion-infographics; updated the public collection count to 15 skills.
- Added manifest-scoped safe pruning for renamed or removed skills, duplicate flattened-name detection, and sync regression coverage in scripts/test_sync_skills.py. Corrected sync_all.py to report failures accurately and verification to allow unmanaged shared-destination skills.
- Ran the full live sync with --plugins search-internet --verify. All 15 canonical skills verified on OpenCode, IBM Bob, Antigravity, Claude Code, and Codex/ChatGPT; all agents verified, including resolved composed OpenCode agents; the selected plugin was installed.

### Decisions

- The skill manifest never claims ownership of existing untracked destination folders, so initial synchronization preserves manually installed skills; later removals only prune manifest-owned folders.
- Remotion's requested legacy remotion-graphic ignore patterns are kept alongside the actual remotion-infographic workspace patterns because neither spelling covers the other.
- No live publishing, scheduling, video rendering, or repository push was performed as part of skill refinement and deployment.

### Verification

- UV_CACHE_DIR=/private/tmp/agent-skills-uv-cache uv run scripts/test_sync_skills.py: 5 tests passed.
- UV_CACHE_DIR=/private/tmp/agent-skills-uv-cache uv run scripts/test_content_research.py: 13 tests passed.
- quick_validate.py passed for content-fact-checker and remotion-infographics; git diff --check passed.
- UV_CACHE_DIR=/private/tmp/agent-skills-uv-cache uv run scripts/sync_all.py --plugins search-internet --verify: all canonical skills, agents, and the selected plugin synchronized and verified successfully.

### Open Items

- [ ] No implementation work remains from this session. The local commit is the final pending handoff step.
