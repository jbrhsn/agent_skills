# Project Planner

Turn a rough idea into a detailed, validated project plan — no guessing, no wasted effort.
Every requirement, every screen state, and every test case comes from answers you actually
gave and explicitly confirmed, not assumptions the planner filled in.

Built for agentic coding harnesses (opencode, Claude Code, and similar). The documents it
produces are the context an agent needs so it stops inventing UI and stops shipping code
nobody defined a way to check.

## When to use it

Before you start building, when you have a project idea but haven't nailed down the
details yet.

**Practical triggers:**
- You have a project idea and don't know where to start
- You're about to start feature work but the scope isn't clear
- You want the UI defined before an agent invents one for you
- You want to learn a new language or framework by building something real
- A repo has no planning docs and you want to add them

## What you'll get

- **`docs/prd.md`** — functional and non-functional requirements with stable IDs
  (`FR-01`, `NFR-01`), out-of-scope items, and open questions (never assumptions)
- **`docs/uiux.md`** — every screen, component, and state, with what triggers each
  transition; or for CLI/chatbot projects, every command, response, and session state;
  or for headless projects, a short interaction contract
- **`docs/plan/`** — a phase-by-phase implementation plan:
  - `overview.md` — phases, sequence, dependencies, requirement coverage, surface coverage
  - `phase-01-*.md`, … — one file per phase, with units (atomic buildable chunks), each
    carrying its own test cases, and phase exit testing at the end
  - `final-test-pass.md` — a full-system test sweep to run once everything is built
- **`learnings/`** (optional) — a curriculum sequenced against the build, covering the
  language, the interface work, and the testing

## What changed in v2

Three things, in response to the two ways v1 plans went wrong in agentic builds:

**1. A UI/UX stage between the PRD and the plan.** An agent given "a user can retry a
failed import" and nothing else will invent a screen, invent its states, and invent
different ones next session. `docs/uiux.md` closes that gap — every component's states are
written down before any unit references them. It adapts to the surface: screens and
components for web/mobile/desktop, commands and session state for CLI/chatbot, an
interaction contract for headless projects.

**2. Testing planned with the work, not after it.** Every unit carries a 3–7 row test
case table derived from the requirement's Verify lines and the UIUX doc's states — steps,
expected result, and whether it's automatable. Every phase ends with integration checks
drawn from the UIUX flows plus regression on earlier phases. When all phases exist, a
final full-system pass is generated automatically.

**3. Two approval gates instead of one.** The PRD gets signed off, then the UIUX doc gets
signed off, and only then does the plan get written. Building a plan against an
unapproved interface spec means redoing units.

## Key principles

- **Interview first, write second** — you answer structured questions; the planner
  *confirms* every answer before writing anything down
- **No invented requirements** — anything unanswered goes to Open Questions, never into
  the spec as a guess. The same rule now covers screens and states.
- **Documents only** — Markdown under `docs/`, never source code, never wireframes,
  never test scripts. The planner names the test; the build session writes it.
- **Explicit approval gates** — PRD, then UIUX, then the plan
- **Traceability end to end** — `FR-03` → `CMP-05` → `P2-U2` → `T-P2U2-3` → the final
  test pass. Nothing in the chain is orphaned, and the quality gates check it.

## Stage map

| Stage | What happens | Output |
|---|---|---|
| 0 | Detect repo state, mode, and surface type | — |
| 1 | Interview in 4–6 question batches (≤20 total) | `docs/.planner-state.md` |
| 2 | Play back and confirm all requirements | — |
| 3 | Write the PRD | `docs/prd.md` |
| 4 | **You review and approve the PRD** | — |
| 5 | Short surface interview (≤10 questions) | — |
| 6 | Write the UI/UX spec | `docs/uiux.md` |
| 7 | **You review and approve the UI/UX spec** | — |
| 8 | Write the plan, with test cases inside each unit | `docs/plan/overview.md` + phase files |
| 9 | (Learning mode) Write the curriculum | `learnings/` |
| 10 | Compile the full-system test pass | `docs/plan/final-test-pass.md` |
| 11 | Final consistency check | — |

For full workflow details, see **[SKILL.md](./SKILL.md)**.

## Layout

```
SKILL.md                          lean entry point — stage map and boundaries
references/
  interview.md                    question bank, batching, state file
  prd-spec.md                     requirement IDs, Verify lines, section rules
  uiux-interview.md               surface questions per project type
  uiux-spec.md                    screen/component/state rules, all three surfaces
  plan-spec.md                    phase and unit decomposition, UIUX traceability
  execution-spec.md               bootstrap, regression guards, execution contracts
  testing-spec.md                 test case format, phase exit tests, final pass
  learning-mode.md                curriculum rules, three topic families
  quality-gates.md                pre-handoff checklist and anti-patterns
assets/
  prd.template.md
  uiux.template.md                three variants: visual, conversational, headless
  plan.template.md                overview + phase file
  final-test-pass.template.md
  topics.template.md
  learning-plan.template.md
```

References are read one stage at a time, not upfront — that's what keeps context small on
a long interview.

## The interview discipline

The planner asks strategically — only what it can't infer from your codebase or what
you've already stated. Two budgets: 20 questions for the main interview, 10 more for the
surface interview, 4–6 per turn. No padding, no generic questions.

---

**Start here:** load the skill when you have an idea or rough notes and want to turn them
into a plan an agent can build from without guessing.
