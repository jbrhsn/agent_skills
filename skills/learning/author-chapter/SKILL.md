---
name: author-chapter
description: Author a complete learning module as a single Markdown file that takes someone who knows nothing about the field to expert-level command of one topic, written in self-contained five-minute units with the takeaway first. Use this skill whenever the user asks to write a chapter, learning module, tutorial, course, guide, primer, explainer, study material, "teach me X properly", "I want to master X", "write a deep dive on X", or wants any long-form educational document about a concept or technology — even if they don't use the word "chapter" or "module". Also use it to fill any file scaffolded by create-learning-repo. Prefer this over answering from scratch for any request whose deliverable is teaching material.
---

# Author Chapter

Produce one `.md` file that teaches a topic from nothing to the level where the reader could make real decisions with it, judge trade-offs, and predict how it fails.

The reader model: **an intelligent 28-year-old who knows nothing about this particular field.** They have a life, a job, and adult judgement — but no vocabulary here and no idea which parts matter. So: assume no domain knowledge whatsoever, and assume everything else. Never talk down, never pad, never explain what an adult already understands about the world. Every unexplained assumption inside the field is a failure; every word spent flattering or reassuring the reader is waste.

They read in short sittings. Write so they can stop after any unit and come back a week later without re-reading.

## The two failure modes this skill exists to prevent

**Format conformity.** A model handed one skeleton will force every domain into it — deriving B-tree page counts when the topic is essay structure, demanding "failure modes at scale" for a savings habit. So this skill fixes *obligations* and leaves their *realisation* to the domain. There is one spine and six questions every unit answers; how you answer them is chosen for the field, not inherited from this file.

**The undifferentiated wall.** Everything at one depth, in one long block, with no signal about what matters. So: the takeaway comes first, the vital 20% is marked as such, and the material is cut into units a reader can actually finish.

Follow the phases in order. The plan is what makes the writing complete; the audit is what makes it honest.

## Workflow

### Phase 1 — Read the assignment

**If the target file was scaffolded by `create-learning-repo`, its frontmatter and brief are the assignment. Do not re-plan.**

Read the file first. Take from it:

| From the file | Governs |
|---|---|
| `title`, filename | Which of the six file types you are writing — read `references/file-types.md` |
| `profile` | Which domain pack applies — read `references/domains.md` |
| `tiers` | The rung names, used **verbatim**. Never relabel them, never assume four |
| Brief `Topics to cover`, with per-topic `covers` and `depth` | The coverage spec. This is what completeness is measured against |
| Brief `Purpose`, `Depth required`, `Style` | What the chapter is for and how deep to go |
| `serves`, `builds_on`, `enables` | What to assume, what to deliver, what to set up |
| `prev`, `next` | What to connect to at the seams |

Relabelling the ladder is the most damaging thing you can do here: it silently breaks a `craft` or `practice` chapter by pasting engineering vocabulary over it.

**Standalone, with no scaffold:** pick a sensible reading of the topic and move on. Ask the user only if the topic name is ambiguous across fields ("normalization", "bootstrapping"), or it is code-heavy with no stack implied anywhere, or the endpoint is unclear in a way that changes the whole ladder. At most three questions, in one message. Then build the assignment yourself: list every concept the reader must own, its prerequisites, and its rung, and order it so nothing appears before what it depends on. Infer the domain pack from the topic. That inventory is your coverage spec for the rest of the workflow — hold yourself to it exactly as if a planner had written it.

### Phase 2 — Scope check, before writing anything

Count the units the assignment implies — roughly one per topic per rung it must reach, merged where topics genuinely share a unit.

A healthy chapter is 8–14 units. **Past roughly 18, stop and report rather than write.** Tell the user the brief is more than one chapter, name the seam you would cut at, and point them at `PLAN.md` — amending the plan and re-scaffolding keeps `progress.md` accurate. Never split the file yourself, never invent a file the plan does not know about, and never thin the coverage to fit. A long chapter is fine; an unscoped one is not.

### Phase 3 — Research (mandatory when a search tool exists)

**If `WebSearch` or `WebFetch` is available, searching is required, not optional.** Your training data has a cutoff and this chapter will be read as current.

