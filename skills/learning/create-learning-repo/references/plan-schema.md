# Plan schema

`scaffold.py` reads `plan.yaml` or `plan.json`. Same shape either way. The plan is the source of truth — it carries both the structure and the **brief** that tells the learner what belongs in each stub and how deep to go.

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
horizon: 20 days                            # optional, recorded only - never scheduled
counts:                                     # optional, per-file slot counts, clamp 1-20
  interview: 12
  quizzies: 10
excluded:                                   # optional, agreed non-goals
  - Frontend / JavaScript
assumptions:                                # optional, only if the user skipped the interview
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
            style: Bullets over prose. Every claim backed by a timing you ran yourself.
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
- **Warned but not fatal:** section `arc`, chapter `depth`, `style`, `serves`. The scaffolder lists these at the end as *thin briefs* — a stub whose brief is thin is a stub nobody knows how to fill, which is the failure this schema exists to prevent.
- Everything else is optional.

`purpose` is required because it is the one field that cannot be inferred from anything else. A chapter that cannot justify its own existence in one sentence should be merged or cut, not scaffolded.

## The cohesion fields

These are what stop chapters reading as disconnected islands. Three are authored, the rest are derived for free from plan order.

| Field | Written by | Appears as |
|---|---|---|
| `arc` (section, module) | You | A line in every chapter file below the breadcrumb |
| `serves` | You | Frontmatter + the chapter header |
| `builds_on` / `enables` | You | Frontmatter + the brief's *assumes / unblocks* lines |
| `position`, `prev`, `next` | Derived from plan order | Frontmatter + nav footer links |

Write `builds_on` and `enables` as **exact chapter names** from elsewhere in the plan. They are the dependency graph; if a chapter has neither, ask yourself why it is in this repo at all.

Order chapters in the plan the way you intend them to be read — `prev`/`next` follow plan order across module and section boundaries, so the whole repo has one reading thread.

## Naming (produced by the script — don't hand-craft)

- Sections: `01-python-core/`
- Modules: `01-data-structures/` (numbering restarts inside each section)
- Chapters: `builtin-collections/` (no number)
- Chapter files: always `learning.md`, `examples.md`, `practice.md`, `interview.md`, `thought_leadership.md`, `quizzies.md`

Names are human-readable Title Case; the script slugifies them for paths and de-duplicates collisions.

## Sizing heuristics

| Signal | Target |
|---|---|
| Topics per chapter | 3–6. Above 8, the chapter has two purposes — split it. |
| Chapters per module | 2–5 |
| Modules per section | 2–5 |
| Sections | 3–7. Above 8, the goal is probably two goals. |

A chapter is now one `learning.md` covering all its topics, so **chapters are the unit to count**, not topics. Budget roughly **one chapter per 3–5 study hours** and scale to the deadline × weekly hours. Undersize rather than oversize — an abandoned repo teaches nothing. If the arithmetic says the goal doesn't fit the deadline, say so before scaffolding rather than shipping a tree the user will quietly abandon.

## Section design

Order sections so each is usable on its own and earlier ones unblock later ones — then make that ordering explicit with `builds_on`/`enables` rather than leaving it implied by position. For interview-driven goals, reserve one section for the interview format itself (system design, behavioural, take-home) instead of scattering it through technical sections.
