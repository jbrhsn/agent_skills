---
name: generate-practice-exam
description: Use when the user asks to generate a practice exam, mock test, question bank, or set of quiz questions for a topic or certification. It builds either a blueprint-weighted full mock exam or a targeted-drill question set, grounded strictly in already-authored chapter content, with per-option answer rationale, and stops rather than inventing subject matter when the source is missing or still in stub form. Do NOT use to author chapter notes (that is author-chapter) or to scaffold a repo (that is create-learning-repo).
---

# Generate Practice Exam

Generate exam-style question sets from a learning repository's **already-authored** content — either a full mock exam weighted to a certification blueprint, or a targeted drill focused on one objective or weak area.

It is **fully generic** — no topic, tool, vendor, or blueprint is hardcoded. Question count, domain weightings, format mix, and pass threshold are all inputs, not assumptions.

**Content-only grounding (hard rule):** questions are generated *only* from content that has already been authored (chapters, notes, definitions, pitfalls). This skill does **not** invent subject matter from training data or from raw objectives. If the source material is missing or still in stub form, it stops and asks the user to author the content first (with `author-chapter`) before generating an exam. This keeps every question and every distractor traceable to material the learner has actually studied.

**What this skill does:**
- Reads authored chapters and extracts concepts, definitions, and real misconceptions
- Allocates questions across domains by blueprint weighting
- Writes questions with plausible, content-grounded distractors and per-option rationale
- Runs a quality gate, then writes a mock-exam or drill file (idempotent naming)

**What this skill does NOT do:**
- Author or edit chapter content (use `author-chapter`)
- Generate questions from stubs, empty files, or raw objective lists alone
- Scaffold repos or templates (use `create-learning-repo`)

## When to use this skill

Trigger on requests like:
- "generate a practice exam / mock test for [topic or cert]"
- "make a question bank from these chapters"
- "quiz me on [module]" when the user wants a written set (for interactive back-and-forth, that is a different need)
- "build a drill for [weak area]"

Do **not** trigger for scaffolding, chapter authoring, or when no authored content exists yet.

## How the workflow is structured

The workflow is a sequence of discrete **units**. Each unit is a self-contained piece of work with a **Goal/scope**, **Inputs**, **Do** steps, a **Self-verify** step, and a terse **Report contract**. Units that require a human/orchestrator decision end at a labeled **STOP GATE (hand back)** — do not proceed past a gate on your own. Units are dependent and run in order (U1 → U6); the content-only grounding gate in U2 can terminate the workflow early.

Shared rules, allocation math, mode differences, quality-gate checklist, and output format are defined **once** in the "Shared reference" section below and referenced by the units — they are not restated per unit.

---

## Shared reference (defined once, referenced by units)

### Intake fields
The information every run needs before any work begins:

```
1. Source material — which repo, folder, chapters, or modules the questions
   are drawn from. (Questions come ONLY from content already written.)
2. Mode — (a) Full mock exam, weighted to a certification blueprint, timed
           (b) Targeted drill, focused on one objective / module / weak area
3. Question count — how many questions total.
4. Format mix — single-choice vs multi-select ratio
   (default: ~20% multi-select, min 1 per domain).
5. Difficulty emphasis — recall / application / analysis balance
   (default: 20% / 40% / 40%).
6. Blueprint weighting (mode a only) — domain names + percentages if a cert
   exists. Blank → fetch the official blueprint, or fall back to even weighting.
7. Answer style — (a) inline <details> per question (study-friendly; default for drills)
                  (b) separate answer key at the end (exam-realistic; default for mocks)
```

### Source-type determination
- **Structured repo** (`AGENTS.md` + `templates/` found by walking up from the source path): use its conventions (answer format, naming, objective wording).
- **Loose Markdown folder** (no repo markers): generate questions from the pointed-at Markdown files using the built-in exam format — but confirm this with the user first (see U1 STOP GATE).

### Content-only grounding rule (non-negotiable)
Never generate questions from stubs, empty files, training data, or raw objectives alone. Every question **and** every distractor must trace to authored material. Distractors should be real misconceptions from the source (Pitfalls section preferred). If any question cannot be grounded in authored content, that is a **flag to surface, not license to fabricate**.

### Allocation math
- Questions per domain = `round(weight% × N)`; reconcile rounding so the total equals exactly N (adjust the largest-remainder domain).
- Within each domain, enforce the difficulty emphasis (recall/application/analysis) and place at least one multi-select per domain (or at least one overall for a small drill).

