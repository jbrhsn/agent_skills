---
name: create-learning-repo
description: Use when the user wants to create a learning repository, study guide, certification prep repo, or expert knowledge base for any topic or certification. It runs a delegation-model workflow of self-contained units — intake, live web research, folder-structure design, template generation, AGENTS.md authoring, blank-stub scaffolding, and git init — where every phase confirmation is an explicit STOP GATE handed back to the user/orchestrator. It creates blank stubs for all content files; only templates/ (and AGENTS.md/README.md) get real content. Do NOT use for editing an existing repo's content.
---

# Create Learning Repo

This skill creates a complete, opinionated Markdown-based learning repository for any topic or certification. It is fully generic — no tool names, vendor names, or repo paths are hardcoded. Everything is derived from the user's inputs.

The workflow is a sequence of discrete **units** (U0 → U6). Each unit has a **Goal/scope**, **Inputs**, **Do**, a **Self-verify** step, and a terse **Report contract**. Most units end with an explicit **STOP GATE (hand back)** where the unit's output is presented and control returns to the user/orchestrator for approval before the next unit runs. **No two units run in the same response**, and a STOP GATE is never combined with the next unit.

**What gets created:**
- A structured folder tree (sections → modules → chapters)
- A `templates/` directory — the only directory with real content (plus `AGENTS.md` and `README.md`)
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

Do **not** trigger if the user is asking to add content to an existing repo — that is content authoring (use `author-chapter`), not repo creation.

---

## Shared reference material (defined once — referenced by the units)

Every unit below points to this section instead of restating rules. Do not duplicate this material inside a unit.

### Naming conventions

Apply the style the user chose in **Unit U0** (or default to lowercase-hyphen if unspecified).

**Lowercase-hyphen style (default):**

| Level | Format |
|---|---|
| Repo root | `topic-slug` chosen or derived |
| Section | `01-section-name/` |
| Module | `01-module-name/` |
| Chapter | `01-chapter-name/` |

**ALLCAPS-underscore style (if user selected):**

| Level | Format |
|---|---|
| Repo root | User-specified or derived |
| Section | `SECTION_XX_DESCRIPTIVE_NAME/` |
| Module | `MODULE_XX_Descriptive_Name/` |
| Chapter | `CHAPTER_XX_Descriptive_Name/` |

**Rules that apply regardless of style:**
- Use the **actual technology/subject names** in folder names — never generic placeholders like `module-1` or `chapter-a`.
- Every folder is numerically prefixed for correct sort order.
- No spaces in any path component.
- **Windows MAX_PATH caution:** Full paths over ~220 characters fail silently on Windows. Apply the 40-character component cap below proactively and note any shortenings in the parent section index.

### Slug derivation algorithm

Use this deterministic algorithm when deriving a folder or file slug from a chapter/module/section name. Apply it consistently — it prevents silent MAX_PATH failures and collision ambiguity.

**Steps (apply in order):**
1. Lowercase the entire name.
2. Replace any character that is not a letter, digit, or space with a space.
3. Collapse all whitespace runs to a single hyphen (or underscore for ALLCAPS style).
4. Trim leading and trailing hyphens/underscores.
5. **Cap each component at 40 characters,** truncating at the last complete word boundary before the limit (never cut mid-word).
6. For ALLCAPS style: uppercase the result and replace hyphens with underscores.

**Collision rule:** If two slugs under the same parent are identical after applying steps 1–6, append a numeric disambiguator to the later one: `-2`, `-3`, … (or `_2`, `_3` for ALLCAPS). Record the collision in the parent index file.

**Recording shortenings:** Any component that was truncated in step 5 must be noted in the parent section or module index, mapping the shortened slug back to the original full name. This ensures forward links remain navigable.

**Worked application of the algorithm:**
- A name at or under 40 characters passes through steps 1–4 unchanged (aside from case/separator normalisation) and is used as-is.
- A name longer than 40 characters is truncated at the last word boundary that keeps the slug within 40 characters; the dropped words are recorded in the parent index per the shortening rule above.
- Two chapters under the same parent that normalise to the same slug get `-2`/`-3` (or `_2`/`_3`) suffixes in scaffold order.

### File naming conventions

