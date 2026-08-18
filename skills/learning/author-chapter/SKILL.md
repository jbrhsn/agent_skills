---
name: author-chapter
description: Author a complete, textbook-quality learning module as a single Markdown file that takes a total beginner from zero to architect-level mastery of one topic, written so a bright teenager can follow it. Use this skill whenever the user asks to write a chapter, learning module, tutorial, course, guide, primer, explainer, study material, "teach me X properly", "I want to master X", "write a deep dive on X", or wants any long-form educational document about a concept or technology — even if they don't use the word "chapter" or "module". Prefer this over answering from scratch for any request whose deliverable is teaching material.
---

# Author Chapter

Produce one `.md` file that teaches a topic from absolute zero to the level where the reader could design systems with it, judge tradeoffs, and predict how it fails.

The reader model: a curious 15-year-old with no background in the field but real patience. They are not stupid — they are *uninformed*. Never dumb the material down; instead remove every unexplained assumption. By the end of the file they should be able to hold their own with a senior practitioner.

## Why this skill is strict

Long educational writing fails in predictable ways: the author skips the prerequisite that felt obvious, uses a term before defining it, explains *what* but never *why*, and stops at tutorial depth. The workflow below front-loads a plan and back-loads an audit precisely to catch those. Follow the phases in order — the plan is what makes the later sections comprehensive, and skipping it produces a shallow document that looks fine and teaches little.

## Workflow

### Phase 1 — Resolve the topic (fast)

Pick a sensible reading and move on. Ask the user **only** when one of these is true, and then ask at most three questions in a single message:

- The topic name is genuinely ambiguous across fields (e.g. "bootstrapping", "normalization", "reduction").
- The topic is code-heavy and no language/stack is implied anywhere in the conversation.
- The requested endpoint is unclear in a way that changes the whole ladder (e.g. "networking" — protocol design, or operating a network?).

Otherwise, choose, and record the choice in the module's Scope section: what this module covers, what it deliberately does not, and what the reader will be able to do at the end.

If the host agent has web search and the topic is fast-moving (versions, APIs, current tooling, recent standards), verify specifics before writing. If it has no search, write from knowledge and mark anything version-sensitive as "check current docs" rather than guessing a version number.

### Phase 2 — Build the concept inventory before writing any prose

This is the highest-leverage step. Write the inventory into the working file first as a scratch section (deleted before delivery).

For the topic, list every concept the reader must own. For each: its name, the concepts it depends on, and its tier.

| Tier | Name | The reader can... |
|---|---|---|
| 0 | Foundations | ...explain what the thing is and what problem it exists to solve, in their own words |
| 1 | Mechanics | ...describe how it actually works, step by step, and predict simple outcomes |
| 2 | Practitioner | ...use it correctly on real work, debug it, and follow the standard idioms |
| 3 | Architect | ...choose it or reject it, defend the choice, predict its failure modes at scale, and design around them |

Then order the concepts so that nothing appears before its prerequisites. That ordering is the module's table of contents.

Sanity-check the inventory before proceeding: if Tier 0 has fewer than three concepts, the on-ramp is too steep for a beginner. If Tier 3 is thin, the module is a tutorial, not a path to architect. Fix the inventory, not the prose.

### Phase 3 — Write section by section, appending to the file

Never attempt the whole document in one pass — long single-shot writing degrades badly and gets truncated. Write one section, append it, move to the next. Keep going until every concept in the inventory has been written. Do not summarise or compress later sections because the file is getting long; length is not a failure mode here, gaps are.

Read `references/structure.md` for the exact document skeleton and the per-concept block. Read `references/voice.md` before writing the first prose section and follow it throughout. Read `references/pedagogy.md` for the learning-science rules that govern examples, analogies, misconceptions, and difficulty pacing.

### Phase 4 — Audit and repair

Delete the scratch inventory. Then run every check in `references/checklist.md` against the finished file and fix what fails. Report to the user only what you actually changed — do not claim a clean pass you didn't verify.

### Phase 5 — Deliver

Save as `<topic-slug>.md` (lowercase, hyphenated, e.g. `database-indexing.md`) unless the user specified a path. Tell the user the tier coverage in one line — concept count per tier — so they can see the shape of what they got.

## Non-negotiables

These are the rules most often broken, so they sit in the main file rather than a reference:

- **No undefined term, ever.** Every piece of jargon is defined in plain language at first use, inline, before it is used in an explanation. If defining term A requires term B, B comes first — that's what the inventory ordering is for.
- **Every concept gets a worked example.** Concrete, specific, with real values or real code, walked through step by step. An abstract description is not an example.
- **Every concept gets a misconception.** State the wrong belief a learner actually forms, then dismantle it. "A common trap is thinking X — here's why that breaks."
- **Every Tier 3 section names a failure mode.** What breaks, at what scale, with what symptom. Architect-level knowledge is mostly knowledge of failure.
- **Answer "why does this exist" before "how does it work".** Mechanism without motivation doesn't stick. Every concept opens with the problem it solves.
- **Cross-reference forward and back.** When a later section pays off an earlier one, say so explicitly: "This is the reason we insisted on X back in section 3."

## Reference files

Read these as you reach the phase that needs them; do not load them all at once.

- `references/structure.md` — the document skeleton and the per-concept block. Read before writing.
- `references/pedagogy.md` — how to build examples, analogies, exercises, and difficulty ramps that work.
- `references/voice.md` — prose rules, sentence-level style, and patterns to avoid.
- `references/examples.md` — an annotated weak-vs-strong section pair. Read this if unsure whether the writing is hitting the bar.
- `references/checklist.md` — the Phase 4 audit. Read at the end, and run every item.