### Item construction rules
Each question uses `reference/question-item-template.md` and obeys:
- **Grounded stem:** every question traces to a specific authored concept, definition, worked example, or pitfall. Introduce no facts absent from the source content.
- **Scenario-first for application/analysis:** frame the stem as a realistic situation requiring a decision, mirroring exam style — not a bare definition lookup (except recall questions).
- **Plausible distractors:** wrong options must be believable misconceptions, drawn from the chapter's Pitfalls section wherever possible. No throwaway options; no "all of the above" / "none of the above" filler.
- **Per-option rationale:** the answer explains why the correct option is right AND why each significant distractor is wrong. For multi-select, explain why both correct answers qualify AND why the most tempting wrong answer fails. One-word rationales are non-compliant.
- **Multi-select phrasing:** use "Which TWO..." / "Which THREE..." and provide 5 options.
- **No duplication:** do not restate an existing Self-Check question verbatim; vary the angle.
- **Traceability note:** for each question, keep an internal note of the source file/section it came from — used in drill mode for the "Review if missed" pointer and in the quality gate for coverage checking.

### Mode differences (assembly)
Built from `reference/exam-file-template.md`.

**Full-mock mode:**
- Header: title, instructions, question count, time limit (if given), passing threshold (if given).
- Domain-weighting table (from U3).
- Questions in blocks, optionally grouped or shuffled across domains.
- **Answer key + self-score sheet at the end** (default): correct answers, per-option rationale, and a score-to-pass calculation.

**Targeted-drill mode:**
- Lighter header (no timing), no blueprint table.
- **Inline `<details>` answer per question** (default).
- Each question ends with a "Review if missed:" pointer to the source chapter (relative path), so a wrong answer routes the learner back to the exact material.

**Convention matching:** match the source repo's answer-format convention where one exists; otherwise use the mode default. Use relative paths for any links back into the repo.

### Quality-gate checklist
| Check | Result | Note |
|---|---|---|
| Per-domain question counts match the allocation | ✓ | |
| Total question count equals requested N | ✓ | |
| Every question traces to authored source content | ✓ | |
| ≥1 multi-select per domain (or ≥1 overall for a small drill) | ✓ | |
| Difficulty emphasis matches the requested balance | ✓ | |
| Every answer explains correct + why each distractor fails | ✗ | Q7 rationale incomplete |
| No "all/none of the above" filler options | ✓ | |
| No duplicate stems (incl. vs existing Self-Check questions) | ✓ | |
| Distractors are plausible misconceptions (pitfall-sourced where possible) | ✓ | |
| Drill mode: every question has a "Review if missed" pointer | ✓ | |
| Any fetched blueprint link verified + dated | ✓ | |

**Rule:** any ✗ blocks completion. Fix and re-run the gate. Only write when every row is ✓.

Deterministic checks:
- Count questions per domain and compare to the allocation table.
- Count `<details>` blocks (drill) or answer-key entries (mock) and compare to the question count.
- Search for `Which TWO` / `Which THREE` to confirm the multi-select minimum.

### Idempotent write naming
Write to the repo's practice-exam location (or the user's path) as `mock-exam-01.md`, `mock-exam-02.md`, … or `drill-[topic]-01.md`, incrementing to avoid overwriting an existing file. Windows-safe: quote paths with spaces; do not assume forward slashes.

---

## Unit U1 — Intake & mode selection

- **Goal/scope**: collect all inputs and lock the mock-vs-drill mode and source type. No content is read or generated yet.
- **Inputs**: the user's request; any scope, mode, count, or format details already stated.
- **Do**:
  - Ask for any missing **Intake fields** (see Shared reference) in a single message. Do not proceed until answered; optional items may be skipped explicitly (defaults apply).
  - Run **Source-type determination** (see Shared reference) against the given source path.
- **Self-verify**: a single source scope is identified, a single mode (mock or drill) is chosen, question count is set, and the answer style is resolved (explicit or defaulted).
- **STOP GATE (hand back)**: present the resolved scope, mode, question count, format preferences, and answer style — and, if the source is a **loose Markdown folder**, state that explicitly and ask to proceed with the built-in exam format. **Stop and confirm before reading source content.** → Hand control back to the user/orchestrator for the mode/scope decision.
- **Report contract**: `intake locked | mode: <mock|drill> | source: <scope> (<repo|loose folder>) | count: <N> | answer style: <inline|key> | awaiting: scope/mode confirmation`.

## Unit U2 — Source ingestion & readiness gate

