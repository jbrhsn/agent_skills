# SQL — Lean Rules

## Engine first (do not do it in application code)

| Need | Use | Not |
|---|---|---|
| Ranking, top-N per group | `ROW_NUMBER() OVER (PARTITION BY ...)` | fetch-all then sort in Python |
| Running totals, deltas | window functions, `LAG`/`LEAD` | self-joins |
| Readable stages | `WITH` CTEs | nested subqueries 3 deep |
| Upsert | `INSERT ... ON CONFLICT DO UPDATE` / `MERGE` | SELECT-then-INSERT round trip |
| Null defaults | `COALESCE` | `CASE WHEN x IS NULL` |
| Set logic | `EXISTS`, `EXCEPT`, `INTERSECT` | `NOT IN` with a subquery (null trap) |
| Pivot | `FILTER (WHERE ...)` / conditional `SUM` | multiple queries merged in code |
| JSON columns | native `jsonb` operators | parse in app |

## Cut

- `SELECT *` — name the columns; it is a contract and a perf fix at once
- Temp tables that a CTE replaces
- `DISTINCT` used to hide a join fan-out — fix the join
- Correlated subqueries repeated per row → one join or window
- Views wrapping a single table with no filter
- `ORDER BY` inside a subquery that is re-sorted outside

## Rules

- One statement per intent; if a query exceeds ~40 lines, split into named CTEs, not into round trips.
- Filter as early as possible — push predicates into the CTE, not after the join.
- Join on indexed keys; never join on an expression (`ON lower(a.x) = lower(b.x)`) without a matching functional index.
- Make it deterministic: `LIMIT` without `ORDER BY` is a bug.

## Security (never cut)

- Parameterized statements only. String-concatenated SQL is an injection, no exceptions for "internal" queries.
- Least-privilege role per service; no app connecting as owner/superuser.
- No PII in `ORDER BY`-visible logs or query comments.
- Explicit column lists on `INSERT` so a schema change cannot silently shift values.
- Row-level security or a mandatory tenant predicate on every multi-tenant table.

## Testability

- Deterministic inputs: pin the clock via a parameter, not `NOW()` inline, so the query is assertable.
- Keep each CTE independently `SELECT`-able — that is the unit test.
- Assert on row counts and on one full expected row, not on the whole result set formatting.
- `EXPLAIN` before merge; regression-test the plan shape for hot queries.

## Example

```sql
-- before: 3 queries + app-side sort
-- after: 1
SELECT user_id, event, ts
FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts DESC) rn
      FROM events WHERE ts >= $1) t
WHERE rn = 1;
```
