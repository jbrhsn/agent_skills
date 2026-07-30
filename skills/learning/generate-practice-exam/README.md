# generate-practice-exam

Generates exam-style question sets from a learning repository's already-authored content. Produces either a full blueprint-weighted mock exam or a targeted drill focused on a specific objective or weak area. Every question and distractor traces to authored chapter material — no questions are invented from training data.

---

## Trigger phrases

| Input | Example |
|---|---|
| Full mock exam | "generate a practice exam for [cert]", "make a mock test from these chapters" |
| Targeted drill | "build a drill on [module/topic]", "quiz me on [weak area]" |
| Question bank | "make a question bank from chapters 1–3" |

Do **not** trigger this skill to author chapter content (use `author-chapter`) or to scaffold a repo (use `create-learning-repo`). Do **not** trigger when no authored content exists yet — the skill will stop and ask you to author content first.

---

## What it does

The workflow is a sequence of six discrete **units**. Each unit is a self-contained piece of work with a **Goal/scope**, **Inputs**, **Do** steps, a **Self-verify** step, and a terse **Report contract** — the shape an orchestrator can delegate to an executor. Units that need a human/orchestrator decision end at a labeled **STOP GATE (hand back)**; do not proceed past a gate without confirmation. Shared rules (intake fields, grounding rule, allocation math, item construction, mode differences, quality-gate checklist, output format) are defined once in a **Shared reference** section the units point to, rather than restated per unit.

| Unit | What happens | Gate |
|---|---|---|
| **U1 — Intake & mode selection** | Collects source scope, mode (mock/drill), question count, format mix, difficulty emphasis, blueprint weighting, answer style; determines repo vs loose folder | STOP GATE: confirm scope/mode before reading content |
| **U2 — Source ingestion & readiness gate** | Classifies every in-scope file as authored or stub/thin; extracts concepts, definitions, pitfalls, worked examples as raw question material (read-only) | STOP GATE only if readiness fails: stop and ask to author content or reduce scope |
| **U3 — Blueprint weighting & allocation** | Uses supplied weights, fetches the official blueprint, or falls back to even weighting; runs allocation math; presents the domain → question table | STOP GATE: confirm allocation before generating |
| **U4 — Question generation** | Writes every question from the extracted material using the item template; **Self-verify enforces that every question traces to authored content (flag, never fabricate) and that per-option rationale is present** | STOP GATE: review questions before assembly |
| **U5 — Assembly** | Builds the exam file from the layout template (header, domain blocks, answer key or inline `<details>` + review pointers) | — |
| **U6 — Quality gate + write** | Self-audits against the pass/fail checklist; fixes any failures; writes the file with idempotent naming | — |

---

## Content-only grounding (hard rule)

Questions are generated **only** from content that is already authored. The skill never invents subject matter from training data or raw objective lists. If in-scope files are stubs or too thin:

> "I can only generate questions from content that is already authored. The following files are still stubs: [list]. Please author them first (the `author-chapter` skill does this), then re-run. I can proceed now with a smaller exam drawn only from the authored files [list] — say the word."

---

## Exam modes

**Full mock exam:**
- Weighted to a certification blueprint (fetched live if not supplied)
- Domain allocation table showing question count per domain
- Separate answer key at the end (default) — exam-realistic
- Header with question count, time limit, passing threshold

**Targeted drill:**
- Focused on one module, objective, or weak area
- Inline `<details>` answer per question (default) — study-friendly
- "Review if missed" pointer to the source chapter after each question

---

## Quality gate checks (U6)

| Check | Type |
|---|---|
| Per-domain question counts match the allocation | Count |
| Total question count equals requested N | Count |
| Every question traces to authored source content | Qualitative |
| ≥1 multi-select per domain (or ≥1 overall for a small drill) | Deterministic |
| Difficulty emphasis matches the requested balance | Qualitative |
| Every answer explains correct + why each distractor fails | Qualitative |
| No "all/none of the above" filler options | Deterministic |
| No duplicate stems (incl. vs existing Self-Check questions) | Deterministic |
| Distractors are plausible misconceptions (pitfall-sourced where possible) | Qualitative |
| Drill mode: every question has a "Review if missed" pointer | Deterministic |
| Any fetched blueprint link is verified + dated | Deterministic |

---

## Inputs (U1)

| Question | Required | Notes |
|---|---|---|
| Source material (repo, folder, chapters, modules) | Yes | Must be already-authored |
| Mode (full mock or targeted drill) | Yes | |
| Question count | Yes | |
| Format mix (single-choice vs multi-select ratio) | Optional | Default: ~20% multi-select, min 1 per domain |
| Difficulty emphasis | Optional | Default: 20% recall / 40% application / 40% analysis |
| Blueprint domain weights (mock mode) | Optional | Fetched live from official source if not provided |
| Answer style | Optional | Default: inline `<details>` for drills, separate key for mocks |

---

## Outputs

A single exam file at the target path (or the repo's practice-exam location):
- `mock-exam-01.md`, `mock-exam-02.md`, ... (full mock)
- `drill-[topic]-01.md`, `drill-[topic]-02.md`, ... (targeted drill)

Naming is idempotent — the skill increments the number rather than overwriting an existing file.

Completion report:

```
Generated:     path/to/exam-file.md
Mode:          full mock  (or targeted drill)
Questions:     N (N multi-select)
Domains:       N (weighted per blueprint | even | drill-focused)
Answer style:  inline <details>  (or separate key)
Source files:  N authored files
Quality gate:  PASS (all checks ✓)
```

---

## Limitations

- **Authored content required.** The skill cannot generate questions from stubs, empty files, or raw objective lists alone.
- **Blueprint accuracy.** Fetched blueprints reflect the certification at fetch time. Re-fetch before final exam prep if significant time has passed.
- **No chapter authoring.** The skill only reads content — use `author-chapter` to write missing chapters.
- **Question variety bounded by source depth.** Thin source material (few concepts, no worked examples, no pitfalls section) produces lower-quality distractors and limited difficulty range.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global — available in all projects (Linux/macOS)
cp -r learning/generate-practice-exam ~/.config/opencode/skills/

# Per-project only
cp -r learning/generate-practice-exam .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse learning\generate-practice-exam "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/generate-practice-exam.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content plus the source chapters as your first message |

---

## Companion skills

- **`create-learning-repo`** — scaffolds the repo structure and stubs
- **`author-chapter`** — writes the chapter content that this skill draws questions from
