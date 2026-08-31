# Gap analysis

Used when the user supplies their own plan. Your job is to critique, not replace. Preserve their structure, ordering, and vocabulary unless they agree to a change.

## Checklist

Run their plan against these. Report only real findings — do not manufacture gaps to look thorough.

### Coverage

1. **Goal mismatch** — topics that don't serve the stated goal, and goal requirements with no chapter covering them.
2. **Missing foundations** — an advanced topic whose prerequisite appears nowhere.
3. **Stale content** — deprecated tools/versions, or a current standard absent entirely.
4. **Depth imbalance** — one module with 20 topics next to one with 2.
5. **Untested-by-reality** — pure theory with no chapter that produces something you can point at afterwards.
6. **Assessment-format gaps** — for interview or exam goals: are all the round types represented?
7. **Orphan topics** — items with no home in the section/module/chapter hierarchy.
8. **Ambiguous naming** — chapter names that don't predict their contents.

### Cohesion

The gaps that produce a repo of disconnected files. These matter more than coverage gaps, because a missing topic is visible and a missing connection is not.

9. **No dependency graph** — chapters with neither `builds_on` nor `enables`. If a chapter connects to nothing, ask why it's in this repo.
10. **Reading order contradicts dependencies** — a chapter that `builds_on` something appearing later in plan order. `prev`/`next` follow plan order, so this makes the repo unreadable front to back.
11. **Missing arcs** — sections or modules with no `arc`. Without one, every chapter file omits the line saying where it sits in the larger story.
12. **Chapter with two purposes** — a `purpose` containing "and" joining unrelated aims, or more than 8 topics. Split it.

### Brief quality

13. **Missing `purpose`** — fatal; the scaffolder refuses to run.
14. **Thin briefs** — no `depth`, `style`, or `serves`. The scaffolder warns, but catch these earlier: a stub with a thin brief gets filled shallowly or not at all.
15. **Depth stated as a topic list** — "cover hashing, collisions, resizing" is coverage, not depth. Depth says *how far*: "far enough to benchmark a claim and be believed."
16. **Wrong profile** — an engineering ladder on a writing goal, or a four-rung ladder on a three-week horizon. Propose the ladder you'd use and let them judge the rung definitions.

## How to present

```
Gaps found (4):
1. [Missing foundation] "Async patterns" assumes generators — no chapter covers them.
2. [Cohesion] Nothing declares builds_on/enables — 11 chapters, no dependency graph.
3. [Thin brief] 6 of 11 chapters have no depth; those stubs will get filled shallowly.
4. [Stale] Pandas 1.x idioms; 2.x changed copy semantics.

Questions:
- Is behavioural prep out of scope deliberately, or an oversight?
```

Then ask which to adopt. Scaffold their plan plus only the accepted additions. Record rejected suggestions under `excluded:` in the plan so a future run doesn't resurface them.

One exception to "critique, don't replace": if they accept a cohesion or brief finding, you write the `purpose`, `depth`, `arc`, and `builds_on` fields yourself — those are plan metadata, not their content, and asking a user to hand-author sixty brief fields is how a plan gets abandoned before it's scaffolded. Show them what you wrote in the approval tree.
