# Interface and interaction specification

Use existing interface docs or an appropriately named document such as `docs/uiux.md`. Choose applicable parts of [the template](../assets/uiux.template.md); a mixed system may need both UI and service contracts.

Describe what consumers can observe and rely on. Include diagrams, wireframes, schemas, or concrete examples when they remove ambiguity. Respect existing design systems and user choices rather than inventing visual constraints.

## Visual interfaces

Describe primary journeys, screen/navigation structure, important components, state ownership, and transitions. For affected operations, cover meaningful loading, empty, error, success, disabled, retry, cancellation, and stale-data behavior; do not invent states merely to fill a table.

Specify validation feedback, focus movement, keyboard/screen-reader access, text scaling, responsive layouts, and permission-dependent behavior. Include account/session changes, offline recovery, interrupted operations, and destructive-action confirmation when relevant.

Stable screen/component/flow IDs help larger plans trace behavior to implementation. Small features can refer to named sections. Background requirements need no artificial screen.

## Conversational and command interfaces

Define invocation, inputs/defaults, output formats, error/exit semantics, session persistence, cancellation, and non-interactive behavior. Include representative successful and recovery flows. Example wording can be illustrative unless exact output is a compatibility contract.

## APIs, events, data jobs, and libraries

Identify caller, authentication/authorization, inputs and outputs, validation, errors, side effects, timeouts, retries, idempotency, ordering, pagination, and compatibility where applicable. Define partial-success behavior and visibility of intermediate state.

Use schemas and examples where precision matters. For data work include grain, keys, freshness, replay, and schema evolution; for Web3 include chain identity, finality, and index reconciliation. Keep implementation choices distinct from public contracts.

## Consistency

Map important interactions to requirements and implementation ownership. Check recovery paths and externally visible states, not only successful flows. Track assumptions/open decisions without forcing another approval stage; document depth follows complexity, not a page cap.
