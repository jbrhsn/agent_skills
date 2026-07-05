---
name: create-learning-repo
description: Use when user asks to create a learning repository, study guide, certification prep repo, or expert knowledge base for any topic or certification. Guides the agent through intake, live web research, folder structure design, template generation, and skeleton file scaffolding — confirmed phase by phase. Creates blank stubs for all content files; only templates/ is populated. Do NOT use for editing an existing repo's content.
---

# Create Learning Repo — Skill

## When to use this skill

Trigger on any request that matches:
- "create a learning repo for X"
- "build a study guide for Y certification"
- "set up a knowledge base to learn Z"
- "I want to become an expert in / thought leader on X"
- "create a certification prep repo for X"
- "scaffold a learning repo"

Do NOT trigger if the user is asking to add content to an **existing** learning repo — that is content authoring, not repo creation.

---

## Core principles

1. **Always fetch live information first.** Never invent curriculum structure from training data alone. Product names, exam blueprints, and API surfaces change. Always fetch official sources and note the retrieval date.
2. **Progress in confirmed phases.** Present output at the end of each phase and wait for explicit user confirmation before proceeding. Never run two phases in one response.
3. **Skeleton only — no content authoring.** Your job is folder structure, blank stubs, and template files. The only files with real content are the files inside `templates/`. Everything else — roadmap, progress tracker, section READMEs, module READMEs, chapter files, capstone files, root README — is a blank stub with a single placeholder comment. Content authoring is a separate workflow done after the skeleton exists.
4. **Intent-driven file types.** Chapter file types are determined by the user's learning goal, not a fixed default.
5. **Templates are the only populated files.** `templates/` contains full, authoritative template scaffolds. All other files are empty stubs pointing authors to those templates.

---

## Phase 0 — Intake

**Before doing any research or design**, ask the user these five questions in a single message. Do not proceed until all five are answered (or the user explicitly skips one).

```
To design the right repo for you, I need a few details:

1. **Topic / Certification:** What is the exact topic or certification name?
   (e.g. "AWS Solutions Architect Associate", "Apache Kafka", "System Design")

2. **Learning goal:** What do you want to achieve? Choose all that apply:
   a) Pass a certification exam
   b) Get a job / ace interviews in this area
   c) Write articles, blog posts, or build a public thought-leadership profile
   d) Deep personal mastery (no external output goal)
   e) Other — describe it

3. **Current level:** How would you rate your current knowledge?
   (Complete beginner / Some exposure / Adjacent expert / Practitioner already)

4. **Time budget:** How many total hours do you want to invest in learning this topic?
   (e.g. 40 hrs, 80 hrs — I'll flag if the budget seems too tight or too generous)

5. **Seed URLs (optional):** Do you have specific documentation pages, exam guides,
   or reference links you want me to use as primary sources?
   (Leave blank if not — I'll find them myself)
```

### Intent logic (run silently after user answers)

After reading the answers, decide which chapter file types to generate:

| Detected intent | Additional files per chapter |
|---|---|
| Goal includes (c) — articles / thought leadership / public profile | `thought-leadership.md` |
| Goal includes (b) — interviews / job / career | `interview-prep.md` |
| Goal is ambiguous (e.g. "learn deeply" with no mention of output) | Ask: "Should I also generate thought-leadership.md and/or interview-prep.md files per chapter, for future use?" |
| Goal is only (a) or (d) | `notes.md` only — no extra files |

Record the file-type decision before proceeding to Phase 1.

---

## Phase 1 — Research

**Goal:** Produce a research summary grounded in live sources that will drive the structure in Phase 2.

### Step 1 — WebFetch (primary source)

Attempt ALL of the following fetches in parallel. Note retrieval date for each.

1. **Official exam blueprint** (if a certification exists):
   - Try: `https://aws.amazon.com/certification/` (AWS), `https://cloud.google.com/learn/certification` (GCP), `https://learn.microsoft.com/en-us/certifications/` (Azure), `https://www.databricks.com/learn/certification` (Databricks), or search `[CERT NAME] exam guide official` to find the right URL.
   - Target: exam domains, domain weightings (%), question count, passing score, retake policy, cost.

