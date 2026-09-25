# Worked coding-agent handoff

This fictional example shows the level of specificity that helps an implementing agent start. Its paths, endpoint, and command are facts only within the example; inspect the real repository before writing a plan. Use fewer fields for simpler work and different contracts for other domains.

## Outcome and contract

**FR-02:** An authenticated task owner can mark a task complete. A different user cannot change it. Completion remains true if the same request is repeated.

**API contract owned by U-01:** `PATCH /api/tasks/{id}` with `{"completed":true}` returns `200` and `{"id":"t-17","completed":true}`. An invalid body returns `400`, no session returns `401`, a non-owner returns `403`, and an unknown task returns `404`; errors do not change stored state. The existing API error envelope still applies. The UI uses this contract after U-01 passes.

**Existing evidence in this example:** `src/server/tasks.ts` contains task mutation handlers; `src/web/TaskRow.tsx` renders the completion control; `tests/api/tasks.test.ts` and `tests/web/task-row.test.tsx` cover nearby behavior. The inspected `package.json` defines `npm test` as the repository test command. These are example facts, not paths or commands to copy into another project.

## Shared design decisions

The server owns authorization and durable completion state. Reuse the existing task mutation/persistence path and ensure the ownership check and write cannot allow another user's task to change. The UI owns pending/error presentation and displays completion only after a successful response. This feature adds no schema, public error format, or separate client-side source of truth. Private helper names and test organization remain executor choices within repository conventions; changes to the request, response, or persistence guarantees require revising this shared decision and dependent checks.

The API and UI are separate units because each has independently verifiable behavior and the UI consumes the API contract. Keep the API authorization and persistence changes together: a write without its ownership enforcement is not a coherent intermediate result. This split follows behavior and dependency, not a one-file-per-unit rule.

## U-01 — Complete a task through the API

**Readiness:** Ready; authentication, task ownership, and persistence already exist. Start by reading the mutation handler and its tests.

**Read first:** Applicable repository guidance; this document's [outcome and contract](#outcome-and-contract) for response semantics and inspected paths, and [shared design decisions](#shared-design-decisions) for ownership boundaries; the task mutation handlers in `src/server/tasks.ts` and their existing persistence helper; `tests/api/tasks.test.ts` for authentication and two-user fixtures; `package.json` for the test command. Follow the handler's actual helper references rather than inventing a new persistence path. Include these section links if this unit is handed off separately.

**Scope:** Add the contract above in `src/server/tasks.ts` and API regression tests. Reuse existing authorization and error helpers. Related-file edits are allowed where necessary.

**Done when:** The owner can complete a task; repeating the request is safe; invalid, unauthenticated, non-owner, and unknown-task requests return the specified result without changing stored state.

**Check:** In `tests/api/tasks.test.ts`, create tasks for two users, issue each request above, assert response and persisted state, then run `npm test`. Record the test run and any pre-existing failures.

## U-02 — Expose completion in the task row

**Readiness:** Blocked until U-01's contract and API check pass. Start by reading `TaskRow` and its existing interaction tests.

**Read first:** Applicable repository guidance; this document's [outcome and contract](#outcome-and-contract) and [shared design decisions](#shared-design-decisions); [U-01](#u-01--complete-a-task-through-the-api) and its execution evidence to confirm the dependency passed; `TaskRow` in `src/web/TaskRow.tsx` and its existing request/state handling; `tests/web/task-row.test.tsx` for interaction-test conventions; `package.json` for the test command. This is the minimum starting context for U-02, even when the executor has not seen the planning conversation.

**Scope:** Add a completion control in `src/web/TaskRow.tsx` using the U-01 request. Keep the control disabled while a request is pending. On success, show the completed state; on failure, keep the previous state, show a retryable error, and re-enable the control. Preserve keyboard access and an accessible name.

**Done when:** The owner can complete a task from the row without duplicate submissions; a failed request leaves the displayed task incomplete and permits retry.

**Check:** In `tests/web/task-row.test.tsx`, exercise success, delayed response, and failure/retry with user-level interactions. Run `npm test`. As the integration owner, U-02 also runs the API and UI checks together against the same contract and records the result.

## Execution handback

At planning time, both units are unstarted and all checks are not run. During an authorized build, record status in each unit or link the existing tracker. For U-01, the handback should identify actual changed paths and any contract changes, API check outcomes and tested revision/environment, deviations or blockers, and whether the evidence now permits U-02 to start. If implementation exists but its checks cannot run, report verification blocked and keep U-02's dependency unresolved. Reuse evidence links instead of copying logs; continuing to U-02 requires no extra stop when execution is already authorized.

## Example handoff walkthrough

A planner reviewing U-01 can locate the mutation handler and its tests from the unit's reading list, identify the owner-only idempotent write as the first behavior to implement, obtain exact responses from the contract, distinguish server-owned persistence from local helper choices, and identify response-plus-stored-state assertions as the completion check. If the persistence helper's ownership guarantees cannot be established from the designated code, inspect that helper and settle the design before marking U-01 ready. This illustrates a document walkthrough; no real repository was inspected and no implementation or model evaluation was performed for this fictional example.

## If the evidence changes

If repository inspection shows an existing task update endpoint with a different method or response shape, pause the affected unit before implementing a conflicting API. Record that evidence, update the authoritative interface contract and U-01/U-02 checks, then continue with the revised contract. Keep FR-02 and unit IDs stable so coverage remains traceable. Unaffected work may proceed.
