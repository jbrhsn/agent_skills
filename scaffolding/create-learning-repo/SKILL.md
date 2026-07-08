---
name: create-learning-repo
description: Use when the user wants to create a learning repository, study guide, certification prep repo, or expert knowledge base for any topic or certification. Guides the agent through intake, live web research, folder structure design, template generation, AGENTS.md authoring, and skeleton file scaffolding — confirmed phase by phase. Creates blank stubs for all content files; only templates/ is populated with real content. Do NOT use for editing an existing repo's content.
---

# Create Learning Repo

This skill creates a complete, opinionated Markdown-based learning repository for any topic or certification. It is fully generic — no tool names, vendor names, or repo paths are hardcoded. Everything is derived from the user's inputs.

The workflow runs in **six confirmed phases**. Each phase ends with an explicit gate — the agent presents output and waits for user approval before proceeding. No two phases run in the same response.

**What gets created:**
- A structured folder tree (sections → modules → chapters)
- A `templates/` directory — the only directory with real content
- An `AGENTS.md` — authoring rules and content depth standards for the repo
- A `README.md` — populated with actual repo metadata
- Blank stub files for all content (one placeholder line each)

**What does NOT get created during this skill:**
- Any learning content, notes, explanations, or exam questions
- Pre-filled chapter headers or section summaries
- Roadmap content or progress tables

---

## When to use this skill

Trigger on any request that matches:
- "create a learning repo for X"
- "build a study guide for Y certification"
- "set up a knowledge base to learn Z"
- "I want to become an expert in / thought leader on X"
- "scaffold a learning repo for X"
- "create a certification prep repo for X"

Do **not** trigger if the user is asking to add content to an existing repo — that is content authoring, not repo creation.

---

## Phase 0 — Intake

**Before any research or design**, collect the following in a single message. Do not proceed until all questions are answered (the user may skip optional ones explicitly).

```
To design the right repo for you, I need a few details:

1. Topic / Certification  
   What is the exact topic or certification name?
   (e.g. "AWS Solutions Architect Associate", "Apache Kafka", "System Design")

2. Learning goal — choose all that apply:
   a) Pass a certification exam
   b) Get a job / ace technical interviews in this area
   c) Write articles or build a public thought-leadership profile
   d) Deep personal mastery (no external output goal)
   e) Other — describe it

3. Current level:
   Complete beginner / Some exposure / Adjacent expert / Practitioner already

4. Time budget:
   How many total hours do you want to invest?
   (I will flag if the budget seems too tight or too generous for the scope)

5. Naming preference (optional):
   Do you have a preferred folder name for the repo?
   If not, I will derive one from the topic.

6. Naming style (optional):
   a) Flat lowercase with hyphens  (e.g. 01-core-concepts/)
   b) ALLCAPS with underscores     (e.g. SECTION_01_CORE_CONCEPTS/)
   If not specified, I will default to (a).

7. Seed URLs (optional):
   Any documentation pages, exam guides, or reference links to use as
   primary sources? Leave blank and I will find them.
```

### Intent logic (run silently after answers are received)

Based on the user's goals, decide which per-chapter file types to generate:

| Detected goal | Additional file per chapter |
|---|---|
| Includes (c) — articles / thought leadership | `thought-leadership.md` stub |
| Includes (b) — interviews / job / career | `interview-prep.md` stub |
| Both (b) and (c) | Both files |
| Ambiguous "learn deeply" with no output goal | Ask: "Should I also add thought-leadership.md and/or interview-prep.md stubs per chapter for future use?" |
| Only (a) or (d) | `notes.md` only |

Record the file-type decision. It affects the file tree in Phase 2 and the templates in Phase 3.

---

## Phase 1 — Research

**Goal:** Produce a research summary grounded in live sources. This drives the structure designed in Phase 2. Never invent curriculum structure from training data alone — product names, exam blueprints, and API surfaces change.

### Step 1 — WebFetch (primary, run in parallel)

Attempt all of the following fetches simultaneously. Record the URL and retrieval date for each.

1. **Official exam blueprint** (if a certification exists):
   - Search for `[CERTIFICATION NAME] official exam guide` or `[CERTIFICATION NAME] exam blueprint` to find the right URL.
   - Do not assume a URL — find it. Every certification has a different landing page.
   - Target: exam domains, domain weightings (%), question count, passing score, duration, cost, retake policy.

2. **Official documentation landing page** for the technology or subject:
   - Target: product/topic overview, key concepts, current version, major recent changes.

3. **Any seed URLs the user provided** in Phase 0.

4. **Changelog or "What's new" page** (if one exists):
   - Target: changes in the last 12–18 months that would affect what to learn or what is now deprecated.

### Step 2 — Fallback AI query stubs

For any area where WebFetch returned thin or no content, generate ready-to-paste prompts the user can run in any AI assistant:

---
**If any fetches above failed or returned thin results, paste this into any AI assistant and share the response:**