- **Goal/scope**: confirm there is enough authored content to ground the exam, and extract the raw question material. **Read-only.**
- **Inputs**: confirmed scope + mode from U1.
- **Do**:
  - For each chapter/file in scope, classify it: **Authored** (real content — Key Concepts, definitions, prose) or **Stub/thin** (a stub marker, only an H1, or too little to question).
  - From each authored file, extract: **Key Concepts** → application/analysis stems; **Key Definitions** → recall questions; **Common Pitfalls & Misconceptions** → **primary source of distractors**; **Worked Examples** → scenario-based application stems; **existing Self-Check / sample questions** → note to avoid duplication.
- **Self-verify**: apply the **Content-only grounding rule** (see Shared reference). If **all** in-scope files are stubs/thin, or the requested question count cannot be supported by the authored material, this unit must **stop** rather than continue.
- **STOP GATE (hand back)** — *only when the readiness check fails*: report the shortfall and stop:

  > "I can only generate questions from content that is already authored. The following in-scope files are still stubs or too thin: [list]. Please author them first (the `author-chapter` skill does this), then re-run this skill. I can proceed now with a smaller exam drawn only from the authored files [list] if you prefer — say the word."

  → Hand control back for authoring or a reduced-scope decision. If readiness passes, no gate — continue to U3.
- **Report contract**: `readiness: <PASS: N authored / N stub excluded | FAIL: insufficient authored content> | material extracted: concepts/defs/pitfalls/examples | awaiting: <nothing, proceeding | author-or-reduce decision>`.

## Unit U3 — Blueprint weighting & allocation

- **Goal/scope**: fix the domain → question allocation the generation unit will fill.
- **Inputs**: extracted material from U2; mode; user-supplied domain weights if any.
- **Do**:
  - **Blueprint (full-mock mode):** if the user gave domain weights, use them. If a certification exists and weights were not given, `webfetch` the official blueprint; record URL + retrieval date; quote domain names verbatim. If no blueprint exists, use even weighting across in-scope modules and say so. (Drill mode: allocate by the focused objective/module instead.)
  - Apply the **Allocation math** (see Shared reference) to produce a domain → question table.
  - Present the exam plan and allocation:

  ```
  ## Exam Plan — [name]

  Mode: [full mock | targeted drill]
  Total questions: [N]   Multi-select: [N]   Answer style: [inline | key]
  Content readiness: [N] authored files in scope, [N] stubs excluded

  | Domain / Module | Weight | Questions | Source files |
  |---|---|---|---|
  | [Domain A] | 30% | 14 | [files] |
  | [Domain B] | 22% | 10 | [files] |
  | Total      | 100%| N  |         |
  ```
- **Self-verify**: per-domain question counts sum to exactly N; each domain maps to at least one authored source file; any fetched blueprint has a recorded URL + date.
- **STOP GATE (hand back)**: present the allocation table and **stop to confirm** before generating questions. → Hand control back for allocation/weighting approval.
- **Report contract**: `allocation: N questions across M domains (sums to N) | blueprint: <user-supplied | fetched+dated | even | drill-focused> | awaiting: allocation approval`.

## Unit U4 — Question generation & draft write

- **Goal/scope**: write every question grounded strictly in the extracted material, with per-option rationale, then **write them to the exam file as this run's draft under review** — do not present all questions inline in chat.
- **Inputs**: approved allocation from U3; extracted material from U2; `reference/question-item-template.md`.
- **Do**:
  - Generate each question per the **Item construction rules** and **Allocation math** (see Shared reference): grounded scenario-first stems, pitfall-sourced plausible distractors, per-option rationale, correct multi-select phrasing, no duplication, difficulty emphasis and multi-select minimum enforced.
  - Record the source file/section for every question (traceability note).
  - **Write the questions to the exam file** using the **Idempotent write naming** rule — pick the next non-colliding filename **now** (`mock-exam-NN.md` / `drill-[topic]-NN.md`). **This chosen filename is this run's file**: it is the draft under review here, and U5/U6 will update/finalize this **same** file in place (they do not create a new incremented file each round).
