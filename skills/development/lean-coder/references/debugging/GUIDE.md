# Troubleshooting and debugging

Use for functional failures, incidents, flaky tests, build problems, and performance regressions. Diagnosis produces evidence; an authorized fix also changes and verifies code.

## Establish evidence

Capture expected versus observed behavior, a useful reproduction, environment and versions, triggering input, timestamps, and the first relevant error. Read the failing path and recent changes; do not assume the last edited line caused the failure. Distinguish application defects from configuration, permissions, dependency failures, resource exhaustion, and test harness problems.

Follow the operation across boundaries using redacted logs, traces, metrics, execution plans, crash reports, or thread dumps. Correlate by request, job, partition, transaction, or build ID. Avoid dumping entire payloads or secrets. Separate observations from hypotheses.

## Narrow the cause

Rank hypotheses by evidence and impact. Choose a check that distinguishes them: compare working/failing inputs, isolate a dependency, inspect state transitions, or bisect in an isolated checkout. Prefer a minimal failing test when practical.

Change one causal variable at a time where possible. A hypothesis needs a predicted observation and a disconfirming check. Repeatedly rerunning a flaky test or increasing timeouts without understanding the condition is not a fix. If reproduction is unavailable, state confidence and gather bounded instrumentation.

For slowness, locate the cost before optimizing: browser render/network, API queue, DB query/lock, Spark shuffle/skew, worker backlog, RPC, or mobile main thread. Compare equivalent workloads; account for warmup, data distribution, concurrency, and noise. Inspect tail latency and resource cost as well as averages.

## Mitigate and repair

During an incident, limit impact within authorized scope while preserving evidence. Separate mitigation from cause: restart, rollback, or traffic reduction may restore service without explaining the defect. Do not replay writes, purge queues, reset checkpoints, run destructive SQL, or broadcast transactions as an unexamined diagnostic step.

Fix the owning boundary instead of suppressing symptoms. Add a regression check that catches the original failure when practical, then test adjacent behavior. For races and flaky tests, control clocks/scheduling or test the invariant; do not replace synchronization with sleeps.

Stop an experiment when it risks data, exceeds its resource budget, or stops producing new evidence. Continue independent investigation and identify missing access, data, or environment precisely.

## Report

Explain symptom → evidence → cause (or leading hypothesis) → fix or mitigation → verification. Include relevant locations, commands, measurements, and uncertainty. A timeout disappearing once does not establish causality; a local green run does not establish production recovery.
