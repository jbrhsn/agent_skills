# File types

A chapter scaffolded by `create-learning-repo` is six files. They are not six views of the same content — each one does a different job, and three of them are jobs you must *not* finish for the learner. Read this before writing anything, and identify which file you are filling from its `title` frontmatter and filename.

Invoked standalone with no scaffold around it, you are writing `learning.md`. Skip to that row.

## What each file is

| File | You write | You must not write |
|---|---|---|
| `learning.md` | The teaching. The whole spine, every unit, every tier rung on the ladder | — |
| `examples.md` | Specimens by other people, annotated: what it is, why it works, what to steal | Your own worked examples — those live inside `learning.md` |
| `practice.md` | Tasks with success criteria | The solutions |
| `interview.md` | Questions, a model answer, and the follow-up they'd ask | Essays. These are spoken answers |
| `thought_leadership.md` | Angles, hooks, and the evidence each would need | The article. And never an angle the learner has no evidence for |
| `quizzies.md` | Questions only | The answers |

## The three refusals

These are the ones that get broken, because filling in a blank looks like helpfulness.

**`quizzies.md` gets no answers.** It is a retrieval instrument. The learner answers from memory later, with the notes closed, and then verifies against a source. An answer already sitting on the page destroys the only thing the file does. Write the questions, leave `**My answer, from memory:**` empty, and leave `**Verified?**` empty. Write questions that cannot be answered by pattern-matching a paragraph in `learning.md` — ask for prediction, transfer, or diagnosis.

**`practice.md` gets no solutions.** Write the task, the tier it sits at, and what *done* looks like concretely enough that the learner can judge their own attempt. Leave `**What I actually did**` and `**What broke**` empty — those are the learner's log, and they are where the learning happens.

**`thought_leadership.md` gets no invented evidence.** Each angle names what evidence would be required to publish it — a benchmark, an incident, a migration, an artefact. If the learner has not done the thing, the honest entry says so. An angle that only restates the documentation is not an angle; discard it rather than filling the slot.

## Per-file notes

### `learning.md`

The main event, and the only file that follows the full spine in `structure.md`. Everything else in this skill is written with this file in mind.

### `examples.md`

Specimens the learner studies, not exercises they do. What counts as a specimen is domain-specific — see `domains.md`. Real and attributed: a named library, a published essay, a documented incident, a released system. If you cannot attribute it, it is not a specimen, it is an illustration, and illustrations belong in `learning.md`.

For each: what it is and where it's from, why it works (mechanism, not praise), and one thing the learner should take from it into their own work. Leave `**My annotation**` empty — that slot is the learner reading it themselves.

### `interview.md`

Questions someone else puts to you, at the level the brief names — not the top rung unless the goal is the top rung. Mix the types the slots list: recall, applied, design, debugging. A model answer here is what a person actually says out loud in two minutes, not a written treatment: it leads with the answer, gives one reason, and stops. Then the follow-up, which is where the real evaluation happens.

Under the `exam` profile this file is examiner questions instead — the exam's own phrasing, including distractors. Under `craft` and `practice` it is the challenge a sharp peer would put to you. Same job, different register.

## Order

If you are filling several files for one chapter, write `learning.md` first. The other five refer to it: the questions, tasks, and angles should reflect what the chapter actually taught, not what you imagined it might. When `learning.md` already exists, read it before writing any sibling.