At minimum: one query for the chapter as a whole — *what is the current state of this, and what changed recently* — plus one query per topic whose facts move. Fetch the primary source rather than trusting a summary of it.

These must be sourced or explicitly flagged as unverified, never written from memory: version numbers, API and interface details, prices and limits, benchmark figures, dates, the current state of a standard or syllabus, and any "best practice" claim about what practitioners now do.

Record what you actually read in the `## Sources` section — each entry with what it supports and the date retrieved. If contemporary sources contradict what you were about to write, the sources win and the disagreement is worth a sentence in the chapter.

**If no search tool is available**, say so in one line under `## Sources`, and mark every version-sensitive claim as needing a docs check rather than guessing.

### Phase 4 — Write, unit by unit

Read `references/structure.md` for the spine and the six unit obligations. Read `references/domains.md` for what evidence and worked examples mean in this field. Read `references/voice.md` before the first prose and hold to it. Read `references/pedagogy.md` for how examples, analogies, misconceptions, and pacing actually work.

Write one unit, append it, move to the next. Never attempt the whole file in one pass, and never regenerate what is already written — long single-shot writing truncates and drifts.

In a scaffolded file, keep the frontmatter and the `## Brief` block exactly as they are and replace everything below them. The stub's one-section-per-rung layout is scaffolding for the assignment, not the shape of a finished chapter — the spine replaces it, and the rungs move down onto individual units. The HTML-comment prompts are instructions to you and must not survive into the delivered file.

Keep a running scratch list as you go, outside the file: terms you have defined, simplifications you promised to pay off later, and units completed against the coverage spec. This is what makes the audit mechanical instead of a matter of recalling ten thousand words. Delete nothing from the file to make room; length is not the constraint.

### Phase 5 — Audit and repair

Run `references/checklist.md` — the universal section always, plus the section for your domain and file type. Audit in passes over sections rather than trying to hold the whole file at once. Fix what fails rather than noting it as a limitation, and report only what you actually changed.

The first check is completeness against the assignment, and it is the one that matters: every topic covered at its briefed depth, every rung on the ladder reached, the stated purpose actually delivered.

### Phase 6 — Deliver

Write into the scaffolded file when there was one, keeping its frontmatter intact and setting `status` to `drafted`. Standalone, save as `<topic-slug>.md` unless the user gave a path.

Report in two lines: coverage against the brief (topics done, rungs reached), unit count and rough read time, and whether sourcing was live or from memory. Name anything you left unverified.

## Non-negotiables

- **Takeaway first, at both levels.** The chapter opens with the answer in one minute; every unit opens with its claim in one bold line. The reasoning follows — it does not lead.
- **Motivation before mechanism.** Every unit answers why the thing exists before how it works. Mechanism without motivation does not stick.
- **No undefined term, ever.** Jargon is defined in plain language at first use, inline, before it is used in an explanation. If defining A needs B, B comes first — that is what the ordering is for.
- **Every unit shows one real thing.** Specific, attributable, walked through with intermediate state visible. What "one real thing" is depends entirely on the domain; a restated abstraction is never it.
- **Every unit names a trap and a cost.** The wrong belief learners actually form, in their voice — and what the choice bought and sold. If a unit has neither, fold it into its neighbour.
- **Use the ladder you were given.** Rung names come from the frontmatter, verbatim, however many there are.
- **The reader can stop.** Units are self-contained, the core path is marked, and stopping at its end is stated to be a legitimate finish.
- **Completeness beats length targets.** Never cut coverage to hit a read time. Never pad to reach one.

## Reference files

Read these as you reach the phase that needs them; do not load them all at once.

- `references/file-types.md` — the six scaffolded files and what "done" means for each, including the three you must leave unanswered. Read in Phase 1.
- `references/domains.md` — evidence standards and worked-example forms per domain. Read in Phase 1, apply throughout.
- `references/structure.md` — the spine and the unit obligations. Read before writing.
- `references/pedagogy.md` — load management, retrieval, analogies, misconceptions, pacing.
- `references/voice.md` — prose rules and patterns to avoid.
- `references/examples.md` — annotated weak-vs-strong pairs, technical and non-technical. Read if unsure whether the writing is hitting the bar.
- `references/checklist.md` — the Phase 5 audit.
