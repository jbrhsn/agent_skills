# Interface specification template

Select applicable sections for visual, conversational, and/or headless systems. Combine variants for mixed products; remove instructional text and unused fields. Use existing naming and document locations.

# <Project> — <Interface / UI/UX / Interaction Contract>

**Status:** Draft | Reviewed | Approved (only when approved)

**Requirements:** <link>

**Implementation plan:** <link when present>

## Consumers and primary flows

<Who uses/calls this, entry points, main outcome, and relevant requirements.>

## Visual surfaces (if applicable)

### <Screen or component ID/name>

**Purpose and entry/exit:** <user goal, navigation, requirement references>

**Layout and behavior:** <existing design system, hierarchy, responsive/platform behavior; diagram or wireframe if useful>

| State | Trigger / condition | What the user sees | Available actions / next state |
|---|---|---|---|
| <meaningful state> | <…> | <…> | <…> |

<Relevant validation, focus/accessibility, double submission, stale data, session expiry, offline and permission behavior.>

## Commands or conversations (if applicable)

### <Command / intent>

**Invocation and inputs:** <syntax, defaults, validation, authorization>

**Output:** <human or machine-readable contract, error/exit semantics>

**State:** <what persists, expires, resets, or can be cancelled>

<Representative success and recovery flows; mark illustrative wording.>

## APIs, events, jobs, or library contracts (if applicable)

### <Entry point / topic / job>

**Caller and authorization:** <who can invoke/read it>

**Input/output:** <schema or concrete example where useful>

**Side effects:** <what changes and when it becomes visible>

| Condition | Result / error | Committed effects | Recovery / retry |
|---|---|---|---|
| <success or failure> | <…> | <…> | <…> |

<Relevant ordering, pagination, idempotency, concurrency, deadlines, compatibility, data grain/keys, freshness/finality, and partial-success semantics.>

## Integrated flows

<Trace important success and failure/recovery paths across surfaces and external systems.>

## Shared conventions

<Accessibility, privacy, errors, configuration, observability, platform/version constraints relevant to these interfaces.>

## Decisions and uncertainty

<Confirmed choices, proposals, assumptions, and open questions with impact.>