| File type | Pattern | Notes |
|---|---|---|
| Topic notes (ALLCAPS style) | `01_snake_case.md` … `03_snake_case.md` | 3 per chapter by default |
| Topic notes (hyphen style) | `01-snake-case.md` … `03-snake-case.md` | 3 per chapter by default |
| Thought leadership | `NN-thought-leadership.md` / `NN_thought_leadership.md` | `NN` = (topic-note count + 1). See numbering rule below. |
| Interview prep | `NN-interview-prep.md` / `NN_interview_prep.md` | `NN` = (topic-note count + 2 if thought leadership also present, else + 1). Only if intent detected. |
| Lab file | `LAB-XX-name.md` / `LAB_XX_name.md` | Global sequence — never reset |
| Section index | `README.md` or `INDEX.md` inside section folder | Created at scaffold time |
| Module index | Not created at scaffold time — on request only | |

**Per-chapter file numbering rule.** Auxiliary files are numbered **sequentially after the topic notes**, in this fixed order: topic notes → thought leadership → interview prep. The number of topic notes (3 standard, 4 for dense chapters) determines the starting point; there is no fixed number for any auxiliary file.

| Chapter config | Topic notes | Thought leadership | Interview prep |
|---|---|---|---|
| 3 notes, no aux | `01`–`03` | — | — |
| 3 notes + thought leadership | `01`–`03` | `04` | — |
| 3 notes + interview prep | `01`–`03` | — | `04` |
| 3 notes + both | `01`–`03` | `04` | `05` |
| 4 notes (dense) + both | `01`–`04` | `05` | `06` |

This ordering is deterministic: interview prep always takes the number *after* thought leadership when both are present, so the two never collide regardless of topic-note count.

**Topic file count per chapter.** Standard is 3 topic notes + any auxiliary files (thought leadership / interview prep) detected in U0. Dense chapters (user-confirmed during U0) use 4 topic notes + auxiliary files. Ask the user to confirm during U0 if any sections should use 4 topic notes — do not assume based on position.

### Filename lock and forward-link contract

**Filenames are locked after the U5 scaffold.** Once the scaffold is written, file and folder names must not be changed. This is the forward-link contract: authored chapters may link to files that do not yet have content (because they will be populated later). Those links resolve correctly as long as names stay stable. Renaming to "fix" a broken-looking link breaks every other link to that file.

- Record the locked names in the U2 tree output so the user has a stable reference.
- Use relative paths for all cross-references between files, so links resolve regardless of where the repo lives on disk.

### Full repo tree structure

