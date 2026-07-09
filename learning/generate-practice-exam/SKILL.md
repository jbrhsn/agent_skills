---
name: generate-practice-exam
description: Use when the user asks to generate a practice exam, mock test, question bank, or set of quiz questions for a topic or certification. Builds blueprint-weighted mock exams or targeted-drill question sets grounded strictly in already-authored chapter content, with per-option answer rationale. Do NOT use to author chapter notes (that is author-chapter) or to scaffold a repo (that is create-learning-repo).
---

# Generate Practice Exam

This skill generates exam-style question sets from a learning repository's **already-authored** content — either a full mock exam weighted to a certification blueprint, or a targeted drill focused on one objective or weak area.

It is **fully generic** — no topic, tool, vendor, or blueprint is hardcoded. Question count, domain weightings, format mix, and pass threshold are all inputs, not assumptions.

**Content-only grounding (hard rule):** questions are generated *only* from content that has already been authored (chapters, notes, definitions, pitfalls). This skill does **not** invent subject matter from training data or from raw objectives. If the source material is missing or still in stub form, it stops and asks the user to author the content first (with `author-chapter`) before generating an exam. This keeps every question and every distractor traceable to material the learner has actually studied.

The workflow runs in **five confirmed phases**. Every phase except the final write ends with an explicit gate.

**What this skill does:**
- Reads authored chapters and extracts concepts, definitions, and real misconceptions
- Allocates questions across domains by blueprint weighting
- Writes questions with plausible, content-grounded distractors and per-option rationale
- Runs a quality gate, then writes a mock-exam or drill file (idempotent naming)

**What this skill does NOT do:**
- Author or edit chapter content (use `author-chapter`)
- Generate questions from stubs, empty files, or raw objective lists alone
- Scaffold repos or templates (use `create-learning-repo`)

---

## When to use this skill

Trigger on requests like:
- "generate a practice exam / mock test for [topic or cert]"
- "make a question bank from these chapters"
- "quiz me on [module]" when the user wants a written set (for interactive back-and-forth, that is a different need)
- "build a drill for [weak area]"

Do **not** trigger for scaffolding, chapter authoring, or when no authored content exists yet.

---

## Phase 0 — Intake

Collect the following in a single message. Do not proceed until answered (optional items may be skipped explicitly).

```
To generate the right exam, I need a few details:

1. Source material
   Which repo, folder, chapters, or modules should the questions be drawn from?
   (I only generate questions from content that is already written.)

2. Mode
   a) Full mock exam  — weighted to a certification blueprint, timed
   b) Targeted drill  — focused on one objective / module / weak area

3. Question count
   How many questions total?

4. Format mix
   Single-choice vs multi-select ratio (default: ~20% multi-select, min 1 per domain).

5. Difficulty emphasis
   Recall / application / analysis balance (default: 20% / 40% / 40%).

6. Blueprint weighting (mode a only)
   Domain names + percentages if a certification exists.
   Leave blank and I will fetch the official blueprint, or fall back to even weighting.

7. Answer style
   a) Inline <details> per question (study-friendly)   ← default for drills
   b) Separate answer key at the end (exam-realistic)  ← default for full mocks
```

### Standalone-folder confirmation
Determine whether the source is a structured learning repo or a loose Markdown folder:
- **Structured repo** (`AGENTS.md` + `templates/` found by walking up from the source path): use its conventions (answer format, naming, objective wording).
- **Loose Markdown folder** (no repo markers): tell the user "This looks like a loose Markdown folder rather than a structured learning repo. I'll generate questions from the Markdown files you point me to, using my built-in exam format. Proceed?" — continue only after confirmation.

### End of Phase 0

> **Phase 0 complete.** I have the scope, mode, question count, format preferences, and answer style.
> Reply **"proceed"** to inspect the source content and confirm readiness, or adjust any settings first.

---

## Phase 1 — Source ingestion and readiness check

**Goal:** confirm there is enough authored content to ground an exam, and extract the raw material for questions. **Read-only.**

### Step 1 — Content-readiness gate (hard stop)
For each chapter/file in scope, classify it:
- **Authored** — has real content (Key Concepts, definitions, prose).
- **Stub / thin** — a stub marker, only an H1, or too little to question.

**Decision:**
- If **all** in-scope files are stubs/thin, or the requested question count cannot be supported by the authored material, **stop** and report:

  > "I can only generate questions from content that is already authored. The following in-scope files are still stubs or too thin: [list]. Please author them first (the `author-chapter` skill does this), then re-run this skill. I can proceed now with a smaller exam drawn only from the authored files [list] if you prefer — say the word."

- If **enough** content exists, continue.

### Step 2 — Extract question material
From each authored file, pull:
- **Key Concepts** → sources of stems (application/analysis questions)
- **Key Definitions** → sources of recall questions
- **Common Pitfalls & Misconceptions** → **primary source of distractors** (the wrong intuitions listed here become the plausible wrong answers)
- **Worked Examples** → sources of scenario-based application questions
- **Existing Self-Check / sample questions** → note them to **avoid duplication**

