# Handoff Log

## Project Summary

`agent_skills` is a curated collection of portable AI-agent skill files (`SKILL.md`) for OpenCode and IBM Bob. It contains 12 skills across four categories: `agent_session_management/` (2), `learning/` (3), `development/` (4), and `content-creation/` (3). The repo has no build system, CI, or formal tests; it is pure content (Markdown) plus small Python sync scripts. Key artifacts: each skill's `SKILL.md` (primary interface, frontmatter `name` must match its folder name) and `README.md` (human-readable guide), global sync infrastructure under root `scripts/` (`sync_all.py`, `sync_opencode_skills.py`, `sync_bob_skills.py`), and `.agent_docs/handoff.md` for session continuity. Architecture is file-centric: each skill is independently installable via directory copy to `~/.config/opencode/skills/` or `~/.bob/skills/`. The prior `content-creation/linkedin-medium/` pipeline (10 skills: seed-expander, draft-builder, linkedin-writer, medium-writer, carousel-builder, medium-imager, tutorial-verifier, editorial-reviewer, voice-profiler, content-tracker) was deleted in commit `7d526b5` and has been replaced this session with a smaller, standalone `content-creation/linkedin/` trio: `linkedin-post-writer`, `linkedin-image-prompts`, `linkedin-post-reviewer`. These new skills have no shared folder conventions or voice-profile dependency — each colocates its output next to whatever source file the user points it at, and craft rules are inlined directly in each `SKILL.md` (no `reference/`/`scripts/` support folder). Critical constant: `scripts/sync_opencode_skills.py` and `scripts/sync_bob_skills.py` have a pre-existing bug (`tarfile.open(fileobj=None, ...)` in `sync_skill()`) that causes every skill to fail copying — not yet fixed, worked around this session via manual `cp -r` into `~/.config/opencode/skills/`.

## Session Log

### Session: 2026-07-28 — LinkedIn Skills Rebuild (current)
**Files touched:**
- `content-creation/linkedin/linkedin-post-writer/SKILL.md` — created (notes/draft → `linkedin_post.md`; hook-engineering gate, Short/Long/Article type detection, scroll-first structure, no-link-in-body, engagement-bait avoidance, self-audit + review-first stop)
- `content-creation/linkedin/linkedin-post-writer/README.md` — created
- `content-creation/linkedin/linkedin-image-prompts/SKILL.md` — created (finished post → `image_prompts.md`; single hero image vs. 6–9 slide carousel decision, one prompt + text overlay + rationale per slide)
- `content-creation/linkedin/linkedin-image-prompts/README.md` — created
- `content-creation/linkedin/linkedin-post-reviewer/SKILL.md` — created (finished post → `linkedin_post_revised.md`; 5-dimension /100 virality rubric, one refined version, itemized change list)
- `content-creation/linkedin/linkedin-post-reviewer/README.md` — created
- `README.md` (root) — Content Creation section, install commands, and support-folder table updated to reference the new `content-creation/linkedin/` trio instead of the deleted `linkedin-medium/` pipeline
- `scripts/sync_opencode_skills.py` — `SKILLS` list fixed: removed 10 stale `content-creation/linkedin-medium/*` entries (deleted in a prior commit), added the 3 new `content-creation/linkedin/*` paths
- `scripts/sync_bob_skills.py` — same `SKILLS` list fix as above
- `~/.config/opencode/skills/linkedin-post-writer/`, `~/.config/opencode/skills/linkedin-image-prompts/`, `~/.config/opencode/skills/linkedin-post-reviewer/` — manually copied (global sync scripts are broken, see Open Items)

**Summary:** Replaced the deleted `linkedin-medium/` skill pipeline with 3 new standalone LinkedIn skills under `content-creation/linkedin/`, each grounded in researched 2026 LinkedIn algorithm mechanics (saves ≈5x reach of a like, comments ≈2x, dwell-time penalty for body links, engagement-bait suppression, carousel engagement advantage). All three write output next to the user-supplied source file rather than to a fixed folder, per explicit user requirement. Root `README.md` and both sync scripts' hardcoded skill lists were updated to match the new structure; the sync scripts previously referenced non-existent deleted paths and would have failed entirely.

