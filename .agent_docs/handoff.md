# Project Handoff

<!-- Managed by the end-session / init-session skills. Section order is fixed; the file is compacted on every write, not appended to. -->

## Project Snapshot

agent_skills: curated 11-skill distribution repo for OpenCode, IBM Bob, Google Antigravity, Claude Code, and Codex/ChatGPT, plus 3 base agent definitions (orchestrator, executor, ask) and 1 opt-in OpenCode plugin (search-internet).
Skill organization: agent_session_management (2), learning (2), development (2), content-creation (5).
Sync model: scripts/common.py + per-platform scripts, dynamic discovery, PEP 723 + `uv run`. Agents/plugins sync fully to OpenCode (composition engine in scripts/plugins.py handles overlays); executor.md also translates to a Claude Code subagent at ~/.claude/agents/; Antigravity gets one global instructions file at ~/.gemini/config/AGENTS.md. IBM Bob and Codex/ChatGPT get skills only (at ~/.bob/skills and ~/.agents/skills respectively). Full SHA-256 checksum and parity verification integrated via `sync_all.py --verify`.

## Cumulative Learnings

- create-learning-repo redesign (2026-08-31): a chapter is now always six fixed files (learning, examples, practice, interview, thought_leadership, quizzies) - topics live as sections inside learning.md, not as separate per-topic files. One file per topic was the root cause of the original complaint (chapters whose parts never referred to each other); collapsing to one tiered narrative file forces cohesion.
- create-learning-repo profiles are pure data, not templates: PROFILES dict in scaffold.py holds only a tier ladder + label overrides for the five slot files. Only two renderers exist (learning_stub, slot_stub) - adding a domain is a dict entry, never a new template. A `custom` profile lets the plan declare its own 2-4 tiers with no code change.
- create-learning-repo cohesion fields: serves/builds_on/enables are authored by the planner; position/prev/next are derived free from plan order. All six chapter files share one frontmatter key set so nothing is special-cased. This is the actual fix for 'topics don't correlate' - not just fewer files, but an explicit dependency graph plus a brief (purpose/depth/style) that scaffold.py refuses to omit (missing `purpose` is a hard validation error; missing depth/style/serves warn as 'thin briefs').
- sync_skills() in scripts/common.py rmtree's each destination skill directory before copytree - confirmed empirically that a redesign changing file names/counts (9 files -> 10) cannot leave stale files behind after a normal sync_all.py run; no extra cleanup step is ever needed for a skill-shape change.

## Last Session

- Added Codex/ChatGPT desktop harness skill sync support (sync_codex_skills.py, --codex-only, docs) and committed (8cb3d30, d1a1b95) - later pushed.
- Verified all 11 skills across all 5 platforms with SHA-256 parity.

## Current Session

**Date:** 2026-08-31
**Focus:** Redesigned skills/learning/create-learning-repo: fixed six-file chapter layout, domain profiles (technical/craft/practice/exam/custom), and plan-driven briefs replacing static stubs

### Done
- Rewrote scripts/scaffold.py end-to-end: PROFILES dict, two generic renderers (learning_stub, slot_stub), brief_block/brief_lite rendering, derived cohesion fields (position/prev/next), thin-brief validation warnings, PEP 723 header for `uv run`
- New references/profiles.md: four presets (technical, craft, practice, exam) plus custom, tier-ladder semantics, how to choose one
- Rewrote references/plan-schema.md, templates.md, SKILL.md, interview.md, gap-analysis.md, research.md, bash-fallback.md, and the skill's README.md for the new file set and brief fields
- Fixed 4 stale descriptions of this skill in sibling docs (root README.md, skills/learning/README.md) that still described the old one-file-per-topic layout
- Smoke-tested all 4 presets + custom via dry-run and real scaffolds, including tier_count trimming, per-file count overrides, and all three validation error paths
- Ran uv run scripts/sync_all.py --verify: synced to all 5 platforms (OpenCode, Bob, Antigravity, Claude Code, Codex/ChatGPT) at 100% SHA-256 parity; grepped all 5 destinations for old-version markers (found none) and ran the synced copy end-to-end from ~/.claude/skills to confirm it scaffolds correctly

### Decisions
- Chosen design: Option C (thin profiles + agent-authored per-chapter brief) over A (full profile packs per domain) and B (no profiles, everything agent-parameterized) - user approved this before implementation
- Final file-set decision (after a second user round) diverged from the very first draft: filenames stay identical across every profile (interview.md, not per-profile names) - profiles only change the tier ladder and in-file labels/framing, never filenames, because stable filenames keep progress.md/greps/author-chapter's contract uniform
- thought_leadership.md is still emitted for the exam profile (shrunk to 2 slots, marked optional) rather than dropped, to keep the six-file set truly universal across profiles
- author-chapter was deliberately not touched this session - its input contract now changes (it should consume the new brief_block as its assignment) and was flagged as the natural next piece of work

### Open Items
- [ ] All create-learning-repo changes are uncommitted in git (11 modified files + new references/profiles.md) - user has not yet asked to commit
- [ ] author-chapter not yet updated to read/consume the new learning.md brief format from create-learning-repo
- [ ] User said 'the two skills are independent, but complementing each other' and named author-chapter as the second target for this same improvement pass - not started