- **Self-verify** (this is the doer's own verification of the grounding + rationale constraints):
  - **Grounding:** every question traces to a specific authored concept/definition/example/pitfall from U2's extraction — confirm each has its recorded source note. **If any question cannot be traced to authored content, do NOT fabricate it — flag it and reduce/reroute** (surface to the user; drop or replace only from grounded material).
  - **Per-option rationale:** every question's answer explains why the correct option is right AND why each significant distractor is wrong (both correct options + the tempting wrong one for multi-select). No one-word rationales.
  - Also confirm: counts per domain match the allocation; difficulty emphasis met; ≥1 multi-select per domain (or ≥1 overall for a small drill); no duplicate/verbatim Self-Check stems.
- **STOP GATE (hand back)**: present ONLY a short summary **plus the draft file path**, and **stop for review** before assembly — **do NOT paste all the questions into chat; point the user to the written draft file to review.** The summary states: N questions generated (M multi-select), per-domain counts matching the allocation, grounding result (all traceable, or K flagged + surfaced), and per-option rationale present (or K fixed). Ask the user to review the draft and request any revisions. **On a revision request, re-edit the same draft file in place and re-point to it** (do not create a new file). → Hand control back for question review/revisions.
- **Report contract**: `draft written to <path>, awaiting review | generated: N questions (M multi-select) | per-domain: matches allocation | grounding: all traceable to authored content <or: K flagged, surfaced> | per-option rationale: present on all <or: K incomplete, fixed> | awaiting: question review (see draft file — questions not pasted in chat)`.

## Unit U5 — Assembly

- **Goal/scope**: assemble the **already-written draft file** (from U4) into the correct layout for the confirmed mode — updating that same file in place, not producing a new one.
- **Inputs**: the reviewed draft file written in U4 (this run's `<path>`); mode; answer style; `reference/exam-file-template.md`.
- **Do**: rewrite/update the draft file per the **Mode differences** (see Shared reference) — full-mock (header + blueprint table + question blocks + answer key & self-score) or targeted-drill (light header + inline `<details>` answers + "Review if missed" pointers). Match the repo's answer-format convention where one exists; use relative paths for links back into the repo. **Edit U4's draft file in place — do not create a new incremented file.**
- **Self-verify**: the file structure matches the selected mode; every question is present; drill answers each carry a relative-path "Review if missed" pointer; full-mock answer-key entries cover every question with per-option rationale.
- **Report contract**: `assembled in place: <path> | layout: <full-mock|drill> | questions: N | answers: <answer key | inline details> | review pointers: <n/a | present on all>`.

## Unit U6 — Quality gate & finalize

- **Goal/scope**: self-audit the written file against the full checklist, then finalize. This is the mandatory final verification. The file already exists (written at U4, assembled at U5) — U6 confirms it passes and reports; it does **not** create a duplicate or a new incremented file.
- **Inputs**: the assembled exam file from U5 (this run's `<path>`).
- **Do**: fill in the **Quality-gate checklist** (see Shared reference), running the deterministic checks against the written file. **Any ✗ blocks completion — fix it in the file and re-run the gate in place.** Only when **every row is ✓**, finalize the file (it is already at `<path>` from U4 — do not write a new incremented file) and report:

  ```
  Finalized:     [path]
  Mode:          [full mock | targeted drill]
  Questions:     [N] ([N] multi-select)
  Domains:       [N] (weighted per blueprint | even | drill-focused)
  Answer style:  [inline <details> | separate key]
  Source files:  [N] authored files
  Quality gate:  PASS (all checks ✓)
  ```
- **Self-verify**: confirm every checklist row is ✓ before finalizing; confirm the finalized file is the same `<path>` chosen at U4 (no duplicate created) and that the U4 idempotent-naming step did not overwrite a pre-existing file (number was incremented).
- **Report contract**: `finalized: <exact path> (same file as U4 draft) | mode: <mock|drill> | questions: N | quality gate: PASS (all ✓) | overwrite: none (incremented at U4)`.

---

## Constraints and Guardrails

- **Content-only grounding is non-negotiable.** Never generate questions from stubs, empty files, training data, or raw objectives alone. If content is missing, stop at U2's gate and ask the user to author it first. If a single question cannot be grounded, flag it in U4's self-verify — never fabricate.
- **Every question and distractor traces to authored material.** Distractors should be real misconceptions from the source (Pitfalls section preferred).
- **Units run in order and gates are respected.** Do not proceed past a labeled STOP GATE without the required confirmation.
- **Blueprint weights are inputs.** Fetch and cite them if a cert exists and the user did not supply them; fall back to even weighting and say so.
- **The quality gate is mandatory.** An exam is not "done" until every gate row is ✓ (U6).
- **Idempotent writes.** Never overwrite an existing exam file — increment the number.
- **Answer rationales cover all options** — one-word rationales are non-compliant.
- **Windows-safe:** quote paths with spaces; do not assume forward slashes.

---

## Portability — Using This Skill on Other Platforms

This skill is written in the `SKILL.md` format for OpenCode. The workflow and rules are platform-agnostic.

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/generate-practice-exam.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full content (below frontmatter) plus the source chapters as your first message |

**To install for all projects (OpenCode):**
```bash
# macOS / Linux
cp -r generate-practice-exam ~/.config/opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse generate-practice-exam "$env:USERPROFILE\.config\opencode\skills\"
```