### Step 3 — Blueprint confirmation (full-mock mode)
- If the user gave domain weights, use them.
- If a certification exists and weights were not given, `webfetch` the official blueprint; record URL + retrieval date; quote domain names verbatim.
- If no blueprint exists, use even weighting across the in-scope modules and say so.

### Step 4 — Present the allocation and gate
Show a domain → question allocation table and the readiness result:

```
## Exam Plan — [name]

Mode: [full mock | targeted drill]
Total questions: [N]   Multi-select: [N]   Answer style: [inline | key]

Content readiness: [N] authored files in scope, [N] stubs excluded

| Domain / Module | Weight | Questions | Source files |
|---|---|---|---|
| [Domain A] | 30% | 14 | [files] |
| [Domain B] | 22% | 10 | [files] |
| ...        |     |    |         |
| Total      | 100%| N  |         |
```

### End of Phase 1

> **Phase 1 complete.** Content is sufficient and the allocation is above.
> Reply **"proceed"** to generate questions, or adjust scope/weighting first.

---

## Phase 2 — Question generation

**Goal:** write every question grounded in the extracted material, using `reference/question-item-template.md` for each item.

### Allocation math
- Questions per domain = `round(weight% × N)`; reconcile rounding so the total equals exactly N (adjust the largest-remainder domain).
- Within each domain, enforce the difficulty emphasis (recall/application/analysis) and place at least one multi-select per domain (or at least one overall for a small drill).

### Item construction rules
Each question uses the item template and obeys:
- **Grounded stem:** every question traces to a specific authored concept, definition, worked example, or pitfall. Do not introduce facts absent from the source content.
- **Scenario-first for application/analysis:** frame the stem as a realistic situation requiring a decision, mirroring exam style — not a bare definition lookup (except recall questions).
- **Plausible distractors:** wrong options must be believable misconceptions, drawn from the chapter's Pitfalls section wherever possible. No throwaway options; no "all of the above" / "none of the above" filler.
- **Per-option rationale:** the answer explains why the correct option is right AND why each significant distractor is wrong. For multi-select, explain why both correct answers qualify AND why the most tempting wrong answer fails. One-word rationales are non-compliant.
- **Multi-select phrasing:** use "Which TWO..." / "Which THREE..." and provide 5 options.
- **No duplication:** do not restate an existing Self-Check question verbatim; vary the angle.

### Traceability
For each question, keep an internal note of the source file/section it came from — used in drill mode for the "review this" pointer and in the quality gate for coverage checking.

### End of Phase 2

> **Phase 2 complete.** All [N] questions are listed above.
> Review the stems, options, and rationale for correctness and coverage.
> Reply **"proceed"** to assemble the final exam file, or request revisions first.

---

## Phase 3 — Assembly

**Goal:** build the exam file from `reference/exam-file-template.md`.

### Full-mock mode
- Header: title, instructions, question count, time limit (if given), passing threshold (if given).
- Domain-weighting table (from Phase 1).
- Questions in blocks, optionally grouped or shuffled across domains.
- **Answer key + self-score sheet at the end** (default for full mocks): correct answers, per-option rationale, and a score-to-pass calculation.

### Targeted-drill mode
- Lighter header (no timing).
- **Inline `<details>` answer per question** (default for drills).
- Each question ends with a "Review if missed:" pointer to the source chapter (relative path), so a wrong answer routes the learner back to the exact material.

### Convention matching
- Match the source repo's answer-format convention where one exists; otherwise use the mode default.
- Use relative paths for any links back into the repo.

---

## Phase 4 — Quality gate and write

**Goal:** self-audit, then write.

Produce a pass/fail table:

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

### Write
- **Idempotent naming:** write to the repo's practice-exam location (or the user's path) as `mock-exam-01.md`, `mock-exam-02.md`, ... or `drill-[topic]-01.md`, incrementing to avoid overwriting an existing file.
- Report:

```
Generated:     [path]
Mode:          [full mock | targeted drill]
Questions:     [N] ([N] multi-select)
Domains:       [N] (weighted per blueprint | even | drill-focused)
Answer style:  [inline <details> | separate key]
Source files:  [N] authored files
Quality gate:  PASS (all checks ✓)
```

---

## Constraints and Guardrails

- **Content-only grounding is non-negotiable.** Never generate questions from stubs, empty files, training data, or raw objectives alone. If content is missing, stop and ask the user to author it first.
- **Every question and distractor traces to authored material.** Distractors should be real misconceptions from the source (Pitfalls section preferred).
- **One phase per response.** Every phase except the final write ends with a gate.
- **Blueprint weights are inputs.** Fetch and cite them if a cert exists and the user did not supply them; fall back to even weighting and say so.
- **The quality gate is mandatory.** An exam is not "done" until every gate row is ✓.
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