> You are an expert in [TOPIC/CERTIFICATION]. Answer all four questions below specifically and cite sources where possible.
>
> 1. What are the official exam domains and their percentage weightings for [CERT NAME]? Include question count, passing score, duration, and cost.
> 2. What is the canonical beginner → intermediate → advanced → expert skill progression for [TOPIC] as described by leading courses, books, and practitioners?
> 3. What are the core prerequisite skills someone should verify they have before starting [TOPIC]?
> 4. What are the most significant changes to [TOPIC] in the last 12–18 months that any learner must know about?
---

### Step 3 — Research summary

Present this structured summary. Fill every field from live sources; mark fields as "N/A — no certification" where applicable.

```markdown
## Phase 1 Research Summary — [TOPIC]

**Sources consulted:**
- [URL] — retrieved [DATE] — [what was found]

**Exam blueprint** (if applicable):
- Domains and weights: [list]
- Format: [N questions / N minutes / passing score / cost]
- Retake policy: [...]
- Stated prerequisites: [...]

**Canonical skill progression:**
- Beginner: [...]
- Intermediate: [...]
- Advanced: [...]
- Expert: [...]

**Core prerequisites to verify before starting:**
- [...]

**Significant changes in the last 12–18 months:**
- [...]

**Fast-evolving areas** (likely to shift within 6–12 months — flag in content):
- [...]

**Recommended section sequence:**
- Section 01: [name] — rationale
- Section 02: [name] — rationale
- ...
```

### End of Phase 1

> **Phase 1 complete.**  
> Does this look accurate? Any corrections before I design the folder structure?  
> Reply **"proceed"** to continue to Phase 2, or give me corrections first.

---

## Phase 2 — Repository Structure

**Goal:** Design the full folder and file hierarchy, confirm with the user, then proceed to templates.

### Naming conventions

Apply the style the user chose in Phase 0 (or default to lowercase-hyphen style if not specified).

**Lowercase-hyphen style (default):**

| Level | Format | Example |
|---|---|---|
| Repo root | `topic-slug` chosen or derived | `apache-kafka-mastery` |
| Section | `01-section-name/` | `01-core-concepts/` |
| Module | `01-module-name/` | `01-producers-and-consumers/` |
| Chapter | `01-chapter-name/` | `01-topic-partitions/` |

**ALLCAPS-underscore style (if user selected):**

| Level | Format | Example |
|---|---|---|
| Repo root | User-specified or derived | `Apache-Kafka-Mastery` |
| Section | `SECTION_XX_DESCRIPTIVE_NAME/` | `SECTION_01_CORE_CONCEPTS/` |
| Module | `MODULE_XX_Descriptive_Name/` | `MODULE_01_Producers_And_Consumers/` |
| Chapter | `CHAPTER_XX_Descriptive_Name/` | `CHAPTER_01_Topic_Partitions/` |

**Rules that apply regardless of style:**
- Use the **actual technology/subject names** in folder names — never generic placeholders like `module-1` or `chapter-a`.
- Every folder is numerically prefixed for correct sort order.
- No spaces in any path component.
- **Windows MAX_PATH caution:** Full paths over ~220 characters fail silently on Windows. Shorten folder names proactively for deep trees and note any shortenings in the section index.

### File naming conventions

| File type | Pattern | Notes |
|---|---|---|
| Topic notes (ALLCAPS style) | `01_snake_case.md` … `03_snake_case.md` | 3 per chapter by default |
| Topic notes (hyphen style) | `01-snake-case.md` … `03-snake-case.md` | 3 per chapter by default |
| Thought leadership | `04-thought-leadership.md` / `04_thought_leadership_article_template.md` | `04_`/`04-` when 3 topic notes; `05_`/`05-` when 4 topic notes |
| Interview prep | `05-interview-prep.md` / `05_interview_prep.md` | Only if intent detected |
| Lab file | `LAB-XX-name.md` / `LAB_XX_name.md` | Global sequence — never reset |
| Section index | `README.md` or `INDEX.md` inside section folder | Created at scaffold time |
| Module index | Not created at scaffold time — on request only | |

### Topic file count per chapter

- **Standard:** 3 topic notes + thought leadership file
- **Dense chapters** (user-confirmed during Phase 0): 4 topic notes + thought leadership file at `05_`/`05-`

Ask the user to confirm during Phase 0 if any sections should use 4 topic notes. Do not assume based on position.

### Full repo tree structure

```
[repo-root]/
├── README.md                        ← populated (written in Phase 5)
├── AGENTS.md                        ← populated (written in Phase 4)
├── templates/
│   ├── chapter-notes-template.md    ← POPULATED
│   ├── section-index-template.md    ← POPULATED
│   ├── module-index-template.md     ← POPULATED
│   ├── authoring-guidelines.md      ← POPULATED
│   ├── thought-leadership-template.md   ← POPULATED (if intent detected)
│   ├── interview-prep-template.md   ← POPULATED (if intent detected)
│   ├── lab-template.md              ← POPULATED (if labs requested)
│   └── capstone-template.md         ← POPULATED
├── 00-roadmap/
│   └── learning-roadmap.md          ← stub
├── 01-[section]/
│   ├── README.md or INDEX.md        ← stub
│   ├── 01-[module]/
│   │   ├── README.md or INDEX.md    ← stub
│   │   └── 01-[chapter]/
│   │       ├── notes.md             ← stub
│   │       ├── thought-leadership.md ← stub (if intent)
│   │       └── interview-prep.md    ← stub (if intent)
│   └── ...
├── ...
├── capstone/
│   ├── README.md                    ← stub
│   └── project-brief.md             ← stub
└── progress-tracker.md              ← stub
```

