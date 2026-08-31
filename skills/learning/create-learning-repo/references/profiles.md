# Profiles

Every chapter gets the same six files, in every domain. A profile changes only the **tier ladder** and the **labels inside those files** — never their names. Stable filenames mean `progress.md`, greps, and `author-chapter` have one contract to honour, and a new domain can never fork the layout.

Set it once at the top of `plan.yaml`. Default is `technical`.

```yaml
profile: technical    # technical | craft | practice | exam | custom
```

## The four presets

| Profile | Fits | Tier ladder |
|---|---|---|
| `technical` | Programming, data, infra, security, ML | Junior → Senior → Architect → Expert |
| `craft` | Writing, blogging, design, speaking, video | Beginner → Practitioner → Voice → Authority |
| `practice` | Productivity, time management, habits, fitness, money habits | Aware → Consistent → Adaptive → Designer |
| `exam` | Certifications, licensing, academic exams | Recall → Applied → Scenario → Edge |

## Why one set of prompts serves all four

The rungs are worded differently but occupy the same four positions, so `learning.md` can carry one set of tier prompts regardless of profile:

1. **Foundation** — you do it correctly when told to, and can explain what it is with no jargon.
2. **Working** — you do it under real constraints, know what it costs, and have made the mistakes.
3. **Systemic** — you place it in a whole system and defend the trade-off to someone who disagrees.
4. **Frontier** — you know where the received wisdom is incomplete, and have evidence for saying so.

Read the ladders against those positions:

- `technical` — Junior (uses it when told) → Senior (chooses it under constraint) → Architect (places it in a system) → Expert (knows where consensus is wrong).
- `craft` — Beginner (follows the form competently) → Practitioner (makes deliberate choices and can justify each) → Voice (the work is recognisably yours and still serves the reader) → Authority (shifts how other practitioners think about the form).
- `practice` — Aware (names the mechanism and spots it in your own week) → Consistent (runs it without motivation) → Adaptive (adjusts when context breaks the default) → Designer (builds systems others can run, and knows their failure modes).
- `exam` — Recall (states it cold, under time) → Applied (uses it on a clean question) → Scenario (finds it inside a messy multi-step problem) → Edge (handles the distractors examiners actually use).

## What else a profile changes

Only labels, and only where the difference is real:

| Profile | Overrides |
|---|---|
| `technical` | None — it is the baseline. |
| `craft` | `examples.md` items are Specimens; `practice.md` items are Exercises; `interview.md` is titled *Hard Questions* and framed as editor pushback. |
| `practice` | `examples.md` items are Cases; `practice.md` becomes Experiments with hypothesis/setup/result slots; `interview.md` is *Hard Questions*, framed as what breaks your system three months in. |
| `exam` | `practice.md` becomes timed Drills; `interview.md` is *Examiner Questions* (15 of them); `quizzies.md` grows to 15; `thought_leadership.md` shrinks to 2 and is marked optional. |

Note what is *not* on that list: which topics, why they matter, how deep to go, what style to write in. Those come from the per-chapter brief in the plan, which is where domain difference actually belongs. Do not reach for a new profile because the content differs — only when the *shape* does.

## Choosing one

Ask what a person at the top of the ladder has that a person at the bottom doesn't.

- *Systems judgement* → `technical`
- *A distinctive point of view* → `craft`
- *A system they run without willpower* → `practice`
- *A score on a fixed date* → `exam`

Goals are often mixed ("learn Rust **and** blog about it"). Don't split the repo — pick the profile matching the terminal goal and let `thought_leadership.md` carry the secondary one.

## `tier_count`

Plan-level, clamped 2–4, default 4. Trims the ladder from the top.

```yaml
tier_count: 3    # stop at Architect / Voice / Adaptive / Scenario
```

Use it when the horizon is short. Scaffolding an Expert section nobody will reach in three weeks just teaches the learner to leave headings empty.

## `custom`

For a domain none of the four fit. The plan declares the ladder itself; the six files are unchanged.

```yaml
profile: custom
tiers:
  - [Apprentice, "You execute a set piece from memory."]
  - [Journeyman, "You adapt it to an unfamiliar room."]
  - [Master, "You compose your own and it holds up."]
```

Two to four rungs, each a name plus a one-line test the learner can apply honestly to themselves. A rung whose definition is a synonym of the rung below it is not a rung.

## Adding a preset

Add an entry to `PROFILES` in `scripts/scaffold.py` — a `tiers` list, plus a `files` dict overriding `item`, `title`, `count`, `slots`, or `framing` for any of the five slot files — and a row to the tables above. Do not add a template: `learning_stub` and `slot_stub` render every file in every profile. If a domain seems to need a third renderer, the renderers are wrong and should be fixed rather than bypassed.
