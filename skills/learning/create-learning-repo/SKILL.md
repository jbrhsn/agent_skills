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

## HOW TO RUN THIS SKILL

Run the units in order. **One unit per response.** A response ends at that unit's STOP GATE — never carry on into the next unit.

| # | Unit | What you do in it | Response ends with |
|---|---|---|---|
| 1 | U0 | Ask every intake question in one message; record the answers | STOP GATE |
| 2 | U1 | Search for, then fetch, live official sources; cite URL + retrieval date | STOP GATE |
| 3 | U2 | Design the folder tree; decompose every chapter into 2–6 named topics; reconcile the hour budget | STOP GATE |
| 4 | U3 | Confirm the template manifest | STOP GATE |
| 5 | U4 | Write `AGENTS.md`; copy each manifest template verbatim from `reference/` into `templates/` | STOP GATE |
| 6 | U5 | Create folders, one-line stubs, and the populated `README.md`; verify planned = actual | STOP GATE |
| 7 | U6 | `git init` if needed; emit the first-commit command | Done — no extra gate |

**The three failure modes that ruin this run, and their fix:**

| Failure mode | Fix |
|---|---|
| **(a) Combining units** — two units in one response, or a STOP GATE with the next unit attached | Never do it. One unit per response, then stop at its gate and wait for the user. |
| **(b) Inventing structure** — writing curriculum structure, exam domains, weightings, or version facts from training data instead of fetching live sources in U1 | Fetch them. If a source is unreachable, stop and ask — see **STOP CONDITIONS**. |
| **(c) Writing content into stub files** | Every file outside `templates/`, `AGENTS.md`, and `README.md` gets **exactly one** stub comment line. Count the lines: 1. |

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

Every chapter folder holds the same five artifact types. All five are **always** created — none is conditional on the learning goals detected in U0.

| File type | Pattern | Notes |
|---|---|---|
| Chapter intro | `00-intro.md` / `00_intro.md` | **Reserved slot.** One per chapter. DERIVED — authored last. |
| Topic notes (hyphen style) | `01-<topic-slug>.md` … `NN-<topic-slug>.md` | 2–6 per chapter. `NN` never exceeds `06`. Slug derived from the topic name via the slug algorithm above. |
| Topic notes (ALLCAPS style) | `01_<TOPIC_SLUG>.md` … `NN_<TOPIC_SLUG>.md` | Same rule, ALLCAPS-underscore slug. |
| Interview prep | `interview-prep.md` / `interview_prep.md` | **Unnumbered.** Always created. |
| Thought leadership | `thought-leadership.md` / `thought_leadership.md` | **Unnumbered.** Always created. |
| Podcast | `99-podcast.md` / `99_podcast.md` | **Reserved slot.** One per chapter. DERIVED — authored last. |
| Lab file | `LAB-XX-name.md` / `LAB_XX_name.md` | Global sequence — never reset |
| Section index | `README.md` or `INDEX.md` inside section folder | Created at scaffold time |
| Module index | Not created at scaffold time — on request only | |

**Reserved slots.** `00` and `99` are reserved for the chapter intro and the podcast respectively. Topic notes therefore always occupy the contiguous range `01`…`NN` where `NN` ≤ `06`, and never take `00` or `99`. `interview-prep.md` and `thought-leadership.md` carry no number at all, so they cannot collide with any topic note however many there are.

**Topic file count per chapter.** Each chapter has **2–6 topic notes**, and the exact count is **derived from the U1 research during U2** — it is not a fixed number and it is not a question put to the user. The topic decomposition step in U2 splits each chapter into the topics the research actually shows it contains, gives each a name and a one-line scope, and turns those names into the `01-<topic-slug>.md` … `NN-<topic-slug>.md` filenames via the slug algorithm. If a chapter appears to need more than 6 topics, that is a signal the chapter is too large — split the chapter instead of exceeding the cap.

