# Behavioral evaluation

Use when evaluating changes to lean-coder, not during ordinary implementation. This is an evaluation protocol and case selection guide; no model performance results are claimed. Prefer captured real-session tasks with reproducible starting states. Label invented fixtures as synthetic and confirm improvements on real work before generalizing.

## Prepare five cases

For each case, retain the original user request, sanitized repository snapshot or commit, setup/check commands, supported environment, and evaluator-only acceptance checks. Provide enough code and dependencies to reproduce the behavior without live credentials or production mutations. Keep expected fixes and hidden checks out of the agent's context.

| Case | Task to capture | Evaluator checks |
|---|---|---|
| Focused defect | Fix a formatter or transformation edge case in an existing project | Original failing input now works; adjacent behavior and public contract remain intact; patch avoids unrelated restructuring. |
| Lean reuse | Add a small feature where an existing helper or standard/platform API fits | Feature works; existing capabilities were considered; new dependencies and abstractions have a present purpose; useful boundaries remain intact. Accept multiple sound designs. |
| Authorization | Repair a tenant/object access defect in an API | Direct unauthorized requests fail at the server; legitimate requests still work; response/cache paths do not leak other users' data. |
| Retry and concurrency | Repair a duplicate durable effect after concurrent requests or an ambiguous timeout | Replay and concurrent attempts preserve the domain invariant; tests exercise persistence and failure timing; an in-process lock or header alone is insufficient evidence. |
| Unlisted language | Implement a bounded change in a language without a dedicated lean-coder guide | Uses supported APIs, native error/resource/concurrency conventions, and existing checks; no unrelated toolchain migration or borrowed language assumptions. |

## Compare runs fairly

1. Freeze task snapshots, checks, skill revision, and scoring criteria before comparing. Use a fresh isolated checkout and conversation for each run.
2. Run each case with and without lean-coder on a selected smaller model and a selected larger model. Record exact model identifiers, settings, tool access, environment, and time/token budgets. Hold these constant within each paired comparison. In the baseline, disable automatic loading of lean-coder while retaining the same repository and other instructions; record unavoidable harness differences.
3. Keep evaluator-only checks separate from instructions given to the agent. Score artifacts and observed behavior rather than claims in its final message. Where practical, review without knowing which configuration produced the patch.
4. Repeat paired trials when feasible to reveal variability. Record the run count and failures; a single successful run is a smoke check, not evidence of consistent improvement. Missing setup or tool access is an environment limitation, not a passing result.
5. Compare per-case outcomes before averages. Investigate regressions and make targeted revisions; use fresh holdout tasks before treating an improvement as general.

## Score outcomes

Score each dimension from 0 to 4: 0 = absent or harmful, 1 = major gaps, 2 = partial, 3 = meets the case requirements, 4 = meets them with robust evidence for relevant edge cases. Mark genuinely inapplicable dimensions N/A and explain why. Convert applicable scores to a percentage using `100 * sum(scores) / (4 * applicable_dimension_count)`; report individual dimensions alongside the total.

| Dimension | Evidence |
|---|---|
| Correctness | Acceptance checks, preserved contracts, and relevant edge cases |
| Security and reliability | Boundary enforcement, failure behavior, resource limits, and invariant preservation affected by this case |
| Lean scope and reuse | Focused diff, suitable reuse, justified abstractions/dependencies, understandable code |
| Verification | Checks that can catch the defect or prove the changed contract, with meaningful integration coverage where needed |
| Evidence honesty | Accurate passed/failed/not-run reporting, supported compatibility claims, and explicit material limitations |

A failing required acceptance check, unauthorized data exposure, data loss, or duplicate effect that violates the case contract makes that run unsuccessful regardless of its average score. Do not reward shorter code that loses correctness or safety.

Record case/snapshot, skill revision or baseline, model/settings, trial, environment limitations, check outcomes, dimension scores, success/failure, wall time, tokens/cost when available, and reviewer notes. Report LOC and dependency changes only as context. Keep setup failures separate from completed-task success rates and publish sample counts; leave unavailable metrics unknown rather than estimating them as measurements.