2. **Official documentation landing page** for the technology:
   - Target: product overview, key concepts, current version, major recent changes.

3. **Any seed URLs the user provided in Phase 0.**

4. **"What's new" or changelog page** (if one exists):
   - Target: changes in the last 12–18 months that would affect what to learn.

### Step 2 — AI query stubs (fallback + supplement)

After fetching, for any area where WebFetch returned thin or no content, generate ready-to-paste prompts. Format them exactly like this so the user can copy-paste into ChatGPT / Claude / Gemini:

---
**If any of the above fetches failed or returned thin results, paste this into ChatGPT / Claude / Gemini and share the response back:**

> You are an expert in [TOPIC/CERTIFICATION]. Please provide a detailed answer to all four questions below. Be specific; cite sources where possible.
>
> 1. What are the official exam domains and their percentage weightings for [CERT NAME]? Include total question count, passing score, exam duration, and cost.
> 2. What is the canonical beginner → intermediate → advanced → expert skill progression for [TOPIC] as taught by leading courses, books, and practitioners?
> 3. What are the core prerequisite skills and knowledge someone should verify they have before starting to study [TOPIC]?
> 4. What are the most significant changes or additions to [TOPIC] in the last 12–18 months that any learner must know about?
---

### Step 3 — Compile research summary

Present a structured research summary with these sections:

```markdown
## Phase 1 Research Summary — [TOPIC]

**Sources consulted:**
- [URL] — retrieved [DATE] — [one-line description of what was found]
- [URL] — retrieved [DATE] — ...

**Exam blueprint** (if applicable):
- Domains: [list with % weights]
- Format: [N questions / N minutes / passing score / cost]
- Retake policy: [...]
- Prerequisites: [...]

**Canonical skill progression:**
- Beginner: [...]
- Intermediate: [...]
- Advanced: [...]
- Expert: [...]

**Core prerequisites** (what to verify before starting):
- [...]

**Recent shifts (last 12–18 months):**
- [...]

**Fast-evolving areas** (likely to change within 6–12 months; flag in content):
- [...]

**Recommended section sequence for the repo:**
- Section 01: [name] — rationale
- Section 02: [name] — rationale
- ...
```

**If the topic has no formal certification**, drop exam-blueprint fields and note it explicitly. Keep all other fields.

### End of Phase 1

> **Phase 1 complete.** Here is the research summary above.
> Does this look accurate? Any corrections or additional context before I design the folder structure?
> Reply **"proceed"** (or any confirmation) to continue to Phase 2, or give me corrections first.

---

## Phase 2 — Repository Structure

**Goal:** Design the full folder and file hierarchy. Present the tree and wait for confirmation.

### Naming and nesting rules

```
[topic-slug]-learning-repo/
├── README.md                              ← blank stub (one placeholder line)
├── 00-roadmap/
│   └── learning-roadmap.md               ← blank stub (one placeholder line)
├── templates/
│   ├── chapter-notes-template.md         ← POPULATED (full template content)
│   ├── section-readme-template.md        ← POPULATED (full template content)
│   ├── module-readme-template.md         ← POPULATED (full template content)
│   ├── authoring-guidelines.md           ← POPULATED (full template content)
│   ├── thought-leadership-template.md    ← POPULATED — only if intent detected in Phase 0
│   └── interview-prep-template.md        ← POPULATED — only if intent detected in Phase 0
├── 01-[section-name]/
│   ├── README.md                         ← blank stub
│   ├── 01-[module-name]/
│   │   ├── README.md                     ← blank stub
│   │   ├── 01-[chapter-name]/
│   │   │   ├── notes.md                  ← blank stub
│   │   │   ├── thought-leadership.md     ← blank stub — only if intent detected
│   │   │   └── interview-prep.md         ← blank stub — only if intent detected
│   │   └── 02-[chapter-name]/
│   │       └── ...
│   └── 02-[module-name]/
│       └── ...
├── 02-[section-name]/
│   └── ...
├── ...
├── capstone/
│   ├── README.md                         ← blank stub
│   └── submission-template.md            ← blank stub
└── progress-tracker.md                   ← blank stub (one placeholder line)
```

### Structural rules