**Derived artifacts.** `00-intro.md` and `99-podcast.md` may only be authored **after every topic note in the chapter is complete and non-stub**, and must introduce **no fact absent from those sibling notes**. They synthesise and connect the notes; they do not research. See the Authoring Order rules written into the repo's `AGENTS.md` in U4.

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
│   ├── topic-notes-template.md      ← POPULATED
│   ├── chapter-intro-template.md    ← POPULATED
│   ├── chapter-podcast-template.md  ← POPULATED
│   ├── section-index-template.md    ← POPULATED
│   ├── module-index-template.md     ← POPULATED
│   ├── authoring-guidelines.md      ← POPULATED
│   ├── thought-leadership-template.md   ← POPULATED
│   ├── interview-prep-template.md   ← POPULATED
│   ├── lab-template.md              ← POPULATED (if labs requested)
│   └── capstone-template.md         ← POPULATED
├── 00-roadmap/
│   └── learning-roadmap.md          ← stub
├── 01-[section]/
│   ├── README.md or INDEX.md        ← stub
│   ├── 01-[module]/
│   │   ├── README.md or INDEX.md    ← stub
│   │   └── 01-[chapter]/
│   │       ├── 00-intro.md          ← stub (DERIVED — authored last)
│   │       ├── 01-[topic-slug].md   ← stub
│   │       ├── 02-[topic-slug].md   ← stub
│   │       ├── ...                  ← 2–6 topic notes, count derived in U2
│   │       ├── interview-prep.md    ← stub
│   │       ├── thought-leadership.md ← stub
│   │       └── 99-podcast.md        ← stub (DERIVED — authored last)
│   └── ...
├── ...
├── capstone/
│   ├── README.md                    ← stub
│   └── project-brief.md             ← stub
└── progress-tracker.md              ← stub
```

Every chapter folder has this same shape. `00-intro.md` and `99-podcast.md` occupy reserved slots and are **authored last** — only once every topic note in that chapter is complete and non-stub — because both are derived from the topic notes.

### Structural rules

- Sections follow a natural difficulty ramp: Foundations → Core Competency → Advanced / Specialised → Expert Practice.
- If a certification exists, the final content section (before capstone) must be **exam prep**: mock questions, common pitfalls, exam strategy, timing.
- Each chapter is sized for **1.5–3 hours** of focused study.
- The capstone must draw on skills from at least two sections.

### Template manifest (source of truth for which files exist and when)

Template bodies are **never** inlined into this SKILL.md — they live in `reference/` (relative to this skill's base directory) and are read on demand. Copy them verbatim; never paraphrase or abbreviate.

| File | Reference source | Destination in repo | When generated |
|---|---|---|---|
| `topic-notes-template.md` | `reference/topic-notes-template.md` | `templates/topic-notes-template.md` | Always |
| `chapter-intro-template.md` | `reference/chapter-intro-template.md` | `templates/chapter-intro-template.md` | Always |
| `chapter-podcast-template.md` | `reference/chapter-podcast-template.md` | `templates/chapter-podcast-template.md` | Always |
| `section-index-template.md` | `reference/section-index-template.md` | `templates/section-index-template.md` | Always |
| `module-index-template.md` | `reference/module-index-template.md` | `templates/module-index-template.md` | Always |
| `authoring-guidelines.md` | `reference/authoring-guidelines.md` | `templates/authoring-guidelines.md` | Always |
| `capstone-template.md` | `reference/capstone-template.md` | `templates/capstone-template.md` | Always |
| `thought-leadership-template.md` | `reference/thought-leadership-template.md` | `templates/thought-leadership-template.md` | Always |
| `interview-prep-template.md` | `reference/interview-prep-template.md` | `templates/interview-prep-template.md` | Always |
| `lab-template.md` | `reference/lab-template.md` | `templates/lab-template.md` | Labs requested in U0 |

**What `topic-notes-template.md` is** (the template every topic note follows): an **adaptive menu of suggested sections, not a fixed running order**. The author picks the sections this specific topic genuinely needs, orders them however teaches best, renames them after real domain concepts, and may invent sections the menu never anticipated. It carries only **three hard requirements**: (1) a **Coverage Plan** — the author enumerates the topic's sub-concepts before writing and verifies each one is genuinely explained before submitting; (2) an **800-word floor** of genuine explanatory prose per topic note, where padding or restatement is a violation rather than a way to meet it; (3) a **reading level** pitched at a bright 14-year-old — short sentences, acronyms expanded on first use, jargon defined inline, and prose (not bullet lists) carrying the explanation. Omissions from the menu are recorded with a topic-specific reason in the template's **Adaptation Note**, and a 12-row outcome-based Final Self-Audit is run before submission.

**Key sections in `authoring-guidelines.md`**: Voice & Reading Level → Prose-First Rule → Adaptive Structure → Completeness → Depth Calibration → Per-Artifact Guidance (topic notes, chapter intro, podcast, interview prep, thought leadership) → Authoring Order → Source Hygiene → Blueprint Drift Warning → Quality Checklist.

**On-demand template display.** If the user asks to see a specific template ("show me the topic-notes template", "what does the lab template look like"), read the relevant `reference/<name>` file and display it in full. Do not pre-display all templates in a single message.

### Constraints and guardrails (non-negotiable, all units)

- **Templates and `AGENTS.md` are the only files with content.** `README.md` also gets content. Everything else is one stub line. No exceptions.
- **Never assume tool names, vendor names, cloud providers, or platform names.** Derive everything from what the user said. Never default to any specific technology in folder names, template language, or `AGENTS.md`.
- **Folder and file names use the actual subject names** — not generic placeholders. Apply the deterministic slug algorithm consistently.
- **Every chapter gets all five artifact types.** Chapter intro, 2–6 topic notes, `interview-prep.md`, `thought-leadership.md`, and the podcast are created for every chapter. None of them is conditional on the learning goals detected in U0.
- **Topic counts are derived, never fixed.** The 2–6 topic notes per chapter come from the topic decomposition in U2, grounded in the approved U1 research.
- **`00` and `99` are reserved slots.** `00-intro.md` and `99-podcast.md` only. Topic notes occupy `01`…`NN` (`NN` ≤ `06`); `interview-prep.md` and `thought-leadership.md` are unnumbered.
- **Derived artifacts come last.** `00-intro.md` and `99-podcast.md` are authored only after every topic note in their chapter is complete and non-stub, and introduce no fact absent from those notes.
- **One unit per response.** Never combine units. Each STOP GATE hands control back before the next unit runs.
- **Always fetch live information in U1.** Never invent curriculum structure from training data alone.
- **Hour budget must reconcile.** If the U0 budget is outside [chapters × 1.5, chapters × 3.0] by more than 25%, propose a specific structural fix before proceeding (U2).
- **Always cite sources** with URL and retrieval date in the U1 research summary.
- **Always use `TodoWrite`** to track progress when file count exceeds 20 (U5).
- **Windows MAX_PATH:** Proactively apply the 40-character component cap from the slug algorithm. Note any shortenings in the relevant index file.
- **Stub creation is idempotent.** Before writing a stub, check for existing non-empty content and skip if found. U5 is re-runnable after any interruption.
- **U5 always ends with a verification pass.** Compare planned files to actual files on disk; re-create any missing stubs; verify README relative links. Only report the scaffold summary once planned = actual.
- **Filenames are locked after U5.** Never renumber or rename — doing so breaks forward links. This includes the topic names approved in U2, which become topic-note filenames.
- **Template bodies live in `reference/`.** Never inline them; always read from `reference/<name>` and copy to `templates/<name>` in U4.

### STOP CONDITIONS

Stopping and asking the user is **correct, expected behaviour**. Guessing in order to avoid stopping is the worse failure: a wrong tree, a wrong blueprint, or an overwritten file costs far more than one extra question.

Stop and ask when any row below is true. Say the thing in the right-hand column, then wait.

| Situation | What to say |
|---|---|
| A required U0 intake field is missing (topic, goal, level, or budget) | "I still need: `<field>`. I can't design the repo without it." Ask for that field only. |
| Official sources are unreachable in U1 after a retry on a more specific sub-page | "I could not reach `<URL>`. Paste the fallback AI-query results, or give me a working source URL. I will not guess the blueprint." |
| The hour budget is outside `[chapters × 1.5, chapters × 3.0]` by more than 25% and the user has not acknowledged it | "Your budget is `X` hrs; this tree needs `low`–`high` hrs. Here is a specific fix: `<cut/merge/add named sections>`. Confirm the fix or confirm you accept the mismatch." |
| A chapter appears to need more than 6 topics | "Chapter `<name>` decomposes into `N` topics, above the cap of 6. I propose splitting it into `<A>` and `<B>`. Confirm before I finalise the tree." |
| The user has not approved the U2 structure, the U3 manifest, or the U5 scaffold at its gate | Nothing further. Present the gate output and wait. Do not begin the next unit. |
| A target file already has content beyond the stub line | "`<path>` already has content. I skipped it — nothing was overwritten." Report it; never overwrite. |
| A U4 template written to `templates/` does not match its `reference/` source | "The copy of `<name>` does not match its source. Re-copying." Re-copy, then re-verify. Do not report success on a mismatch. |

---

## Workflow

The units run in order U0 → U6. U0–U5 each end with a STOP GATE that hands control back for confirmation; U6 runs immediately after U5 is confirmed (no extra gate). Do not skip a STOP GATE and do not combine a gate with the next unit in one response.

### Unit U0 — Intake

- **Goal/scope**: collect every input needed to design the repo — before any research or design.
- **Inputs**: the user's initial request.
- **Do**:
  - **Step 1 — ask everything at once.** Send the question block below as a **single message**. Do not ask the questions one at a time and do not start researching while you wait.

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
  - **Step 2 — wait.** Stop after sending the block. Do not run U1, do not propose a tree, do not assume defaults for the required fields.
  - **Step 3 — handle a partial answer.** Check the four **required** fields: topic, learning goal, current level, time budget. For each one still missing, ask again **for that field only** — do not re-send the whole block, and **never assume a default** for any of the four. The three **optional** fields may be defaulted silently: repo name → derived from the topic; naming style → lowercase-hyphen; seed URLs → none (you will find sources in U1).
  - **Step 4 — record the derived decisions** once all four required fields are in:

    | Decision | Derived from |
    |---|---|
    | Repo root name | stated preference, else slug of the topic |
    | Naming style | stated preference, else lowercase-hyphen |
    | Labs: yes / no | an explicit request for hands-on labs anywhere in the conversation, else no |
    | Research emphasis | the learning goal (see below) |
    | Seed URLs | listed, else none |

  - **Every chapter gets all five artifact types regardless of the answers.** The chapter intro (`00-intro.md`), 2–6 topic notes, `interview-prep.md`, `thought-leadership.md`, and the podcast (`99-podcast.md`) are always created. There is no per-chapter file-type decision to make here, and no file type is conditional on a detected goal.
  - **What question 2 is actually for.** The learning goal shapes *emphasis*, not file existence: it steers what U1 researches hardest (exam blueprint depth for (a), role-and-level framing for (b), argument and positioning angles for (c), breadth-and-mechanism for (d)), and it shapes how `README.md` frames the repo's purpose in U5. Record the goals for that purpose only.
  - **What is still conditional.** Only labs. If the user has asked for hands-on lab files — in the initial request or alongside these answers — record it: it adds `lab-template.md` to the U3 manifest and `LAB-XX-*.md` files to the tree.
  - **Topic counts are not asked here.** The number of topic notes per chapter (2–6) is derived from the U1 research during the U2 topic decomposition. Do not ask the user, and do not assume a number.
- **Self-verify**: topic, goal(s), level, and time budget are all captured; naming preference/style and seed URLs are captured or explicitly defaulted; the labs preference is captured or defaulted; no per-chapter file-type or topic-count decision was made or asked for.
- **STOP GATE (hand back)**: if any required answer is missing, **stop and ask** rather than assuming. Do not begin research until intake is complete. → Hand control back to the user/orchestrator for the missing inputs.
- **Report contract**: `intake: <complete | awaiting: fields> | goals: <a/b/c/d — emphasis only> | level: <...> | budget: <N hrs> | naming: <style, repo name> | labs: <yes | no> | per-chapter artifacts: intro + topic notes + interview-prep + thought-leadership + podcast (all chapters)`.

### Unit U1 — Research (live, cited)

- **Goal/scope**: produce a research summary grounded in **live** sources that drives the structure in U2. Never invent curriculum structure from training data alone — product names, exam blueprints, and API surfaces change.
- **Inputs**: the confirmed intake from U0 (topic, cert, seed URLs).
- **Do**:

  **Hard rule:** never write curriculum structure, exam domains, weightings, question counts, passing scores, prices, or version facts from memory. Every one of them comes from a fetched page. An unfetchable source means **stop and ask** — not guess. See **STOP CONDITIONS**.

  - **Step 1 — search to FIND the URLs. Do not assume them.** Run a web search per target below and take the URL from the results. Guessing a documentation URL from a pattern you remember is a failure even when the guess resolves.

    | Target | Search for | Capture from it |
    |---|---|---|
    | Official exam blueprint (only if a certification exists) | `[CERTIFICATION NAME] official exam guide`, `[CERTIFICATION NAME] exam blueprint` | exam domains, domain weightings (%), question count, passing score, duration, cost, retake policy |
    | Official documentation landing page | `[TOPIC] official documentation` | topic overview, key concepts, current version, major recent changes |
    | Changelog / "What's new" page (if one exists) | `[TOPIC] release notes`, `[TOPIC] what's new` | changes in the last 12–18 months; what is now deprecated |
    | Seed URLs the user gave in U0 | — use them as given | whatever they contain |

  - **Step 2 — fetch them in parallel.** Issue all the fetches in one batch, not one at a time.
  - **Step 3 — record URL + retrieval date for every fetch,** as you go, in the form `[URL] — retrieved [YYYY-MM-DD] — [what was found]`. A fact with no recorded source cannot go in the summary.
  - **Step 4 — retry any thin or failed fetch on a more specific sub-page.** "Thin" means the page yielded none of its Capture-from-it column. Retry once against a deeper page — the exam-domains page rather than the certification overview, the concepts page rather than the docs home.
  - **Step 5 — if it still fails, emit the fallback prompts below and wait** for the user to paste results back. Do not proceed to Step 6 with an unfilled required field.
  - **Step 6 — assemble the research summary** in the template below.

  **Fallback AI query stubs** (Step 5 output — ready to paste):

    ---
    **If any fetches above failed or returned thin results, paste this into any AI assistant and share the response:**

    > You are an expert in [TOPIC/CERTIFICATION]. Answer all four questions below specifically and cite sources where possible.
    >
    > 1. What are the official exam domains and their percentage weightings for [CERT NAME]? Include question count, passing score, duration, and cost.
    > 2. What is the canonical beginner → intermediate → advanced → expert skill progression for [TOPIC] as described by leading courses, books, and practitioners?
    > 3. What are the core prerequisite skills someone should verify they have before starting [TOPIC]?
    > 4. What are the most significant changes to [TOPIC] in the last 12–18 months that any learner must know about?
    ---
  - **Research summary format** (Step 6). Fill every field from live sources; mark "N/A — no certification" where applicable:

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
- **Inputs**: approved U1 research summary + U0 intake (naming style, labs preference, budget).
- **Do**: run **A** (draft the tree), then **B** (decompose every chapter), then **C** (reconcile the budget), then **D** (present). Do not present anything until C is done.

  **A — Draft the section / module / chapter tree.** Use the **naming conventions**, **slug derivation algorithm**, **file naming conventions**, **filename lock / forward-link contract**, **full repo tree structure**, and **structural rules** in shared reference material. Apply the actual subject names — never placeholders.

  **B — Topic decomposition. Run these 9 steps for every chapter, one chapter at a time.**

  1. **List the candidates.** Re-read the approved U1 research and write down every distinct thing this chapter has to teach — a blueprint objective, a documented concept, a step in the canonical skill progression. Do not invent candidates the research does not support.
  2. **Test each candidate.** A topic qualifies if it is **a distinct idea that can be explained on its own in one sitting**. Ask both: (a) could a reader learn this without first reading its siblings? (b) is there enough in it to explain for one sitting? Two yeses → it qualifies.
  3. **Merge what cannot stand alone.** Any candidate that fails test (a) — it only makes sense as part of another candidate — is merged into that other candidate. It becomes a sub-heading inside that topic note later, not a topic of its own.
  4. **Split what needs two unrelated explanations.** Any candidate that requires two explanations with no shared mechanism between them is two topics. Split it and name both.
  5. **Stop between 2 and 6.** Count the surviving topics. Fewer than 2 → return to step 1, the chapter is under-decomposed or should be merged with a neighbour. More than 6 → **split the CHAPTER**, never exceed the cap; re-run steps 1–5 on each half. See **STOP CONDITIONS** before finalising a chapter split.
  6. **Name each topic as a concrete noun phrase naming the real concept.** Banned names: `Part 1`, `Part 2`, `Overview`, `Introduction`, `Basics`, `Fundamentals`, `Key Concepts`, `Advanced Topics`, `Miscellaneous`, `Other`. The test: read the name alone, with no chapter title — does it tell you what you will learn? If no, rename it.
  7. **Write a one-line scope per topic** — what that note covers, and where useful what it deliberately leaves to a sibling. Two scopes that overlap mean you skipped step 3.
  8. **Slug each name.** Run every topic name through the **slug derivation algorithm**, then number in teaching order: `01-<topic-slug>.md` … `NN-<topic-slug>.md`, `NN` ≤ `06`. `00` and `99` are reserved for `00-intro.md` and `99-podcast.md`; `interview-prep.md` and `thought-leadership.md` take no number.
  9. **Check for slug collisions within the chapter.** Compare the finished slugs pairwise. Identical after slugging → apply the collision rule (`-2`, `-3` / `_2`, `_3`) and record it, or better, rename the topic to something more distinct.

  **Worked micro-example of steps 1–9 — ILLUSTRATION ONLY, from an unrelated everyday domain.** The chapter below is "Baking a loaf of bread". It has nothing to do with the subject of this repo. Copy the shape, never the content.

  - Step 1 candidates: `yeast`, `what yeast eats`, `kneading`, `proving`, `the oven spring`, `oven temperature`, `slashing the top`.
  - Step 3 merge: `what yeast eats` cannot stand alone — it only means anything alongside yeast. Merged into the yeast topic. `slashing the top` merged into the oven topic.
  - Step 4 split: `proving` needed two unrelated explanations — the gas that inflates the dough, and the timing you judge it by — so it became one topic about the rise and left timing to the oven topic.
  - Step 5 count: 4 surviving topics. Inside 2–6. Proceed.

  | # | Topic name | Scope (one line) | Filename |
  |---|---|---|---|
  | 01 | How Yeast Turns Flour Into Gas | What yeast is, what it feeds on, and the gas that makes dough rise | `01-how-yeast-turns-flour-into-gas.md` |
  | 02 | Why Kneading Builds The Stretchy Web | How working the dough forms the network that traps that gas | `02-why-kneading-builds-the-stretchy-web.md` |
  | 03 | Judging When The Dough Has Risen Enough | The signs of a finished rise; leaves oven timing to topic 04 | `03-judging-when-the-dough-has-risen-enough.md` |
  | 04 | What The Oven Does In The First Ten Minutes | Oven spring, crust setting, and why you slash the top | `04-what-the-oven-does-in-the-first-ten-minutes.md` |

  What to copy from it: every name is a concrete noun phrase you could learn from with the chapter title removed; no name is `Part 1` or `Overview`; scopes do not overlap and one hands off explicitly to a sibling; each slug came from the algorithm; the count landed inside 2–6 by merging and splitting, not by trimming to a target.

  **Present the decomposition as a table per chapter, above or inline with the tree,** so the user approves the topic names *before* they become filenames. Use the four-column shape above.

  **C — Budget reconciliation. Run these 5 steps before presenting anything.**

  1. **Estimate per topic note first.** Give each topic note an hour estimate. The derived (`00-intro.md`, `99-podcast.md`) and auxiliary (`interview-prep.md`, `thought-leadership.md`) artifacts are review and application of that same material — do **not** budget them separately.
  2. **Sum per chapter.** A chapter's estimate is the sum across its topic notes. Sums well above 3.0 hrs → split that chapter. Well below 1.5 hrs → merge it with a neighbour. Then re-run step 2.
  3. **Compute the totals.** `low = chapters × 1.5`; `high = chapters × 3.0`.
  4. **Compare to the U0 budget and apply the decision rule.**

     | Budget `X` vs `[low, high]` | Do this |
     |---|---|
     | Inside the range | Proceed to D. |
     | Outside by ≤ 25% | Proceed to D, noting the variance in the table. |
     | Below `low` by > 25% | Name the specific section(s) to cut or chapters to merge, show the revised tree, and stop for confirmation. |
     | Above `high` by > 25% | Name the specific section(s) or bonus chapters to add, **or** flag the budget as generous — either way stop for confirmation. |

  5. **Only proceed** when the budget is inside the range or the user has explicitly acknowledged the mismatch. A vague "we can adjust later" is not a fix — name the sections.

  Include this **reconciliation table above the full tree**:

  | Section | Chapters | Hrs low | Hrs high |
  |---|---|---|---|
  | [Section 1 name] | N | N×1.5 | N×3.0 |
  | [Section 2 name] | N | N×1.5 | N×3.0 |
  | … | | | |
  | **Total** | **N** | **N×1.5** | **N×3.0** |
  | **Your budget** | — | **X hrs** | ← within range? |

  **D — Present the tree.** Show the complete folder + file tree annotated with: the per-chapter topic decomposition (real topic filenames, never `01-[topic].md` placeholders); estimated hours per chapter (the sum across its topic notes) and per topic note; exam domain mapping per section (if a cert exists); total hours sum; `← POPULATED` next to template files and `← stub` next to all content files; `← DERIVED — authored last` next to `00-intro.md` and `99-podcast.md`; any fast-evolving areas flagged in U1 (inline). Every chapter shows all five artifact types.
