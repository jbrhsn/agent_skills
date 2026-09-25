# Worked coding-agent handoff

This fictional example shows the level of specificity that helps an implementing agent start. Its paths, endpoint, and command are facts only within the example; inspect the real repository before writing a plan. Use fewer fields for simpler work and different contracts for other domains.

## Outcome and contract

**FR-02:** An authenticated task owner can mark a task complete. A different user cannot change it. Completion remains true if the same request is repeated.

**API contract owned by U-01:** `PATCH /api/tasks/{id}` with `{"completed":true}` returns `200` and `{"id":"t-17","completed":true}`. An invalid body returns `400`, no session returns `401`, a non-owner returns `403`, and an unknown task returns `404`; errors do not change stored state. The existing API error envelope still applies. The UI uses this contract after U-01 passes.

**Existing evidence in this example:** `src/server/tasks.ts` contains task mutation handlers; `src/web/TaskRow.tsx` renders the completion control; `tests/api/tasks.test.ts` and `tests/web/task-row.test.tsx` cover nearby behavior. The inspected `package.json` defines `npm test` as the repository test command. These are example facts, not paths or commands to copy into another project.

## U-01 — Complete a task through the API

**Readiness:** Ready; authentication, task ownership, and persistence already exist. Start by reading the mutation handler and its tests.

**Scope:** Add the contract above in `src/server/tasks.ts` and API regression tests. Reuse existing authorization and error helpers. Related-file edits are allowed where necessary.

**Done when:** The owner can complete a task; repeating the request is safe; invalid, unauthenticated, non-owner, and unknown-task requests return the specified result without changing stored state.

**Check:** In `tests/api/tasks.test.ts`, create tasks for two users, issue each request above, assert response and persisted state, then run `npm test`. Record the test run and any pre-existing failures.

## U-02 — Expose completion in the task row

**Readiness:** Blocked until U-01's contract and API check pass. Start by reading `TaskRow` and its existing interaction tests.

**Scope:** Add a completion control in `src/web/TaskRow.tsx` using the U-01 request. Keep the control disabled while a request is pending. On success, show the completed state; on failure, keep the previous state, show a retryable error, and re-enable the control. Preserve keyboard access and an accessible name.

**Done when:** The owner can complete a task from the row without duplicate submissions; a failed request leaves the displayed task incomplete and permits retry.

**Check:** In `tests/web/task-row.test.tsx`, exercise success, delayed response, and failure/retry with user-level interactions. Run `npm test`. As the integration owner, U-02 also runs the API and UI checks together against the same contract and records the result.

## If the evidence changes

If repository inspection shows an existing task update endpoint with a different method or response shape, pause the affected unit before implementing a conflicting API. Record that evidence, update the authoritative interface contract and U-01/U-02 checks, then continue with the revised contract. Keep FR-02 and unit IDs stable so coverage remains traceable. Unaffected work may proceed.
