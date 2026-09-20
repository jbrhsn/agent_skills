# Project Handoff

<!-- Managed by the end-session / init-session skills. Section order is fixed; the file is compacted on every write, not appended to. -->

## Project Snapshot

agent_skills is a curated distribution repository with 16 canonical skills under skills/, 3 base agent definitions under agents/, and the optional OpenCode search-internet plugin under plugins/. Canonical content syncs to OpenCode, IBM Bob, Antigravity, Claude Code, and Codex/ChatGPT through scripts/sync_all.py and platform-specific scripts. Python tooling uses PEP 723 and must run with uv run. Primary validation: uv run scripts/sync_all.py --dry-run; use --verify when destination harnesses are available. Skills flatten from category directories to destination skills/{name}/. Repository rules live in AGENTS.md; root README.md and category READMEs describe the public collection.

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
- video-production skill (skills/content-creation/Common/video-production/) uses Kokoro ONNX (local TTS via kokoro-onnx) and Whisper (local timestamps via openai-whisper), all run with uv via PEP 723 scripts. Model assets (~500 MB total) go in {repo-root}/.video_production_assets/kokoro/, gitignored. 03_scaffold.py is re-run safe and never overwrites existing scene TSX files. sync_all.py discovers and syncs new skill folders automatically; no script changes are needed when adding a skill.

## Previous Session

- 2026-09-19: Created content-strategy as platform-neutral superset of planning and idea research. Added x-post-writer for single posts plus threads with five-proposal workflow. Both skills exercised; sync dry-run and live sync passed.

## Last Session

- 2026-09-20: Refined LinkedIn, Medium, and X writers (five-proposal review gate), renamed evidence-preserving-refinement to content-fact-checker, expanded remotion-infographics with retention research, six style variants, theme/palette gate, workspace, MP4+hero PNG delivery and verification. Added manifest-scoped safe pruning, duplicate-name detection, sync regression tests. Ran full live sync --plugins search-internet --verify: all 15 canonical skills verified across all 5 platforms.

## Current Session

**Date:** 2026-09-20

**Focus:** Add video-production skill — a 7-phase narrated, audio-synchronized multi-scene pipeline: Kokoro TTS + Whisper timestamps + Remotion.

### Done

- Created skills/content-creation/Common/video-production/ with 8 files: SKILL.md (7-phase agent prompt, 4 user review gates), README.md (prereqs, layout, pipeline table), references/video-production-pipeline.md (script I/O contracts, storyboard JSON schema, Remotion TypeScript templates, render commands, audio sync checklist), references/kokoro-voices.md (54 Kokoro v1.0 voices), scripts/01_tts.py (Kokoro ONNX synthesizer, PEP 723), scripts/02_timestamps.py (Whisper word-level extractor, PEP 723), scripts/03_scaffold.py (Remotion scaffolder, stdlib, re-run safe), scripts/04_setup_assets.sh (one-time HF model downloader).
- Original remotion-infographics skill confirmed untouched.
- Ran uv run scripts/sync_all.py --verify: 16 skills x 100% SHA-256 parity on all 5 platforms.

### Decisions

- video-production is a parallel skill; remotion-infographics remains unchanged as the fast silent-infographic path.
- Kokoro assets are NOT auto-downloaded; 04_setup_assets.sh requires explicit user invocation to avoid silent large downloads.
- Whisper default is openai-whisper base with word_timestamps=True (lowest friction); skill notes whisper-timestamped and WhisperX as upgrade options.
- 03_scaffold.py never overwrites existing scene TSX files, making re-runs safe after storyboard edits.

### Verification

- py_compile: 01_tts.py, 02_timestamps.py, 03_scaffold.py — all pass.
- bash -n: 04_setup_assets.sh — pass.
- SKILL.md frontmatter (name + description): valid.
- All 5 JSON schema examples in video-production-pipeline.md: valid JSON.
- uv run scripts/sync_all.py --verify: 16 skills x 100% SHA-256 parity across all 5 platforms.

### Open Items

- [ ] video-production has not been exercised in a real production session yet; per AGENTS.md rules, it should be before being considered fully mature.
- [ ] Category README.md skill count may need updating from 15 to 16 if a skill count is explicitly tracked there.
