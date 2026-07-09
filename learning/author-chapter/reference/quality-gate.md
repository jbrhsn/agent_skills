# Quality Gate — Standard Chapter Rubric (fallback contract)

This file is the **built-in authoring contract** for the `author-chapter` skill. It is used only when the target repo has no `templates/chapter-notes-template.md` / `templates/authoring-guidelines.md` / `AGENTS.md` to derive rules from (i.e. a loose Markdown folder), and only after the user confirms.

When a repo's own template and `AGENTS.md` exist, **those take precedence** — this file is the fallback, not the override.

It doubles as the checklist the skill runs in Phase 3 (Quality Gate). Every row must be ✓ before a chapter is written.

---

## Standard chapter section order (fallback)

Author these sections in this exact order. Skip a section only where the rule below says it is conditional.

1. **Title (H1)** + a metadata line: `Section | Module | Est. time | Objective/mapping`
2. **TL;DR**
3. **ELI5 — Explain It Like I'm 5**
4. **Learning Objectives**
5. **Visual Overview** — conditional (include if the topic has a visualisable process/architecture/decision path/before-after; omit for purely conceptual topics)
6. **Key Concepts** — with these sub-sections:
   - one `###` sub-section per concept
   - **Key Parameters / Configuration Knobs** (conditional — see rule)
   - **Worked Example: Requirement → Decision**
7. **Implementation**
8. **Common Pitfalls & Misconceptions**
9. **Key Definitions**
10. **Summary / Quick Recall**
11. **Self-Check Questions**
12. **Further Reading**

Separate every major section with a horizontal rule (`---`).

---

## Content depth rules

### Rule 1 — ELI5 must use a structural analogy
Plain English, zero jargon, 3–6 sentences, prose only. A concrete everyday analogy that maps *structurally* onto the concept, and an explicit correction of the most common misconception. A vague comparison is non-compliant.

### Rule 2 — Every concept sub-section explains the mechanism
Each `###` concept answers three questions: (1) What is it? (2) How does it work under the hood? (3) Where does it appear in the tool/platform? Answering only (1) is non-compliant.

### Rule 3 — Key Parameters required for configurable topics
Table: `Parameter | What it controls | Decision rule`. The decision rule is an actionable "set X when Y" rule, not a restatement of the parameter. If the topic has no tunable settings, write "No configurable parameters for this topic."

### Rule 4 — Worked Example required
One realistic scenario, walked through: Step 1 goal → Step 2 inputs → Step 3 outputs → Step 4 constraints → Step 5 approach + one-sentence rationale vs alternatives. If there is no selection decision, substitute a realistic failure-diagnosis walkthrough.

### Rule 5 — Snippets are scenario-first
≥2 snippets from different angles. Every snippet opens with a comment naming the real-world problem (`# Scenario: ...`). At least one is an anti-pattern (`# Anti-pattern:`) immediately followed by the corrected version and an explanation of what breaks.

### Rule 6 — Pitfalls have three parts
Each bullet: **bolded label** + one sentence on why beginners make the mistake + one sentence on the correct mental model. Bare bullets are non-compliant.

### Rule 7 — Answer rationales cover all options
Every question's answer explains why the correct answer is right AND why each significant distractor is wrong. One-word rationales are non-compliant. For multi-select, explain why both correct answers qualify AND why the most tempting wrong answer fails.

### Rule 8 — Questions span cognitive levels
5 questions: Q1 recall, Q2–Q3 application, Q4–Q5 analysis/trade-off. At least one multi-select. Five recall questions is non-compliant even if one is multi-select. Each answer lives in an inline `<details><summary>Answer</summary>` block immediately after its options.

### Rule 9 — Visual Overview format (when included)
Placed after Learning Objectives, before Key Concepts. Each diagram under its own `###` sub-header in a plain fenced block (no language tag). Use `──►` for flow and `│ ├ └ ─ ┌ ┐` for structure. 2–4 diagrams; one clear diagram beats four cluttered ones.

### Source hygiene
Official documentation only — no third-party blogs, Medium, or YouTube. Every external link: `[Title](url) — *verified YYYY-MM-DD*`, verified live this session. Quote exam objectives verbatim.

---

## Phase 3 gate checklist

Every row must be ✓ before writing.

- [ ] TL;DR ends with a bolded "one thing to remember"
- [ ] ELI5 uses a concrete structural analogy, no jargon, corrects a misconception
- [ ] Every Key Concept sub-section answers What? How does it work? Where does it appear?
- [ ] Key Parameters table present (or explicit "no configurable parameters" note)
- [ ] Worked Example follows the 5-step Requirement → Decision format
- [ ] ≥2 implementation snippets from different angles
- [ ] ≥1 anti-pattern snippet with a corrected version
- [ ] Every snippet opens with a `# Scenario:` or `# Anti-pattern:` comment
- [ ] Visual Overview present if the topic is visualisable (2–4 diagrams, each under a `###` header in a plain fenced block)
- [ ] Pitfalls have all 3 parts (label + why + correct model)
- [ ] 5 Self-Check questions spanning 3 cognitive levels
- [ ] ≥1 multi-select question
- [ ] `<details>` count equals the total question count
- [ ] Every answer explains why correct AND why distractors fail
- [ ] Further Reading: official docs only, every link webfetch-verified this session
- [ ] Zero `TODO` / `STUB` markers remain
- [ ] No filler — every sentence earns its space