### Structural rules

- Sections follow a natural difficulty ramp: Foundations → Core Competency → Advanced / Specialised → Expert Practice.
- If a certification exists, the final content section (before capstone) must be **exam prep**: mock questions, common pitfalls, exam strategy, timing.
- Each chapter is sized for **1.5–3 hours** of focused study. If total chapters × avg hours does not roughly match the user's Phase 0 budget, flag it and suggest a rescope before proceeding.
- The capstone must draw on skills from at least two sections.

### Present the tree

Show the complete folder + file tree annotated with:
- Estimated hours per chapter
- Exam domain mapping per section (if cert exists)
- Total hours sum
- `← POPULATED` next to template files, `← stub` next to all content files
- Any fast-evolving areas flagged in Phase 1 (note them inline)

### End of Phase 2

> **Phase 2 complete.**  
> Does this structure look right? Confirm folder names, section order, chapter sizing, and total hours.  
> Reply **"proceed"** to continue to Phase 3 (templates), or request changes.

---

## Phase 3 — Templates

**Goal:** Generate all template files in full. Present them and wait for confirmation before writing anything to disk.

### Always generate these four

#### 3a. `chapter-notes-template.md`

````markdown
# [Chapter Title]

**Section:** [Section] | **Module:** [Module] | **Est. time:** [X hrs] | **Exam mapping:** [Domain/objective or "Supporting content"]

---

## TL;DR

<!-- 2–4 sentences. What this topic is, why it matters, and the single most important thing to remember.
     End with: **The one thing to remember: ...** -->

---

## ELI5 — Explain It Like I'm 5

<!-- Mandatory. 3–6 sentences of plain English using a concrete everyday analogy.
     The analogy must map structurally onto the technical concept — not just vaguely compare.
     No jargon in this section. Prose only, no bullets.
     Non-compliant: "Think of X as a way to represent Y." (too vague)
     Compliant: name a familiar object, map its mechanism to the technical process,
     and explicitly correct the most common misconception. -->

---

## Learning Objectives

By the end of this chapter you will be able to:
- [ ] [Action-verb outcome — specific and testable, e.g. "Configure X to achieve Y"]
- [ ] [Outcome 2]
- [ ] [Outcome 3–5 total — use verbs: implement, diagnose, compare, explain, design]

---

## Key Concepts

<!-- For EACH concept sub-section, answer all three questions:
     1. What is it? (1–2 sentence definition)
     2. How does it work mechanistically? (2–4 sentences on the process/behaviour that produces the result)
     3. Where does it appear in the tool/platform ecosystem? (command, API call, config field, UI location)
     A sub-section that only answers question 1 is non-compliant. -->

### [Concept A]

### [Concept B]

### [Concept C]

### Key Parameters / Configuration Knobs

<!-- Required for any chapter covering a configurable component.
     "Decision rule" must be a concrete actionable rule, not a restatement of the parameter.
     If no configurable parameters exist for this topic, write: "No configurable parameters for this topic." -->

| Parameter | What it controls | Decision rule |
|---|---|---|
| [param] | [what it does] | [when to set it to X vs Y] |

### Worked Example: Requirement → Decision

<!-- Mandatory. Walk through one complete, realistic decomposition.
     Given: [plain-English scenario — not "Example: configure X"]
     Step 1 — Identify the goal: [what outcome is needed]
     Step 2 — Define inputs: [what data/config/context enters]
     Step 3 — Define outputs: [what the downstream step expects]
     Step 4 — Apply constraints: [constraints relevant to this domain and topic]
     Step 5 — Select the approach: [specific tool/command/pattern + one-sentence rationale vs alternatives]
     If no selection decision exists, substitute a realistic failure diagnosis walkthrough. -->

---

## Implementation

<!-- At least 2 code or config snippets from different angles.
     Every snippet starts with a comment naming the business/operational problem it solves.
     At least one snippet must be an anti-pattern, labeled # Anti-pattern: or # Wrong:,
     immediately followed by the corrected version with an explanation of what breaks. -->

```[language]
# Scenario: [the real-world problem this solves]

```

```[language]
# Anti-pattern: [describe the wrong approach and why it fails]

# Correct approach:

```

---

## Common Pitfalls & Misconceptions

<!-- Each bullet: (1) bolded label, (2) why beginners make this mistake, (3) correct mental model.
     Bare bullets with no explanation are non-compliant. -->

