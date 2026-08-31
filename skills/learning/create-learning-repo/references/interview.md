# Interview

Goal: extract enough to build a plan the user won't immediately want to rewrite — and enough to write a **brief** for every chapter. Batch questions, two rounds maximum. Use tappable/multiple-choice options where the harness supports them.

## Round 1 — always ask (unless already answered)

1. **Terminal goal.** What must be true when this repo is finished? ("Pass a senior data engineer loop at a FAANG-scale company" — not "know Python better.")
2. **Current level.** Beginner / working knowledge / rusty professional / strong but narrow. Ask for a concrete signal: what can you already build, write, or debug unaided?
3. **Deadline and weekly hours.** Used for *sizing* (how many chapters), never for scheduling.
4. **Depth vs breadth.** Broad recall across many topics, or deep mastery of few?
5. **Existing plan or syllabus?** If yes, get it before doing anything else.

## Round 2 — sharpen scope and fill the briefs

6. **In-scope specifics.** Languages, frameworks, tools, versions — or for non-technical goals, the form, medium, or exam board.
7. **Explicit exclusions.** What they already know cold or refuse to cover. Record these — they go in PLAN.md so they don't get re-added later.
8. **Assessment format**, if there is one: coding screen, system design, take-home, behavioural, portfolio review, written exam. Each maps to different chapters and to `interview.md`'s framing.
9. **Long-term arc.** Where does this sit in a 1–3 year trajectory? Drives whether to include architecture, leadership, or ecosystem chapters the immediate goal doesn't require.
10. **Public-writing intent.** Which platform and audience? Shapes `thought_leadership.md`. If they don't write publicly, still generate the file — say it's optional.
11. **Evidence standard.** What would convince *them* they'd actually learned something — a benchmark they ran, a piece they published, a week they sustained, a mock score? This is the single most useful answer you get: it becomes `depth` and `serves` on every chapter, and without it every brief comes out vague.

## Detecting the profile

Don't ask "which profile?" — the user doesn't know the vocabulary. Infer it from answers 1 and 11, and state your choice when you present the plan so they can correct it.

Ask what a person at the top of the ladder has that a person at the bottom doesn't:

| Signal in their goal | Profile |
|---|---|
| Systems judgement, design trade-offs, production code | `technical` |
| A distinctive point of view, an audience, published work | `craft` |
| A routine that survives a bad week | `practice` |
| A score on a fixed date | `exam` |

If the goal is genuinely mixed, pick the profile matching the *terminal* goal and let `thought_leadership.md` carry the secondary one. If none of the four fit, propose a `custom` ladder of 2–4 rungs and get the user to confirm the rung definitions — they are the yardstick they'll be marking themselves against, so their wording beats yours.

Also settle `tier_count` here: if the horizon is short, say so and drop to 2 or 3 rungs rather than scaffolding an Expert section nobody will reach.

## Rules

- Never ask something the user already told you. Re-reading their message beats asking.
- If they resist questioning ("just make it"), ask the two highest-leverage ones — terminal goal and evidence standard — then proceed and flag assumptions in PLAN.md under `## Assumptions`.
- Do not ask about folder naming, file formats, or which six files a chapter gets. Those are fixed by this skill.
