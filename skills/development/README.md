# Development Skills

Two skills covering the two halves of building software: deciding what to build, and writing the code well.

```
project-planner/  -> rough idea      → PRD, UX spec, phased plan under docs/
lean-coder/       -> any coding work → the least code that is correct and secure
```

They compose in that order — plan first, then implement against the plan — but neither depends on the other.

| Skill | Fires when | Produces |
|---|---|---|
| [**project-planner**](./project-planner/README.md) | You describe something you want to build, or say "write a PRD", "spec this out", "break this into phases" | Markdown only: `docs/prd.md`, a UI/UX or interaction-contract spec, and a phase-by-phase implementation plan with test cases. Never application code |
| [**lean-coder**](./lean-coder/README.md) | Writing, refactoring, reviewing a diff, or debugging — including "clean this up", "is this good code", "make this production-ready", "why is this slow" | Edits to your code, plus a `before → after` LOC delta on refactors |

## lean-coder is meant to fire unprompted

Most code bloat enters in small snippets nobody thought to review, so the skill is written to trigger on *any* coding activity rather than waiting for "keep it short". Its discipline is a fixed loop — Delete, Stdlib, Inline, Secure, Production-grade, Test — where fewer lines is the tiebreaker, never the goal. Security code and anything a test asserts on are never cut.

It ships nine per-language guides (Python, SQL, Scala/Spark, TypeScript/React/Next.js, Solidity, Rust, Swift, Kotlin, React Native) plus a cross-language production-grade checklist. Only the guide for the language in play is loaded.

This repo's `executor` agent mandates loading it before any coding work — a good skill description is a suggestion to the harness's matcher, an agent instruction is a requirement. See [`agents/README.md`](../../agents/README.md).

## Install

```bash
uv run scripts/sync_all.py            # every skill in the repo, all five platforms
```

Or copy a single folder into whichever skills directory your harness reads:

```bash
cp -r lean-coder ~/.claude/skills/    # or ~/.config/opencode/skills/,
                                      # ~/.agents/skills/,
                                      # ~/.gemini/config/skills/, ~/.bob/skills/
```

`project-planner` writes into `docs/` (and optionally `learnings/`) in whatever repo you invoke it from. `lean-coder` writes nothing on its own — it changes how the agent edits your code.
