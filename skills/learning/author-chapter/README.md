# Author-Chapter Skill

## Skill Overview

The author-chapter skill produces one textbook-quality Markdown file that teaches any topic comprehensively, taking a reader from absolute zero to architect-level mastery. Use this skill whenever someone asks you to write a chapter, learning module, tutorial, course, guide, primer, explainer, study material, or any long-form educational document about a concept or technology — even if they don't explicitly use the word "chapter" or "module".

## Reader Model

The target reader is a **curious 15-year-old with no background in the field but real patience**. They are not stupid — they are *uninformed*. The skill never dumbs down the material; instead, it removes every unexplained assumption. By the end of the module, the reader should be able to hold their own with a senior practitioner in the domain, judge tradeoffs, and predict how systems fail.

This reader model shapes every decision in the skill: concrete examples over abstract explanation, problem-first over definition-first, and always defining jargon at the moment it appears.

## Key Philosophy

Long educational writing fails in predictable ways: authors skip prerequisites they thought were obvious, use terms before defining them, explain *what* but never *why*, and stop at tutorial depth. The author-chapter skill prevents these failures through a strict **5-phase workflow structure** that front-loads planning and back-loads auditing.

**Follow the phases in order.** The plan is what makes later sections comprehensive; skipping phases produces a shallow document that looks complete but teaches little. Each phase exists because it catches a specific failure mode that looser processes miss.

## Phases Overview

### Phase 1: Resolve the Topic (Fast)

Pick a sensible scope and move on. Ask the user **only** when one of these is true:
- The topic name is genuinely ambiguous across fields (e.g., "bootstrapping", "normalization")
- The topic is code-heavy and no language/stack is implied
- The endpoint is unclear in a way that changes the entire learning ladder

Otherwise, make a decision and record it in the module's **Scope** section: what this module covers, what it deliberately does not, and what the reader will be able to do at the end.

If the host agent has web search capability and the topic is fast-moving (versions, APIs, standards), verify specifics before writing. If it has no search, write from knowledge and mark version-sensitive claims as "check current docs."

### Phase 2: Build the Concept Inventory Before Writing Any Prose

This is the highest-leverage step. Write every concept the reader must own, along with its dependencies and its tier.

**The Tier System:**

| Tier | Name | The reader can... |
|---|---|---|
| 0 | Foundations | ...explain what the thing is and what problem it solves, in their own words |
| 1 | Mechanics | ...describe how it actually works, step by step, and predict simple outcomes |
| 2 | Practitioner | ...use it correctly on real work, debug it, and follow standard idioms |
| 3 | Architect | ...choose it or reject it, defend the choice, predict failure modes at scale, and design around them |

Order concepts so that nothing appears before its prerequisites. That ordering becomes the module's table of contents.

**Sanity checks:**
- If Tier 0 has fewer than three concepts, the on-ramp is too steep for a beginner.
- If Tier 3 is thin, the module is a tutorial, not a path to architect level.
- Fix the inventory, not the prose, if something is wrong here.

### Phase 3: Write Section by Section, Appending to the File

Never attempt the whole document in one pass — long single-shot writing degrades badly and gets truncated. Write one section, append it, move to the next.

Before writing prose, read:
- `references/structure.md` — the exact document skeleton and per-concept block
- `references/voice.md` — prose rules and sentence-level style
- `references/pedagogy.md` — how to build examples, analogies, and difficulty ramps

Keep writing until every concept in the inventory has been covered. Do not summarise or compress later sections because the file is getting long; length is not a failure mode here — gaps are.

### Phase 4: Audit and Repair

Delete the scratch inventory. Run every check in `references/checklist.md` against the finished file and fix what fails. Report to the user only what was actually changed — do not claim a clean pass without verifying it.

### Phase 5: Deliver

Save as `<topic-slug>.md` (lowercase, hyphenated, e.g., `database-indexing.md`) unless the user specified a path. Tell the user the tier coverage in one line — concept count per tier — so they can see the shape of what they received.