```
[repo-root]/
├── README.md                        ← populated (written in U5)
├── AGENTS.md                        ← populated (written in U4)
├── templates/
│   ├── README.md                    ← POPULATED (lists templates + destinations)
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
- Each chapter is sized for **1.5–3 hours** of focused study.
- The capstone must draw on skills from at least two sections.

### Template manifest (source of truth for which files exist and when)

Template bodies are **never** inlined into this SKILL.md — they live in `reference/` (relative to this skill's base directory) and are read on demand. Copy them verbatim; never paraphrase or abbreviate.

| File | Reference source | Destination in repo | When generated |
|---|---|---|---|
| `chapter-notes-template.md` | `reference/chapter-notes-template.md` | `templates/chapter-notes-template.md` | Always |
| `section-index-template.md` | `reference/section-index-template.md` | `templates/section-index-template.md` | Always |
| `module-index-template.md` | `reference/module-index-template.md` | `templates/module-index-template.md` | Always |
| `authoring-guidelines.md` | `reference/authoring-guidelines.md` | `templates/authoring-guidelines.md` | Always |
| `capstone-template.md` | `reference/capstone-template.md` | `templates/capstone-template.md` | Always |
| `thought-leadership-template.md` | `reference/thought-leadership-template.md` | `templates/thought-leadership-template.md` | Goal (c) detected in U0 |
| `interview-prep-template.md` | `reference/interview-prep-template.md` | `templates/interview-prep-template.md` | Goal (b) detected in U0 |
| `lab-template.md` | `reference/lab-template.md` | `templates/lab-template.md` | Labs requested in U0 |

**Key sections in `chapter-notes-template.md`** (the core template every notes file follows):
TL;DR → ELI5 → Learning Objectives → Visual Overview (recommended) → Key Concepts (definition + mechanism + platform manifestation per sub-section) → Key Parameters table → Worked Example (Requirement → Decision, 5 steps) → Implementation (≥2 snippets, ≥1 anti-pattern) → Common Pitfalls (3-part format) → Key Definitions → Summary / Quick Recall → Self-Check Questions (5 Qs spanning recall/application/analysis, ≥1 multi-select, all answers with rationale) → Further Reading (official docs only, verified URLs).

**Key sections in `authoring-guidelines.md`**: Voice & Tone → Depth Calibration → ELI5 Requirements → Worked Examples → Visual Overview guidelines → Self-Check Questions → Source Hygiene → Blueprint Drift Warning → Quality Checklist.

**On-demand template display.** If the user asks to see a specific template ("show me the chapter-notes template", "what does the lab template look like"), read the relevant `reference/<name>` file and display it in full. Do not pre-display all templates in a single message.

### Constraints and guardrails (non-negotiable, all units)

- **Templates and `AGENTS.md` are the only files with content.** `README.md` also gets content. Everything else is one stub line. No exceptions.
- **Never assume tool names, vendor names, cloud providers, or platform names.** Derive everything from what the user said. Never default to any specific technology in folder names, template language, or `AGENTS.md`.
- **Folder and file names use the actual subject names** — not generic placeholders. Apply the deterministic slug algorithm consistently.
- **One unit per response.** Never combine units. Each STOP GATE hands control back before the next unit runs.
- **Always fetch live information in U1.** Never invent curriculum structure from training data alone.
- **Hour budget must reconcile.** If the U0 budget is outside [chapters × 1.5, chapters × 3.0] by more than 25%, propose a specific structural fix before proceeding (U2).
- **Always cite sources** with URL and retrieval date in the U1 research summary.
- **Always use `TodoWrite`** to track progress when file count exceeds 30 (U5).
- **Windows MAX_PATH:** Proactively apply the 40-character component cap from the slug algorithm. Note any shortenings in the relevant index file.
- **Stub creation is idempotent.** Before writing a stub, check for existing non-empty content and skip if found. U5 is re-runnable after any interruption.
- **U5 always ends with a verification pass.** Compare planned files to actual files on disk; re-create any missing stubs; verify README relative links. Only report the scaffold summary once planned = actual.
- **Filenames are locked after U5.** Never renumber or rename — doing so breaks forward links.
- **Template bodies live in `reference/`.** Never inline them; always read from `reference/<name>` and copy to `templates/<name>` in U4.

---

## Workflow

The units run in order U0 → U6. U0–U5 each end with a STOP GATE that hands control back for confirmation; U6 runs immediately after U5 is confirmed (no extra gate). Do not skip a STOP GATE and do not combine a gate with the next unit in one response.

### Unit U0 — Intake & intent logic

- **Goal/scope**: collect every input needed to design the repo, and decide which per-chapter file types to generate — before any research or design.
- **Inputs**: the user's initial request.
- **Do**:
  - Ask all of the following in a **single message**. Do not proceed until every question is answered (the user may explicitly skip optional ones):

    ```
    To design the right repo for you, I need a few details:

    1. Topic / Certification
       What is the exact topic or certification name?
       (a certification, a technology or tool, or a broad concept — anything you want to master)

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
  - **Intent logic (run silently after answers are received).** Decide which per-chapter file types to generate and record the decision — it affects the file tree in U2 and the templates in U3:

    | Detected goal | Additional file per chapter |
    |---|---|
    | Includes (c) — articles / thought leadership | `thought-leadership.md` stub |
    | Includes (b) — interviews / job / career | `interview-prep.md` stub |
    | Both (b) and (c) | Both files |
    | Ambiguous "learn deeply" with no output goal | Ask: "Should I also add thought-leadership.md and/or interview-prep.md stubs per chapter for future use?" |
    | Only (a) or (d) | `notes.md` only |
  - Also confirm during this unit whether any sections should use **4 dense topic notes** rather than 3 (see file naming conventions in shared reference material). Do not assume based on position.