**Outcome:** All 3 new skills have valid frontmatter (`name` matches folder name) and are live in `~/.config/opencode/skills/`, installed via manual copy due to a pre-existing sync-script bug. Repo skill count is now 12 (down from the previously recorded 19, reflecting the `linkedin-medium/` deletion plus this session's 3 additions). Nothing is committed to git yet.

### Session: 2026-07-25 — Skills Sync & Repair (previous)
**Files touched:**
- `scripts/sync_all.py` — created (unified sync script, both configs)
- `scripts/sync_opencode_skills.py` — created (OpenCode-only sync)
- `scripts/sync_bob_skills.py` — created (Bob-only sync)
- `scripts/README.md` — created (sync documentation)
- `PROJECT_COMPLETION.md` — created (project completion report)
- `content-creation/linkedin-medium/medium-imager/` — 7 bugs fixed
  - `engine/layout_engine.py` — Pygments code_highlight integrated
  - `engine/render.py` — slug bug fixed, auto-mode implemented, error handling enhanced
  - `templates/code_card.html` — highlighted HTML rendering
  - `examples/example_spec.yaml` — created (110-line example)
  - `SKILL.md` — output filenames documentation fixed
- `content-creation/linkedin-medium/carousel-builder/` — 2 issues fixed
  - `SKILL.md` — overflow auto-fit behavior documented
  - `engine/render.py` — no-op --pdf flag removed
- `~/.config/opencode/skills/` — all 19 skills re-synced with fixes
- `~/.bob/skills/` — all 19 skills synced with fixes

**Summary:** Complete skills evaluation, bug-fix cycle, and global deployment. Identified and fixed 8 bugs across medium-imager (7: Pygments disconnection, slug inconsistency, auto-mode stub, dead code, missing examples, poor error handling, docs mismatch) and carousel-builder (2: overflow documentation, no-op flag). Implemented all fixes using subagents (lean-coder discipline). Created three production-ready Python sync scripts in `/scripts/` repository folder to automate syncing to both OpenCode and Bob global configs. Synced all 19 skills to both locations with 100% parity, excluded build artifacts (~2.5GB saved). All fixes verified with dry-run tests.

**Outcome:** Repository skills are production-ready in both OpenCode and Bob global configs. Sync infrastructure in place and tested. All 8 bugs resolved. Complete documentation and project completion report generated. Next session can start with testing or further enhancements.

## Open Items / Next Steps

- [ ] `scripts/sync_opencode_skills.py` (`sync_skill()`, lines ~88–103) — fix the broken tar-copy block: `tarfile.open(fileobj=None, ...)` raises on every call, so `python3 scripts/sync_opencode_skills.py` currently fails to sync all 12 skills. Replace with a plain `shutil.copytree(source_path, dest_path, ignore=shutil.ignore_patterns(*EXCLUSIONS))` call, removing the dead `tarfile` usage entirely.
- [ ] `scripts/sync_bob_skills.py` — verify whether it has the same tar-copy bug as `sync_opencode_skills.py` (not yet inspected line-by-line this session) and apply the same fix if present.
- [ ] `content-creation/linkedin` skills — not yet synced to `~/.bob/skills/`; only manually copied to `~/.config/opencode/skills/` this session.
- [ ] Root `.agent_docs/handoff.md` / `README.md` skill counts — no other stale references to `linkedin-medium/` were found outside `README.md` and the two sync scripts, but a full-repo grep was not exhaustively re-run after the edits in this session.

## Quick Reference

- **Root folders:** `agent_session_management/` (2 skills), `learning/` (3), `development/` (4), `content-creation/linkedin/` (3: `linkedin-post-writer`, `linkedin-image-prompts`, `linkedin-post-reviewer`).
- **Sync workflow (currently broken):** Edit in repo → `python3 scripts/sync_all.py --dry-run` → `python3 scripts/sync_all.py` → verify with `ls ~/.config/opencode/skills/` and `ls ~/.bob/skills/`. `sync_opencode_skills.py`'s `sync_skill()` fails on the actual copy step (only `--dry-run` currently works) — see Open Items.
- **Skill template:** Every skill needs `SKILL.md` (frontmatter `name` + `description`, must match folder name) + `README.md`.
- **LinkedIn skill conventions:** each of the 3 `content-creation/linkedin/` skills reads a user-supplied source file and writes its output **in that same directory** (`linkedin_post.md`, `image_prompts.md`, `linkedin_post_revised.md` respectively) — never to a fixed `linkedin/`/`drafts/` folder, and never silently overwrites an existing output file.
- **LinkedIn skill chain:** `linkedin-post-writer` → `linkedin-image-prompts` and/or `linkedin-post-reviewer` (both read the writer's output, no hard dependency).
- **No voice-profile system anymore:** the 3 new LinkedIn skills are self-contained with no `voice-tone/` dependency, unlike the deleted `linkedin-medium/` pipeline.
- **Global config locations:** OpenCode = `~/.config/opencode/skills/`, Bob = `~/.bob/skills/`. OpenCode currently has stale leftover folders from the deleted pipeline (`linkedin-writer`, `editorial-reviewer`, `carousel-builder`, etc.) alongside the new 3 — not cleaned up this session.
- **Session continuity:** Use `/init-session` at session start, `/end-session` at session end to restore/save context to `.agent_docs/handoff.md`.
- **No AGENTS.md exists** at the repo root — this handoff file is the only persistent cross-session context document.
- **Status (2026-07-28):** 3 new LinkedIn skills built and manually installed to OpenCode global config. Sync scripts fixed for path references but still have an unrelated pre-existing copy bug. Nothing committed to git yet this session.
