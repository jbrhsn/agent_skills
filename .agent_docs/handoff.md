# Project Handoff

<!-- Managed by the end-session / init-session skills. Section order is fixed; the file is compacted on every write, not appended to. -->

## Project Snapshot

agent_skills: curated 11-skill distribution repo for OpenCode, IBM Bob, Google Antigravity, and Claude Code, plus 3 base agent definitions (orchestrator, executor, ask) and 1 opt-in OpenCode plugin (search-internet).
Skill organization: agent_session_management (2), learning (2), development (2), content-creation (5).
Sync model: scripts/common.py + per-platform scripts, dynamic discovery, PEP 723 + `uv run`. Agents/plugins sync fully to OpenCode (composition engine in scripts/plugins.py handles overlays); executor.md also translates to a Claude Code subagent at ~/.claude/agents/; Antigravity gets one global instructions file at ~/.gemini/config/AGENTS.md. IBM Bob gets skills only (no agent target — config format undocumented).

## Cumulative Learnings

- Shared helper module (`common.py`) + dynamic skill discovery (`Path.glob('**/SKILL.md')`) eliminates hardcoded lists and reduces multi-platform sync boilerplate by ~75% while keeping CLI backwards compatibility.
- Compaction on every write (never append) keeps handoff.md read cost bounded even on 100+ session projects.
- Claude Code on macOS uses `~/.claude/skills/{skill-name}/SKILL.md` for personal skills, with direct drop-in compatibility with OpenCode/Antigravity/Bob format.
- Evidence-backed ideation (velocity scoring, live sources) outperforms interview-driven brainstorm; users want signals, not questions.
- LinkedIn algorithm mechanics (dwell time, saves, substantive comments) differ materially from generic engagement; algorithm-informed rules yield better results.
- OpenCode plugin-provided custom tools are allow-by-default in every agent unless a permission explicitly denies them (verified empirically on 1.18.23) — a plugin's runtime file and its agent permission overlays must install atomically, or the orchestrator silently gains the tool.
- OpenCode 1.18.23 reads the singular `agent/` and `plugin/` config paths, not the plural `agents/`/`plugins/` its own docs describe — verified empirically, don't 'fix' this.
- Frontmatter deep-merge across plugin overlays must recurse via `dst.setdefault(key, {})`, not `dst.get(key)` — `.get` lets the first plugin's nested dict win wholesale, so conflict provenance is only recorded on the parent key and a second plugin silently overwrites the leaf with no error.
- Claude Code subagent frontmatter (confirmed against official docs) has no per-command bash permission map like OpenCode's `permission.bash` patterns — required fields are just `name`+`description`; granular allow/ask/deny gates have to be expressed as a plain-language instruction in the body instead, not faked in frontmatter.
- Any agent-file instruction that references a skill by literal repo path (e.g. `skills/development/lean-coder/SKILL.md`) breaks once the file is synced to another platform/project — skills flatten to `skills/{name}/` at every destination (no category subfolder) and live in a completely different tree than the target project. Invoke skills by name, never by hardcoded path, in anything that gets synced out.
- Antigravity has no per-mode agent-file concept — one flat `AGENTS.md` at `~/.gemini/config/AGENTS.md` governs every agent session in the workspace; IBM Bob has real subagents/custom-modes but no publicly documented config file format to target.
- `.gitignore` line 18 is a bare `.*`, which already ignores every dotfile including `.DS_Store` — no separate entry is needed, and none is tracked. `.agent_docs/handoff.md` is nonetheless committed despite `.agent_docs/` being listed, because gitignore has no effect on already-tracked files. Verify with `git check-ignore -v` before re-flagging either as a hygiene gap.
- The destination/env-var mapping is duplicated across four docs — root `README.md`, `AGENTS.md` §5-6, `scripts/README.md`, and `agents/README.md`. Adding or changing a sync target means editing all four or the docs silently drift; the 2026-08-26 pass found three of them still claiming agents sync to OpenCode only.

## Last Session

- Built the plugin composition engine (scripts/plugins.py) and converted search-internet from forked agent copies into plugin.json + overlays; verified live on OpenCode 1.18.23 that orchestrator denies web_search_tool while executor/ask/researcher allow it.
- Evolved lean-coder into a full coding-assistant skill: sharpened description (debugging + quoted triggers), added a production-grade loop step and reference guide, deepened the React guide, and made executor.md mandate loading it.
- Added cross-platform agent sync — sync_claude_agents.py (executor.md translated to Claude Code's subagent schema) and sync_antigravity_agents.py (agents/ANTIGRAVITY_AGENTS.md → ~/.gemini/config/AGENTS.md, full overwrite by design). Bob deliberately excluded.
- Caught that agent files must invoke skills by name, not repo path, since the path doesn't survive syncing elsewhere.

## Current Session

**Date:** 2026-08-26
**Focus:** Documentation accuracy pass across root README, AGENTS.md, and the agents/plugins/scripts READMEs after the plugin + cross-platform-agent work landed

### Done
- Rewrote the root README: agents and plugins were entirely absent from it, all invocations said `python3` instead of `uv run`, the destinations table was missing 3 of 8 rows (OpenCode plugins, Claude Code agents, Antigravity AGENTS.md), and the 'other agents' table still told Claude Code users to paste skills into CLAUDE.md despite native ~/.claude/skills sync existing.
- Removed two factual errors from the root README: a reference to a `carousel-builder` skill that does not exist in the repo, and a layout table claiming learning/session skills use `reference/` (singular) and that LinkedIn/Medium skills have no support folder — verified against the tree that every skill uses `references/`, `assets/`, and/or `scripts/`.
- Cut agents/README.md from 284 to 116 lines by dropping prose that restated the frontmatter permission maps verbatim; kept the safety split, the orchestrator/executor workflow, and added a cross-platform table plus the invoke-skills-by-name rule.
- Fixed AGENTS.md: its header claimed the file is gitignored and never committed (it is tracked and not ignored), §6 still said agents and plugins sync to OpenCode only, §5 omitted both new agent-sync scripts and their env vars, §7 listed `tests/` as a sync exclusion that isn't in EXCLUSIONS, and §4 documented no `ask` agent at all.
- Updated scripts/README.md: every `--*-only` flag comment said '(skills)' although three targets now sync agents too; replaced the run-order paragraph with a table and dropped a `chmod +x` troubleshooting entry that is meaningless under `uv run`.
- Fixed two small real bugs in sync_all.py found while verifying the docs: `--help` described it as syncing skills only, and unflushed parent prints made child-script output arrive out of order through a pipe so `--dry-run` was unreadable.
- Verified the pass: every relative link in the five edited docs resolves, `--help` output matches every documented flag, and a full `uv run scripts/sync_all.py --dry-run` exits 0 with all eight scripts reporting in order.

### Decisions
- Left plugins/README.md and plugins/search-internet/README.md untouched — both were written in the same session as the code they describe and audited as accurate.
- Did not create the missing per-category READMEs under skills/learning, skills/development, and skills/content-creation (only agent_session_management has one) — the root README covers those categories and the ask was accuracy, not new surface area.

### Open Items
- [x] Everything through this docs pass is committed (36d4ca0) and the working tree is clean — the previous 'nothing committed' item is resolved.
- [x] .DS_Store hygiene was a false alarm: .gitignore's bare `.*` already covers it and nothing is tracked. Resolved, do not re-flag.
- [ ] skills/learning, skills/development, and skills/content-creation still have no category-level README, unlike skills/agent_session_management — inconsistent, deliberately deferred.