## Non-Negotiables

These six rules are violated most often, so they sit in the main file rather than references. They are never negotiable:

1. **No undefined term, ever.** Every piece of jargon is defined in plain language at first use, inline, before it's used in an explanation. If defining term A requires term B, then B comes first — that's what the inventory ordering is for.

2. **Every concept gets a worked example.** Concrete, specific, with real values or real code, walked through step by step. An abstract description is not an example.

3. **Every concept gets a misconception.** State the wrong belief a learner actually forms, then dismantle it. "A common trap is thinking X — here's why that breaks."

4. **Every Tier 3 section names a failure mode.** What breaks, at what scale, with what symptom. Architect-level knowledge is mostly knowledge of failure.

5. **Answer "why does this exist" before "how does it work".** Mechanism without motivation doesn't stick. Every concept opens with the problem it solves.

6. **Cross-reference forward and back.** When a later section pays off an earlier one, say so explicitly: "This is the reason we insisted on X back in section 3."

## Document Structure

The final output follows a strict skeleton that ensures logical pacing and comprehensive coverage:

```
# <Topic>: From Zero to Architect

## Before You Start
- What you'll be able to do (concrete capabilities)
- What you need to know already (minimal and honest)
- What this module deliberately does not cover
- How to read this: the tiers and checkpoints

## Part 0 — Why This Exists
- The problem that made someone invent this
- What people did before it and what went wrong
- One-sentence version of the whole topic

## Part 1 — Foundations
- Tier 0 concept blocks (minimum 3)
- Checkpoint (3-5 questions with folded answers)

## Part 2 — Mechanics
- Tier 1 concept blocks
- Checkpoint

## Part 3 — Practitioner
- Tier 2 concept blocks
- Exercises (3-5 real tasks with worked solutions)
- Checkpoint

## Part 4 — Architect
- Tier 3 concept blocks
- Case Studies (2-3 real systems or incidents)
- Design Drills (open-ended scenarios with reference answers)

## The Whole Picture
- One page that reassembles everything now that vocabulary is complete
- Should feel obvious on rereading

## Glossary
- Every term defined in the module, alphabetical, one line each

## Spaced Recall
- Questions worth re-answering in a week and a month
- Grouped by tier, no answers

## Where To Go Next
- Specific books, specs, papers
- What each one is good for
```

## The Per-Concept Block

Every concept in the inventory gets this 8-part structure. It is the unit of the module — repeat it, don't improvise around it:

### Structure of a Concept Block

1. **The problem.** The situation that makes this concept necessary. Something goes wrong or is impossible without it. (2-4 sentences, concrete.)

2. **The idea.** The concept in plain language, no jargon, as if explaining to a friend. (One short paragraph.)

3. **An analogy.** One analogy, chosen well. Then immediately state where the analogy breaks down — an unmarked analogy becomes a misconception later.

4. **How it actually works.** The precise mechanics. This is where jargon is introduced, each term defined at first use. Be technically exact; the earlier sections bought you the right to be dense.

5. **Worked example.** Real values, real code, real numbers. Walk through it step by step, showing intermediate state. The reader should be able to follow it with a pen and reproduce the result.

6. **The trap.** The wrong belief learners actually form here. State it in the learner's voice, then take it apart. Explain why it's tempting — that's what makes the correction stick.

7. **Why it's built this way.** The tradeoff. What was given up to get this, what the alternatives are, and when the alternative wins. For Tier 3 concepts, add the failure mode: what breaks, at what scale, with what symptom.

8. **Check yourself.** One question the reader can only answer if they got it. Answer folded below it in a `<details>` block.

Blocks may be shorter for small concepts, but no part may be dropped. If a concept has no meaningful trap or no meaningful tradeoff, it is probably not a concept — fold it into a neighbouring one.

## Reference Files

Read these as you reach the phase that needs them; do not load them all at once. All five files are in the `references/` subdirectory:

### references/structure.md
The complete document skeleton, the per-concept block structure, and rules for diagrams, tables, and code blocks. Read before writing any prose.

