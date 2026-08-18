# Structure

## Document skeleton

Use this order. Section names may be reworded to fit the topic; the sequence and content must not change.

```markdown
# <Topic>: From Zero to Architect

## Before You Start
What you'll be able to do at the end (concrete capabilities, not "understand X").
What you need to know already (be honest and minimal; link out for anything heavy).
What this module deliberately does not cover, and where to go for it.
How to read this: the tiers, and the checkpoints.

## Part 0 — Why This Exists
The problem that made someone invent this. Told as a situation, not a definition.
What people did before it, and what specifically went wrong.
The one-sentence version of the whole topic, which the reader will not fully
understand yet — and a promise that they will by Part 3.

## Part 1 — Foundations
<concept blocks for every Tier 0 concept>
### Checkpoint
3-5 questions. Answers immediately after, folded in a details block.

## Part 2 — Mechanics
<concept blocks for every Tier 1 concept>
### Checkpoint

## Part 3 — Practitioner
<concept blocks for every Tier 2 concept>
### Exercises
3-5 tasks that produce something real. Full worked solutions after each.
### Checkpoint

## Part 4 — Architect
<concept blocks for every Tier 3 concept>
### Case Studies
2-3 real systems or real incidents. What they chose, why, what it cost them.
### Design Drills
Open-ended scenarios with no single right answer. Give a strong reference
answer that shows the reasoning, and name the tradeoffs it accepted.

## The Whole Picture
One page that reassembles everything, now that all the vocabulary is available.
Reread this after finishing; it should feel obvious, and that feeling is the point.

## Glossary
Every term defined in the module, alphabetical, one line each.

## Spaced Recall
A list of the questions worth re-answering in a week and in a month, grouped
by tier, without answers. Point back to the section that covers each.

## Where To Go Next
Specific books, specs, source code, papers. Say what each one is good for.
```

## The per-concept block

Every concept in the inventory gets this block. It is the unit of the module — repeat it, don't improvise around it.

```markdown
### <Concept name>

**The problem.** The situation that makes this concept necessary. Something
goes wrong or is impossible without it. Two to four sentences, concrete.

**The idea.** The concept in plain language, no jargon, as if explaining to a
friend on the walk home. One short paragraph.

**An analogy.** One analogy, chosen well. Then immediately state where the
analogy breaks down — an unmarked analogy becomes a misconception later.

**How it actually works.** The precise mechanics. This is where jargon is
introduced, each term defined at first use. Be technically exact here; the
earlier sections bought you the right to be dense.

**Worked example.** Real values, real code, real numbers. Walk through it step
by step, showing intermediate state. The reader should be able to follow it
with a pen and reproduce the result.

**The trap.** The wrong belief learners actually form here. State it in the
learner's voice, then take it apart. Explain why it's tempting — that's what
makes the correction stick.

**Why it's built this way.** The tradeoff. What was given up to get this, what
the alternatives are, and when the alternative wins. For Tier 3 concepts, add
the failure mode: what breaks, at what scale, with what symptom.

**Check yourself.** One question the reader can only answer if they got it.
Answer folded below it.
```

Blocks may be shorter for small concepts, but no part may be dropped. If a concept has no meaningful trap or no meaningful tradeoff, it is probably not a concept — fold it into a neighbouring one.

## Diagrams

Use a Mermaid block when the relationship is genuinely two-dimensional: state machines, request flows, dependency graphs, layered architectures, tree structures. Do not draw a diagram for a linear list of steps — prose or a numbered list is clearer and less likely to render badly.

Every diagram is followed by a sentence explaining what to look at in it. A diagram nobody is told how to read is decoration.

## Tables

Use tables for comparisons across a fixed set of dimensions (option vs option, tier vs capability, algorithm vs complexity). Do not use tables for explanation — they have no room for reasoning.

## Code

Code blocks are complete and runnable, with the language tagged. Comments explain *why*, never *what* — the reader can see what. Show the output. If the code is long, show it in pieces and then once in full.
