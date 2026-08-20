# Project Planner

Turn a rough idea into a detailed, validated project plan — no guessing, no wasted effort. Every requirement comes from answers you actually gave and explicitly confirmed, not assumptions the planner filled in.

## When to Use It

Use Project Planner before you start building, when you have a project idea but haven't nailed down the details yet. The skill guides you through a structured interview and produces a PRD (Product Requirements Document) and a phase-by-phase implementation plan.

**Practical triggers:**
- You have a project idea and don't know where to start
- You're about to start feature work but the scope isn't clear
- You want to learn a new language or framework by building something real
- A repo has no planning docs and you want to add them
- You have rough notes and need a formal project structure

## What You'll Get

- **`docs/prd.md`** — a complete PRD with functional requirements, non-functional requirements, out-of-scope items, and open questions (never assumptions)
- **`docs/plan/`** — a phase-by-phase implementation plan with:
  - `overview.md` — phases, sequence, dependencies, and milestones
  - `phase-01-*.md`, `phase-02-*.md`, etc. — one file per phase, with units (atomic buildable chunks)
- **`learnings/`** (optional) — if you're learning a new language or framework, structured learning topics and a curriculum tied to the build phases
- **Stability** — every requirement gets a stable ID (`FR-01`, `NFR-01`) so the plan doesn't break if you add more later

## Key Principles

The planner is built on a few core beliefs:

- **Interview first, write second** — you answer structured questions; the planner *confirms* every answer before writing anything down
- **No invented requirements** — if something isn't answered, it goes into "Open Questions," never into the spec as a guess
- **Documents only** — the plan is Markdown files under `docs/`, never any source code or scaffolding
- **Explicit approval gates** — the PRD needs your sign-off before any phase files are created
- **Minimal but complete** — each unit is small enough to build and verify in one sitting

## Stage Map

The skill follows a structured 7-stage workflow:

| Stage | What Happens | Output |
|-------|------|--------|
| 0 | Detect repo state and mode (standard vs. learn-by-building) | — |
| 1 | Interview in 4–6 question batches (≤20 total questions) | Answers saved to `docs/.planner-state.md` |
| 2 | Play back and confirm all requirements | — |
| 3 | Write the PRD with requirement IDs | `docs/prd.md` |
| 4 | **You review and approve the PRD** | — |
| 5 | Write the phase-by-phase plan | `docs/plan/overview.md` + phase files |
| 6 | (Learning mode) Write learning curriculum | `learnings/topics.md` + learning plan |
| 7 | Final consistency check | — |

For full workflow details and templates, see **[SKILL.md](./SKILL.md)**.

## The Interview Discipline

The planner asks strategically — only what it can't infer from your codebase or what you've already stated. The budget is tight: 20 questions maximum, 4–6 per turn. No padding, no generic questions.

---

**Start here:** Load the skill when you have an idea or rough notes and want to turn them into a solid, buildable plan.
