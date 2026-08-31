# Stub templates

What `scripts/scaffold.py` emits. Reproduce it verbatim if generating by hand. **Every slot stays unanswered** — the brief says what to write and how deep; it never writes it.

Six files per chapter, the same six in every profile. Only `learning.md` is bespoke; the other five are one renderer with different labels, so read the shared parts once and the differences are small.

## Shared by all six files

**Frontmatter — identical key set everywhere**, so nothing has to be special-cased by tooling:

```yaml
---
title: "Builtin Collections"          # chapter name in learning.md; "Practice — Builtin Collections" elsewhere
section: "Python Core"
module: "Data Structures"
chapter: "Builtin Collections"
position: "1 of 2"                    # within the module, derived
profile: "technical"
tiers: ["Junior", "Senior", "Architect", "Expert"]
serves: "The coding screen's first fifteen minutes."
builds_on: []
enables: ["Complexity and Trade-offs"]
prev: ""                              # derived from plan order
next: "Complexity and Trade-offs"
status: "todo"                        # todo | learning | drafted | mastered
tier_reached: "none"                  # none, or the top rung you could defend out loud
tags: []
---
```

**Header — breadcrumb and arcs**, immediately under the H1:

```markdown
> Python Core › Data Structures · chapter 1 of 2
> **Section arc:** Rebuild the fluency an interviewer assumes you never lost.
> **Module arc:** From what the builtins are to why CPython made them that way.
> **This chapter serves:** The coding screen's first fifteen minutes.
```

**Nav footer**, after a `---` rule: sibling files as relative links, plus previous/next chapter pointing at their `learning.md`.

```markdown
**This chapter:** [examples](examples.md) · [practice](practice.md) · [interview](interview.md) · [thought leadership](thought_leadership.md) · [quizzies](quizzies.md)
**Previous:** [Builtin Collections](../builtin-collections/learning.md)
**Next:** [Pipeline Design Round](../../../02-interview-format/01-system-design/pipeline-design-round/learning.md)
```

## `learning.md`

The only bespoke template: a full brief, then one section per tier rung.

```markdown
## Brief

<!-- Written by the planner from the approved plan. Read it before you write anything
     below. Do not edit it while learning - amend PLAN.md and re-scaffold instead. -->

**Purpose:** {chapter purpose}

**Depth required:** {depth}

**Style:** {style}

**Assumes you already have:** {builds_on, joined}

**Unblocks later:** {enables, joined}

**Topics to cover:**

1. **Dictionaries** — hashing, collision handling, insertion order, dict views
   *Depth:* Explain the compact layout; benchmark it, don't just describe it.
2. **Lists and arrays** — over-allocation, amortised append
3. **Sets**

## Junior — You use it correctly when someone tells you to.

**Scope here:** Pick the right collection for a stated requirement.

<!-- What each topic *is*, in your own words, plus the vocabulary you need to read anything
     else about it. Write a three-sentence explanation with no jargon - if you can't, you
     don't have it yet. -->

## Senior — You choose it under real constraints and know what it costs.
...

## Sources

<!-- Links you actually read. -->
```

Optional brief lines (`Depth required`, `Style`, `Assumes`, `Unblocks`) are omitted entirely when the plan doesn't supply them, rather than emitted empty. `Scope here:` falls back to a prompt when the plan has no `tiers` entry for that rung.

The four tier prompts are fixed and domain-neutral — foundation, working, systemic, frontier. See `profiles.md` for why one set covers every profile.

## The five slot files

Same skeleton, different labels:

```markdown
{frontmatter}

# {File title} — {Chapter}

{breadcrumb block}

**This file's job:** {framing, from the profile}

**Topics in scope:** {topic names, joined}

**Depth target:** {chapter depth}

## {Item} 1

**{Slot}:**
**{Slot}:** <!-- hint, when the slot has one -->
...

---

{nav footer}
```

The two-line brief is derived — no extra authoring — so every file knows its own job without the planner writing five briefs.

Default labels (the `technical` baseline; see `profiles.md` for per-profile overrides):

| File | Item | Count | Slots |
|---|---|---|---|
| `examples.md` | Example | 3 | Source · Why it works · What to take from it · My annotation |
| `practice.md` | Task | 4 | Task · Tier · What done looks like · What I actually did · What broke |
| `interview.md` | Q | 12 | Type · Answer · Follow-up they'd ask |
| `thought_leadership.md` | Idea | 4 | Angle · Hook · Audience · Platform · Evidence I have |
| `quizzies.md` | Q | 10 | Question · My answer, from memory · Verified? · Revisit on |

`examples.md` is what you study; `practice.md` is what you do. Keeping them apart is the point — a chapter with four examples and no tasks is a chapter you have read, not learned.

## Root files

- `README.md` — goal, the six-file layout, the profile's ladder with rung definitions, and how to use `status` / `tier_reached`.
- `PLAN.md` — source of truth: goal, profile, ladder, exclusions, assumptions, research notes, full tree.
- `progress.md` — one row per chapter (`Section | Module | Chapter | Topics | Tier reached | Status`) plus a per-chapter checklist of the six files, with topics nested in a `<details>` block under `learning.md`.

## Editing rules

- Prompts are HTML comments so rendered Markdown stays clean. Brief content is visible text — it is instruction the learner needs to see.
- Keep headings and the frontmatter key set stable across files; the user greps and diffs them.
- Never pre-fill `status` as anything but `todo`, or `tier_reached` as anything but `none`.
- Never answer a slot, and never let the brief drift into being the content. "Explain the compact dict layout" is a brief; "the compact layout stores a sparse index array" is content, and belongs to the learner.
