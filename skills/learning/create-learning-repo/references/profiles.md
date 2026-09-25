# Profiles

In the bundled helper, every chapter gets the files selected by `chapter_files`, defaulting to `learning`, `examples`, and `practice`. A profile changes the tier ladder and file labels, counts, slots, and framing, but not the selection or filenames. Add interview, recall, or public-writing files only when useful to the goal.

Set it once at the top of `plan.yaml`. The helper default is `technical`; select the profile that fits the goal.

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
| `exam` | `practice.md` becomes timed Drills (3); selected `interview.md` is *Examiner Questions* (3); selected `quizzies.md` has 5 slots; selected `thought_leadership.md` has 2 optional writing slots. |

Note what is *not* on that list: which topics, why they matter, how deep to go, what style to write in. Those come from the per-chapter brief in the plan, which is where domain difference actually belongs. Use a custom profile when the presets do not describe the intended progression.

## Choosing one

Ask what a person at the top of the ladder has that a person at the bottom doesn't.

- *Systems judgement* → `technical`
- *A distinctive point of view* → `craft`
- *A system they run without willpower* → `practice`
- *A score on a fixed date* → `exam`

Goals are often mixed ("learn Rust **and** blog about it"). A single dominant profile is often sufficient; use a custom progression or another layout when both goals need substantial treatment.

## `tier_count`

Plan-level, clamped 1–4, default 2 for presets. Custom profiles use all declared rungs unless trimmed explicitly. Trims the ladder from the top; select only the levels needed for the goal.

```yaml
tier_count: 3    # stop at Architect / Voice / Adaptive / Scenario
```

Use fewer rungs when the requested scope does not call for the full ladder. Treat the names as learning milestones, not promises of professional expertise on a deadline.

## `custom`

For a domain none of the four fit. The plan declares the ladder itself; file selection is still controlled by `chapter_files`.

```yaml
profile: custom
tiers:
  - [Apprentice, "You execute a set piece from memory."]
  - [Journeyman, "You adapt it to an unfamiliar room."]
  - [Master, "You compose your own and it holds up."]
```

One to four rungs, each a name plus a one-line test the learner can apply honestly to themselves. A rung whose definition is a synonym of the rung below it is not a rung. Chapter completion checks make these broad levels concrete for the actual assignment.

## Adding a preset

Add an entry to `PROFILES` in `scripts/scaffold.py` — a `tiers` list, plus a `files` dict overriding `item`, `title`, `count`, `slots`, or `framing` for any of the five slot files — and a row to the tables above. The existing `learning_stub` and `slot_stub` renderers usually suffice; change implementation only when the requested behavior needs it.