- **Sections** map to a natural difficulty ramp: Foundations → Core Competency → Advanced / Specialized → Expert Practice.
- If a formal certification exists, the final section before the capstone must be dedicated to **exam prep** (mock questions, common pitfalls, exam strategy, timing).
- **Every folder** is prefixed `01-`, `02-`, etc. for correct sort order. Use only lowercase, hyphens — no spaces, no underscores, no camelCase.
- **Folder names use the actual technology/framework name** — not generic placeholders. If the user says "LangGraph" (not "LangChain"), the folder says `langgraph`, not `langchain`. Get this right in Phase 2, not after.
- Each chapter is sized for approximately **1.5–3 hours** of study (one focused sitting).
- Total hours across all chapters must sum to approximately the user's Phase 0 budget. If the budget is unrealistic, say so now and suggest an alternative.
- The `capstone/` directory must cover at least two sections' worth of skills.
- `README.md` at the root is a **blank stub** — it is created as an empty file in Phase 4. Content is filled by the author later.

### Present the tree

Show the complete folder + file tree with:
- Estimated hours next to each chapter
- Exam domain mapping next to each section (if cert exists)
- Total hours sum at the bottom
- A one-line note on any fast-evolving areas flagged in Phase 1
- Clear annotation: `← POPULATED` next to template files, `← stub` next to everything else

### End of Phase 2

> **Phase 2 complete.** Does this structure look right?
> Confirm folder names, section order, chapter sizing, and total hours.
> Reply **"proceed"** to continue to Phase 3 (templates), or request changes.

---

## Phase 3 — Templates

**Goal:** Generate all template files. Present them in full and wait for confirmation.

### Always generate these four

#### 3a. `chapter-notes-template.md`

```markdown
# [Chapter Title]

**Section:** [Section Name] | **Module:** [Module Name] | **Est. time:** [X hrs] | **Exam mapping:** [Domain / objective, or "Supporting content"]

## Learning Objectives

By the end of this chapter you will be able to:
- [ ] [Action-verb outcome 1 — specific and testable]
- [ ] [Action-verb outcome 2]
- [ ] [Action-verb outcome 3–5 total]

## Core Concepts

<!-- ===================================================================
     AUTHORING NOTE: This section is ~80% of your effort.
     Teach the ideas — don't just list them. Use analogies, diagrams
     (ASCII or Mermaid), and concrete examples. Assume the reader knows
     prerequisites but is new to this specific topic.
     =================================================================== -->

[Explain foundational ideas, definitions, and mental models here.]

## Deep Dive / Advanced Topics

<!-- ===================================================================
     AUTHORING NOTE: ~15% of effort.
     Mechanics, nuance, edge cases, "why it works this way."
     This is where intermediate and expert understanding diverge.
     =================================================================== -->

[Advanced mechanics, internals, and edge cases.]

## Worked Examples & Practice

<!-- ===================================================================
     AUTHORING NOTE: ~5% of effort, but non-negotiable.
     At least one complete end-to-end example. Show realistic inputs,
     realistic outputs, and at least one failure mode or edge case.
     =================================================================== -->

[Complete worked example(s) with realistic context.]

## Common Pitfalls & Misconceptions

| Pitfall | Why it happens | Fix |
|---|---|---|
| [Pitfall 1] | [Root cause] | [Correct approach] |
| [Pitfall 2] | [Root cause] | [Correct approach] |

## Key Definitions

| Term | Definition |
|---|---|
| [Term] | [Precise, scoped definition — not a dictionary entry] |

## Summary / Quick Recall

- [Key takeaway 1 — one line]
- [Key takeaway 2]
- [Key takeaway 3–7 total; designed for pre-exam scan]

## Self-Check Questions

1. [Question 1 — answerable only after reading this chapter]

   <details><summary>Answer</summary>

   [3–5 sentence answer with substance, not just "yes, correct."]

   </details>

2. [Question 2]

   <details><summary>Answer</summary>

   [Answer]

   </details>

3–5. [Continue for 5 questions total]

## Further Reading

- [Title](URL) — [one-line description; note if likely to go stale]
- [Title](URL) — [one-line description]
- [Title](URL) — [one-line description]
```

