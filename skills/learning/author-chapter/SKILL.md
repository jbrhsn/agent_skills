---
name: author-chapter
description: Use when the user asks to populate, author, write, or fill in a chapter, notes file, or topic stub in a learning repository or a Markdown study folder. It locates the authoring contract on disk, researches live official sources with citations and retrieval dates, drafts every template section to spec, runs a mandatory quality gate as a self-audit, then writes one chapter file only after every check passes. Do NOT use to scaffold a new repo (that is create-learning-repo) or to generate quizzes/mock exams (that is generate-practice-exam).
---

# Author Chapter

This skill turns a blank stub (or a thin, incomplete file) into a fully template-compliant learning chapter. It researches live sources, writes every section to the repo's own standard, and runs an automated quality gate before finishing.

It is **fully generic** — no topic, tool, vendor, or repo path is hardcoded. The section order and quality rules are read from the target repo's own `templates/` and `AGENTS.md` at runtime. When those files do not exist (a loose Markdown folder), the skill falls back to the bundled `reference/quality-gate.md` after confirming with the user.

The workflow is a sequence of discrete **units**. Each unit has a Goal/scope, Inputs, Do, a Self-verify step, and a terse Report contract. Two units are **STOP GATES** where scope or a plan must be confirmed before proceeding. The quality gate (Unit U3) is the doer's own self-audit run against the contract before any file is written.

**What this skill does:**
- Reads the authoring contract (template + depth rules) from disk
- Researches the topic from live official sources, with citations and retrieval dates
- Drafts every section in the correct order to the required depth
- Runs a pass/fail quality gate and fixes failures before writing
- Writes one chapter file (idempotent — never clobbers authored content without confirmation)

**What this skill does NOT do:**
- Scaffold folders, templates, or new repos (use `create-learning-repo`)
- Generate standalone quizzes or mock exams (use `generate-practice-exam`)
- Author more than the file(s) the user explicitly names

---

## When to use this skill

Trigger on requests like:
- "populate this chapter / stub / notes file"
- "author the notes for [topic]"
- "fill in `path/to/notes.md`"
- "write the [chapter name] chapter following the template"

Do **not** trigger if the user wants to create a new repo, generate an exam/quiz, or edit non-learning content.

---

## Shared reference material (defined once — referenced by the units)

Every unit below points to this section instead of restating rules. Do not duplicate this material inside a unit.

### The authoring contract (source of truth)

The section order and depth rules come **from disk, not from this skill**. Resolve the contract in Unit U0 and reuse it in every later unit:

| Found at/above the target file | Contract used |
|---|---|
| `AGENTS.md` + `templates/` both present | Structured learning repo. Read both; they are authoritative. Derive section order and rules from them. |
| Neither present (loose Markdown folder) | After user confirmation only, fall back to the built-in `reference/quality-gate.md`. |
| Partial (one present) | Use whatever is present; fall back to `reference/quality-gate.md` for the missing piece; tell the user which contract applies. |

> **Never hardcode the section list.** When `templates/chapter-notes-template.md` exists, the section order and headings come from it. This is what keeps the skill portable across repos with different templates. The built-in fallback and its full section order live in `reference/quality-gate.md`.

### Section-by-section depth requirements (portable minimum)

Follow the Content Depth Rules from the repo's `AGENTS.md` (or `reference/quality-gate.md` in fallback mode). The following is the portable minimum every draft must meet:

- **TL;DR** — 2–4 sentences; end with a single bolded "one thing to remember."
- **ELI5** — 3–6 sentences, prose only, zero jargon. A concrete everyday analogy that maps *structurally* onto the concept, and explicitly corrects the most common misconception. A vague comparison ("think of X as a way to represent Y") is non-compliant.
- **Learning Objectives** — 3–5 checkboxed, testable, action-verb outcomes.
- **Visual Overview** (if the template includes it and the topic is visualisable) — 2–4 ASCII diagrams, each under its own `###` sub-header in a plain fenced block (no language tag). Use `──►` for flow and `│ ├ └ ─ ┌ ┐` for structure. Omit only for purely conceptual topics.
- **Key Concepts** — each sub-section answers three questions: (1) What is it? (2) How does it work under the hood? (3) Where does it appear in the tool/platform? Answering only (1) is non-compliant.
- **Key Parameters / Configuration Knobs** — required for any configurable component. Table `Parameter | What it controls | Decision rule`; the decision rule must be an actionable rule, not a restatement. If none exist, write "No configurable parameters for this topic."
- **Worked Example: Requirement → Decision** — one realistic scenario walked through Step 1 goal → Step 2 inputs → Step 3 outputs → Step 4 constraints → Step 5 approach + rationale vs alternatives. If there is no selection decision, use a failure-diagnosis walkthrough.
- **Implementation** — ≥2 snippets from different angles. Every snippet opens with a comment naming the real-world problem (`# Scenario: ...`). At least one is an anti-pattern (`# Anti-pattern:`) immediately followed by the corrected version and an explanation of what breaks.
- **Common Pitfalls & Misconceptions** — each bullet has three parts: bolded label + why beginners make the mistake + the correct mental model. Bare bullets are non-compliant.
- **Key Definitions** — `Term | Definition` table; precise scoped definitions, not dictionary entries.
- **Summary / Quick Recall** — 3–7 scannable one-line takeaways for a 60-second review.
- **Self-Check / Checkpoint Questions** — 5 questions: Q1 recall, Q2–Q3 application, Q4–Q5 analysis/trade-off. At least one multi-select ("Which TWO..."). Each answer in an inline `<details><summary>Answer</summary>` block immediately after its options, explaining why the correct answer is right AND why each significant distractor is wrong. One-word rationales are non-compliant. Do not add a separate flat "Answers" section unless the repo's template uses one.
- **Further Reading** — official-docs-only links, each with a verified date.

### Source hygiene (applies to all research and links)

- Only official documentation counts as a citable source — no third-party blogs, Medium, or YouTube.
- Format every link as `[Title](url) — *verified YYYY-MM-DD*`, verified live this session.
- Quote exam objectives **verbatim** — never paraphrase them.
- Flag any fast-evolving feature inline with a note to re-verify before relying on it.

### Draft discipline

- Match the repo's naming style (ALLCAPS-underscore vs lowercase-hyphen) and answer-format convention (inline `<details>` vs separate key) detected in Unit U0.
- Leave zero `<!-- TODO -->` or `STUB` markers.
- Depth calibration: Key Concepts + ELI5 + Worked Example carry the teaching load (~75% of effort); snippets ~15%; questions ~10% but non-negotiable.

### Constraints and guardrails (non-negotiable, all units)

- **Contract comes from disk, not this skill.** When the repo has `templates/` + `AGENTS.md`, they win. The built-in `reference/quality-gate.md` is a fallback for loose folders only, and its use must be confirmed with the user.
- **Never overwrite authored content without explicit confirmation.** Only populate stubs freely.
- **Always research live in Unit U1.** Cite URL + retrieval date. Official docs only.
- **The quality gate (Unit U3) is mandatory.** A chapter is not "done" until every gate row is ✓.
- **Author only what the user named.** Do not batch-populate a module unless explicitly asked.
- **Windows-safe:** quote paths with spaces; do not assume forward slashes.

---

## Workflow

The units run in order U0 → U4. Two of them are STOP GATES that hand control back for confirmation; the rest are self-verified by the doer. Do not skip the STOP GATES and do not combine a gate with the next unit in one response.

### Unit U0 — Locate the authoring contract & confirm scope

- **Goal/scope**: find the rules this chapter must follow and lock the exact target file, before writing anything.
- **Inputs**: the file path or chapter/topic name the user named.
- **Do**:
  - **Identify the target.** Confirm the exact file path. If the user named a chapter/topic but not a file, list the candidate stub(s) and ask which one. Read the target and classify it:
    - **Stub** — a single comment line (e.g. `<!-- stub: ... -->`), a `> **Status:** STUB` marker, or only an H1 title. Safe to populate.
    - **Has real content** — anything more. Do not overwrite silently (see STOP GATE below).
  - **Find the contract by walking up the tree.** From the target file's directory, walk toward the filesystem root looking for `AGENTS.md` (Content Depth Rules, naming style, answer format), `templates/chapter-notes-template.md` (or the repo's equivalent topic-note template), and `templates/authoring-guidelines.md` (the quality rubric). Resolve which contract applies using the **authoring contract** table in shared reference material.
  - **Gather chapter context.** Read the parent section/module index (if present) for the chapter's declared exam objective, topic scope, and estimated time. Read 1–2 already-authored sibling chapters (if any) to match voice, depth, and formatting. Note naming style and answer format so the draft matches.