- **[Pitfall label]** — [Why the wrong intuition forms]. [Correct mental model].
- **[Pitfall label]** — [Why the wrong intuition forms]. [Correct mental model].
- **[Pitfall label]** — [Why the wrong intuition forms]. [Correct mental model].

---

## Key Definitions

| Term | Definition |
|---|---|
| [Term] | [Precise, scoped definition — not a dictionary entry] |

---

## Summary / Quick Recall

- [Key takeaway 1 — one line, scannable]
- [Key takeaway 2]
- [3–7 takeaways total — designed for a 60-second pre-exam scan]

---

## Self-Check Questions

<!-- 5 questions. Cognitive level distribution:
     Q1: recall (definition or fact)
     Q2–Q3: application (apply concept to a new scenario)
     Q4–Q5: analysis or trade-off (compare options, select best under constraints)
     At least 1 must be multi-select ("Which TWO...").
     Every answer: explain why correct AND why main distractor(s) are wrong.
     One-word answers are non-compliant. -->

1. [Recall question]

   <details><summary>Answer</summary>

   [Why this is the correct answer. Why the most tempting wrong answer fails.]

   </details>

2. [Application question]

   <details><summary>Answer</summary>

   [Answer with rationale.]

   </details>

3. **Which TWO** [multi-select question]
   - A.
   - B.
   - C.
   - D.
   - E.

   <details><summary>Answer</summary>

   [Why both correct answers qualify. Why the most tempting wrong answer fails.]

   </details>

4. [Analysis question]

   <details><summary>Answer</summary>

   [Answer with rationale.]

   </details>

5. [Trade-off question]

   <details><summary>Answer</summary>

   [Answer with rationale.]

   </details>

---

## Further Reading

<!-- Official documentation only. No third-party blogs, Medium, or YouTube.
     Format: [Title](url) — *verified YYYY-MM-DD* — [one-line description]
     Verify every URL with webfetch before writing. -->

- [Title](url) — *verified YYYY-MM-DD* — [description]
````

#### 3b. `module-index-template.md`

````markdown
# [Module Name]

**Part of:** [Section] | **Estimated time:** [X hrs] | **Prerequisites:** [Prior module or "None"] | **Exam mapping:** [Domain/objective]

## Overview

[1–2 sentences: what this module covers and why it matters in the learning arc.]

## Learning Outcomes

By completing this module you will be able to:
- [Outcome 1]
- [Outcome 2]
- [Outcome 3–5]

## Chapters

| # | Chapter | Est. time | File |
|---|---|---|---|
| 1 | [Chapter name] | [X hrs] | [relative link to notes file] |
| 2 | [Chapter name] | [X hrs] | [relative link] |

## How This Module Fits

[What came before, what this module unlocks, what comes next.]

## Study Tips

[Specific, practical advice for this module — tools to set up, known difficulty spikes, common pacing mistakes. Generic advice ("take notes") does not belong here.]
````

#### 3c. `section-index-template.md`

````markdown
# [Section Name]

**Estimated time:** [X hrs] | **Exam domain weight:** [~X% or "N/A"] | **Prerequisites:** [Prior section or "None"]

## Overview

[2–3 sentences: scope of this section, what phase of the learning arc it covers, why it matters.]

## Learning Outcomes

By completing this section you will be able to:
- [Outcome 1]
- [Outcome 2]
- [Outcome 3–5]

## Modules

| # | Module | Est. time | Chapters |
|---|---|---|---|
| 1 | [Module name] | [X hrs] | [N] |
| 2 | [Module name] | [X hrs] | [N] |

## How This Section Fits

[Connection to the previous section and what it unlocks for the next.]

## Study Tips

[Section-specific advice — environments to set up, things to review from prerequisites, known difficulty spikes.]
````

#### 3d. `authoring-guidelines.md`

````markdown
# Authoring Guidelines & Quality Rubric

## Voice & Tone

- Write for **learning**, not documentation. Explain *why* things work the way they do.
- Active voice. Concrete examples over abstract definitions.
- Target voice: "knowledgeable colleague at a whiteboard" — not a textbook, not a marketing page.
- Assume the reader knows the prerequisites but is new to this specific topic.

## Depth Calibration

- **Key Concepts (incl. ELI5, Worked Example):** ~75% of authoring effort. This is where teaching happens.
- **Implementation snippets:** ~15%. Must be realistic and runnable. At least one anti-pattern.
- **Self-Check Questions:** ~10% but non-negotiable. 5 questions, spanning recall → application → analysis.
- Do not invert these proportions. A chapter with 10 code examples and 2 sentences of explanation teaches nothing.

## ELI5 Requirements

Every chapter opens with an ELI5 section. Rules:
- Plain English, zero jargon.
- A concrete everyday analogy that maps structurally onto the concept — not just a vague comparison.
- 3–6 sentences, prose only.
- Must address the most common misconception about the topic.

## Worked Examples

Every chapter must have at least one complete Worked Example following the Requirement → Decision format:
- Given a realistic scenario (not a toy example)
- Step through goal → inputs → outputs → constraints → approach + rationale
- If no selection decision exists, use a failure diagnosis walkthrough instead

