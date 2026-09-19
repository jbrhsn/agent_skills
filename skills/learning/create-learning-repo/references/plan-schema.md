# Plan schema

`scaffold.py` reads `plan.yaml` or `plan.json`. Same shape either way. The machine-readable plan is the helper input: it carries the structure and chapter briefs. Keep it consistent with the generated `PLAN.md` summary. The requirements below apply when using this helper; a custom layout can be authored directly.

## Schema

```yaml
repo_name: python-senior-data-engineer      # slug; becomes the root folder if --out omitted
goal: >                                     # required, one paragraph, concrete
  Pass a senior data engineer interview loop focused on Python,
  distributed data processing, and pipeline design.
profile: technical                          # optional, default technical - see profiles.md
tier_count: 4                               # optional, 2-4, default 4
target: Senior Data Engineer                # optional: role/exam/project
level: rusty-professional                   # optional
horizon: 20 days                            # optional, recorded only by the helper
counts:                                     # optional, per-file slot counts, clamp 1-20
  interview: 12
  quizzies: 10
excluded:                                   # optional, agreed non-goals
  - Frontend / JavaScript
assumptions:                                # optional, record material assumptions when useful
  - Assumed batch over streaming focus

sections:
  - name: Python Core
    arc: Rebuild the fluency an interviewer assumes you never lost.
    modules:
      - name: Data Structures
        arc: From what the builtins are to why CPython made them that way.
        chapters:
          - name: Builtin Collections
            purpose: >                      # REQUIRED
              Interviewers open with collections because the answers reveal
              whether you think about memory or only about syntax.
            depth: Far enough to explain the CPython layout and benchmark a claim.
            style: Concrete examples, with measured timings clearly distinguished from estimates.
            serves: The coding screen's first fifteen minutes.
            builds_on: []                   # earlier chapter names this assumes
            enables: [Complexity and Trade-offs]
            topics:
              - name: Dictionaries
                covers: [hashing, collision handling, insertion order, dict views]
                depth: Explain the compact layout; benchmark it, don't just describe it.
              - name: Lists and arrays
                covers: [over-allocation, amortised append]
              - Sets                        # bare strings still work
            tiers:                          # optional per-rung scope, keyed by lowercase rung
              junior: Pick the right collection for a stated requirement.
              senior: Predict the memory cost before you measure it.
```

## Required vs optional

- **Required:** `repo_name`, `goal`, `sections`; every section `name`, module `name`, chapter `name`, chapter `topics`, and chapter **`purpose`**.
- **Warned but not fatal:** section `arc`, chapter `depth`, `style`, `serves`. The scaffolder lists these at the end as *thin briefs* — review these warnings and add detail where it helps the assignment; they do not prevent scaffolding.
- Everything else is optional.

`purpose` is required by the script. Infer a useful purpose from the goal and topics when possible; reconsider a chapter if its role remains unclear.

## The cohesion fields

These are what stop chapters reading as disconnected islands. Three are authored, the rest are derived for free from plan order.

| Field | Written by | Appears as |
|---|---|---|
| `arc` (section, module) | You | A line in every chapter file below the breadcrumb |
| `serves` | You | Frontmatter + the chapter header |
| `builds_on` / `enables` | You | Frontmatter + the brief's *assumes / unblocks* lines |
| `position`, `prev`, `next` | Derived from plan order | Frontmatter + nav footer links |

Write `builds_on` and `enables` as **exact chapter names** from elsewhere in the plan. These describe genuine dependencies; independent chapters may leave both empty.

Order chapters in the plan the way you intend them to be read — `prev`/`next` follow plan order across module and section boundaries, so the whole repo has one reading thread.

## Naming produced by the script

- Sections: `01-python-core/`
- Modules: `01-data-structures/` (numbering restarts inside each section)
- Chapters: `builtin-collections/` (no number)
- Chapter files in helper output: `learning.md`, `examples.md`, `practice.md`, `interview.md`, `thought_leadership.md`, `quizzies.md`

Names are human-readable Title Case; the script slugifies them for paths and de-duplicates collisions.

## Sizing heuristics

| Signal | Target |
|---|---|
| Topics per chapter | Often 3–6; consider splitting when purposes diverge, not solely on count. |
| Chapters per module | 2–5 |
| Modules per section | 2–5 |
| Sections | Often 3–7 for a broad curriculum; fewer or more may fit. |

Treat these ranges as rough planning cues, not limits. Estimate effort from the actual reading, practice, prior knowledge, and depth; a chapter count alone cannot predict study time. If a deadline is unrealistic, explain the trade-off and prioritize useful progress without promising mastery.

## Section design

Order sections so each is usable on its own and earlier ones unblock later ones — then make that ordering explicit with `builds_on`/`enables` rather than leaving it implied by position. For interview-driven goals, a dedicated assessment section can help, while integrated practice may fit other plans better.
