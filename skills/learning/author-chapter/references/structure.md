# Structure

## The spine

This is the only fixed shape. Everything inside it — the tier names, the unit headings, the form every example takes — is chosen for the domain and the brief.

```markdown
# <Chapter>

**In one minute.** The takeaway, stated flat, before any setup.
**The mental model.** One bounded analogy, and how this connects to what came before.

## Contents          (only when the chapter runs past ~8 units)

## Core path         (the 20% that gives 80%)
### <Unit> · ~5 min
### <Unit> · ~5 min
...

## Going deeper      (the rest, honestly optional-for-now)
### <Unit> · ~7 min
...

## The whole picture
## Glossary
## Spaced recall
## Sources
## Where to go next
```

### In one minute

The first thing on the page, before any framing. State what the reader will be able to do and the single idea the chapter turns on — in three or four lines, in plain language, with no jargon that the chapter itself introduces. Someone who reads only this should come away with something true and useful.

This is not a summary of the document's headings. It is the answer, given up front. The reasoning that earns it follows.

### The mental model

One analogy, chosen to map structure rather than mood, and immediately bounded — name the one place it breaks. Then one or two sentences on where this chapter sits relative to the chapter before it and what it unblocks. When the file carries `builds_on` and `enables` frontmatter, this is where they get paid off in prose.

### Core path and Going deeper

The split is the point. **Core path** holds the units a reader must have to be functional. **Going deeper** holds everything else — genuinely valuable, genuinely postponable. A reader who stops at the end of the core path has not failed; say so explicitly in one line at the split.

Be strict about what earns a place in the core path. If everything is core, the split has told the reader nothing. Where the brief supplies per-topic `depth`, use it to decide: topics briefed for working command are core, topics briefed for awareness are not.

The two sections still respect the tier ladder — the core path typically carries the lower rungs of every topic, and Going deeper carries the upper rungs. Do not turn the split into "easy chapter, hard chapter"; a top-rung insight belonging to a core topic can sit in the core path if the reader needs it to function.

### The tier ladder

When the file has `tiers` in its frontmatter, **those are the rung names and you use them verbatim.** They vary by domain — `Junior → Senior → Architect → Expert`, `Beginner → Practitioner → Voice → Authority`, `Aware → Consistent → Adaptive → Designer`, `Recall → Applied → Scenario → Edge`, or whatever a `custom` plan declared. Never relabel them, and never assume four rungs; `tier_count` may have trimmed the ladder to two or three.

Mark each unit with the rung it serves. Every rung on the ladder must be reached by the end of the chapter — that is a completeness requirement, checked in `checklist.md`.

**The spine replaces the stub's tier headings.** A scaffolded `learning.md` arrives organised as one `##` section per rung, with a prompt under each. That is stub organisation — a place to hold the assignment — not the shape of a finished chapter. Replace it with the spine above and carry the rung down onto the individual units, because a reader needs the material grouped by what makes them functional, not by what level it is. Keep the frontmatter and the `## Brief` block untouched; everything below the brief is yours to restructure. The rung prompts in the HTML comments are instructions to you and never survive into the delivered file.

Standalone, with no frontmatter, use `Foundations → Mechanics → Practitioner → Architect` and pick a domain-appropriate wording for the top rung.

### The closing sections

**The whole picture** reassembles the chapter now that all the vocabulary exists. It should read as obvious, and that feeling is the point. It is not a list of the headings.

**Glossary:** every term the chapter defined, alphabetical, one line each.

**Spaced recall:** questions worth re-answering in a week and in a month, grouped by rung, without answers, each pointing at the unit that covers it.

**Sources:** what you actually read, with the date retrieved and what each one supports. Never a reading list — that is *Where to go next*, which names specific books, specs, papers, or source code and says what each is good for.

## The unit

A unit is one idea, self-contained enough that a reader can stop after it and have gained something whole. Target roughly five minutes of reading; put the estimate in the heading.

Every unit opens with a **one-line takeaway in bold** — the claim of the unit, before the argument for it. Then the body answers these six questions. **They are obligations, not headings.** Do not print them as labels. Do not answer them in this order if the material reads better another way. Do not skip one because it is awkward for your domain — an awkward one usually means the unit is mis-scoped.

**Why does this exist?** The situation that makes the idea necessary — something goes wrong or is impossible without it. Concrete, and told as a situation rather than a definition. This comes before the mechanism: motivation first, always.

**What is it?** The idea in plain language, as you would say it to a friend on the walk home. Then the precise version, with every term defined at first use. The plain version buys you the right to be dense.

**Show me one.** The obligation most often failed, and the one that varies most by domain — read `domains.md` for what it means in yours. Whatever form it takes, it is specific, attributable, and walked through with intermediate state visible. An abstract description restated is not an example.

**Where do people go wrong?** The wrong belief a learner actually forms here, written in their voice ("so it just caches everything, right?"). Acknowledge why it is a reasonable inference, then show the specific case where it produces a wrong prediction. A concrete counterexample beats a correction.

**What did it cost?** Every choice bought something and sold something. Name both sides, and name what you would use instead and when that wins. At the top rung this extends to what breaks — at what scale, with what symptom, and which misleading symptom appears first.

**Can I do it?** One question the reader can only answer if they actually got it — prediction, transfer, or diagnosis, never recall of the nearest paragraph. Fold the answer in `<details><summary>Answer</summary>…</details>` so looking is a choice.

If a unit has no real trap and no real trade-off, it is probably not a unit — fold it into its neighbour.

## Sizing

The unit is a shaping guide, not a limit. A unit that needs nine minutes to be complete takes nine minutes. **Completeness against the brief always wins over the read-time target** — never cut coverage to hit five minutes, and never pad to reach it.

A healthy chapter runs 8–14 units. Past that, see the halt condition in `SKILL.md`: the fix is a smaller chapter in `PLAN.md`, never a thinner one here.

## Diagrams, tables, code

Use a Mermaid block when the relationship is genuinely two-dimensional — state machines, request flows, dependency graphs, layered architectures, trees. Not for a linear list of steps. Follow every diagram with a sentence saying what to look at in it; a diagram nobody is told how to read is decoration.

Tables are for comparisons across a fixed set of dimensions. They have no room for reasoning, so never explain in one.

Code blocks are complete, language-tagged, and show their output. Comments explain *why*; the reader can already see *what*. Long code goes in pieces first, then once in full.