- **Self-verify**: a single target file is selected and classified; the contract source is resolved (repo `templates/`+`AGENTS.md`, partial, or built-in fallback); naming style and answer format are noted.
- **STOP GATE (hand back)**: present target file, contract source, and topic/objective, and **stop to confirm** before research. Two cases force this gate: (a) the target **has real content** — ask whether to rewrite, extend, or leave it; never overwrite authored content silently; (b) the folder is loose (no `AGENTS.md`/`templates/`) — state "I'll author using the built-in standard structure (`reference/quality-gate.md`)" and get confirmation before continuing. → Hand control back to the user/orchestrator for the scope/contract decision.
- **Report contract**: `target: <path> (<stub | has-content>) | contract: <repo templates/AGENTS.md | partial | built-in fallback> | topic/objective: <...> | awaiting: scope confirmation`.

### Unit U1 — Research (live, cited)

- **Goal/scope**: ground the chapter in current official sources and present a plan for approval. Never write technical content from training data alone — product names, APIs, and exam objectives drift.
- **Inputs**: confirmed target + contract from U0; the topic/objective.
- **Do**:
  - **Parallel fetches.** Run these `webfetch` calls in parallel; record URL + retrieval date for each: (1) **official documentation** for the topic (primary source for mechanism and parameters); (2) **the exam/objective wording** if a certification is involved (quote it verbatim); (3) **changelog / "what's new"** if the topic is fast-evolving.
  - **Handle truncation.** If a doc page is long and `webfetch` truncates, delegate a targeted read to the `explore` agent or fetch a more specific sub-page. Do not author from truncated output.
  - **Offline / unreachable sources.** If official sources cannot be reached (no network, or every fetch fails), **stop rather than author from training data**. Tell the user and offer two paths: (a) paste the relevant official-doc excerpts into the chat, or (b) run `create-learning-repo`'s Phase 1 fallback AI-query prompts elsewhere and paste the results back. Only resume once cited source material is available.
  - Apply **source hygiene** (shared reference material) to every source and link.
  - **Assemble the research brief:**
    ```
    ## Research Brief — [Chapter]

    **Objective covered:** [verbatim objective or topic scope]
    **Sources:**
    - [url] — verified [date] — [what it provides]

    **Planned Key Concepts (sub-sections):**
    1. [Concept A] — mechanism + where it appears
    2. [Concept B] — ...
    3. [Concept C] — ...

    **Worked Example scenario:** [one line]
    **Anti-pattern to feature:** [one line]
    **Fast-evolving flags:** [list or "none"]
    ```
- **Self-verify**: at least the official documentation source was fetched and cited with a retrieval date; any exam objective is quoted verbatim; no source is a non-official blog/video; the brief lists concrete planned concepts, a worked-example scenario, and an anti-pattern.
- **STOP GATE (hand back)**: present the research brief and **stop**. Ask the user to confirm the sources and concept breakdown, or adjust the plan. **Do not draft until confirmed.** → Hand control back for the research/plan decision.
- **Report contract**: `sources: <N> official (dated) | objective quoted: <yes/n-a> | planned concepts: <N> | awaiting: brief approval`.

### Unit U2 — Draft the chapter

- **Goal/scope**: write every section in the contract's order to the required depth.
- **Inputs**: approved research brief + resolved contract + naming/answer-format conventions from U0.
- **Do**:
  - Author every section in the contract's order, meeting the **section-by-section depth requirements** (shared reference material). When a repo template exists, its order and headings win over the portable list.
  - Apply **draft discipline** (shared reference material): match naming style and answer format; leave zero TODO/STUB markers; respect the depth calibration.
  - Apply **source hygiene** to Further Reading links.
