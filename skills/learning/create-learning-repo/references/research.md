# Research

Only runs when the user gave no plan, or gave one with agreed gaps. Skip otherwise — do not "improve" a complete plan the user is happy with.

## What to search

Aim for 4–8 searches, in this order of value. The framing below is interview-shaped; for a `craft`, `practice`, or `exam` goal, substitute the equivalent primary source — published work by practitioners you'd want to sound like, protocols that survived contact with real weeks, or the exam board's own syllabus and released past papers.

1. **Current expectations for the target** — job postings for the exact title and seniority; for non-technical goals, the actual artefacts people at that level produce. The most honest source of what's really tested.
2. **First-hand reports** — recent write-ups of interview loops, exam sittings, or practitioner retrospectives. Reveals format weighting.
3. **Official docs changelogs / syllabus updates** — version-specific detail. Training knowledge goes stale here fastest.
4. **Established roadmaps and curricula** — use as a checklist against your draft, not as the draft.
5. **Shifts in the last 12 months** — what replaced the thing you'd otherwise include.

## Weighting

- Primary sources (postings, official syllabi, recent docs) > practitioner write-ups > blog roadmaps > aggregator listicles.
- If two sources disagree on whether a topic still matters, include it as a chapter and note the contention in PLAN.md.
- Never cite a source inside a stub file. Sources belong in PLAN.md; the learner fills the chapter's own `## Sources` with what *they* actually read.

## Output of this step

Two things, not one.

**1. What research changed about your draft** — a short bullet list of topics added, dropped, or reordered, with one-line reasons. Show this to the user alongside the plan. If research changed nothing, say so plainly.

**2. Depth notes per chapter.** This is the part that feeds the brief, and the reason research is worth doing at all. For each chapter, research should tell you:

- **`depth`** — how far to go, expressed as a capability rather than a topic list. "Far enough to explain the CPython layout and benchmark a claim" beats "cover hashing and resizing."
- **`serves`** — which part of the goal this chapter delivers. Job postings and interview reports name these directly; quote their language where you can.
- **per-topic `depth`** — for the two or three topics where sources disagree about how deep is deep enough, or where the obvious depth is wrong.

A research pass that returns topic names and nothing else has done half the job: it tells the user *what* to learn and leaves them guessing *how well*, which is exactly the gap the brief exists to close.