#### 3b. `module-readme-template.md`

```markdown
# [Module Name]

**Part of:** [Section Name] | **Estimated time:** [X hrs] | **Prerequisites:** [Prior module, or "None"] | **Exam mapping:** [Domain / objective]

## Overview

[1–2 sentences: what this module covers and why it matters in the larger learning arc.]

## Learning Outcomes

By completing this module, you will be able to:
- [Outcome 1]
- [Outcome 2]
- [Outcome 3–5 total]

## Topics Covered

| # | Chapter | Est. time | File |
|---|---|---|---|
| 1 | [Chapter name] | [X hrs] | [link to notes.md] |
| 2 | [Chapter name] | [X hrs] | [link to notes.md] |

## How This Module Fits

[Brief context: what came before, what this unlocks, what comes next.]

## Study Tips

[Specific, practical advice for this module — tools to set up, mindset, common pacing mistakes. Generic advice (e.g. "take notes") does not belong here.]
```

#### 3c. `section-readme-template.md`

```markdown
# [Section Name]

**Estimated time:** [X hrs] | **Exam domain weight:** [~X% of exam, or "N/A"] | **Prerequisites:** [Prior section, or "None"]

## Overview

[2–3 sentences: scope of this section, what phase of the learning arc it covers, and why it matters.]

## Learning Outcomes

By completing this section, you will be able to:
- [Outcome 1]
- [Outcome 2]
- [Outcome 3–5 total]

## Modules in This Section

| # | Module | Est. time | Chapters |
|---|---|---|---|
| 1 | [Module name] | [X hrs] | [N chapters] |
| 2 | [Module name] | [X hrs] | [N chapters] |

## How This Section Fits

[How it connects to the previous section and what it unlocks for the next.]

## Study Tips

[Section-specific advice — lab environments to set up, things to review from prerequisites, known difficulty spikes.]
```

#### 3d. `authoring-guidelines.md`

```markdown
# Authoring Guidelines & Quality Rubric

## Expectations for Authors

### Tone & Voice
- Write for **learning**, not just documentation. Explain *why* things work the way they do.
- Active voice. Concrete examples over abstract definitions.
- "Knowledgeable colleague explaining at a whiteboard" — not a textbook, not a marketing page.
- Assume the reader knows prerequisites but is new to this specific topic.

### Depth calibration
- **Core Concepts** = ~80% of authoring effort. This is where teaching happens.
- **Deep Dive** = ~15%. Expert-level nuance, internals, edge cases.
- **Worked Examples** = ~5% but non-negotiable. At least one end-to-end, realistic example per chapter.
- Do not invert these proportions. A chapter with 10 examples and 2 paragraphs of explanation teaches nothing.

### Worked Examples
- Every chapter must have **at least one complete end-to-end example**.
- Examples must be realistic — not toy/contrived problems.
- Show at least one failure mode or edge case per chapter.
- If the topic involves code: examples must be runnable (correct imports, no placeholder variables).

### Self-Check Questions
- Must be answerable **only** after reading the chapter.
- Avoid questions that can be Googled directly (test understanding, not recall).
- Use `<details><summary>Answer</summary>` collapse for all answers.
- Answers must be 3–5 substantive sentences — not "yes, that's correct."

### Exam alignment (if certification exists)
- Each chapter header lists its **Exam mapping** field.
- Distinguish clearly between "cert-required knowledge" and "depth/mastery knowledge."
- Chapters in the exam-prep section must include realistic question formats (multiple-choice with 4 options and explanation of the correct answer).
- **Blueprint drift warning:** Databricks, AWS, GCP, and similar vendors update exam objectives frequently. If you are authoring more than 6 months after the repo was created, verify the current official exam guide before writing.

### Source hygiene
- Always cite the source URL and retrieval date when using a specific doc, API reference, or changelog entry.
- Flag any section that covers a fast-evolving feature with: `> ⚠️ Fast-evolving: verify against current docs before relying on this.`

## Quality Checklist (run before marking a chapter complete)

- [ ] Learning objectives are specific and testable (action verbs: "implement", "diagnose", "compare" — not "understand" or "know")
- [ ] Core Concepts section teaches, not just lists
- [ ] Deep Dive adds meaningful expert-level depth
- [ ] All worked examples are complete, realistic, and runnable (if code)
- [ ] At least one failure mode or edge case shown
- [ ] Common Pitfalls are specific and grounded (not generic)
- [ ] Key Definitions are accurate and scoped to this chapter's context
- [ ] Summary is scannable and covers all main takeaways
- [ ] Self-Check questions are answerable only after reading; answers are substantive
- [ ] Further Reading links are current and high-quality
- [ ] No filler or padding — every sentence earns its space
- [ ] Tone is conversational but authoritative
- [ ] All sources cited with URL and retrieval date

## Templates as Living Documents

These templates evolve. If authoring a chapter reveals a gap in the template, flag it for discussion rather than silently working around it. Document the gap in the PR or session notes.
```

