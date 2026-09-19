# Development Skills

Two complementary skills support production software work. Use either independently; planning is helpful when it resolves real uncertainty, not a prerequisite for every code edit.

| Skill | Use for | Result |
|---|---|---|
| [project-planner](project-planner/README.md) | Product/feature planning, requirements, interface contracts, migrations, learning roadmaps | Actionable documents with dependencies, acceptance evidence, and relevant release/recovery considerations |
| [lean-coder](lean-coder/README.md) | Implementation, review, refactoring, optimization, troubleshooting, debugging | Focused changes when authorized, or evidence-backed findings, with proportionate verification |

Both cover web, data engineering, Web3, Android/iOS, and troubleshooting. Domain guidance addresses actual failure modes: authorization and cache isolation, replay and partial writes, signatures and reorgs, mobile lifecycle and offline recovery, and causal debugging.

The instructions support agent judgment. They do not impose line-count targets, blanket abstraction bans, fixed interviews, or automatic approval stops. The planner can continue into implementation when the user has already authorized it. Reviews and diagnoses preserve their requested scope.

Detailed references load only when relevant. Templates adapt to the project; production checks scale with the consequences of failure. Repository executor agents load lean-coder according to their own instructions; see [agent documentation](../../agents/README.md).

## Distribution

Edit canonical sources here, preview with `uv run scripts/sync_all.py --dry-run`, and synchronize through the repository scripts when requested. See the [repository guide](../../README.md) for destinations and verification.
