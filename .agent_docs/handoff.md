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

## Last Session

- Added Claude Code skill sync (`sync_claude_skills.py`, `--claude-only`); all 4 platforms got skills for the first time.
- Refactored sync scripts onto a shared `common.py` with dynamic skill discovery, cutting sync tooling from 1003 to 255 LOC.
- Updated docs (scripts/README.md, README.md, AGENTS.md) to match the refactor.

## Current Session

**Date:** 2026-08-26
**Focus:** Convert search-internet into a real opt-in OpenCode plugin with composable agent overlays; evolve lean-coder into a full coding-assistant skill; align Claude Code and Antigravity agent sync with the OpenCode model

### Done
- Built the plugin composition engine (scripts/plugins.py): discovery, manifest validation, frontmatter deep-merge with cross-plugin conflict detection, append-only '## Capability' body sections, manifest-scoped pruning.
- Converted search-internet from 3 forked full-agent copies into plugin.json + 3 small overlays (orchestrator denies web_search_tool, executor/ask allow it) + a net-new researcher.md subagent.
- Rewrote sync_opencode_agents.py (compose + sync + --verify against `opencode debug agent`), sync_opencode_plugins.py (was broken/hardcoded to a nonexistent path), and sync_all.py (--plugins/--list-plugins/--verify).
- Verified live on OpenCode 1.18.23: orchestrator web_search_tool=False, executor/ask/researcher=True; deselect-then-reselect round-trip clean and byte-identical to base.
- Evolved the lean-coder skill: fixed a mangled title, sharpened its description to explicitly cover debugging plus quoted trigger phrases, added a 'production-grade' loop step backed by a new references/production-grade/GUIDE.md, and deepened references/typescript-react/GUIDE.md with accessibility, error boundaries/Suspense, and performance guidance.
- Added a mandatory 'load lean-coder' instruction to executor.md — this, not the skill description alone, is what actually gets it invoked during coding work.
- Built cross-platform agent sync: scripts/sync_claude_agents.py (translates OpenCode mode:subagent agents into Claude Code's real subagent schema, verified against Claude Code's own docs rather than a first guess) and scripts/sync_antigravity_agents.py (copies a new agents/ANTIGRAVITY_AGENTS.md to ~/.gemini/config/AGENTS.md, full overwrite per explicit user choice). Factored a shared `install()` helper into plugins.py to remove duplication between the OpenCode and Claude Code agent syncs.
- Caught and fixed a bug from earlier in the session: the lean-coder instruction added to executor.md pointed at a literal repo path that doesn't exist once synced elsewhere; switched to name-based skill invocation.
- Ran a full sync across all 4 platforms with --dry-run then live; verified Claude Code's synced executor.md parses as valid YAML and both new destination files landed correctly.

### Decisions
- Antigravity's AGENTS.md is treated as fully repo-managed and overwritten on every sync, not merged or appended — explicit user choice, since the pre-existing file's content and provenance were uncertain.
- IBM Bob agent/subagent sync deliberately skipped for now — its custom-agent config format isn't documented publicly enough to target without guessing.
- orchestrator/ask (mode: primary) get no Claude Code subagent translation — Claude Code's own top-level session is that equivalent, governed by CLAUDE.md, not an agent file.

### Open Items
- [ ] Nothing has been committed this session — plugins/search-internet/, scripts/plugins.py, scripts/sync_claude_agents.py, scripts/sync_antigravity_agents.py, agents/ANTIGRAVITY_AGENTS.md, the executor.md fix, lean-coder skill changes, and doc updates are all uncommitted.
- [ ] .DS_Store hygiene still unaddressed: .gitignore has no .DS_Store entry and stray .DS_Store files exist under plugins/ — flagged previously, never fixed.