- **Self-verify**: every folder/file name is derived via the slug algorithm and uses real subject names; every chapter has 2–6 named topics, each with a one-line scope and a resolved filename, each traceable to the U1 research; the decomposition table is present in the gate output; no chapter uses `00` or `99` for a topic note and no aux file is numbered; the reconciliation table is present and the budget is inside range (or the mismatch is explicitly acknowledged); per-chapter hours are the sum across that chapter's topic notes; the tree annotates every content file as `← stub`, every template as `← POPULATED`, and both derived artifacts as authored last; locked names are recorded.
- **STOP GATE (hand back)**: present the reconciliation table + per-chapter topic decomposition + full annotated tree and **stop**. Ask the user to confirm folder names, section order, **the topic names and counts per chapter** (these become filenames and are locked after U5), chapter sizing, and the budget table before templates. → Hand control back for the structure decision.
- **Report contract**: `structure: <N sections / N modules / N chapters> | topics: <N total, N–N per chapter> | budget: <within range | acknowledged mismatch> | per-chapter artifacts: intro + topic notes + interview-prep + thought-leadership + podcast | awaiting: structure approval`.

### Unit U3 — Template manifest confirmation

- **Goal/scope**: confirm the exact set of template files that will be written to disk, before any files are created.
- **Inputs**: approved U2 structure + U0 labs preference.
- **Do**:
  - Resolve the applicable rows of the **template manifest** (shared reference material) for this repo: every "Always" template, plus `lab-template.md` only if labs were requested in U0.
  - Present the resulting list — each file, its `reference/` source, its destination in the repo, and why it is (or is not) included. Do not inline template bodies; use the on-demand display rule only if the user asks to see one.
