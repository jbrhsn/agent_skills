# Gap analysis

Used when the user supplies their own plan. Your job is to critique, not replace. Preserve their structure, ordering, and vocabulary unless they agree to a change.

## Checklist

Run their plan against these. Report only real findings — do not manufacture gaps to look thorough.

1. **Goal mismatch** — topics that don't serve the stated goal, and goal requirements with no topic covering them.
2. **Missing foundations** — an advanced topic whose prerequisite appears nowhere.
3. **Stale content** — deprecated tools/versions, or a current standard absent entirely.
4. **Depth imbalance** — one module with 20 topics next to one with 2.
5. **Untested-by-reality** — pure theory with no chapter that produces something runnable.
6. **Interview-format gaps** — for interview goals: coding, design, behavioral, and domain rounds all represented?
7. **Orphan topics** — items with no home in the section/module/chapter hierarchy.
8. **Ambiguous naming** — chapter names that don't predict their contents.

## How to present

```
Gaps found (4):
1. [Missing foundation] "Async patterns" assumes generators — no chapter covers them.
2. [Stale] Pandas 1.x idioms; 2.x changed copy semantics.
...

Questions:
- Is behavioral prep out of scope deliberately, or an oversight?
```

Then ask which to adopt. Scaffold their plan plus only the accepted additions. Record rejected suggestions under `excluded:` in the plan so a future run doesn't resurface them.
