# Execution readiness

A plan should let an implementing agent start without rediscovering prerequisites. It does not grant additional permissions or force a branch, commit, or stop after every unit.

## Environment and prerequisites

Inspect existing package managers, supported versions, CI, test runners, configuration, and deployment setup. Reuse working infrastructure. For a new project, include only the setup needed for reproducible builds and relevant verification: dependencies/lockfiles according to ecosystem conventions, safe configuration examples, ignored generated/secrets files, and test tooling.

State real commands when known. Label proposed commands until implemented and verified. A single check command can be convenient, but multiple established commands are fine. Python commands use `uv run`; obtain confirmation before installing missing uv.

Identify fixtures, database instances, emulators/devices, local chains, credentials, or external sandboxes required by checks. Mark unavailable prerequisites and what they block; do not imply local availability.

## Unit execution notes

Record the intended outcome, likely affected code/contracts, dependencies, checks, and completion evidence. Point to tests for behavior that could regress. Keep the outcome in scope while allowing necessary related-file edits.

For a plan handed to coding agents, mark a unit ready only when its prerequisites exist or are explicitly available, its externally visible behavior and relevant edge cases are settled, its verification environment is identified, and the next implementation action is clear. Give the agent the smallest useful context: links to authoritative decisions/contracts, existing paths and symbols when known, representative input/output or state transitions where ambiguity matters, and a check with an expected result. Do not fill gaps with invented repository facts or commands. If a decision can be deferred safely, state the allowed assumption and its boundary; if it changes the contract or acceptance result, name the blocked unit and who or what resolves it.

When implementation contradicts an assumption or reveals a missing contract, record the evidence and affected requirements/units, update the authoritative decision or contract, then revise dependencies and checks before continuing affected work. Preserve stable IDs and distinguish superseded guidance from the current plan. Keep the plan's detail proportional to the work; a small unit may need only a short paragraph and one check.

Use the repository's isolation/commit conventions and user instructions. Continue through authorized units once their dependencies are satisfied; do not impose a new permission gate between them. Unrelated failures should be recorded and distinguished from regressions introduced by the change.

Separate local preparation from production actions. Migrations, deployments, contract broadcasts, store submissions, and destructive recovery steps require the applicable authorization and a concrete reviewable target; a plan is not blanket approval.