- **Self-verify**: the confirmed manifest includes all nine "Always" templates and includes `lab-template.md` if and only if labs were requested in U0; no template body was inlined into the response.
- **STOP GATE (hand back)**: present the manifest and **stop**. Note that these files will be copied from `reference/` to `templates/` in U4. Ask: "Any template additions or removals before I create the files?" → Hand control back for the manifest decision.
- **Report contract**: `manifest: <N templates> (always: <N>, conditional: <list>) | awaiting: manifest approval`.

### Unit U4 — Write AGENTS.md and templates to disk

- **Goal/scope**: write `AGENTS.md` and all confirmed template files. Every other file stays a blank stub.
- **Inputs**: approved U3 manifest + repo root path + U0/U1 values for substitution.
- **Do**: run these 5 steps in order.

  1. **Create `AGENTS.md`** at `<repo-root>/AGENTS.md` from the document below, substituting each placeholder with this repo's actual value:

     | Placeholder | Substitute with |
     |---|---|
     | `[TOPIC]` | the topic/certification name from U0 |
     | `[TOOL/PLATFORM]` | the tool or platform this subject lives in, from U0/U1 |
     | `[EXAM/GOAL]` | the learning goal from U0 |
     | `[SOURCE OF TRUTH]` | the authoritative syllabus/exam-guide URL from U1 |

     Substitute nothing else. Every other placeholder in the document is authoring guidance for the finished repo and stays as written.
  2. **Copy the Content Depth Rules section verbatim.** Rules 1–9 are topic-agnostic and govern authoring quality for any subject. Do not shorten, reorder, merge, or reword them.
  3. **For each template in the approved U3 manifest:** read `reference/<name>` (relative to this skill's base directory) with the `Read` tool, then write that content to `<repo-root>/templates/<name>` with the `Write` tool. Copy it — do not paraphrase, summarise, abbreviate, re-indent, or "improve" it. Do one template at a time; do not write a template you have not just read.
  4. **Create `templates/README.md`** listing each template file, its `reference/` source, and its destination in the repo.
  5. **Verify each written template matches its source.** Do not assume the copy worked. **Observable test:** for every template, compare the file you wrote against `reference/<name>` — same line count and same first and last line at minimum — and confirm they match. A mismatch means re-copy that file and re-check; never report success on a mismatch.

  **The `AGENTS.md` document to write in step 1:**

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

    ### Topic Note Template
    The authoritative template for every topic note is `templates/topic-notes-template.md`. It is a **menu of suggested sections, not a fixed running order.**

    - Pick the sections this specific topic genuinely needs; leave out the ones that do not serve it.
    - Order them however teaches the topic best. There is no required first section and no required last section.
    - Name every sub-heading after the real domain concept it discusses. Generic headings (`### Overview`, `### How does it work?`, `### Key Concepts`, `### Details`) are non-compliant.
    - Invent a section the topic calls for if the menu never anticipated it.
    - Record every omitted menu section in the template's **Adaptation Note**, with a one-line reason specific to this topic. Omission is fine; silent omission is not.

    The template carries only **three hard requirements**:

    1. **Coverage Plan** — before writing, enumerate the topic's sub-concepts in the template's Coverage Plan; before submitting, verify each one is genuinely explained in the body, not merely name-dropped.
    2. **800-word prose floor** — each topic note contains at least 800 words of genuine explanatory prose. Padding, hedging, and restatement are violations of this requirement, not ways to meet it.
    3. **Reading level** — written for a bright 14-year-old: short sentences, one idea each; every acronym expanded on first use; every piece of jargon defined inline in plain words on first use; prose paragraphs (not bullet lists) carrying the explanation.

    Run the template's Final Self-Audit before submitting any topic note.

    ### Template → destination mapping

    | Template | Destination |
    |---|---|
    | `topic-notes-template.md` | `[chapter]/NN-<topic-slug>.md` (2–6 per chapter) |
    | `chapter-intro-template.md` | `[chapter]/00-intro.md` (derived — authored last) |
    | `chapter-podcast-template.md` | `[chapter]/99-podcast.md` (derived — authored last) |
    | `interview-prep-template.md` | `[chapter]/interview-prep.md` |
    | `thought-leadership-template.md` | `[chapter]/thought-leadership.md` |
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

    ### Rule 1 — Voice and reading level
    Write for a bright 14-year-old: smart, but never taught this before.
    - Short, direct sentences. One idea per sentence.
    - Plain everyday words wherever a plain word exists.
    - Expand every acronym the first time it appears.
    - Define every piece of jargon inline, in plain words, the first time it appears — in the same sentence or the one right after. Do not defer definitions to a glossary at the bottom.
    - Active voice, and explain **why**, not only what.
    Formal register that restates the same idea in harder words is non-compliant. It is not more correct; it is only harder to reach.

    ### Rule 2 — Prose-first
    Explanation is carried by **prose paragraphs** with real transitions between ideas — "because of that", "which means", "the problem with this is". A reader should be able to follow one continuous line of reasoning from the start of a section to its end.
    Bulleted lists must **not** be used as a substitute for explanation. Lists are for genuine enumerations only: a parameter table, a checklist, a list of links, a set of options being compared.
    Why: a page of bullets looks organised but teaches nothing. The connective reasoning *between* the points is exactly what the learner does not yet have and cannot infer.

    ### Rule 3 — Adaptive structure
    There is **no fixed section order and no required section list.** The author picks the sections this specific topic genuinely needs from the template's menu, reorders them into whatever order teaches best, and may invent a section the menu never anticipated.
    - Sub-headings are named after the actual domain concept being explained. `### Overview`, `### How does it work?`, `### Key Concepts`, `### Details` are all non-compliant. Name the thing.
    - Every omitted menu section is recorded in the template's **Adaptation Note** with a one-line reason specific to this topic. "Not needed" is not a reason. Omission is fine; silent omission is not.

    ### Rule 4 — Coverage is enumerated, then verified
    Adaptive must not become thin.
    1. **Before writing:** enumerate the topic's sub-concepts — every distinct idea a reader must hold to understand this topic — in the template's Coverage Plan. Name actual mechanisms, stages, parameters, failure modes, and neighbouring concepts, not vague buckets. Do not trim the list to make the writing easier.
    2. **Before submitting:** verify every enumerated sub-concept is genuinely explained in the body, not merely name-dropped.

    ### Rule 5 — 800-word explanatory prose floor
    Each topic note contains a minimum of **800 words of genuine explanatory prose**, measured across the body as a whole rather than per section. "Genuine" means each sentence adds a mechanism, a reason, a consequence, a constraint, a name, or a number. Padding, hedging, restating the title, and repeating an earlier sentence in new words are **violations of this rule, not ways to satisfy it**. If the floor is out of reach, go deeper — another mechanism, a concrete consequence, an edge case, a worked case — never repeat yourself in new words. The count excludes the metadata line, diagrams, code, tables, HTML comments, and the Further Reading list.

    ### Rule 6 — Explain the mechanism, not just the definition
    A definition alone is non-compliant. Wherever a concept is introduced, the note must also say **how it actually works** — the process or system behaviour that produces the result — and **where it shows up in [TOOL/PLATFORM]**: a specific command, API call, UI location, config field, or observable output the reader could go and look at. This applies wherever the concept is explained; it does not require a section with any particular name.

    ### Rule 7 — Snippets are scenario-first, not topic-first
    Any code or configuration snippet opens with a comment naming the real operational problem it solves and the constraint that makes this the right choice.
    Non-compliant: a comment that only names the feature or command being demonstrated.
    Snippets must be syntactically valid for their language. Include a snippet only when there is code or configuration a reader would actually write — inventing code for the sake of having code is non-compliant.

    ### Rule 8 — Answer rationales cover the distractor
    Any self-check answer explains why the correct answer is right **and** why the most tempting wrong answer fails. One-word rationales are non-compliant. For multi-select, explain why each correct option qualifies and why the most tempting wrong option does not. This rule governs self-check questions when a note has them; it does not require that a note have them.

    ### Rule 9 — Derived artifacts introduce no new facts
    `00-intro.md` and `99-podcast.md` are derived artifacts. Every claim, number, name, and definition in them must already appear in a sibling topic note in the same chapter. They summarise and connect; they do not research. If a derived artifact needs a citation, that is the signal it is smuggling in a new fact — cut it, or add it to the relevant topic note first. `99-podcast.md` additionally contains **zero code blocks** (and no tables or diagrams): it is spoken audio, so anything technical is described in words.

    ---

    ## Authoring Order

    Order is not optional:

    1. **First:** all topic notes (`01-…`, `02-…`, …) for the chapter, plus `interview-prep.md` and `thought-leadership.md`. These are researched and written from sources.
    2. **Last:** `00-intro.md` and `99-podcast.md` — and only once **every** topic note in that chapter is complete and non-stub.

    Why: both derived artifacts exist to synthesise the topic notes. The intro maps how the chapter's topics interconnect; the podcast retells them as conversation. Writing either one earlier means guessing at content that does not exist yet, which guarantees drift between the derived file and the notes it claims to summarise. If any topic note in the chapter is still a stub, stop and finish it before touching the intro or the podcast.

    ---

    ## File Naming Rules
    (Adjust based on repo naming style)
    - Topic notes: `01-<topic-slug>.md` … `NN-<topic-slug>.md` / `01_<TOPIC_SLUG>.md` … `NN_<TOPIC_SLUG>.md` — zero-padded, contiguous from `01`, `NN` never exceeds `06`
    - Chapter intro: `00-intro.md` / `00_intro.md` — **reserved slot**, one per chapter
    - Podcast: `99-podcast.md` / `99_podcast.md` — **reserved slot**, one per chapter
    - Interview prep: `interview-prep.md` / `interview_prep.md` — **unnumbered**
    - Thought leadership: `thought-leadership.md` / `thought_leadership.md` — **unnumbered**
    - Labs: `LAB_XX_snake_case.md` / `LAB-XX-kebab.md` (global sequence)
    - Section folders: `SECTION_XX_NAME/` or `01-name/`
    - Module folders: `MODULE_XX_Name/` or `01-name/`
    - Chapter folders: `CHAPTER_XX_Name/` or `01-name/`

    `00` and `99` are reserved for the chapter intro and the podcast. Topic notes never take them. `interview-prep.md` and `thought-leadership.md` carry no number at all, so they cannot collide with a topic note however many there are.

    ---

    ## Markdown Style
    - H1 for file title, H2 for major sections, H3 for sub-sections
    - All code blocks carry a language tag
    - Horizontal rules (`---`) separate every major section
    - Self-check answers use `<details><summary>Answer</summary>` collapsible blocks, when a file includes self-check questions
    - HTML comments (`<!-- -->`) carry authoring guidance in templates — preserve them

    ## What Not to Do
    - Do not populate stubs without explicit user instruction
    - Do not paraphrase syllabus or exam objectives — quote verbatim from the source of truth
    - Do not add content not traceable to the authoritative source
    - Do not author a chapter intro (`00-intro.md`) or podcast (`99-podcast.md`) while any topic note in that chapter is still a stub
    - Do not introduce into a derived artifact (`00-intro.md`, `99-podcast.md`) any fact absent from the sibling topic notes
    - Do not renumber or rename files or folders after scaffold — filenames are locked once U5 writes them. That includes renumbering topic notes, moving a topic note into the reserved `00`/`99` slots, and adding a number to `interview-prep.md` or `thought-leadership.md`. Authored chapters may forward-link to not-yet-written stubs; those links resolve when the target is populated. Renaming to "fix" a link breaks every other reference to that file.
    - Do not link to third-party blogs, Medium, or YouTube
    - Do not skip or merge sections without user approval
    ````

  `templates/*`, `templates/README.md`, `AGENTS.md`, and (in U5) `README.md` are the **only** non-stub files in the repo. Touch nothing else in this unit.
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

    No headings, no tables, no prose — one comment line only. This applies to all section/module/chapter content files, `progress-tracker.md`, `00-roadmap/learning-roadmap.md`, and all capstone files. Section, module, and per-chapter artifact stubs point to their specific template:

    ```markdown
    <!-- stub: populate using templates/section-index-template.md -->
    ```
    ```markdown
    <!-- stub: populate using templates/module-index-template.md -->
    ```
    ```markdown
    <!-- stub: populate using templates/topic-notes-template.md -->
    ```
    ```markdown
    <!-- stub: populate using templates/chapter-intro-template.md -->
    ```
    ```markdown
    <!-- stub: populate using templates/chapter-podcast-template.md -->
    ```
    ```markdown
    <!-- stub: populate using templates/interview-prep-template.md -->
    ```
    ```markdown
    <!-- stub: populate using templates/thought-leadership-template.md -->
    ```
  - **Idempotency rule.** Before writing a stub, check whether the file already exists with content beyond the stub line. If it does, **skip it — never overwrite.** This makes U5 re-runnable: re-invoking it after an interruption creates only missing files and leaves authored content intact.
  - **README.md** — the one content file written here. Include: H1 title (actual topic/cert name); goal statement (what the repo is, who for, what the reader can do after); learning path table (Phase | Section | Estimated hours | Focus area); repository structure (top 2–3 levels only); section summaries (one bullet per section, relative link + one-line description); file type guide (File type | Pattern | Purpose | Created at scaffold?); certification/exam target (only if a cert exists). Use only the user's topic name, section names, and goal — no generic boilerplate or assumed tool names.
  - **Use `TodoWrite` for large repos.** For repos with more than 20 files, track scaffold progress: mark each section `pending` → `in_progress` → `completed` as its files are written; write one section at a time.
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
  Chapter intros:        N  (stubs, 00-intro.md — one per chapter)
  Topic notes:           N  (stubs, NN-<topic-slug>.md — 2–6 per chapter)
  Interview prep:        N  (stubs, one per chapter)
  Thought leadership:    N  (stubs, one per chapter)
  Podcasts:              N  (stubs, 99-podcast.md — one per chapter)
  Lab stubs:             N  (if applicable)
  Capstone stubs:        N
  Template files:        N  (fully populated, incl. templates/README.md)
  AGENTS.md:             1  (fully populated)
  README.md:             1  (fully populated)
  ────────────────────────────────
  Total files:           N
  ```

  Then tell the user: *"All content files are blank stubs. Ask me to populate any file, chapter, or section and I will follow `templates/topic-notes-template.md` and the Content Depth Rules in `AGENTS.md`."* Then state the authoring order: topic notes come first — plus `interview-prep.md` and `thought-leadership.md` — and `00-intro.md` and `99-podcast.md` come **last**, only once every topic note in that chapter is complete, because both are derived from those notes and introduce no fact absent from them. Remind them that module-level index files are created on request (not at scaffold time). → Hand control back for the scaffold confirmation.
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

    **Next step:** read `templates/authoring-guidelines.md`, then start populating stubs section by section using `templates/topic-notes-template.md`. Author each chapter's topic notes first (along with `interview-prep.md` and `thought-leadership.md`); leave `00-intro.md` and `99-podcast.md` until last, once every topic note in that chapter is complete.

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
