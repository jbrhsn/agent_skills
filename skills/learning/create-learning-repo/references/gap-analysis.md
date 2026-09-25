# Reviewing an existing plan

Preserve the user's goal and useful structure. Match the action to the request: report findings for a review, or apply improvements when asked to improve the plan. Ask about changes that would alter an explicit scope choice rather than adding an approval step for routine edits.

Consider these signals where relevant:

- Goal requirements without coverage, or topics with no useful connection to the goal.
- Missing prerequisites, confusing order, or unexplained dependencies.
- Stale versions, standards, or exam expectations needing verification.
- Depth that does not match the learner's level or available time.
- Missing practice or assessment for the capability being developed.
- Chapters with unrelated purposes, vague titles, or unclear briefs.
- A progression whose language or levels do not fit the domain.
- Missing observable completion checks for chapters or the overall goal.
- Optional activities or advanced tiers that consume the time needed for essential capabilities.

Counts alone do not establish a gap. Independent chapters, uneven topic counts, and omitted optional metadata can be appropriate. Judge whether the learner can navigate and use the plan.

For the bundled helper, missing required schema fields such as chapter `purpose` must be resolved before execution. Missing optional fields produce warnings, not a requirement to invent unnecessary detail. Write useful metadata yourself from context rather than asking the user to fill every field.

Report concrete findings with their effect and a suggested correction. Record deliberate exclusions and material assumptions. Keep the machine-readable plan and human-readable summary consistent when applying changes; avoid replacing learner work just to regenerate metadata.

Before delivery, trace each requested capability to chapter coverage and assessment, and each chapter back to the goal or a necessary prerequisite. Compare estimated study and practice effort with the time budget when supplied. The helper validates dependency references and order, but it cannot establish goal coverage, estimate educational effort, or judge whether a completion check is meaningful.
