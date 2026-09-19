# Project Planner

Create a practical plan for a new product, substantial feature, migration, or learning project. It covers web, data engineering, Web3, Android/iOS, and troubleshooting work.

The planner reads available project evidence, asks about material unknowns, and distinguishes confirmed constraints from reversible assumptions. It does not require an interview when the brief is sufficient, impose repeated document approvals, or stop an authorized build in a separate session.

## Deliverables

For a substantial project, defaults are `docs/prd.md`, `docs/uiux.md` (or an interaction contract), and `docs/plan/` with implementation units, dependencies, acceptance checks, and release verification. Small features can use one plan. Existing paths and document conventions take precedence.

Plans include domain-specific failure behavior: replay and backfill for data, finality and signing for Web3, lifecycle and offline recovery for mobile, and authorization and cache isolation for web. Proposed performance/reliability targets include measurement conditions and remain labeled assumptions until established.

Optional `learnings/` documents connect relevant concepts and exercises to the build. Templates are adaptable; test cases can be linked instead of copied into multiple documents.

Planning alone writes documents. If the request includes implementation, the agent continues after sufficient planning within the same authorization. Review gates apply when requested or a consequential decision is unresolved.

See [SKILL.md](SKILL.md) for resource routing. Quality checks establish document consistency and actionable coverage; they do not certify the software or execute the planned tests.
