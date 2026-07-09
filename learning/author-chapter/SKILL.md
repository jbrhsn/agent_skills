---
name: author-chapter
description: Use when the user asks to populate, author, write, or fill in a chapter, notes file, or topic stub in a learning repository or a Markdown study folder. Researches live sources, writes every template section to spec, and runs a quality gate before reporting. Do NOT use to scaffold a new repo (that is create-learning-repo) or to generate quizzes/mock exams (that is generate-practice-exam).
---

# Author Chapter

This skill turns a blank stub (or a thin, incomplete file) into a fully template-compliant learning chapter. It researches live sources, writes every section to the repo's own standard, and runs an automated quality gate before finishing.

It is **fully generic** — no topic, tool, vendor, or repo path is hardcoded. The section order and quality rules are read from the target repo's own `templates/` and `AGENTS.md` at runtime. When those files do not exist (a loose Markdown folder), the skill falls back to the bundled `reference/quality-gate.md` after confirming with the user.

The workflow runs in **five confirmed phases**. Every phase except the final write ends with an explicit gate: present output, wait for approval, do not combine phases in one response.

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

## Phase 0 — Locate the authoring contract

**Goal:** find the rules this chapter must follow, and confirm the target, before writing anything.

### Step 1 — Identify the target file
- Confirm the exact file path the user wants populated. If they named a chapter or topic but not a file, list the candidate stub(s) and ask which one.
- Read the target file. Classify it:
  - **Stub** — a single comment line (e.g. `<!-- stub: ... -->`), an `> **Status:** STUB` marker, or only an H1 title. Safe to populate.
  - **Has real content** — anything more. **Stop and ask** whether to rewrite, extend, or leave it. Never overwrite authored content silently.

### Step 2 — Find the contract by walking up the tree
From the target file's directory, walk up toward the filesystem root looking for:
- `AGENTS.md` — the repo's authoring rules (Content Depth Rules, naming style, answer format)
- `templates/chapter-notes-template.md` (or the repo's equivalent named topic-note template)
- `templates/authoring-guidelines.md` (the quality rubric)

**Branch on what is found:**

| Found | Action |
|---|---|
| `AGENTS.md` + `templates/` both present | This is a structured learning repo. Read both. They are the authoritative contract — derive the section order and rules from them, not from this skill. |
| Neither present (loose Markdown folder) | Tell the user: "No `AGENTS.md`/`templates/` found — this looks like a loose Markdown folder. I'll author using my built-in standard chapter structure (`reference/quality-gate.md`). Proceed?" Only continue after confirmation. |
| Partial (one present) | Use whatever is present; fall back to `reference/quality-gate.md` for the missing piece. Tell the user which contract you are using. |

> **Never hardcode the section list.** When `templates/chapter-notes-template.md` exists, the section order and headings come from it. This is what keeps the skill portable across repos with different templates.

### Step 3 — Gather chapter context
- Read the parent section/module index (if present) to find the chapter's declared exam objective, topic scope, and estimated time.
- Read 1–2 sibling chapters that are already authored (if any) to match voice, depth, and formatting conventions.
- Note the repo naming style (ALLCAPS-underscore vs lowercase-hyphen) and the answer format (inline `<details>` vs separate key) so the draft matches.

### End of Phase 0

> **Phase 0 complete.** Target file: `[path]`. Contract source: `[repo templates/AGENTS.md | built-in fallback]`. Topic/objective: `[...]`.
> Reply **"proceed"** to start research, or correct the target/scope first.

---

## Phase 1 — Research (live, cited)

**Goal:** ground the chapter in current official sources. Never write technical content from training data alone — product names, APIs, and exam objectives drift.

### Step 1 — Parallel fetches
Run these `webfetch` calls in parallel; record URL + retrieval date for each:
1. **Official documentation** for the topic (the primary source for mechanism and parameters).
2. **The exam/objective wording** if a certification is involved (quote it verbatim — never paraphrase objectives).
3. **Changelog / "what's new"** if the topic is fast-evolving.

### Step 2 — Handle truncation
If a doc page is long and `webfetch` truncates, delegate a targeted read to the `explore` agent or fetch a more specific sub-page. Do not author from truncated output.

### Step 3 — Source hygiene
- Only official documentation counts as a citable source — no third-party blogs, Medium, or YouTube.
- Format every link as `[Title](url) — *verified YYYY-MM-DD*`.
- Flag any fast-evolving feature inline with a note to re-verify before relying on it.

### Step 4 — Present the research brief
Show a compact brief and gate:

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

### End of Phase 1

> **Phase 1 complete.** Do the sources and concept breakdown look right?
> Reply **"proceed"** to draft the chapter, or adjust the plan first.

---

## Phase 2 — Draft the chapter

**Goal:** write every section in the contract's order to the required depth. Follow the Content Depth Rules from the repo's `AGENTS.md` (or `reference/quality-gate.md` in fallback mode). The rules below are the portable minimum every draft must meet.

### Section-by-section requirements

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

### Draft discipline
- Match the repo's naming style and answer-format convention detected in Phase 0.
- Leave zero `<!-- TODO -->` or `STUB` markers.
- Depth calibration: Key Concepts + ELI5 + Worked Example carry the teaching load (~75% of effort); snippets ~15%; questions ~10% but non-negotiable.

### End of Phase 2

> **Phase 2 complete.** The full draft is above.
> Review the content, section order, depth, and examples.
> Reply **"proceed"** to run the quality gate, or give corrections first.

---

## Phase 3 — Quality gate

**Goal:** self-audit the draft against `reference/quality-gate.md` (and any extra rules in the repo's `AGENTS.md`) before writing. This is the step that guarantees consistency.

Produce a pass/fail table. Example:

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

**Rule:** any ✗ blocks completion. Fix each failure, then re-run the gate. Only proceed when every row is ✓.

Deterministic checks to run mechanically:
- Count `<details>` occurrences and compare to the question count.
- Search for residual `TODO` / `STUB` markers (must be zero).
- Search for `Which TWO` / `Which THREE` (must be ≥1).
- Re-`webfetch` each Further Reading URL to confirm 200 + content matches the citation.

---

## Phase 4 — Write and report

**Goal:** commit the file and report compliance.

1. **Idempotency guard:** if the target file gained real content since Phase 0 (e.g. a parallel edit), stop and ask before overwriting.
2. Write the full chapter to the target path with the `Write` tool.
3. Report:

```
Authored:      [path]
Contract:      [repo templates/AGENTS.md | built-in fallback]
Sections:      [N] (all template sections present)
Snippets:      [N] (incl. [N] anti-pattern)
Questions:     5 ([N] multi-select)
Links verified:[N]/[N]
Quality gate:  PASS (all checks ✓)
```

4. Suggest the next logical stub in the same chapter or module (do not author it without a new request).

---

## Constraints and Guardrails

- **Contract comes from disk, not this skill.** When the repo has `templates/` + `AGENTS.md`, they win. The built-in `reference/quality-gate.md` is a fallback for loose folders only, and its use must be confirmed with the user.
- **Never overwrite authored content without explicit confirmation.** Only populate stubs freely.
- **One phase per response.** Every phase except the final write ends with a gate.
- **Always research live in Phase 1.** Cite URL + retrieval date. Official docs only.
- **Quote exam objectives verbatim** — never paraphrase them.
- **The quality gate is mandatory.** A chapter is not "done" until every gate row is ✓.
- **Author only what the user named.** Do not batch-populate a module unless explicitly asked.
- **Windows-safe:** quote paths with spaces; do not assume forward slashes.

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
