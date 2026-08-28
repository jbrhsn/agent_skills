# Project Handoff

<!-- Managed by the end-session / init-session skills. Section order is fixed; the file is compacted on every write, not appended to. -->

## Project Snapshot

agent_skills: curated 11-skill distribution repo for OpenCode, IBM Bob, Google Antigravity, Claude Code, and Codex/ChatGPT, plus 3 base agent definitions (orchestrator, executor, ask) and 1 opt-in OpenCode plugin (search-internet).
Skill organization: agent_session_management (2), learning (2), development (2), content-creation (5).
Sync model: scripts/common.py + per-platform scripts, dynamic discovery, PEP 723 + `uv run`. Agents/plugins sync fully to OpenCode (composition engine in scripts/plugins.py handles overlays); executor.md also translates to a Claude Code subagent at ~/.claude/agents/; Antigravity gets one global instructions file at ~/.gemini/config/AGENTS.md. IBM Bob and Codex/ChatGPT get skills only (at ~/.bob/skills and ~/.agents/skills respectively). Full SHA-256 checksum and parity verification integrated via `sync_all.py --verify`.

## Cumulative Learnings

- Shared helper module (`common.py`) + dynamic skill discovery (`Path.glob('**/SKILL.md')`) eliminates hardcoded lists and reduces multi-platform sync boilerplate by ~75% while keeping CLI backwards compatibility.
- Compaction on every write (never append) keeps handoff.md read cost bounded even on 100+ session projects.
- Claude Code on macOS uses `~/.claude/skills/{skill-name}/SKILL.md` for personal skills, with direct drop-in compatibility with OpenCode/Antigravity/Bob format.
- Codex CLI and ChatGPT desktop harness discover user-wide skills at `~/.agents/skills/{skill-name}/` with identical drop-in layout (SKILL.md, references, assets, scripts); agent translation is omitted as Codex uses TOML layers rather than OpenCode Markdown frontmatter.
- Evidence-backed ideation (velocity scoring, live sources) outperforms interview-driven brainstorm; users want signals, not questions.
- LinkedIn algorithm mechanics (dwell time, saves, substantive comments) differ materially from generic engagement; algorithm-informed rules yield better results.
- OpenCode plugin-provided custom tools are allow-by-default in every agent unless a permission explicitly denies them (verified empirically on 1.18.23) — a plugin's runtime file and its agent permission overlays must install atomically, or the orchestrator silently gains the tool.
- OpenCode 1.18.23 reads the singular `agent/` and `plugin/` config paths, not the plural `agents/`/`plugins/` its own docs describe — verified empirically, don't 'fix' this.
- Frontmatter deep-merge across plugin overlays must recurse via `dst.setdefault(key, {})`, not `dst.get(key)` — `.get` lets the first plugin's nested dict win wholesale, so conflict provenance is only recorded on the parent key and a second plugin silently overwrites the leaf with no error.
- Claude Code subagent frontmatter (confirmed against official docs) has no per-command bash permission map like OpenCode's `permission.bash` patterns — required fields are just `name`+`description`; granular allow/ask/deny gates have to be expressed as a plain-language instruction in the body instead, not faked in frontmatter.
- Any agent-file instruction that references a skill by literal repo path (e.g. `skills/development/lean-coder/SKILL.md`) breaks once the file is synced to another platform/project — skills flatten to `skills/{name}/` at every destination (no category subfolder) and live in a completely different tree than the target project. Invoke skills by name, never by hardcoded path, in anything that gets synced out.
- Antigravity has no per-mode agent-file concept — one flat `AGENTS.md` at `~/.gemini/config/AGENTS.md` governs every agent session in the workspace; IBM Bob has real subagents/custom-modes but no publicly documented config file format to target.
- .gitignore line 18 is a bare `.*`, which already ignores every dotfile including `.DS_Store` — no separate entry is needed, and none is tracked. `.agent_docs/handoff.md` is nonetheless committed despite `.agent_docs/` being listed, because gitignore has no effect on already-tracked files. Verify with `git check-ignore -v` before re-flagging either as a hygiene gap.
- The destination/env-var mapping is duplicated across four docs — root `README.md`, `AGENTS.md` §5-6, `scripts/README.md`, and `agents/README.md`. Adding or changing a sync target means editing all four or the docs silently drift; the 2026-08-26 pass found three of them still claiming agents sync to OpenCode only.
- Repo-only files can live safely at `skills/{category}/` level (category READMEs, notes) — discovery globs `**/SKILL.md` and copies only the containing skill directory, so anything outside a skill dir is never synced anywhere. Verified against a full `--dry-run`.
- All 11 skills require exact 1:1 matching between folder name and YAML frontmatter `name:` (e.g., `medium-article-writer`) to ensure multi-platform discovery and invocation consistency.
- `sync_all.py --verify` performs full SHA-256 tree hashing, file-by-file parity checking, and extra/orphaned directory detection across all destinations.
- When adding new reference files to project-planner, split by concern to keep individual files under ~170 lines — the Stage 8 load already pulls 4 files together; bloating any one of them wastes context. Extracted agent-execution material into `execution-spec.md` (69 lines) to avoid plan-spec.md growing to ~200 lines.

## Last Session

- Evaluated dev skills (lean-coder, project-planner) and implemented 7 improvements across references and templates.
- Expanded lean-coder production-grade guide with 6 new operational hardening sections.
- Created project-planner execution-spec.md and updated plan templates with per-unit execution contracts.
- Verified all 11 skills across platforms with SHA-256 parity and committed changes (commit 8cb3d30).

## Current Session

**Date:** 2026-08-28
**Focus:** Added Codex and ChatGPT desktop harness skill sync support and committed changes

### Done
- Created `scripts/sync_codex_skills.py` targeting `~/.agents/skills/` with `--verify` and `--dry-run` support.
- Integrated `codex` target into `scripts/sync_all.py` (`--codex-only` and master sync).
- Updated `AGENTS.md`, `README.md`, and `scripts/README.md` to document the 5 supported harnesses and `CODEX_SKILLS` env var.
- Verified dry-run sync across all 5 targets.
- Committed all changes to `main` (commit `d1a1b95`).

### Decisions
- Codex/ChatGPT sync targets skills only (~/.agents/skills/) without translating Markdown agent files, as Codex uses TOML layers rather than OpenCode Markdown frontmatter.

### Open Items
- [ ] Push local commits (8cb3d30, d1a1b95) to remote repository
