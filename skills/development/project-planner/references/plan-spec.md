# Implementation planning

Use existing plan conventions or start from [the plan template](../assets/plan.template.md). For small work, combine requirements, approach, and checks in one document. For larger work, an overview plus phase files keeps each unit reviewable.

## Sequence by dependencies and risk

Choose milestones that produce observable value or retire significant uncertainty. Prefer an early end-to-end slice over completing isolated architectural layers. Existing projects may start with a failing regression test, compatibility check, or migration rehearsal rather than new scaffolding.

Use bounded discovery spikes for unresolved technical risks: state the question, experiment, evidence needed, and decision it will unlock. Do not turn an unknown into a confident estimate or unsupported implementation commitment.

## Units

Each unit needs an outcome, scope, dependencies, acceptance evidence, and relevant risks. For coding-agent handoffs, include the starting state, relevant contracts or concrete examples, likely affected paths/components, meaningful edge cases, and verification instructions so the agent can begin without choosing unspecified product behavior. Add regression checks, migration/release steps, and rollback conditions when they help execution. Existing code paths may be named; proposed paths must be labeled. See the [worked handoff](handoff-example.md) for the level of detail, not a required format.

Size units so the result can be implemented and checked coherently. Counts of phases, units, or test rows are not quality criteria. A helper refactor may need one check; a money-moving state machine needs more.

Use stable IDs when needed across documents. Trace requirements and important interface states to work or an explicit deferred/blocked decision. Include enabling infrastructure and operations when they serve an outcome; not every useful unit directly adds a screen.

## Execution and verification

Read [execution guidance](execution-spec.md) and [testing guidance](testing-spec.md). Use repository commands, meaningful regression checks, and dependencies to determine readiness. Avoid rigid file allowlists that prevent required related edits and arbitrary stops between authorized units.

The overview should identify milestones, sequence/parallel opportunities, dependency risks, coverage gaps, and the next executable unit. Where units share an interface or edited surface, name the contract owner, integration order, and cross-unit check; only claim parallel readiness when their dependencies and ownership allow it. Parallel opportunities do not authorize spawning agents or concurrent edits.

For production changes, include deployment compatibility, data migration/reconciliation, observability, and recovery as relevant. A feature is not releasable merely because implementation units exist.

Optional learning material belongs in linked learning documents; retain one authoritative source for acceptance tests and decisions.