- **Self-verify**: run **Unit U3 (quality gate)** before reporting — the draft is not "done" until the gate passes or its ✗ rows are surfaced.
- **STOP GATE (hand back)**: present the full draft and **stop**. Ask the user to review content, section order, depth, and examples, then approve or give corrections before the gate/write. → Hand control back for draft review. (If running non-interactively, note the gate as "skipped — auto-proceeding with draft as written" and continue.)
- **Report contract**: `draft complete | sections: <N> (contract order) | snippets: <N> (incl. <N> anti-pattern) | quality gate: <PASS | N flagged, fixed | N flagged, unresolved> | awaiting: draft approval`.

### Unit U3 — Quality gate (self-audit, run inside U2 before any hand-back)

- **Goal/scope**: self-audit the draft against the contract before it is shown or written. This is the doer's own verification step — the mandatory gate that guarantees consistency.
- **Inputs**: the drafted chapter + `reference/quality-gate.md` (and any extra rules in the repo's `AGENTS.md`).
- **Do**: produce a pass/fail table; record ✓ or ✗ with a one-line note per row. Any ✗ blocks completion — fix each failure, then re-run the gate. Only pass when every row is ✓. Example:

  | Check | Result | Note |
  |---|---|---|
  | TL;DR ends with bolded "one thing to remember" | ✓ | |
  | ELI5 has structural analogy + corrects a misconception | ✓ | |
  | Every Key Concept sub-section has How + Where | ✗ | Concept B missing mechanism |
  | Key Parameters table present or explicit "none" note | ✓ | |
  | Worked Example follows 5-step format | ✓ | |
  | ≥2 implementation snippets, different angles | ✓ | |
  | ≥1 anti-pattern snippet with corrected version | ✓ | |
  | Every snippet opens with a `# Scenario:`/`# Anti-pattern:` comment | ✓ | |
  | Pitfalls have all 3 parts | ✓ | |
  | 5 questions spanning 3 cognitive levels | ✓ | |
  | ≥1 multi-select question | ✓ | |
  | `<details>` count == question count (+1 if a sample question section exists) | ✓ | |
  | Every answer explains correct + why distractors fail | ✓ | |
  | Further Reading: official docs only, all links verified this session | ✗ | 1 link not yet verified |
  | Zero TODO/STUB markers remain | ✓ | |

  Run these deterministic checks mechanically:
  - Count `<details>` occurrences and compare to the question count.
  - Search for residual `TODO` / `STUB` markers (must be zero).
  - Search for `Which TWO` / `Which THREE` (must be ≥1).
  - Re-`webfetch` each Further Reading URL to confirm 200 + content matches the citation.
- **Self-verify**: every row is ✓, or every remaining ✗ is surfaced explicitly with the reason it could not be fixed.
- **Report contract**: folded into U2's report (`quality gate: PASS` or the flagged/fixed/unresolved counts).

### Unit U4 — Write and report

- **Goal/scope**: commit the file and report compliance.
- **Inputs**: approved draft that passed the U3 gate + target path from U0.
- **Do**:
  - **Idempotency guard:** if the target file gained real content since U0 (e.g. a parallel edit), stop and ask before overwriting.
  - Write the full chapter to the target path with the `Write` tool.
  - Report:
    ```
    Authored:      [path]
    Contract:      [repo templates/AGENTS.md | built-in fallback]
    Sections:      [N] (all template sections present)
    Snippets:      [N] (incl. [N] anti-pattern)
    Questions:     5 ([N] multi-select)
    Links verified:[N]/[N]
    Quality gate:  PASS (all checks ✓)
    ```
  - Suggest the next logical stub in the same chapter or module (do not author it without a new request).
- **Self-verify**: the file exists at the expected path, matches the approved+gated draft, and the U3 gate was PASS (all rows ✓) before the write.
- **Report contract**: `wrote: <exact path> | contract: <source> | quality gate: PASS | next stub suggested: <path or none>`.

---

## Portability — Using This Skill on Other Platforms

This skill is written in the `SKILL.md` format for OpenCode. The workflow and rules are platform-agnostic.

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/author-chapter.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full content (below frontmatter) as your first message before naming the chapter to author |

**To install for all projects (OpenCode):**
```bash
# macOS / Linux
cp -r author-chapter ~/.config/opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse author-chapter "$env:USERPROFILE\.config\opencode\skills\"
```
