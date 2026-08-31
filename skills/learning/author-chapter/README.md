# Author-Chapter Skill

## Skill Overview

The author-chapter skill writes teaching material: one Markdown file that takes someone who knows nothing about a field to the level where they can make real decisions in it. Use it whenever the deliverable is educational — a chapter, module, tutorial, course, guide, primer, explainer, or study material — even if the user never says "chapter". It also fills any file scaffolded by create-learning-repo, reading that file's brief as its assignment.

## Reader Model

**An intelligent 28-year-old who knows nothing about this particular field.**

Both halves do work. *Knows nothing about the field:* no term goes undefined, no step is skipped as obvious, nothing is assumed from prior study. *Intelligent adult:* they have judgement and a job, so nothing is explained about how the world works, nothing is padded, and nothing reassures them. Their scarce resource is time, not capacity.

They read in short sittings, interrupted, over weeks — which is why the material is cut into units they can finish and come back from.

## What the skill is defending against

**Format conformity.** A model given one skeleton forces every domain into it — deriving page counts when the topic is essay structure, demanding "failure modes at scale" for a savings habit. So this skill fixes *obligations* and leaves their *realisation* to the domain. One spine, six questions per unit; how you answer them is chosen for the field.

**The undifferentiated wall.** Everything at one depth, in one block, with no signal about what matters. So the takeaway comes first, the vital 20% is marked, and units are sized to be finished.

## What it produces

```
# <Chapter>

**In one minute.** The takeaway, before any setup.
**The mental model.** One bounded analogy + the link to what came before.

## Contents            (past ~8 units)

## Core path           the 20% that gives 80% — stopping here is a real finish
  ### <Unit> · ~5 min
  ### <Unit> · ~5 min

## Going deeper        the rest, honestly optional-for-now

## The whole picture · Glossary · Spaced recall · Sources · Where to go next
```

## The unit

One idea, self-contained, roughly five minutes. Opens with a one-line bold takeaway, then answers six questions **in prose, never as printed labels**:

| Obligation | What it means |
|---|---|
| Why does this exist? | The situation that makes it necessary — before any mechanism |
| What is it? | Plain language first, then precise, every term defined at first use |
| Show me one | Specific, attributable, walked through. **Varies most by domain** |
| Where do people go wrong? | The wrong belief, in the learner's voice, with a counterexample |
| What did it cost? | Both sides of the trade, plus the alternative and when it wins |
| Can I do it? | Prediction, transfer, or diagnosis — answer folded in `<details>` |

## Domains

Obligations are universal; evidence is not. Each pack — keyed to create-learning-repo's profile names — says what counts as evidence, what a worked example is, what the top rung means, and what to never do.

| Profile | A worked example is | Top rung means |
|---|---|---|
| `technical` | Real values traced with intermediate state; runnable code | Predicting what breaks, at what scale, with what symptom |
| `craft` | A real artefact quoted and taken apart; a before/after with every edit named | Breaking the form on purpose and knowing what it protected |
| `practice` | A logged week with what actually broke | Designing for constraints unlike your own, and naming where it fails |
| `exam` | A question in the exam's real format, worked under time | Recognising the question type from its shape |

## File types

When filling a scaffolded chapter, the six files are six different jobs — and three of them must be left unfinished on purpose.

| File | Writes | Must not write |
|---|---|---|
| `learning.md` | The whole spine | — |
| `examples.md` | Attributed specimens, annotated | The learner's own annotation |
| `practice.md` | Tasks + success criteria | The solutions |
| `interview.md` | Q, spoken model answer, follow-up | Essays |
| `thought_leadership.md` | Angles + evidence required | Invented evidence |
| `quizzies.md` | Questions | The answers |

`quizzies.md` is a retrieval instrument; answering it destroys the only thing it does.

## Workflow

**Phase 1 — Read the assignment.** If the file was scaffolded, its frontmatter and brief *are* the plan: topics, per-topic depth, purpose, `serves`/`builds_on`/`enables`, and the tier ladder — whose rung names are used **verbatim**. Standalone, build a concept inventory instead and hold to it the same way.

**Phase 2 — Scope check.** Count units. 8–14 is healthy. Past ~18 the skill **stops before writing** and reports that the brief is more than one chapter, naming the seam. Fix it in `PLAN.md` and re-scaffold — the skill never splits a file or thins coverage to fit.

**Phase 3 — Research.** If a web search tool is available, using it is **mandatory**: one query for the chapter's current state, plus one per volatile topic. Version numbers, prices, benchmarks, dates, and "what practitioners now do" claims are sourced or explicitly flagged — never written from memory. Findings land in `## Sources` with dates. No tool available, the file says so.

**Phase 4 — Write unit by unit.** Append, never regenerate. A running scratch list tracks terms defined, simplifications owed, and coverage.

**Phase 5 — Audit.** `checklist.md`, universal section plus your domain and file type. Completeness against the brief runs first.

**Phase 6 — Deliver.** Keep the frontmatter, set `status: drafted`. Report coverage, unit count, and whether sourcing was live.

## Completeness, not length

A chapter is judged against its brief: every topic at its briefed depth, every rung reached, the stated purpose delivered. The five-minute unit is a *shaping* guide — it decides how material is cut up, never how much there is. Coverage is never cut to hit a read time, and nothing is padded to reach one.

A long chapter is fine. An unscoped one is not — that is what the Phase 2 halt is for.

## Non-Negotiables

1. **Takeaway first, at both levels.** Chapter opens with the answer; each unit opens with its claim.
2. **Motivation before mechanism.** Why it exists, then how it works.
3. **No undefined term, ever.** Defined in plain language at first use, inline.
4. **Every unit shows one real thing.** Attributable, specific, with intermediate state visible.
5. **Every unit names a trap and a cost.** Neither present? Fold it into its neighbour.
6. **Use the ladder you were given.** Rung names verbatim, however many there are.
7. **The reader can stop.** Units self-contained, core path marked, stopping stated as legitimate.
8. **Completeness beats length targets.**

## Reference Files

| File | Read at |
|---|---|
| `references/file-types.md` | Phase 1 — the six files, and the three refusals |
| `references/domains.md` | Phase 1 — evidence standards per domain |
| `references/structure.md` | Before writing — the spine and the six obligations |
| `references/pedagogy.md` | While writing — BLUF, the vital few, load, retrieval, pacing |
| `references/voice.md` | While writing — prose rules, reader model, length |
| `references/examples.md` | If unsure of the bar — weak/strong pairs, technical and craft |
| `references/checklist.md` | Phase 5 — the audit |

## When NOT to Use This Skill

- **Scaffolding a learning repo** — use `create-learning-repo`. That skill builds structure and briefs; this one fills them.
- **Editing existing code** — use `lean-coder`.

## Key Outputs

- One Markdown file, audit-passed, in self-contained units with the takeaway first
- Filename: a lowercase hyphenated slug, or the scaffolded file with frontmatter preserved
- A two-line report: coverage against the brief, unit count and read time, and what was left unverified