## Self-Check Questions

- 5 questions per chapter. Distribution: Q1 recall, Q2–Q3 application, Q4–Q5 analysis/trade-off.
- At least 1 must be multi-select ("Which TWO...").
- Every answer must explain why the correct answer is right AND why the main distractor(s) are wrong.
- Use `<details><summary>Answer</summary>` for all answers.
- One-word answers are non-compliant.

## Source Hygiene

- Cite source URL and retrieval date for every specific doc, API reference, or changelog entry.
- Flag fast-evolving features with: `> ⚠️ Fast-evolving: verify against current official docs before relying on this.`
- Official documentation only — no third-party blogs, Medium, or YouTube.

## Blueprint Drift Warning

Exam objectives and API surfaces change over time. If you are authoring more than 6 months after the repo was created, verify the current official exam guide or documentation before writing. Do not assume the Phase 1 research summary is still current.

## Quality Checklist

Run before marking a chapter complete:

- [ ] TL;DR ends with a bolded "one thing to remember"
- [ ] ELI5 uses a concrete structural analogy, no jargon, addresses a misconception
- [ ] Every Key Concepts sub-section answers: What? How does it work? Where does it appear?
- [ ] Key Parameters table exists (or explicit "no configurable parameters" note)
- [ ] Worked Example follows the Requirement → Decision 5-step format
- [ ] At least 2 implementation snippets from different angles
- [ ] At least 1 anti-pattern snippet with corrected version
- [ ] All snippets start with a `# Scenario:` or `# Anti-pattern:` comment
- [ ] Pitfalls have all 3 parts: label + why beginners make it + correct mental model
- [ ] 5 Self-Check questions spanning 3 cognitive levels
- [ ] At least 1 multi-select question
- [ ] All answers explain why correct AND why distractors fail
- [ ] Further Reading uses only official docs, all links verified with webfetch
- [ ] No filler — every sentence earns its space
````

### Conditionally generate (based on Phase 0 intent)

#### 3e. `thought-leadership-template.md` — only if goal (c) detected

````markdown
# [Chapter Title] — Thought Leadership

**Section:** [Section] | **Target audience:** [e.g. senior engineers, tech leads, general tech audience] | **Target publication:** [e.g. personal blog, LinkedIn, conference talk]

## Hook / Opening Thesis

[1–2 sentences that stop a busy person scrolling. What is the non-obvious claim this piece makes? Do NOT open with "In today's world..." or "As X continues to evolve..."]

## Key Claims (3–5)

1. [Specific and defensible claim — not generic]
2. [Claim 2]
3. [Claim 3]

## Supporting Evidence & Examples

[For each claim: data, case study, observed pattern, or first-hand experience. Be specific — name the tools, the failure, the numbers.]

## The Original Angle

[What does this say that cannot be found elsewhere? Why are YOU the right person to say it?]

## Counterarguments to Address

[What would a skeptical expert push back with? Acknowledge and respond to the strongest objections.]

## Practical Takeaways for the Reader

- [What can the reader do differently after reading this?]
- [Concrete action or mental model shift]

## Call to Action

[What do you want the reader to do next?]

## Further Reading / References

- [Source](URL) — [why it supports the argument]

---
<!-- PUBLISHING CHECKLIST (delete before posting):
  - [ ] Hook does NOT start with "In today's world" or "As X evolves"
  - [ ] At least one concrete example or metric
  - [ ] Personal voice throughout ("I", "we", "my team")
  - [ ] Ends with a specific discussion question or call to action
  - [ ] 600–900 words when measured
-->
````

#### 3f. `interview-prep-template.md` — only if goal (b) detected

````markdown
# [Chapter Title] — Interview Prep

**Section:** [Section] | **Role target:** [e.g. Senior Engineer, Solutions Architect, Data Engineer]

## Core Conceptual Questions

These test whether you understand the fundamentals.

| Question | Key points to cover | Common weak-answer trap |
|---|---|---|
| [Question 1] | [2–3 bullet points] | [What shallow candidates say] |
| [Question 2] | [...] | [...] |

## Applied / Scenario Questions

**Q:** [Realistic engineering scenario]

**Strong answer framework:**
- [Point 1]
- [Point 2]
- [How to show tradeoff awareness]

## System Design / Architecture Questions (if applicable)

**Q:** [Design question]

**Approach:**
1. Clarify requirements
2. Propose structure
3. Justify choices and name tradeoffs explicitly

## Vocabulary That Signals Expertise

Use these terms naturally — don't force them:
- [Term] — [when/why to use it]

## Vocabulary That Signals Weakness

