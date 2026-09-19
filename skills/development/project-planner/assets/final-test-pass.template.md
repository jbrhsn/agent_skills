# <Project> — Release Verification

**Requirements / contracts / plan:** <links>

**Candidate revision or artifact:** <identifier>

**Environment and dataset/device/chain:** <reproducible conditions>

**Status:** Planned | In progress | Complete with evidence

Select checks relevant to release risk. Reference existing tests rather than copying the whole suite; add release-specific cases when needed. Planned tests are not passed tests.

## Coverage and evidence

| Outcome / requirement | Check or test reference | Result | Evidence / limitation |
|---|---|---|---|
| <ID / named behavior> | <link or command> | Not run / Pass / Fail | <run, log, measurement> |

## Integrated journeys and recovery

| Check ID | Setup / action | Observable expected result | Result / evidence |
|---|---|---|---|
| <ID> | <primary flow> | <…> | Not run |
| <ID> | <interruption, retry, recovery> | <…> | Not run |

## Performance and operational checks

| Property | Workload / measurement method | Target and basis | Measured result |
|---|---|---|---|
| <relevant NFR> | <…> | <confirmed / proposed> | Not run |

<Relevant authorization/isolation, upgrade/migration, restore, release-build/device, freshness/finality, compatibility, observability, and rollout/recovery checks. Omit irrelevant categories.>

## Defects and release decision

| Finding | Impact | Owner / next action | Status |
|---|---|---|---|
| <…> | <…> | <…> | <open / fixed / accepted by whom> |

**Remaining gaps:** <untested behavior, missing access, or unsupported environment>

**Release / recovery criteria:** <what permits rollout, what stops it, and rollback or roll-forward action>

**Decision:** <pending or actual authorized decision; do not infer approval from test success>
