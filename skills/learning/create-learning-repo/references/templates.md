# Stub templates

These are the exact templates `scripts/scaffold.py` emits. Reproduce them verbatim if generating by hand. **Every prompt stays unanswered** — the value of the repo is that the user writes these.

## Topic file — `<topic-slug>.md`

```markdown
---
title: {Topic}
section: {Section}
module: {Module}
chapter: {Chapter}
status: todo          # todo | learning | drafted | mastered
confidence: 0         # 0-5, self-rated after a recall check
tags: []
---

# {Topic}

> **Why this matters:** <!-- Where does this show up in real systems, and what breaks without it? One or two sentences, written after you understand it. -->

## Mental model
<!-- Explain it in three sentences with no jargon. If you can't, you don't have it yet. -->

## Core concepts
<!-- The ideas you must recall cold. Bullets, not prose. -->

## Hands-on
<!-- Smallest runnable example. Then break it deliberately and record what happened. -->

## Gotchas and trade-offs
<!-- Cost, limits, failure modes, and when NOT to use this. -->

## Recall check
<!-- Three questions you should answer without notes. Write them now, answer them later. -->

## Sources
<!-- Links you actually read. -->
```

## Chapter interview file — `interview.md`

```markdown
---
title: Interview Questions — {Chapter}
section: {Section}
module: {Module}
chapter: {Chapter}
status: todo
---

# Interview Questions — {Chapter}

<!-- Fill each slot with a question you'd actually be asked at your target level.
     Mix recall, applied, and design/judgement questions. Answer in your own words. -->

## Q1.
**Type:** <!-- recall | applied | design | debugging -->
**Answer:**
**Follow-up they'd ask:**

## Q2.
...
```
(Repeats to the configured count, default 12, clamped 10–15.)

## Chapter thought-leadership file — `thought_leadership.md`

```markdown
---
title: Thought Leadership — {Chapter}
section: {Section}
module: {Module}
chapter: {Chapter}
status: todo
---

# Thought Leadership — {Chapter}

<!-- Ideas for public writing that demonstrate real understanding.
     Ship only what you've actually done or verified. -->

## Idea 1
**Angle:** <!-- The non-obvious claim. If it's a summary of the docs, discard it. -->
**Hook:**
**Audience:**
**Platform:** <!-- LinkedIn post | Medium article | conference talk | internal writeup -->
**Evidence I have:** <!-- Benchmark, incident, code, or migration you can point to. -->
**Status:** idea
```
(Repeats to the configured count, default 4.)

## Root files

- `README.md` — goal, target, how the repo is organized, how to use the status fields.
- `PLAN.md` — source of truth: goal, level, horizon, exclusions, assumptions, research notes, full tree.
- `progress.md` — one table row per chapter (`Section | Module | Chapter | Topics | Status`) plus a topic-level checklist.

## Editing rules

- Prompts are HTML comments so rendered Markdown stays clean.
- Keep headings stable across files — the user greps and diffs them.
- Never pre-fill `status` as anything but `todo`.
