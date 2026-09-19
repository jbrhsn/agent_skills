# Domain planning prompts

Read the sections relevant to the project. These are decision prompts, not a list of required features. Include the decisions, contracts, and checks that materially change implementation or release safety.

## Web development

Identify browser/server boundaries, user/tenant roles, API contracts, session model, cache ownership, and database consistency. Plan accessible user journeys including validation, loading, empty, error, retry, and session expiry. Define relevant rendering/SEO, deployment, responsive, and compatibility constraints.

For production work, decide what latency/availability means under the expected workload, how failures are observed, and how changes reach users. Include schema migration, old/new API compatibility, cache invalidation, rollout and recovery when affected.

## Data engineering

Record source and sink, row/event grain, business keys, schema ownership, sensitivity/retention, and downstream consumers. Establish volume, cadence/freshness, incremental boundaries, late data, deletes, and quality checks.

Plan delivery semantics end to end: deduplication, partial writes, checkpointing, retries, replay, and concurrent runs. Backfill work needs ranges, capacity limits, live-run isolation, and reconciliation. Include schema evolution and observability for freshness/quality, not just scheduler success.

## Web3 development

Identify chains/networks, custody model, signers/roles, assets and invariants, external protocols, and on-chain/off-chain responsibilities. Distinguish permissionless product actions from privileged administration.

Plan signature replay protection, transaction rejection/pending/finality/replacement, reorg reconciliation, integer units/rounding, and relevant oracle/MEV/slippage assumptions. For upgrades, define storage compatibility, governance, initialization, and recovery limits. Budget for adversarial/invariant testing and independent review when warranted; automated tests do not certify security.

Prepare deployment targets, simulation evidence, and key-management responsibilities without treating planning as authorization to deploy or move funds.

## Android and iOS

Establish supported OS/device targets, native/cross-platform choice, existing design conventions, distribution, and backend compatibility. Design lifecycle, offline behavior, navigation, links, permission denial/revocation, accessibility, and durable versus transient state.

Account for process death, background restrictions, secure storage/backup, persistence migration, notification behavior, and old app versions still calling new APIs. Plan representative device/release-build checks, performance/battery measurements when relevant, signing/release configuration, and recovery constrained by store rollout latency. Verify current store/platform requirements when needed.

## Troubleshooting and debugging

An investigation may need an experiment plan rather than a PRD. Capture symptom, expected behavior, impact, environment, reproduction, observations, and ranked hypotheses. Each experiment should predict a distinguishing result and have a resource/safety boundary.

Separate mitigation from root-cause repair; preserve diagnostic evidence and user data. Include a regression check and evidence needed to conclude recovery. For performance, define the baseline workload, measurement conditions, bottleneck hypothesis, and comparison metrics. Report unknowns instead of fabricating certainty.

## Mixed systems

Define contracts where domains meet: webhook-to-chain confirmation, mobile offline writes to APIs, indexed events to warehouses, or batch publications to web caches. Assign ownership of retries, deduplication, authorization, finality/freshness, and schema compatibility. End-to-end guarantees are no stronger than these boundaries.
