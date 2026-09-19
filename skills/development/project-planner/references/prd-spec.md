# Product requirements

Use an existing product document or `docs/prd.md` as appropriate. [The template](../assets/prd.template.md) provides a starting shape, not a fixed section count.

Separate observed facts, confirmed constraints, proposed decisions, assumptions, and open questions. Describe the requested scope faithfully; do not silently reduce it to fit a page count or invent a larger product.

Requirements should identify an actor or system, observable behavior, relevant conditions, and a way to verify. For example, a retried import must not duplicate previously committed records; verify by replaying the same batch after an interrupted write. Non-functional targets need a workload, environment, and measurement method; do not invent an SLA and label it confirmed.

Use stable identifiers such as FR-01/NFR-01/CON-01 when other artifacts reference them. Preserve existing IDs and mark removed requirements rather than renumbering referenced entries.

Capture users/jobs, scope and exclusions, external integrations, data ownership, technical constraints, and success criteria. Add meaningful security, reliability, accessibility, performance, cost, and recovery requirements based on project risk. If a target needs user input, record a proposed value and the decision it affects.

Include entities, keys, state transitions, retention, and trust boundaries at the detail needed to avoid incompatible implementations. Schemas or diagrams are useful when they clarify a real contract; avoid speculative exhaustive design.

Open questions name who or what can resolve them, impact, and whether they block implementation. Cross-link only artifacts actually produced, and update links as the document set evolves.
