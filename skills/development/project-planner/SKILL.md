---
name: project-planner
description: Turn a project idea or substantial feature into actionable requirements, interface contracts, and an implementation plan with verification and release considerations. Use for planning, PRDs, architecture tradeoffs, UI/UX specifications, or learn-by-building roadmaps across web, data, Web3, and mobile projects.
---

# Project Planner

Produce enough shared understanding to implement and verify the requested outcome. Planning should remove uncertainty and expose costly decisions, not create ceremony. Match the document set and depth to the project; a bounded feature may need one concise plan rather than a full PRD and phase tree.

## Start from evidence

Read existing product docs, repository guidance, relevant implementation, deployment configuration, and tests. Distinguish a new project from an extension, migration, or repair. Preserve existing decisions and IDs unless the request changes them. Do not infer that a missing PRD requires a planning exercise before ordinary coding.

Extract known requirements and constraints from the conversation and repository. Ask only about unresolved choices that materially change scope, architecture, cost, or irreversible behavior. State reasonable reversible assumptions and proceed with independent work. Do not present assumptions as user-confirmed requirements.

A request for a complete plan authorizes drafting its related documents without separate approvals for every stage. Pause for a real blocking decision or an explicitly requested review gate. Silence is not approval. See [interview guidance](references/interview.md) for targeted discovery.

## Choose useful artifacts

Use existing documentation locations or the user's chosen paths. The following are defaults for a substantial project, not mandatory files.

| Deliverable | Guidance | Starting template |
|---|---|---|
| Goals, scope, requirements, constraints | [PRD](references/prd-spec.md) | [PRD template](assets/prd.template.md) |
| UI behavior, API/event/data contracts | [Interface specification](references/uiux-spec.md), [surface questions](references/uiux-interview.md) | [Interface variants](assets/uiux.template.md) |
| Dependencies, implementation units, rollout | [Plan](references/plan-spec.md), [execution](references/execution-spec.md) | [Plan template](assets/plan.template.md) |
| Acceptance and release verification | [Testing](references/testing-spec.md) | [Release test pass](assets/final-test-pass.template.md) |
| Optional build-aligned curriculum | [Learning mode](references/learning-mode.md) | [Topics](assets/topics.template.md), [learning plan](assets/learning-plan.template.md) |

For domain-sensitive decisions, read the relevant section of [project domains](references/domains.md): web, data engineering, Web3, Android/iOS, or troubleshooting. Mixed projects need the contracts between domains as well as each domain's local design. Load only applicable resources.

## Make the plan executable

Trace important outcomes to implementation units and observable verification. Use stable IDs when cross-document traceability helps. Sequence by dependencies and risk: a thin end-to-end slice, a compatibility spike, or a migration rehearsal may be the best first step. Avoid prescribing counts of phases, units, questions, or tests. When coding agents will execute the plan, make each ready unit a bounded handoff with explicit design boundaries, focused reading, and checks so execution does not require repeating product discovery. Use [unit sizing](references/plan-spec.md), [execution readiness](references/execution-spec.md), and the [worked handoff](references/handoff-example.md) to support executors with different model capabilities.

For production work, establish relevant reliability, security, data integrity, performance, accessibility, and operational requirements. Record proposed targets as assumptions with measurement conditions. Include migration, deployment compatibility, observability, and recovery where affected. Identify remaining decisions and the work they block.

Use concrete existing file paths, schemas, diagrams, examples, and commands when they make the plan more actionable. Label proposed structures as proposed. Templates are starting points: remove irrelevant sections, preserve useful project conventions, and avoid duplicating full test inventories across documents.

## Respect scope and continue

Planning alone produces documentation, not application changes, installations, Git initialization, deployment, or external actions. When the user has also authorized implementation, finish the necessary planning and continue building in the same session; this skill creates no extra approval gate. Do not stop after each unit unless the user's workflow requires it.

Before handing off, check [document quality](references/quality-gates.md). Summarize the artifacts, important decisions/assumptions, actual validation, and next executable work or blocker. Do not call a proposed plan approved or its tests passed.