Avoid these — they signal outdated or shallow understanding:
- [Term/phrase] — [why it's a red flag]

## STAR Answer Frame

**Situation:** [Realistic scenario using this chapter's concepts]  
**Task:** [What you were responsible for]  
**Action:** [Specific technical decisions and why]  
**Result:** [Quantified outcome if possible]

## Red Flags Interviewers Watch For

[Specific to this topic area — not generic interview advice]
````

#### 3g. `lab-template.md` — only if labs were requested in Phase 0

````markdown
# [Lab Title]

**Lab:** LAB-[XX] | **Section:** [Section] | **Module:** [Module] | **Est. time:** [X hrs]

## Objective

[One sentence: what the learner will have built or demonstrated by the end.]

## Prerequisites

- [Prior lab or concept]
- [Environment requirement]

## Setup

[Environment setup steps — specific commands, not vague instructions.]

```[language]
# Setup commands
```

## Steps

### Step 1 — [Action]

[Instructions]

```[language]
# Step 1 code/config
```

### Step 2 — [Action]

...

## Validation

[How to verify the lab succeeded — specific observable output or test command.]

```[language]
# Validation command / expected output
```

## Teardown

[How to clean up resources created during the lab.]

## Reflection Questions

1. [What would break if you changed X?]
2. [What would you do differently in production?]
3. [How does this connect to [next topic]?]
````

#### 3h. `capstone-template.md` — always generate

````markdown
# [Capstone Project Title]

**Sections covered:** [list sections this draws on] | **Est. time:** [X hrs]

## Problem Statement

[A realistic scenario that requires integrating skills from multiple sections. Must not be solvable using only one section's knowledge.]

## Requirements

- Functional: [what it must do]
- Non-functional: [performance, reliability, cost, or other constraints]

## Architecture Design

[Describe the high-level approach before implementing. Justify the key choices.]

## Implementation Guide

[Step-by-step — specific enough to follow, not so prescriptive that there is only one solution.]

## Tradeoffs & Optimisation

[What tradeoffs did you make? What would you change with more time or budget?]

## Reflection

- What was harder than expected?
- What would you do differently?
- What did this project reveal that the individual chapters didn't?

## Thought Leadership Hook

[One paragraph: what insight from building this project is worth sharing publicly?]
````

### End of Phase 3

> **Phase 3 complete.** The templates above will be written to `templates/`.  
> Any changes before I create the files?  
> Reply **"proceed"** to continue to Phase 4 (AGENTS.md + templates on disk), or request edits.

---

## Phase 4 — Write AGENTS.md and Templates to Disk

**Goal:** Write `AGENTS.md` and all template files. Every other file remains a blank stub.

### 4a — Write AGENTS.md

Create `<repo-root>/AGENTS.md`. Replace `[TOPIC]`, `[TOOL/PLATFORM]`, `[EXAM/GOAL]`, and `[SOURCE OF TRUTH]` with the actual values for this repo. The **Content Depth Rules section must be copied verbatim** — these rules are topic-agnostic and govern authoring quality for any subject.

````markdown
# AGENTS.md

This file provides guidance to agents working in this repository.

---

## What This Repo Is

A Markdown-only learning repository for **[TOPIC]**. No build system, no tests. All content is `.md` files. The agent's job is always one of: populate a stub, write an index, or update structured Markdown.

**Goal:** [EXAM/GOAL]  
**Source of truth:** [SOURCE OF TRUTH — link or description of the authoritative syllabus/exam guide]

---

## Critical Conventions

### Stub files are intentionally empty
All `.md` files (except those in `templates/`) were created as single-line stubs. An empty file is NOT missing content — populate only what the user explicitly requests.

### Never edit template originals
Templates in `templates/` are reference-only. Copy content from a template into the target file; never modify the template itself.

### Standard Chapter Template
The authoritative template is `templates/chapter-notes-template.md`. Every notes file must follow this structure in this order:

1. **TL;DR** — 2–4 sentences ending with a bolded "one thing to remember"
2. **ELI5** — Mandatory plain-language analogy section, no jargon
3. **Learning Objectives** — Specific, testable, action-verb outcomes
4. **Key Concepts** — Each sub-section: definition + mechanism + [TOOL/PLATFORM] manifestation
5. **[TOOL/PLATFORM] Implementation** — ≥2 snippets (different angles) including one anti-pattern
6. **Common Pitfalls** — Each: bolded label + why beginners make it + correct mental model
7. **Key Definitions** — Precise, scoped definitions only
8. **Summary / Quick Recall** — 3–7 scannable takeaways
9. **Self-Check Questions** — 5 questions spanning recall → application → analysis; ≥1 multi-select
10. **Further Reading** — Official docs only, all links verified

### Template → destination mapping

| Template | Destination |
|---|---|
| `chapter-notes-template.md` | `[chapter]/notes.md` (and `01_*.md`–`03_*.md` if ALLCAPS style) |
| `thought-leadership-template.md` | `[chapter]/thought-leadership.md` |
| `interview-prep-template.md` | `[chapter]/interview-prep.md` |
| `lab-template.md` | `[chapter]/LAB-XX-name.md` |
| `module-index-template.md` | `[module]/README.md` or `[module]/INDEX.md` |
| `section-index-template.md` | `[section]/README.md` or `[section]/INDEX.md` |
| `capstone-template.md` | `capstone/project-brief.md` |

### Lab numbering is global
Lab numbers run continuously across the entire repo. Never reset per section or module.

### Index placement
- Section-level index exists at scaffold time — do not recreate.
- Module-level index does not exist at scaffold time — create on request.

### External links
Official documentation only. No third-party blogs, Medium, or YouTube.  
Format: `[Title](url) — *verified YYYY-MM-DD*`  
Verify every URL with `webfetch` before writing.

---

## Content Depth Rules

These rules are topic-agnostic and govern authoring quality regardless of subject matter.

### Rule 1 — ELI5 is mandatory and must use a structural analogy
Every notes file must open with an ELI5 section after TL;DR:
- Plain English, zero jargon
- A concrete everyday analogy that maps structurally onto the technical concept
- Specific enough that a complete beginner could build the correct mental model from it
- 3–6 sentences, prose only, no bullet lists
- Non-compliant: "Think of X as a way to represent Y." (too vague — no structure)
- Compliant: names a familiar object, maps its mechanism to the technical process, explicitly corrects the most common misconception

### Rule 2 — Every concept sub-section must explain the mechanism
Each Key Concepts sub-header must answer three questions:
1. What is it? (1–2 sentence definition)
2. How does it work under the hood? (2–4 sentences on the mechanism — the process or system behaviour that produces the result)
3. Where does it appear in [TOOL/PLATFORM]? (specific command, API call, UI location, config field, or observable output)
Answering only question 1 is non-compliant.

### Rule 3 — Key Parameters sub-section is required for configurable topics
Any chapter covering a component with tunable settings must include a **Key Parameters / Configuration Knobs** table: `Parameter | What it controls | Decision rule`. The Decision rule must be a concrete actionable rule, not a restatement of the parameter's purpose. If no configurable parameters exist, write "No configurable parameters for this topic." and continue.

### Rule 4 — Worked Example is required in every chapter
Every notes file must include a **Worked Example: Requirement → Decision** sub-section following this structure:
- Given: a realistic scenario in plain English
- Step 1 — Identify the goal
- Step 2 — Define inputs
- Step 3 — Define outputs
- Step 4 — Apply constraints (constraints relevant to this domain and topic)
- Step 5 — Select the approach with a one-sentence rationale vs alternatives
If no selection decision exists, substitute a realistic failure diagnosis walkthrough.

### Rule 5 — Snippets must be scenario-first, not topic-first
Every code or config snippet must begin with a comment naming the real-world problem being solved.  
Non-compliant: `# Example: create index`  
Compliant: `# Scenario: provision a read-replica to offload reporting queries without impacting the primary`  
At least one snippet per file must be an anti-pattern (`# Anti-pattern:`) immediately followed by the corrected version with an explanation of what breaks.

### Rule 6 — Pitfalls must have three parts
Each pitfall bullet: (1) **bolded label**, (2) one sentence on why beginners make this mistake, (3) one sentence on the correct mental model. Bare bullets are non-compliant.

### Rule 7 — Answer rationales must cover all options
Every Self-Check answer must explain why the correct answer is right AND why the main distractor(s) are wrong. One-word rationales are non-compliant. For multi-select, explain why both correct answers qualify AND why the most tempting wrong answer fails.

### Rule 8 — Self-Check questions must span cognitive levels
Required distribution: Q1 recall, Q2–Q3 application, Q4–Q5 analysis/trade-off. Five recall questions is non-compliant even if one is multi-select.

---

## File Naming Rules
(Adjust based on repo naming style)
- Notes: `01_snake_case.md` / `01-kebab-case.md` (zero-padded)
- Thought leadership: `04_thought_leadership_article_template.md` / `04-thought-leadership.md`
- Labs: `LAB_XX_snake_case.md` / `LAB-XX-kebab.md` (global sequence)
- Section folders: `SECTION_XX_NAME/` or `01-name/`
- Module folders: `MODULE_XX_Name/` or `01-name/`
- Chapter folders: `CHAPTER_XX_Name/` or `01-name/`

---

## Markdown Style
- H1 for file title, H2 for major sections, H3 for sub-sections
- All code blocks carry a language tag
- Horizontal rules (`---`) separate every major section
- Self-Check answers use `<details><summary>Answer</summary>` collapsible blocks
- HTML comments (`<!-- -->`) carry authoring guidance in templates — preserve them

## What Not to Do
- Do not populate stubs without explicit user instruction
- Do not paraphrase syllabus or exam objectives — quote verbatim from the source of truth
- Do not add content not traceable to the authoritative source
- Do not renumber files or folders after scaffold — names are locked
- Do not link to third-party blogs, Medium, or YouTube
- Do not skip or merge sections without user approval
````

### 4b — Write all template files

Write all templates from Phase 3 to `<repo-root>/templates/` using the `Write` tool, with their full content exactly as presented in Phase 3. These are the only non-stub files other than `AGENTS.md` and `README.md`.

Also create `templates/README.md` listing each template file and its destination.

### End of Phase 4

> **Phase 4 complete.** `AGENTS.md` and all templates written.  
> Reply **"proceed"** to continue to Phase 5 (scaffold stubs + README), or request changes.

---

## Phase 5 — Scaffold Stubs and README

**Goal:** Create every folder, every stub file, and the root `README.md`.

### Stub rule

Every file outside `templates/` and outside `AGENTS.md`/`README.md` contains exactly one line:

```
<!-- stub: populate using templates/ -->
```

No headings, no tables, no prose — one comment line only. This applies to: all section/module/chapter content files, `progress-tracker.md`, `00-roadmap/learning-roadmap.md`, all capstone files.

### Section and module index stubs

Section and module index files are stubs at scaffold time:

```markdown
<!-- stub: populate using templates/section-index-template.md -->
```

```markdown
<!-- stub: populate using templates/module-index-template.md -->
```

### README.md

The root `README.md` is the one file that gets real content at scaffold time. Write it with:

- **H1 title** — the actual topic/certification name
- **Goal statement** — what this repo is, who it is for, what the reader can do after completing it
- **Learning path table** — Phase | Section | Estimated hours | Focus area
- **Repository structure** — folder tree (top 2–3 levels only)
- **Section summaries** — one bullet per section with a relative link and a one-line description
- **File type guide** — File type | Pattern | Purpose | Created at scaffold?
- **Certification / exam target** — include only if a cert exists; omit if pure learning

Use only the user's topic name, section names, and goal — no generic boilerplate or assumed tool names.

### Use TodoWrite for large repos

For repos with more than 30 files, use the `TodoWrite` tool to track scaffold progress: mark each section `pending` → `in_progress` → `completed` as its files are written. Write one section at a time.

### End of Phase 5

Report the scaffold summary:

```
Repo:                  [name]
Sections:              N
Modules:               N
Chapters:              N
Notes stubs:           N
Thought leadership:    N  (stubs)
Interview prep:        N  (stubs, if applicable)
Lab stubs:             N  (if applicable)
Capstone stubs:        N
Template files:        N  (fully populated)
AGENTS.md:             1  (fully populated)
README.md:             1  (fully populated)
────────────────────────────────
Total files:           N
```

Then tell the user:

> "All content files are blank stubs. Ask me to populate any file, chapter, or section and I will follow the Standard Chapter Template from `templates/chapter-notes-template.md` and the Content Depth Rules in `AGENTS.md`."

Remind the user that:
- Module-level index files are created on request, not at scaffold time
- Thought leadership files are best populated after the notes files are written, since they draw on what was learned during authoring

---

## Phase 6 — Git Initialisation

**Goal:** Initialise git (if not already a repo) and give the user a ready-to-run first-commit command. Run this phase immediately after Phase 5 is confirmed — no additional confirmation gate needed.

1. Check whether a `.git` directory exists in the repo root. If not, run `git init`. If yes, skip.

2. Print this block verbatim, substituting `[TOPIC]`:

---
**Your skeleton repo is ready. Capture the baseline:**

```bash
git add .
git commit -m "chore: initial skeleton, templates, and stubs for [TOPIC]"
```

This commit captures the folder structure, templates, and `AGENTS.md` before any content authoring begins. It gives you a clean baseline to branch from for each section.

**Next step:** read `templates/authoring-guidelines.md`, then start populating stubs section by section using `templates/chapter-notes-template.md`.

---

**Done. Your [TOPIC] learning repo is scaffolded and ready.**

---

## Constraints and Guardrails

- **Templates and AGENTS.md are the only files with content.** `README.md` also gets content. Everything else is one stub line. No exceptions.
- **Never assume tool names, vendor names, cloud providers, or platform names.** Derive everything from what the user said. Never default to any specific technology in folder names, template language, or AGENTS.md.
- **Folder and file names use the actual subject names** — not generic placeholders like `module-1` or `chapter-a`.
- **One phase per response.** Never combine phases. Each phase (except Phase 6) ends with an explicit confirmation gate.
- **Always fetch live information in Phase 1.** Never invent curriculum structure from training data alone.
- **If the hour budget is unrealistic**, say so with a reasoned alternative before proceeding. A typical chapter is 1.5–3 hours; flag any scope that cannot fit within the user's budget.
- **Always cite sources** with URL and retrieval date in the Phase 1 summary.
- **Always use TodoWrite** to track progress when file count exceeds 30.
- **Windows MAX_PATH:** Proactively shorten deep path components for Windows compatibility. Note any shortenings in the relevant index file.

---

## Portability — Using This Skill on Other Platforms

This skill is written in the `SKILL.md` format for OpenCode. The workflow, phases, and constraints are platform-agnostic.

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/create-learning-repo.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full content (below frontmatter) as your first message before describing the task |

**To install for all projects (OpenCode):**
```bash
# macOS / Linux
cp -r create-learning-repo ~/.config/opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse create-learning-repo "$env:USERPROFILE\.config\opencode\skills\"
```

**To install for one project only:**
```bash
# macOS / Linux
cp -r create-learning-repo .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse create-learning-repo .opencode\skills\
```