- **Self-verify**: topic, goal(s), level, and time budget are all captured; naming preference/style and seed URLs are captured or explicitly defaulted; the per-chapter file-type decision (and any dense-chapter flag) is recorded.
- **STOP GATE (hand back)**: if any required answer is missing, or the "learn deeply" case is ambiguous, **stop and ask** rather than assuming. Do not begin research until intake is complete. → Hand control back to the user/orchestrator for the missing inputs.
- **Report contract**: `intake: <complete | awaiting: fields> | goals: <a/b/c/d> | level: <...> | budget: <N hrs> | naming: <style, repo name> | aux files: <notes-only | +thought-leadership | +interview-prep | both>`.

### Unit U1 — Research (live, cited)

- **Goal/scope**: produce a research summary grounded in **live** sources that drives the structure in U2. Never invent curriculum structure from training data alone — product names, exam blueprints, and API surfaces change.
- **Inputs**: the confirmed intake from U0 (topic, cert, seed URLs).
- **Do**:
  - **Step 1 — WebFetch (primary, run in parallel).** Attempt all of the following simultaneously; record the URL and retrieval date for each:
    1. **Official exam blueprint** (if a certification exists): search for `[CERTIFICATION NAME] official exam guide` / `exam blueprint` to find the right URL — do not assume it. Target: exam domains, domain weightings (%), question count, passing score, duration, cost, retake policy.
    2. **Official documentation landing page** for the technology/subject: target product/topic overview, key concepts, current version, major recent changes.
    3. **Any seed URLs the user provided** in U0.
    4. **Changelog / "What's new" page** (if one exists): changes in the last 12–18 months that affect what to learn or what is now deprecated.
  - **Step 2 — Fallback AI query stubs.** For any area where WebFetch returned thin or no content, generate ready-to-paste prompts the user can run in any AI assistant:

    ---
    **If any fetches above failed or returned thin results, paste this into any AI assistant and share the response:**

    > You are an expert in [TOPIC/CERTIFICATION]. Answer all four questions below specifically and cite sources where possible.
    >
    > 1. What are the official exam domains and their percentage weightings for [CERT NAME]? Include question count, passing score, duration, and cost.
    > 2. What is the canonical beginner → intermediate → advanced → expert skill progression for [TOPIC] as described by leading courses, books, and practitioners?
    > 3. What are the core prerequisite skills someone should verify they have before starting [TOPIC]?
    > 4. What are the most significant changes to [TOPIC] in the last 12–18 months that any learner must know about?
    ---
  - **Step 3 — Assemble the research summary.** Fill every field from live sources; mark "N/A — no certification" where applicable:

    ```markdown
    ## U1 Research Summary — [TOPIC]

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
- **Self-verify**: at least the official documentation (and blueprint, if a cert exists) was fetched and cited with a retrieval date; no source is a non-official blog/video; every summary field is filled or explicitly marked N/A; a recommended section sequence is present.
- **STOP GATE (hand back)**: present the research summary and **stop**. Ask: "Does this look accurate? Any corrections before I design the folder structure?" **Do not design the structure until confirmed.** → Hand control back for the research/plan decision.
- **Report contract**: `sources: <N> official (dated) | blueprint: <captured | n-a> | section sequence: <N proposed> | awaiting: research approval`.

### Unit U2 — Repository structure design

- **Goal/scope**: design the full folder + file hierarchy, reconcile it against the user's time budget, and confirm before touching templates.
- **Inputs**: approved U1 research summary + U0 intake (naming style, aux-file decision, dense-chapter flag).
- **Do**:
  - Design the tree using the **naming conventions**, **slug derivation algorithm**, **file naming conventions**, **filename lock / forward-link contract**, **full repo tree structure**, and **structural rules** in shared reference material. Apply the actual subject names — never placeholders.
  - **Budget reconciliation.** Once the chapter count is known, compute the hour range and compare it to the U0 budget **before presenting the tree**:
    - `low = chapters × 1.5 hrs`; `high = chapters × 3.0 hrs`.
    - **Decision rule:** if the user's budget falls outside `[low, high]` by more than 25%, do not silently proceed. Propose a specific structural fix: budget too low → name section(s) to cut or chapters to merge, then show a revised tree; budget too high → name section(s)/bonus chapters to add, or flag the budget as generous and proceed as-is only if the user confirms.
    - Only proceed when the budget is inside the range, or the user has explicitly acknowledged the mismatch.
    - Include this **reconciliation table above the full tree**:

      | Section | Chapters | Hrs low | Hrs high |
      |---|---|---|---|
      | [Section 1 name] | N | N×1.5 | N×3.0 |
      | [Section 2 name] | N | N×1.5 | N×3.0 |
      | … | | | |
      | **Total** | **N** | **N×1.5** | **N×3.0** |
      | **Your budget** | — | **X hrs** | ← within range? |
  - **Present the tree.** Show the complete folder + file tree annotated with: estimated hours per chapter; exam domain mapping per section (if a cert exists); total hours sum; `← POPULATED` next to template files and `← stub` next to all content files; any fast-evolving areas flagged in U1 (inline).
- **Self-verify**: every folder/file name is derived via the slug algorithm and uses real subject names; the reconciliation table is present and the budget is inside range (or the mismatch is explicitly acknowledged); the tree annotates every content file as `← stub` and every template as `← POPULATED`; locked names are recorded.
- **STOP GATE (hand back)**: present the reconciliation table + full annotated tree and **stop**. Ask the user to confirm folder names, section order, chapter sizing, and the budget table before templates. → Hand control back for the structure decision.
- **Report contract**: `structure: <N sections / N modules / N chapters> | budget: <within range | acknowledged mismatch> | aux files per chapter: <...> | awaiting: structure approval`.

### Unit U3 — Template manifest confirmation

- **Goal/scope**: confirm the exact set of template files that will be written to disk, before any files are created.
- **Inputs**: approved U2 structure + U0 aux-file decision (thought leadership / interview prep / labs).
- **Do**:
  - Resolve the applicable rows of the **template manifest** (shared reference material) for this repo: the "Always" templates plus any conditional templates whose intent was detected in U0.
  - Present the resulting list — each file, its `reference/` source, its destination in the repo, and why it is (or is not) included. Do not inline template bodies; use the on-demand display rule only if the user asks to see one.
- **Self-verify**: the confirmed manifest includes all "Always" templates and exactly the conditional templates justified by U0's intent decision; no template body was inlined into the response.
- **STOP GATE (hand back)**: present the manifest and **stop**. Note that these files will be copied from `reference/` to `templates/` in U4. Ask: "Any template additions or removals before I create the files?" → Hand control back for the manifest decision.
- **Report contract**: `manifest: <N templates> (always: <N>, conditional: <list>) | awaiting: manifest approval`.

### Unit U4 — Write AGENTS.md and templates to disk

- **Goal/scope**: write `AGENTS.md` and all confirmed template files. Every other file stays a blank stub.
- **Inputs**: approved U3 manifest + repo root path + U0/U1 values for substitution.
- **Do**:
  - **4a — Write `AGENTS.md`.** Create `<repo-root>/AGENTS.md`. Replace `[TOPIC]`, `[TOOL/PLATFORM]`, `[EXAM/GOAL]`, and `[SOURCE OF TRUTH]` with the actual values for this repo. The **Content Depth Rules section must be copied verbatim** — these rules are topic-agnostic and govern authoring quality for any subject.

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
    4. **Visual Overview** — Recommended when the topic has a visualisable process; 2–4 ASCII diagrams in plain fenced blocks under `###` sub-headers; placed after Learning Objectives, before Key Concepts
    5. **Key Concepts** — Each sub-section: definition + mechanism + [TOOL/PLATFORM] manifestation
    6. **[TOOL/PLATFORM] Implementation** — ≥2 snippets (different angles) including one anti-pattern
    7. **Common Pitfalls** — Each: bolded label + why beginners make it + correct mental model
    8. **Key Definitions** — Precise, scoped definitions only
    9. **Summary / Quick Recall** — 3–7 scannable takeaways
    10. **Self-Check Questions** — 5 questions spanning recall → application → analysis; ≥1 multi-select
    11. **Further Reading** — Official docs only, all links verified

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
    Non-compliant: a comment that only names the feature or command being demonstrated.
    Compliant: a comment that states the concrete operational goal the snippet achieves and the constraint that makes it the right choice.
    At least one snippet per file must be an anti-pattern (`# Anti-pattern:`) immediately followed by the corrected version with an explanation of what breaks.

    ### Rule 6 — Pitfalls must have three parts
    Each pitfall bullet: (1) **bolded label**, (2) one sentence on why beginners make this mistake, (3) one sentence on the correct mental model. Bare bullets are non-compliant.

    ### Rule 7 — Answer rationales must cover all options
    Every Self-Check answer must explain why the correct answer is right AND why the main distractor(s) are wrong. One-word rationales are non-compliant. For multi-select, explain why both correct answers qualify AND why the most tempting wrong answer fails.

    ### Rule 8 — Self-Check questions must span cognitive levels
    Required distribution: Q1 recall, Q2–Q3 application, Q4–Q5 analysis/trade-off. Five recall questions is non-compliant even if one is multi-select.

    ### Rule 9 — Visual Overview is recommended for visualisable topics
    When a topic involves a pipeline, decision path, architecture, or before/after contrast, include a `## Visual Overview` section placed **after `## Learning Objectives` and before `## Key Concepts`**. Format: each diagram under its own `### [Diagram Title]` sub-header inside a plain fenced code block (no language tag). Use `──►` for flow arrows and `│ ├ └ ─ ┌ ┐` for tree/box structure. Aim for 2–4 diagrams. Omit this section only for purely conceptual topics where no process or structure exists to diagram.

    ---

    ## File Naming Rules
    (Adjust based on repo naming style)
    - Notes: `01_snake_case.md` / `01-kebab-case.md` (zero-padded)
    - Thought leadership: `NN_thought_leadership.md` / `NN-thought-leadership.md` — `NN` is the next number after the topic notes
    - Interview prep: `NN_interview_prep.md` / `NN-interview-prep.md` — `NN` is the number after thought leadership when both are present
    - Labs: `LAB_XX_snake_case.md` / `LAB-XX-kebab.md` (global sequence)
    - Section folders: `SECTION_XX_NAME/` or `01-name/`
    - Module folders: `MODULE_XX_Name/` or `01-name/`
    - Chapter folders: `CHAPTER_XX_Name/` or `01-name/`
    - Auxiliary files (thought leadership, interview prep) are numbered sequentially after the topic notes; interview prep always follows thought leadership so they never collide.

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
    - Do not renumber or rename files or folders after scaffold — filenames are locked once U5 writes them. Authored chapters may forward-link to not-yet-written stubs; those links resolve when the target is populated. Renaming to "fix" a link breaks every other reference to that file.
    - Do not link to third-party blogs, Medium, or YouTube
    - Do not skip or merge sections without user approval
    ````
  - **4b — Write all template files.** For each template in the confirmed U3 manifest that applies to this repo, read the corresponding file from `reference/<name>` (relative to this skill's base directory) and write its content **verbatim** to `<repo-root>/templates/<name>` using the `Write` tool. Do not paraphrase or abbreviate. Also create `templates/README.md` listing each template file, its reference source, and its destination in the repo. These are the only non-stub files other than `AGENTS.md` and `README.md`.
- **Self-verify**: `AGENTS.md` exists with all placeholders substituted and the Content Depth Rules copied verbatim; every manifest template exists at `templates/<name>` matching its `reference/` source byte-for-byte (no paraphrase); `templates/README.md` lists every template with source + destination; **no content file outside `templates/`, `AGENTS.md` has been touched.**
- **STOP GATE (hand back)**: report that `AGENTS.md` and all templates are written and **stop**. Ask: "Reply proceed to continue to U5 (scaffold stubs + README), or request changes." → Hand control back for the write approval.
- **Report contract**: `wrote: AGENTS.md + <N> templates + templates/README.md | verbatim copy: confirmed | stubs: not yet created | awaiting: proceed to scaffold`.

### Unit U5 — Scaffold stubs and README

- **Goal/scope**: create every folder, every **blank stub** file, and the root `README.md` (the only content file written here), then verify planned = actual.
- **Inputs**: approved U2 tree + written templates/`AGENTS.md` from U4.
- **Do**:
  - **Stub rule.** Every file outside `templates/` and outside `AGENTS.md`/`README.md` contains exactly one line:

    ```
    <!-- stub: populate using templates/ -->
    ```

    No headings, no tables, no prose — one comment line only. This applies to all section/module/chapter content files, `progress-tracker.md`, `00-roadmap/learning-roadmap.md`, and all capstone files. Section and module index stubs point to their specific template:

    ```markdown
    <!-- stub: populate using templates/section-index-template.md -->
    ```
    ```markdown
    <!-- stub: populate using templates/module-index-template.md -->
    ```
  - **Idempotency rule.** Before writing a stub, check whether the file already exists with content beyond the stub line. If it does, **skip it — never overwrite.** This makes U5 re-runnable: re-invoking it after an interruption creates only missing files and leaves authored content intact.
  - **README.md** — the one content file written here. Include: H1 title (actual topic/cert name); goal statement (what the repo is, who for, what the reader can do after); learning path table (Phase | Section | Estimated hours | Focus area); repository structure (top 2–3 levels only); section summaries (one bullet per section, relative link + one-line description); file type guide (File type | Pattern | Purpose | Created at scaffold?); certification/exam target (only if a cert exists). Use only the user's topic name, section names, and goal — no generic boilerplate or assumed tool names.
  - **Use `TodoWrite` for large repos.** For repos with more than 30 files, track scaffold progress: mark each section `pending` → `in_progress` → `completed` as its files are written; write one section at a time.
  - **Verification pass** (run before reporting the summary — catches Windows MAX_PATH truncations, permission errors, interrupted writes):
    1. Build the **planned file list** from the U2 tree (every stub, all `templates/` files + `templates/README.md`, `AGENTS.md`, `README.md`).
    2. Check each planned file's existence on disk.
    3. Produce a diff table:

       | Planned file | Exists? | Action taken |
       |---|---|---|
       | `path/to/file.md` | ✓ | — |
       | `path/to/missing.md` | ✗ | Created now |
    4. Re-create any missing files (applying the idempotency rule).
    5. For `README.md`, verify every relative link in Section summaries and repository structure points to a file/folder that now exists. List and fix any broken links.
    6. Only proceed once planned count = actual count.
- **Self-verify**: **every content file outside `templates/`/`AGENTS.md`/`README.md` is exactly one stub line** (blank stub — no headings/prose); `templates/*` and `AGENTS.md` remain fully populated and untouched; `README.md` is fully populated with real repo metadata; the verification pass shows planned count = actual count with all README relative links resolving.
- **STOP GATE (hand back)**: report the scaffold summary and **stop** for confirmation before git init:

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
  Template files:        N  (fully populated, incl. templates/README.md)
  AGENTS.md:             1  (fully populated)
  README.md:             1  (fully populated)
  ────────────────────────────────
  Total files:           N
  ```

  Then tell the user: *"All content files are blank stubs. Ask me to populate any file, chapter, or section and I will follow the Standard Chapter Template from `templates/chapter-notes-template.md` and the Content Depth Rules in `AGENTS.md`."* Remind them that module-level index files are created on request (not at scaffold time), and that thought-leadership files are best populated after the notes files, since they draw on what was learned while authoring. → Hand control back for the scaffold confirmation.
- **Report contract**: `scaffold: <N total files> | stubs blank-verified: yes | templates+AGENTS.md+README populated: yes | planned==actual: yes | awaiting: proceed to git init`.

### Unit U6 — Git initialisation

- **Goal/scope**: initialise git (if needed) and hand the user a ready-to-run first-commit command. Runs immediately after U5 is confirmed — **no additional gate**.
- **Inputs**: confirmed scaffold from U5 + repo root path + topic name.
- **Do**:
  - Check whether a `.git` directory exists in the repo root. If not, run `git init`. If yes, skip.
  - Print this block verbatim, substituting `[TOPIC]`:

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
- **Self-verify**: the repo root is a git repository (either pre-existing or `git init` succeeded); the first-commit command was emitted with `[TOPIC]` substituted.
- **Report contract**: `git: <initialised | already a repo> | first-commit command emitted: yes | complete`.

---

## Portability — Using This Skill on Other Platforms

This skill is written in the `SKILL.md` format for OpenCode. The workflow, units, and constraints are platform-agnostic.

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
