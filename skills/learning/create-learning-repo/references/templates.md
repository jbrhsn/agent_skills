# Stub templates

This describes the standard output of `scripts/scaffold.py`. Match its metadata and links when compatibility matters; adapt headings and content to the request. The helper creates unanswered stubs. Authoring can fill teaching content and requested model answers while preserving learner response fields.

Three files per chapter by default (`learning.md`, `examples.md`, `practice.md`); `chapter_files` selects from six supported files. Only `learning.md` is bespoke; activity files share one renderer with different labels.

## Shared by selected files

**Frontmatter — identical key set everywhere**, so nothing has to be special-cased by tooling:

```yaml
---
title: "Builtin Collections"          # chapter name in learning.md; "Practice — Builtin Collections" elsewhere
section: "Python Core"
module: "Data Structures"
chapter: "Builtin Collections"
position: "1 of 2"                    # within the module, derived
profile: "technical"
tiers: ["Junior", "Senior"]
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
>
> **Section arc:** Rebuild the fluency an interviewer assumes you never lost.
>
> **Module arc:** From what the builtins are to why CPython made them that way.
>
> **This chapter serves:** The coding screen's first fifteen minutes.
```

**Nav footer**, after a `---` rule: selected sibling files as relative links, plus previous/next chapter pointing at their `learning.md`.

```markdown
**This chapter:** [examples](examples.md) · [practice](practice.md)

**Previous:** [Builtin Collections](../builtin-collections/learning.md)

**Next:** [Pipeline Design Round](../../../02-interview-format/01-system-design/pipeline-design-round/learning.md)
```

## `learning.md`

The only bespoke template: a full brief, then one section per tier rung.

```markdown
## Brief

<!-- Chapter assignment from the plan. Adapt when scope changes, keeping the machine-readable plan and PLAN.md consistent. Preserve existing learner work. -->

**Purpose:** {chapter purpose}

**Depth required:** {depth}

**Style:** {style}

**Assumes you already have:** {builds_on, joined}

**Unblocks later:** {enables, joined}

**Completion check:** {observable task and success condition}

**Estimated effort:** {study plus practice estimate, if supplied}

**Topics to cover:**

1. **Dictionaries** — hashing, collision handling, insertion order, dict views *Depth:* Explain the compact layout; benchmark it, don't just describe it.
2. **Lists and arrays** — over-allocation, amortised append
3. **Sets**

## Junior — You use it correctly when someone tells you to.

**Scope here:** Pick the right collection for a stated requirement.

<!-- What each topic *is*, in your own words, plus the vocabulary you need to read anything else about it. A short plain-language explanation is a useful starting point. -->

## Senior — You choose it under real constraints and know what it costs.
...

## Sources

<!-- Links you actually read. -->
```

Optional brief lines are omitted when absent. Missing `completion_check` is accepted for older plans but warned about; provide one for new plans. `Scope here:` falls back to a prompt when the plan has no `tiers` entry for that rung.

The four tier prompts are fixed and domain-neutral — foundation, working, systemic, frontier. See `profiles.md` for why one set covers every profile.

## The five slot files

Same skeleton, different labels:

```markdown
{frontmatter}

# {File title} — {Chapter}

{breadcrumb block}

**This file's job:** {framing, from the profile}

**Chapter purpose:** {chapter purpose}

**Topics in scope:** {topic names, joined}

**Depth target:** {chapter depth}

**Completion check:** {chapter completion check}

Before filling this file, read the [full chapter brief](learning.md#brief) for topic coverage, depth, and prerequisites. Keep this activity within that assignment.

## {Item} 1

**{Slot}:**

**{Slot}:** <!-- hint, when the slot has one -->
...

---

{nav footer}
```

The compact brief is derived, so every selected file has assignment context without duplicating the full topic-level brief. The visible link tells a later author to read the authoritative coverage and depth before filling the activity.

Default labels (the `technical` baseline; see `profiles.md` for per-profile overrides):

| File | Item | Count | Slots |
|---|---|---|---|
| `examples.md` | Example | 2 | Source · Why it works · What to take from it · My annotation |
| `practice.md` | Task | 2 | Task · Tier · What done looks like · What I actually did · What broke |
| `interview.md` (opt-in) | Q | 3 | Question · Type · Answer · Follow-up they'd ask |
| `thought_leadership.md` (opt-in) | Idea | 1 | Angle · Hook · Audience · Platform · Evidence I have |
| `quizzies.md` (opt-in) | Q | 3 | Question · My answer, from memory · Verified? · Revisit on |

`examples.md` is what you study; `practice.md` is what you do. Keeping them apart is the point — a chapter with four examples and no tasks is a chapter you have read, not learned.

## Root files

- `README.md` — goal, selected layout, the profile's ladder with rung definitions, and how to use completion checks, `status`, and `tier_reached`.
- `PLAN.md` — goal and goal check, profile, ladder, exclusions, assumptions, research notes, linked roadmap, and full tree. Roadmap columns: chapter, purpose, coverage and depth, prerequisites, completion check, effort. Missing checks and effort are explicitly marked, not invented.
- `progress.md` — one row per chapter (`Section | Module | Chapter | Topics | Tier reached | Status`) plus a per-chapter completion check and checklist of selected files. A separate `<details>` block lists topics. Filling files and demonstrating learning are distinct.

## Maintaining the output

- Prompts are HTML comments so rendered Markdown stays clean. Brief content is visible text — it is instruction the learner needs to see.
- Keep metadata and links consistent when adapting headings or layout.
- Fresh stubs start at `status: todo` and `tier_reached: none`. Drafted content may use `drafted`; do not invent mastery or reset existing learner progress.
- Separate the assignment from teaching content. If authoring is requested, populate the appropriate material and put model answers apart from personal attempt and reflection fields.
