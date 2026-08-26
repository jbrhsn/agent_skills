# Production-Grade — Cross-Language Rules

Load this alongside the language-specific guide when the task is explicitly
about hardening or shipping, not on every routine edit. These are the things
"lean" doesn't cover on its own: what to add once correctness and brevity are
settled.

## Logging & observability

- Structured/leveled logging (`info`/`warn`/`error` + context fields) over
  `print`/`console.log`. A log line with no level or context is unusable in
  aggregation.
- Log at the point that has context (what operation, what input identifiers),
  not deep in a shared helper that doesn't know why it was called.
- One log line per meaningful state transition or failure — not one per
  function call. Noise buries signal.
- Before shipping, ask: if this fails at 3am, does the log tell you what to
  do next? If not, add the missing field, don't add more logs.

## Errors

- Propagate or handle — never catch-and-ignore, never catch-log-rethrow (that's
  two log lines for one failure).
- Fail fast at the boundary that first detects the problem. Don't let a bad
  value travel three layers deep before something rejects it.
- Distinguish expected failures (validation, not-found) from unexpected ones
  (bugs, infra). Expected failures get typed/structured results or specific
  exceptions; unexpected ones should crash loudly in dev and alert in prod —
  never both silently return `null`/`None`.
- Retries need idempotency. Don't add a retry loop around an operation with a
  side effect (write, charge, send) unless it's safe to run twice.

## Dependencies & versioning

- Pin versions for anything that ships (lockfile committed, no floating
  ranges in production dependencies).
- Before adding a dependency, check: does this replace <20 lines of stdlib
  code? If yes, don't add it (same rule as the base lean-coder loop, restated
  because it's the first thing people relax under deadline pressure).

## The gate before "done"

- Run the project's own lint, typecheck, and test commands — whatever's
  already configured (`package.json` scripts, `Makefile`, CI config) — before
  declaring work finished. Don't invent a new tool; use what's there.
- If no such tooling exists, verify by re-reading the diff against the stated
  requirement and say so explicitly rather than claiming a check that didn't
  happen.
- A change that "works on my machine" but wasn't run through the project's
  existing gate isn't verified yet.

## Security posture (on top of the language guide's list)

- Secrets never appear in code, logs, or error messages — including stack
  traces surfaced to a client.
- Any input crossing a trust boundary (network, file, subprocess, DB) gets
  validated there, not three functions later where it happens to be used.
