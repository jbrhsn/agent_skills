# Scala / Spark — Lean Rules

## Language first

| Need | Use | Not |
|---|---|---|
| Data holder | `case class` | class + constructor + equals + toString |
| Optionality | `Option`, `getOrElse`, `fold` | null checks |
| Errors | `Either` / `Try` | exceptions for control flow |
| Chained transforms | `for`-comprehension | nested `flatMap` pyramids |
| Pattern dispatch | `match` | if/else chains on type |
| Constants set | `sealed trait` + objects, or `enum` (Scala 3) | string literals |
| Default config | default parameter values | builder classes |

## Spark

- Stay in the DataFrame/Dataset API — Catalyst optimizes it; RDDs and Python-style UDFs are opaque to it.
- No UDF if a built-in `functions._` expression exists. If a UDF is unavoidable, make it a typed one and test it as a plain function.
- `select` only needed columns immediately after read — column pruning is free LOC and free money.
- Filter before join; broadcast the small side explicitly when it fits.
- One `cache()` at most, and only if the DataFrame is reused; `unpersist` after.
- Never `collect()` to driver except for a bounded, known-small result. `take(n)` for inspection.
- Partition on the column you filter on. Avoid `repartition` unless you measured skew.
- Chain transformations in one pipeline value rather than reassigning `var df` at each step.

## Cut

- `var` — use `val` and a transformation chain
- Explicit type annotations where inference is obvious (keep them on public method signatures)
- Getter methods on `case class` fields
- Companion-object factories that only call `apply`
- `.map(x => f(x))` → `.map(f)`
- Try/catch around Spark actions that only rethrows

## Security (never cut)

- Read secrets from the secret manager or env, never from code or notebook cells.
- No PII in `.show()`, `explain()`, or driver logs.
- Validate schema explicitly on read (`.schema(expected)`) — `inferSchema` on untrusted input is an availability and correctness risk.
- Restrict output paths and table names to an allowlist when they come from parameters.

## Testability

- Split every job into: `read` → `transform(df): DataFrame` → `write`. Only `transform` gets tested, and it needs no cluster mocking.
- Pure `transform` functions take and return DataFrames — no reads, no writes, no `spark` global inside.
- One shared local `SparkSession` fixture per test suite; do not create one per test.
- Assert on `collect()` of a tiny fixture, comparing `Seq[case class]`, not string output.

## Example

```scala
// before: 9 lines with var, UDF, collect
// after: 3
def topEventPerUser(events: DataFrame): DataFrame =
  events.select($"user_id", $"event", $"ts")
    .withColumn("rn", row_number().over(Window.partitionBy($"user_id").orderBy($"ts".desc)))
    .filter($"rn" === 1).drop("rn")
```
