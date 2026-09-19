# Execution readiness

A plan should let an implementing agent start without rediscovering prerequisites. It does not grant additional permissions or force a branch, commit, or stop after every unit.

## Environment and prerequisites

Inspect existing package managers, supported versions, CI, test runners, configuration, and deployment setup. Reuse working infrastructure. For a new project, include only the setup needed for reproducible builds and relevant verification: dependencies/lockfiles according to ecosystem conventions, safe configuration examples, ignored generated/secrets files, and test tooling.

State real commands when known. Label proposed commands until implemented and verified. A single check command can be convenient, but multiple established commands are fine. Python commands use `uv run`; obtain confirmation before installing missing uv.

Identify fixtures, database instances, emulators/devices, local chains, credentials, or external sandboxes required by checks. Mark unavailable prerequisites and what they block; do not imply local availability.

## Unit execution notes

Record the intended outcome, likely affected code/contracts, dependencies, checks, and completion evidence. Point to tests for behavior that could regress. Keep the outcome in scope while allowing necessary related-file edits.

Use the repository's isolation/commit conventions and user instructions. Continue through authorized units once their dependencies are satisfied; do not impose a new permission gate between them. Unrelated failures should be recorded and distinguished from regressions introduced by the change.

Separate local preparation from production actions. Migrations, deployments, contract broadcasts, store submissions, and destructive recovery steps require the applicable authorization and a concrete reviewable target; a plan is not blanket approval.