### Conditionally generate (based on Phase 0 intent)

#### 3e. `thought-leadership-template.md` ← only if thought leadership detected

```markdown
# [Chapter Title] — Thought Leadership

**Section:** [Section Name] | **Target audience:** [e.g. "Senior engineers", "Tech decision-makers", "General tech audience"] | **Target publication:** [e.g. personal blog, Medium, LinkedIn, conference talk]

## Hook / Opening Thesis

[1–2 sentences that would stop a busy person scrolling. What is the non-obvious claim or insight this piece makes?]

## Key Claims (3–5)

1. [Claim 1 — specific and defensible, not generic]
2. [Claim 2]
3. [Claim 3]

## Supporting Evidence & Examples

[For each key claim: data, case study, observed pattern, or first-hand experience that backs it up.]

## The Original Angle

[What does this piece say that you cannot find elsewhere? Why are YOU the right person to say it?]

## Counterarguments to Address

[What would a skeptical expert push back with? Acknowledge and respond to the strongest objections.]

## Practical Takeaways for the Reader

- [What can the reader do differently after reading this?]
- [Concrete action or mental model shift]

## Call to Action

[What do you want the reader to do next? Subscribe, reply, try something, share a perspective?]

## Further Reading / References

- [Source](URL) — [why it supports the argument]
```

#### 3f. `interview-prep-template.md` ← only if interview intent detected

```markdown
# [Chapter Title] — Interview Prep

**Section:** [Section Name] | **Role target:** [e.g. "Senior ML Engineer", "Data Engineer", "Solutions Architect"]

## Core Questions (Conceptual)

These test whether you understand the fundamentals — expect them in any interview for this topic.

| Question | Key points to cover | Common trap |
|---|---|---|
| [Question 1] | [2–3 bullet points] | [What weak candidates say] |
| [Question 2] | [...] | [...] |
| [3–5 questions total] | | |

## Applied / Scenario Questions

These test whether you can apply the knowledge under realistic constraints.

**Q:** [Scenario question 1 — describe a realistic engineering situation]

**Strong answer framework:**
- [Point 1]
- [Point 2]
- [How to show tradeoff awareness]

**Q:** [Scenario question 2]
...

## System Design / Architecture Questions (if applicable)

**Q:** [Design question]

**Approach:**
1. [Step 1 — clarify requirements]
2. [Step 2 — propose structure]
3. [Step 3 — justify choices, name tradeoffs]

## Vocabulary to Use

These terms signal expertise in this area. Use them naturally — don't force them.
- [Term 1] — [when/why to use it]
- [Term 2] — ...

## Vocabulary to Avoid

These phrases signal shallow understanding or outdated knowledge.
- [Term / phrase] — [why it signals weakness]

## STAR Answer Frames

For behavioral questions about this topic area:

**Situation template:** [Setup a realistic scenario using this chapter's concepts]
**Task:** [What you were responsible for]
**Action:** [Specific technical decisions you made and why]
**Result:** [Quantified outcome if possible]

## Red Flags to Watch For

[Things interviewers flag as signs of a weak candidate in this specific area — not generic interview advice.]
```

### End of Phase 3

> **Phase 3 complete.** The templates above will be written to the `templates/` folder.
> Any changes before I create all the files?
> Reply **"proceed"** to continue to Phase 4 (file creation), or request edits.

---

## Phase 4 — Delivery