### references/pedagogy.md
How to build examples, analogies, misconceptions, and exercises that actually work. Covers load management (introducing one new idea at a time), why worked examples come before independent practice, the role of retrieval in retention, how to make analogies useful without being misleading, and why Tier 3 is about judgement, not just facts.

### references/voice.md
Prose rules, sentence-level style, and patterns to avoid. Emphasizes concrete language, second-person present tense, numbered specifics over adjectives, and respect for the reader's intelligence. Lists what to avoid: undefined jargon, filler openers, hollow enthusiasm, rhetorical questions as headings, and talking down.

### references/examples.md
An annotated weak-vs-strong section pair (both about database indexes). The weak version shows common failures; the strong version shows how each element works when done correctly. Read this if unsure whether the writing is hitting the bar.

### references/checklist.md
The Phase 4 audit checklist — 30+ verification points covering coverage, per-concept integrity, vocabulary, learning scaffolding, prose quality, and mechanics. Run every item before delivering.

## When to Use This Skill

Trigger this skill on any of these requests:

- "Write a chapter on X"
- "Create a learning module about X"
- "I want to master X"
- "Teach me X properly"
- "Write a deep dive on X"
- "Create a tutorial for X"
- "Write a guide to X"
- "Build a course on X"
- "Write a primer on X"
- "Create an explainer for X"
- "I need study material on X"

Even if the user doesn't use the word "chapter" or "module", if the deliverable is teaching material, use this skill instead of answering from scratch.

## When NOT to Use This Skill

Do not use this skill for:

- **Scaffolding a new learning repository** — use the `create-learning-repo` skill instead. That skill is for setting up repo structure, templates, and stub files. This skill is for authoring one complete chapter within an already-structured repo.
- **Editing existing repo content** — if the content is already in a repo and needs updating or refactoring, use the `lean-coder` skill instead.

This skill is specifically for authoring one complete, self-contained educational module from scratch.

## Quick Start Example

**User request:** "Write a tutorial that teaches database indexing from the ground up. I want someone with no database experience to understand why indexes exist, how they work, what they cost, and how to use them."

**Workflow:**

1. **Phase 1** — Resolve: The request is clear (database indexing, beginner to practitioner level). Scope is set: this covers indexes in relational databases, not key-value stores or search engines. The endpoint is defined: the reader will understand tradeoffs and know when to index.

2. **Phase 2** — Inventory: Build the concept list:
   - Tier 0: Why indexes exist (full table scans are slow), the index as a sorted lookup structure
   - Tier 1: B-tree structure, page boundaries, search algorithms, update cost
   - Tier 2: Choosing columns, covering indexes, composite indexes, real tools
   - Tier 3: Tradeoffs at scale, failure modes (write amplification), alternatives (hash indexes, LSM trees)

3. **Phase 3** — Write: Section by section, following structure.md and voice.md. Each concept gets the 8-part block. Checkpoints after each tier. Real examples with numbers and code.

4. **Phase 4** — Audit: Run every check in checklist.md. Fix any undefined terms, missing examples, or weak analogies.

5. **Phase 5** — Deliver: Save as `database-indexing.md`. Report: "Tier coverage: 2 concepts at Foundation, 4 at Mechanics, 3 at Practitioner, 3 at Architect."

## Key Outputs

At the end of the skill's workflow, the user receives:

- **One complete Markdown file** with comprehensive coverage from beginner to architect level
- **Filename**: a lowercase, hyphenated slug of the topic (e.g., `http-caching.md`, `git-internals.md`)
- **Tier coverage**: a one-line summary of how many concepts at each tier (e.g., "3 Foundation / 5 Mechanics / 4 Practitioner / 3 Architect")
- **Ready to use**: the file is audit-passed and ready to publish, link, or include in a learning repository

The file teaches one person, alone, to understand the topic deeply. It is not a reference manual and it is not a blog post; it is a complete path from zero to expert understanding.
