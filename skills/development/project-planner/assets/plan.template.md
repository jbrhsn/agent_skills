# Plan templates

For substantial projects, use an overview and phase files; for smaller work combine relevant sections. Replace placeholders, omit irrelevant fields, and preserve existing repository conventions.

## Overview shape

# <Project> — Implementation Plan

**Requirements / contracts:** <links to existing artifacts>

**Scope and assumptions:** <requested outcome and consequential assumptions>

| Milestone | Observable outcome | Dependencies | Work / file |
|---|---|---|---|
| <name> | <demonstrable result or risk retired> | <dependency> | <unit IDs / phase link> |

### Sequence and risks

<Why this order, open decisions, external dependencies, and which work can proceed independently. For shared contracts, name the owner, integration order, and cross-unit check.>

### Coverage and verification

| Outcome / requirement | Implementation owner | Evidence |
|---|---|---|
| <ID or named outcome> | <unit> | <check / test / measurement> |

<Known commands, required environments/fixtures, proposed tooling, and checks needing external access. Link authoritative cases rather than duplicating them.>

### Release and recovery

<Applicable data migration, old/new compatibility, rollout, monitoring, rollback or roll-forward.>

### Next executable work

<First ready unit, prerequisites, or specific blocker.>

## Phase or unit shape

# <Phase> — <Outcome>

**Dependencies:** <existing capability or earlier unit>

### <Unit ID> — <Observable change>

**Covers:** <requirement / contract / enabling outcome>

**Starting state:** <existing behavior, prerequisite, relevant paths/symbols and evidence; label proposed paths>

**Read first:** <applicable repository guidance, exact contract/decision sections, implementation entry points, and nearby tests; include when context spans several sources>

**Scope:** <behavior and likely affected paths; proposed paths labeled>

**Contract / examples:** <authoritative link or concrete input/output/state transition and meaningful edge cases where ambiguity matters>

**Approach / design boundaries:** <settled component responsibilities, data flow, state or transaction ownership where relevant; authoritative decisions and rationale; choices the executor may make locally>

**Dependencies / open decisions:** <what is needed before or during implementation>

**Readiness:** <ready with available prerequisites and clear next action, or blocked by named decision/evidence; omit for plans that are not coding-agent handoffs>

**Done when:** <observable acceptance and relevant failure behavior>

| Check ID | Setup/action | Expected result | Level / environment | Automation |
|---|---|---|---|---|
| <ID> | <…> | <…> | <unit / integration / device / manual> | <existing / proposed / manual> |

**Verify with:** <real command or clearly labeled proposed command / manual steps>

**Regression:** <affected existing contracts and checks>

**Execution notes:** <repository conventions, needed fixtures, permissions, relevant scope limits; continue authorized dependent work after verification>

**Risks / recovery:** <specific migration, failure, or operational concern where relevant>

**If evidence changes:** <authoritative contract/decision and dependent units or checks to update; include when uncertainty is material>

**Execution record (when work spans agents/sessions):** <planned until execution; link the existing tracker or record status, actual changed paths/contracts, checks/results and revision/environment, deviations/blockers, and next ready work; do not prefill successful results>

### Milestone verification

<Integrated flows, cross-boundary failure/recovery, and relevant regressions. Record tested revision/environment and passed/failed/not-run evidence during implementation.>
