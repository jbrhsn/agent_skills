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
- Repo-only files can live safely at `skills/{category}/` level (category READMEs, notes) — discovery globs `**/SKILL.md` and copies only the containing skill directory, so anything outside a skill dir is never synced anywhere. Verified against a full `--dry-run`.
- `skills/content-creation/Medium/medium-article-writer/` declares `name: medium-article` in its SKILL.md frontmatter — folder name and frontmatter name disagree. Sync uses the directory name for the destination folder, so harnesses keying off frontmatter and harnesses keying off the directory will resolve different skill names. Unresolved as of 2026-08-26.

## Last Session

- Documentation accuracy pass across root README, AGENTS.md, agents/README.md and scripts/README.md — agents and plugins were absent from the root README, all invocations said `python3` instead of `uv run`, and three docs still claimed agents sync to OpenCode only.
- Removed real factual errors: a nonexistent `carousel-builder` skill, a wrong support-folder table, `tests/` listed as a sync exclusion it isn't, and AGENTS.md's false claim that it is gitignored.
- Fixed two small sync_all.py bugs found while verifying docs: `--help` described skills-only, and unflushed parent prints made `--dry-run` output arrive out of order through a pipe.
- Deliberately deferred the missing per-category skill READMEs — closed in this session.

## Current Session

**Date:** 2026-08-26
**Focus:** Category-level READMEs for the three skill categories that lacked them

### Done
- Created skills/development/README.md, skills/learning/README.md, and skills/content-creation/README.md, modeled on the existing agent_session_management house style: ASCII flow block, fires-when/produces table, one 'why this category coheres' section, Install.
- Grounded each in actual SKILL.md frontmatter and grepped output filenames rather than paraphrasing the root README — content-creation's table names the real artifacts (source.md, kresearch.md, linkedin_post.md, linkedin_post_notes.md, medium_article.md, medium_image_prompts.md).
- Documented the source.md-per-folder convention in content-creation/README.md as the actual handoff format between all five skills, including why being inside such a folder is usually enough to trigger the right skill without naming it.
- Linked all four category headings in the root README to their category directories.
- Verified: every relative link in the root README and the three new files resolves, and a full `uv run scripts/sync_all.py --dry-run` (49 sync lines) confirms the category READMEs are not picked up as skills.

### Decisions
- Category READMEs stay repo-only by construction rather than by an exclusion rule — they sit outside any skill directory, so `**/SKILL.md` discovery never reaches them. No change to EXCLUSIONS was needed.
- Each category README explains one non-obvious thing rather than restating the root README's skill table: why lean-coder is meant to fire unprompted, why scaffolding and authoring are split, and the source.md convention.

### Open Items
- [ ] medium-article-writer's SKILL.md declares `name: medium-article` while its folder is `medium-article-writer` — raised with the user, not fixed. Decide which name wins before it causes an invocation miss.
- [x] Category READMEs and the root README heading links are committed (6b077ec); working tree clean.
