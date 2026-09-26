---
name: end-session
description: Save compact project memory, current work, and two previous sessions in .agent_docs/handoff.md and commit session changes to Git when the user wraps up, requests a checkpoint, or context is about to reset.
---

# End Session

Keep `.agent_docs/handoff.md` useful as memory for the whole project, including work outside the latest task. Adapt the detail to what another agent needs to continue accurately. A checkpoint saves context and then continues authorized work; stop only when the user is ending work.

## Python execution

Run Python scripts with `uv run` using the target project's `.venv`, including these helpers and project Python commands. Resolve the target root first, then invoke helpers with that environment, for example `uv run --python /absolute/project/.venv/bin/python python /absolute/skill/scripts/helper.py`. Do not execute generated program source through the terminal; save any new reusable script under `/absolute/project/.temp/` first. Check `uv --version` before first use if availability is unknown. If uv is missing, explain that this workflow requires it, ask the user to confirm installation, and wait. After approval, install uv using the official method appropriate to the system and verify `uv --version` before continuing. Existing explicit installation approval counts; do not ask again. If installation is declined or unavailable, use file tools for the handoff and continue independent work; do not silently substitute bare Python.

## Memory to retain

Read the existing handoff before updating it. Use [assets/handoff_template.md](assets/handoff_template.md) as a starting shape. The helper uses these headings; they are a format contract, not a limit on what the agent can remember.

| Section | Content |
|---|---|
| Project Snapshot | Purpose, scope, architecture, important paths, current milestones, and run/test entry points; link to authoritative project docs for detail |
| Cumulative Learnings | Durable decisions with reasons, user preferences relevant to the project, constraints, pitfalls, rejected approaches and why; merge and correct rather than accumulate duplicates |
| Previous Session | Concrete summary of the second session before the current one |
| Last Session | Concrete summary of the session immediately before the current one |
| Current Session | Latest work, decisions, validation results, and all remaining project work needed to resume |

This means current work **plus two previous sessions**, not two writes. Preserve the window during repeated checkpoints and context compaction in the same session. At the next distinct session, rotate it once. Do not infer session boundaries from dates alone.

Aim for roughly 1,000–2,000 tokens for the whole handoff as a flexible starting point, not a cutoff. Prefer concrete paths, outcomes, decisions and reasons, exact useful commands, test results, and next actions over transcripts or repeated descriptions. Keep enough detail to distinguish tested, untested, failed, blocked, abandoned, and completed work. Carry unresolved work across sessions until resolved or explicitly dropped, even when unrelated to today's focus. Do not record secrets.

Keep project memory current: promote durable facts from older sessions before they rotate out, remove obsolete facts, and link to detailed docs or archives when needed. Avoid copying instruction files already maintained elsewhere. A compact memory is an index and decision record for the project, not a replacement for all its source files.

## Write and verify

Use the helper at this skill's installed location, with the target project passed explicitly. Paths below are placeholders; resolve them from the loaded skill location, not from the target project's `scripts/` directory.

```bash
uv run --python /absolute/project/.venv/bin/python python /absolute/path/to/end-session/scripts/handoff_write.py --repo-root /absolute/project --input /absolute/project/.temp/handoff_payload.json --dry-run
uv run --python /absolute/project/.venv/bin/python python /absolute/path/to/end-session/scripts/handoff_write.py --repo-root /absolute/project --input /absolute/project/.temp/handoff_payload.json
```

See [README.md](README.md) for the payload schema. Supply compact `last_session` and `previous_session` summaries when useful; omitted summaries rotate existing concrete records automatically. On subsequent writes for the same session, add `--checkpoint` to both commands. Include the whole updated current session, not just the checkpoint delta. Omitted snapshot/learnings are preserved; supplied learnings replace that section, so merge existing knowledge first.

The helper archives the entire prior handoff before replacing it. Archives contain previously recorded detail, not an automatic transcript. Check the preview for lost project facts or open work, then write and verify the result. Direct file editing is also appropriate when the helper is unavailable; preserve equivalent memory and archive behavior.

## Commit session changes

After saving memory, create a local Git commit for the session's changes, including at checkpoints, unless the user requested a memory-only save or no commit. This is part of the skill workflow; proceed without a separate confirmation when existing instructions allow it. The handoff helper only writes memory; the agent handles Git.

Inspect the repository status and staged and unstaged diffs to identify the session's work. Stage the relevant files or hunks and review the exact commit contents. Preserve unrelated edits and existing staging; do not sweep them into the commit. If unrelated staged changes exist, use a scoped commit that leaves them staged. Ask only if ownership or scope cannot be resolved from the session context.

Include the handoff and archives when project conventions track them. Respect ignore rules; do not force-add `.agent_docs/` or change ignore rules just to create a commit. Commit the project changes even when memory stays local. Use a concise message describing the actual outcome; identify incomplete work as a checkpoint and retain its outstanding checks in the handoff. Run relevant checks as needed, reusing still-valid session results.

Verify the commit succeeded and inspect the remaining working tree. Do not push or amend an existing commit unless separately requested. If there are no eligible changes, skip the empty commit. Outside a Git repository, save memory and report that no commit was possible; do not initialize a repository automatically. If a hook, missing identity, conflict, or permission blocks the commit, retain the saved handoff and report the blocker without bypassing hooks or changing Git identity.

Report the handoff path, commit hash and summary (or why no commit was created), and any material unresolved work. Avoid rewriting a tracked handoff solely to include its own commit hash, which would leave another uncommitted change.