**Goal:** Create all directories and files on disk. Templates get full content. Everything else is a blank stub.

### Rule: two categories of files, strictly separated

| Category | Files | What to write |
|---|---|---|
| **Populated** | Everything inside `templates/` | Full template content from Phase 3 — exactly as presented |
| **Blank stubs** | Every other file in the repo | A single HTML comment: `<!-- stub: populate using templates/ -->` |

That's the complete rule. There are no exceptions.

### What to create

1. **Full directory tree** — every folder and file from the Phase 2 tree. Create all directories first, then write each file.

2. **`templates/` folder** — write all template files from Phase 3 with their complete content. These are the only files with real content.

3. **All other files** — write each with exactly this single line and nothing else:
   ```
   <!-- stub: populate using templates/ -->
   ```
   This applies to: `README.md`, `00-roadmap/learning-roadmap.md`, `progress-tracker.md`, all section `README.md` files, all module `README.md` files, all chapter `notes.md` files, all conditional chapter files (`thought-leadership.md`, `interview-prep.md`), `capstone/README.md`, `capstone/submission-template.md`.

### What NOT to do

- Do NOT write any prose, tables, headers, or placeholder text into stubs — one comment line only.
- Do NOT pre-fill chapter headers, section names, or time estimates into stub files.
- Do NOT generate roadmap content, progress tracker tables, or capstone briefs.
- Do NOT write mock exam questions or any learning content anywhere.

### End of Phase 4

> **Phase 4 complete.** All [N] directories and [N] files created.
> - `templates/` — [N] files, fully populated
> - Stubs — [N] files, one placeholder line each
> - Total: [N] files across [N] directories
>
> Reply **"proceed"** to continue to Phase 5 (initialize git + first-commit guide), or stop here.

---

## Phase 5 — Git initialization & first-commit guide

**Goal:** Initialize git (if not already a repo) and give the user a ready-to-run first-commit command.

### What to do

1. Check if a `.git` directory already exists in the repo root.
   - If not: run `git init`.
   - If yes: skip.

2. Print the following block verbatim (substituting the actual topic slug):

---
**Your skeleton repo is ready. Run this to capture the baseline:**

```bash
git add .
git commit -m "chore: initial skeleton, templates, and stubs for [TOPIC]"
```

This commit captures the folder structure and templates before any content authoring begins. It gives you a clean baseline to branch from for each section.

**Next step:** open `templates/authoring-guidelines.md` to understand the authoring workflow, then start populating stubs section by section using `templates/chapter-notes-template.md`.

---

**Phase 5 complete. Skeleton repo is ready.**

Summary:
- [N] sections, [N] modules, [N] chapters
- [N] template files written to `templates/`
- [N] blank stubs created across all sections
- Total estimated learning time: [X hrs]
- Next action: author content section by section, starting with `01-[section]/`

---

## Constraints

- **Templates are the only files with content.** Everything outside `templates/` is a blank stub — one HTML comment line. No exceptions.
- **If the hour budget is unrealistic**, push back with a reasoned alternative. A typical chapter is 1.5–3 hrs. If the user says "learn Kubernetes in 5 hours," explain why that's insufficient and suggest a scoped alternative (e.g. "Kubernetes for App Developers in 20 hrs").
- **Always cite sources** with URL and retrieval date in the Phase 1 research summary.
- **Flag fast-evolving topics** in the Phase 1 summary and Phase 2 tree annotations. Authors will handle callouts when they populate content.
- **Folder and file names must use actual technology names**, not generic placeholders. If the user says "LangGraph", write `langgraph` in the folder name.
- **One phase per response.** Never run Phase 2 and Phase 3 in the same response. Each phase ends with an explicit confirmation gate.
- **Phase 5 has no confirmation gate** — after Phase 4 is confirmed, run Phase 5 (git init check + first-commit guide) immediately without asking.

---

## Reference: directory layout for this skill

```
~/.config/opencode/skills/create-learning-repo/
└── SKILL.md       ← this file
```

To make this skill available to all projects on this machine, it lives in global scope.
To restrict it to one project, move it to `.opencode/skills/create-learning-repo/SKILL.md`
inside that project's root.
