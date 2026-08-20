# Plan schema

`scaffold.py` reads `plan.yaml` or `plan.json`. Same shape either way.

## Schema

```yaml
repo_name: python-senior-data-engineer      # slug; becomes the root folder if --out omitted
goal: >                                     # required, one paragraph, concrete
  Pass a senior data engineer interview loop focused on Python,
  distributed data processing, and pipeline design.
target: Senior Data Engineer                # optional: role/exam/project
level: rusty-professional                   # optional
horizon: 20 days                            # optional, recorded only — never scheduled
excluded:                                   # optional, agreed non-goals
  - Frontend / JavaScript
  - Kubernetes internals
assumptions:                                # optional, only if user skipped the interview
  - Assumed batch over streaming focus

sections:
  - name: Python Core
    summary: Language fundamentals a senior is expected to use without hesitation.
    modules:
      - name: Data Structures
        chapters:
          - name: Builtin Collections
            topics:
              - Lists and arrays
              - Tuples
              - Dictionaries
              - Sets
              - Strings and bytes
            interview_questions: 12         # optional, default 12, clamp 10–15
            thought_leadership_ideas: 4     # optional, default 4
          - name: Complexity and Trade-offs
            topics: [Big-O in CPython, Amortized cost, Memory layout]
```

## Field rules

- `repo_name`, `goal`, `sections` are required. Everything else is optional.
- Every section needs ≥1 module; every module ≥1 chapter; every chapter ≥1 topic.
- `name` fields are human-readable Title Case. The script slugifies them for paths.

## Naming (produced by the script — don't hand-craft)

- Sections: `01-python-core/`
- Modules: `01-data-structures/`  (numbering restarts inside each section)
- Chapters: `builtin-collections/`  (no number)
- Topic files: `lists-and-arrays.md`
- Plus per chapter: `interview.md`, `thought_leadership.md`

## Sizing heuristics

| Signal | Target |
|---|---|
| Topics per chapter | 4–8. Above 10, split the chapter. |
| Chapters per module | 2–5 |
| Modules per section | 2–5 |
| Sections | 3–7. Above 8, the goal is probably two goals. |

Scale total topic count to the user's deadline × weekly hours, roughly **one topic per 1–2 study hours**. Undersize rather than oversize — an abandoned repo teaches nothing. If the math says the goal doesn't fit the deadline, say so before scaffolding.

## Section design

Order sections so each is usable on its own and earlier ones unblock later ones. For interview-driven goals, reserve one section for the interview format itself (system design, behavioral, take-home) rather than scattering it through technical sections.
