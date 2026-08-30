# Execution spec

Read alongside `plan-spec.md` at Stage 8. This covers the three additions that make a plan agent-executable, not just human-readable: bootstrap expectations, regression guards, and the per-unit execution contract.

## Phase 1 bootstrap expectations

Before Phase 2 starts, Phase 1 must establish these — not as implementation details, but as "Done when" items on the relevant Phase 1 units:

- **Dependency lockfile committed.** `package-lock.json`, `uv.lock`, `Cargo.lock` — whichever the stack uses. Without this, the next agent session resolves different versions and breaks silently.
- **Linter/formatter configured and passing.** Every subsequent unit starts from a clean baseline. A unit that introduces lint failures and leaves them is not done.
- **Single verification command.** One command that runs lint + typecheck + test (e.g. `npm run check`, `make ci`, a script in `package.json`). This is what every unit's execution contract references as the verification command.
- **`.gitignore` for the stack.** `node_modules/`, `__pycache__/`, `.env`, build artifacts — committed in Phase 1 so no agent session accidentally commits them.
- **Environment variable handling.** A `.env.example` or config module pattern established before any unit needs secrets or environment-specific values.

These are prerequisites for the test harness, not the harness itself. A project with a working test runner but no lockfile will drift across agent sessions.

## Regression guard

When a unit's **In scope** touches files or behavior introduced by a unit it **Depends on**, that dependency's test cases must re-pass as part of this unit's verification — do not defer to phase exit. List them in a **Regression check** line in the unit.

This catches breaks at the unit level (one sitting, cheap to fix) instead of the phase level (multiple sittings deep, expensive). In agentic builds this matters even more: the agent has no memory of why the earlier unit worked, so a late regression is doubly expensive to debug.

**Regression check** lists specific test case IDs from dependency units. Omit the line when the unit does not touch anything an earlier unit built. Include it whenever **In scope** overlaps with a dependency's scope — the executing agent runs these before declaring done.

## Verify with

Tells the executing agent exactly how to prove the unit works:

- For automated units: the project's single verification command from Phase 1.
- For manual units: the specific steps to walk through and what to observe.

This is not implementation code — it is the contract between the plan and the agent that builds it. A "Done when" with no "Verify with" leaves the agent guessing how to prove it.

## Execution contract

Scopes the executing agent's session. Four lines:

- **Isolation:** how to isolate this work (branch per unit, commit on green, etc.)
- **Verification:** the exact command or steps that prove the unit works
- **Done signal:** what must all be true before the agent stops (test cases pass, regression check passes, lint clean)
- **Scope boundary:** do not modify files outside what **In scope** names; do not start the next unit

The executing agent follows this contract rather than inventing its own strategy. Without it, different agent sessions scope differently — one commits to main, the next branches, the third forgets to run tests — and the codebase drifts.
