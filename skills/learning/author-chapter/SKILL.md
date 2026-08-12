---
name: author-chapter
description: Use when the user asks to populate, author, write, or fill in a chapter file, topic note, chapter intro, podcast transcript, interview-prep, or thought-leadership stub in a learning repository or a Markdown study folder. It resolves the target's artifact type from its filename, locates the matching authoring contract on disk, researches live official sources with citations and retrieval dates (or, for derived artifacts, synthesises strictly from the sibling topic notes), drafts the sections the topic genuinely needs, runs the matching mandatory quality gate as a self-audit, then writes one file only after every check passes. It refuses to author a chapter intro or podcast while any sibling topic note is still a stub. Do NOT use to scaffold a new repo (that is create-learning-repo) or to generate quizzes/mock exams (that is generate-practice-exam).
---

# Author Chapter

This skill turns a blank stub (or a thin, incomplete file) into one fully contract-compliant learning file. A chapter folder holds **five kinds of file**, and this skill authors any one of them — resolving which kind it is from the filename before doing anything else.

It is **fully generic** — no topic, tool, vendor, or repo path is hardcoded. The section menu, depth rules, and quality rubric are read from the target repo's own `templates/` and `AGENTS.md` at runtime. When those files do not exist (a loose Markdown folder), the skill falls back to the bundled `reference/quality-gate.md` after confirming with the user.

The workflow is a sequence of discrete **units**. Each unit has a Goal/scope, Inputs, Do, a Self-verify step, and a terse Report contract. Three units are **STOP GATES** where scope, a plan, or a written draft must be confirmed before proceeding. The quality gate (Unit U3) is the doer's own self-audit run against the contract before the draft is written. To keep long files out of the conversation, the draft is **written to the target file first** and the review gate hands back only a short pointer + summary — never the full body.

**What this skill does:**
- Resolves the target's **artifact type** from its filename — chapter intro, topic note, interview prep, thought leadership, or podcast — and uses it to select the template, the depth rules, and the quality-gate rubric
- Reads the authoring contract (template + depth rules) for that artifact type from disk
- For **source-based** artifacts (topic note, interview prep, thought leadership): researches the topic from live official sources, with citations and retrieval dates
- For **derived** artifacts (`00-intro.md`, `99-podcast.md`): skips live research and synthesises strictly from the sibling topic notes — and **refuses to start** while any sibling topic note is still a stub, because derived artifacts are authored last
- Drafts the sections this artifact and topic genuinely need, chosen from the template's suggested menu, in the order that teaches best — recording omitted suggested sections in the Adaptation Note
- Runs the matching pass/fail quality gate and fixes failures before writing the draft to the target file
- Writes the draft to the file first, then hands back only a short pointer + summary for review (never the full body); finalizes on approval (idempotent — never clobbers pre-existing authored content without confirmation)

**What this skill does NOT do:**
- Scaffold folders, templates, or new repos (use `create-learning-repo`)
- Generate standalone quizzes or mock exams (use `generate-practice-exam`)
- Author more than the file(s) the user explicitly names

---

## HOW TO RUN THIS SKILL

Read this first. It is the whole run, end to end. Do the steps in order.

1. **Resolve the target.** Get one exact file path. Read the file. Classify it **stub** or **has-content**. (U0)
2. **Resolve the artifact type from the filename** using U0's routing table, and write it down. It selects the template, the research mode, and the gate. (U0)
3. **Find the contract on disk.** Walk up from the target's folder looking for `AGENTS.md`, `templates/`, and `templates/authoring-guidelines.md`. Select the template for this artifact type. (U0)
4. **Derived artifacts only** (`00-intro.md`, `99-podcast.md`): list the chapter folder and classify every sibling topic note **Authored** or **Stub/thin**. Any stub → **stop and refuse**. (U0)
5. **STOP GATE** — present target, artifact type, contract source, and template. Wait. (U0)
6. **Build the source brief.** Branch A (topic note, interview prep, thought leadership) = live official-source fetches with retrieval dates. Branch B (chapter intro, podcast) = read every sibling note in full, no web research. (U1)
7. **STOP GATE** — present the brief. Wait for approval. (U1)
8. **Draft against the template's own procedure.** The on-disk template carries the step-by-step authoring phases; follow them. Draft section by section, checking each section as you finish it. (U2)
9. **Run the gate that matches the artifact type**, recording a measured value for every row. Fix each ✗, re-run that check. (U3)
10. **Write the file** to the confirmed target path. (U2)
11. **STOP GATE** — hand back only a pointer + short summary. Never paste the body into chat. (U2)
12. **Finalize and report** the compliance block, then name the next logical stub without authoring it. (U4)

**The two failure modes that ruin this skill, and their fix:**

- **Drafting before reading the on-disk template.** Always read the template for this artifact type first, in full. It overrides this skill. This skill only routes, orders, gates, and stops — the drafting procedure lives in the template.
- **Reporting a gate as PASS without running the measurements.** Every gate row needs recorded evidence: a number, a filename, or a quoted line. A tick with no measurement behind it is a failed row, not a pass.

---

## When to use this skill

Trigger on requests like:
- "populate this chapter / stub / topic note"
- "author the notes for [topic]"
- "fill in `<chapter>/02-<topic-slug>.md`"
- "write the chapter intro (`00-intro.md`) now that the topics are done"
- "write the podcast transcript (`99-podcast.md`) for this chapter"
- "author `interview-prep.md` / `thought-leadership.md` for this chapter"
- "write the [chapter name] topic notes following the template"

Do **not** trigger if the user wants to create a new repo, generate an exam/quiz, or edit non-learning content.

---

## Shared reference material (defined once — referenced by the units)

Every unit below points to this section instead of restating rules. Do not duplicate this material inside a unit.

### The per-chapter file layout

A chapter folder holds five kinds of file. The filename determines the artifact type, and the artifact type determines everything else:

```
<chapter>/
  00-intro.md              <- chapter overview + how the topics interconnect. DERIVED, authored LAST.
  01-<topic-slug>.md       <- topic note. 2-6 per chapter. Authored FIRST.
  02-<topic-slug>.md
  ...
  interview-prep.md        <- authored alongside the topic notes
  thought-leadership.md    <- authored alongside the topic notes
  99-podcast.md            <- two-speaker conversational transcript. DERIVED, authored LAST.
```

**DERIVED artifacts** (`00-intro.md`, `99-podcast.md`) may only be authored once **every** topic note in the chapter is complete and non-stub, and must introduce **no fact absent from those sibling notes**. They synthesise; they do not add.

### The authoring contract (source of truth)

The section menu and depth rules come **from disk, not from this skill**. Resolve the contract in Unit U0 — keyed to the artifact type resolved there — and reuse it in every later unit:

| Found at/above the target file | Contract used |
|---|---|
| `AGENTS.md` + `templates/` both present | Structured learning repo. Read both; they are authoritative. Read the template matching the resolved artifact type, plus `templates/authoring-guidelines.md` if present. |
| Neither present (loose Markdown folder) | After user confirmation only, fall back to the built-in `reference/quality-gate.md` and its filename → rubric routing table. |
| Partial (one present) | Use whatever is present; fall back to `reference/quality-gate.md` for the missing piece; tell the user which contract applies. |

Template selection is **per artifact type**. In a structured repo, prefer the repo's own file; the names below are the conventional ones and the skill must tolerate a repo naming them differently:

| Artifact type | Template to read |
|---|---|
| Topic note | `templates/topic-notes-template.md` |
| Chapter intro | `templates/chapter-intro-template.md` |
| Podcast | `templates/chapter-podcast-template.md` |
| Interview prep | `templates/interview-prep-template.md` |
| Thought leadership | `templates/thought-leadership-template.md` |

> **Never hardcode the section list.** When the repo has a template for this artifact type, its section menu and headings win. If the repo has no `templates/` — or has no template for this artifact type — fall back to `reference/quality-gate.md`, whose routing table maps the filename pattern to the applicable rubric, section menu, and gate. This is what keeps the skill portable across repos with different templates.

### Depth and quality requirements (contract-driven)

**The on-disk contract is the single source of truth for which sections to write and how deep to go.** That means the repo's `templates/` + `AGENTS.md`, or `reference/quality-gate.md` in fallback mode. This skill deliberately does **not** restate a section list or per-section counts — those drift, and a drifted copy is worse than no copy. Read the contract in U0 and obey it.

**The four hard requirements (topic notes).** These are the only structural floors, and they are non-negotiable. **The on-disk template states each one authoritatively — read it there and obey its numbers.** The summaries below exist only so you know what to look for:

1. **Coverage.** Before writing, enumerate the topic's sub-concepts in the template's **Coverage Plan** block (which stays in the finished file so the gate can read it back). Name real mechanisms, stages, settings, failure modes, and neighbouring concepts — not vague buckets. Before writing the file, verify every enumerated sub-concept is genuinely explained in the body. Adaptive structure is allowed; skipping material is not. If the subject is a **closed enumerable set**, coverage means **every member of that set** — see the enumerable-set rules in U1 and U3.
2. **Prose floor.** The explanatory body, **taken as a whole**, must reach the template's stated minimum of genuine explanation — **800 words** unless the on-disk template states otherwise. This applies to the document overall, never per section. Padding, hedging, restating the title, or repeating an earlier sentence in new words is a **violation**, not a way to satisfy it. The count excludes the metadata line, diagrams, code, tables, HTML comments, and the link list.
3. **Reading level / prose-first.** As in the universal rules below.
4. **Source fidelity.** The note carries the exact substance a practitioner needs, not just a feel for the topic. Every exact proper name, designation, term of art, or identifier is spelled as the authoritative source spells it. Every quantity, date, threshold, limit, unit, range, and closed set of permitted values the source states, the note states too. Every artifact whose REQUIRED-IF trigger fired is actually present. An analogy may **illustrate** a mechanism but may **never substitute** for naming the real thing, stating a real number, or enumerating a set. This requirement is graded **independently** of requirement 2: artifacts neither count toward the prose floor nor against it, so adding one can never reduce compliance with the floor.

**Universal voice and prose-first rules (every artifact type).**

- Write for a **bright 14-year-old**. Short sentences. One idea per sentence. Plain everyday words wherever a plain word exists. Active voice. Warm, never condescending.
- Expand every **acronym** the first time it appears. Define every piece of **jargon inline, in plain words**, on first use. A definitions table lower down does not excuse an undefined term in the prose above it.
- **Prose paragraphs carry the explanation.** A bulleted or numbered list must never stand in for explaining something. Lists are for genuine enumerations only — a table of settings, a checklist, a list of links, a set of options being compared. This rule targets **bullets used as a substitute for explanation**; it does **not** discourage diagrams, tables, or concrete artifacts, and an artifact a REQUIRED-IF trigger fired for is never in tension with it. Deliver both the artifact and the prose that says what to take from it.
- Explain **why**, not just what. Every sentence must add a mechanism, a reason, a consequence, a constraint, a name, or a number.
- **Adaptive structure.** No fixed section order and no required section list. Choose the sections this artifact and topic genuinely need from the template's suggested menu, order them so they teach best, and invent a section the menu never anticipated if the topic calls for one. Name every sub-heading after the **real domain concept** it discusses — generic headings ("Overview", "How does it work?", "Key Concepts", "Details") are non-compliant. Never leave an empty heading or "not applicable" filler; omit the section and record it in the **Adaptation Note**.

**What each artifact type is for, and its distinctive bar.**

| Artifact type | What it is for | Distinctive bar |
|---|---|---|
| **Topic note** (`NN-<slug>.md`) | The primary teaching artifact: one topic explained start to finish for someone who has not seen it before. | All four hard requirements apply here most strictly — Coverage Plan, prose floor, domain-named sub-headings, and source fidelity. |
| **Chapter intro** (`00-intro.md`) | An overview of every topic in the chapter and, above all, **how those topics interconnect** — what depends on what, what competes with what, what order to learn them in. | The connective map is the reason the file exists. A bare list of topic titles is non-compliant. Derived: no new facts, and a suggested reading order with a stated reason. |
| **Podcast** (`99-podcast.md`) | A two-speaker conversational transcript covering every topic at orientation depth. Spoken audio on the page. | Genuine back-and-forth, not two monologues. Consistent generic role labels, never invented personalities. **Zero code blocks** — nothing that cannot be said aloud. Breadth over depth. Derived: no new facts. |
| **Interview prep** (`interview-prep.md`) | Role-targeted question and answer preparation. | Questions realistic for the stated role and seniority, not trivia. Each answer is substance a candidate could say out loud, with the reasoning behind it so a follow-up is survivable, plus weak-answer traps specific to *this* subject matter — never generic interview advice. |
| **Thought leadership** (`thought-leadership.md`) | One original, defensible argument in the author's own voice. | Takes a position in its opening lines, no throat-clearing clichés, anchors the argument in a concrete example or number, states the strongest counterargument fairly and answers it, and leaves a concrete takeaway. A neutral summary is non-compliant. |

### Source hygiene (applies to all research and links)

- Only official documentation counts as a citable source — no third-party blogs, Medium, or YouTube.
- Format every link as `[Title](url) — *verified YYYY-MM-DD*`, verified live this session.
- Quote exam objectives **verbatim** — never paraphrase them.
- Flag any fast-evolving feature inline with a note to re-verify before relying on it.
- Never invent a URL, document title, product name, parameter, figure, or verification date.
- **Derived artifacts cite nothing new.** For a chapter intro or podcast, the source *is* the sibling topic notes. If the draft seems to need a fresh citation, that is a signal it is smuggling in a new fact — cut it, or add it to the relevant topic note first as a separate authoring task.

### Draft discipline

- Match the repo's naming style (ALLCAPS-underscore vs lowercase-hyphen) and answer-format convention (inline `<details>` vs separate key) detected in Unit U0.
- Leave zero `<!-- TODO -->`, `TBD`, or `STUB` markers, and no leftover square-bracket template placeholders.
- Record every omitted suggested section in the **Adaptation Note**, with a one-line reason specific to *this* topic. "Not needed" is not an acceptable reason — say what about this topic made the section unhelpful. Omission is fine; silent omission is not.
- Depth calibration: the **prose explanation and worked examples carry the teaching load** and should dominate. Diagrams, tables, concrete examples, and questions support that load — they illustrate and test what the prose explained, and never stand in for it. The reverse also holds: prose never stands in for an artifact a trigger required. Deliver both, and do not invert these proportions.

### Constraints and guardrails (non-negotiable, all units)

- **Contract comes from disk, not this skill.** When the repo has `templates/` + `AGENTS.md`, they win. The built-in `reference/quality-gate.md` is a fallback for loose folders only, and its use must be confirmed with the user.
- **Artifact type drives everything.** Resolve it from the filename in U0. It selects the template, the depth rules, the research mode in U1, and the gate rubric in U3.
- **Derived artifacts introduce no new facts.** A chapter intro or podcast may contain nothing absent from the sibling topic notes. If a needed fact is missing, the correct action is to add it to the proper topic note first — a separate authoring task — never to invent it here.
- **Sibling-readiness refusal.** Never author a chapter intro or podcast while any sibling topic note is a stub or too thin to synthesise from. U0 **stops and refuses** — it does not warn and continue. A derived artifact written over stubs is worthless.
- **Voice and reading level are requirements, not style preferences.** Bright-14-year-old register, short sentences, acronyms expanded and jargon defined inline on first use, and explanation carried by prose rather than lists — in every artifact type.
- **Never overwrite authored content without explicit confirmation.** Only populate stubs freely.
- **Always research live in Unit U1 — for source-based artifacts.** Topic notes, interview prep, and thought leadership must be grounded in live official docs, cited with URL + retrieval date. **Derived artifacts (chapter intro, podcast) are exempt:** they skip live research and read the sibling topic notes instead, using the web only to re-verify a link they carry over.
- **The quality gate (Unit U3) is mandatory.** A file is not "done" until every row of the rubric for *its* artifact type is ✓.
- **Author only what the user named.** Do not batch-populate a chapter or module unless explicitly asked.
- **Windows-safe:** quote paths with spaces; do not assume forward slashes.

### STOP CONDITIONS (consolidated — every place the skill must stop and ask)

**Stopping is expected, correct behaviour.** It is a successful outcome of the run, not a failure of it. Fabricating content — a section, a number, a URL, a synthesis over stubs — in order to avoid stopping is the **worse failure**, because a confidently wrong file looks finished and will not be fixed. When in doubt, stop and say what you need.

| # | Situation | Detected in | Say this to the user |
|---|---|---|---|
| 1 | The target already has real authored content and the user has not said how to handle it | U0 | "`[path]` already has authored content. Rewrite it, extend it, or leave it?" Then wait. |
| 2 | No `templates/` and no `AGENTS.md` anywhere above the target, and the fallback has not been confirmed | U0 | "This folder has no authoring contract. I'll author using the built-in standard structure (`reference/quality-gate.md`) — confirm?" Then wait. |
| 3 | A derived artifact (`00-intro.md`, `99-podcast.md`) whose siblings are stubs or too thin | U0 | Name the exact stub filenames, say a derived artifact can only synthesise what the notes already say, and refuse. Do not offer a reduced-scope version. |
| 4 | Official sources unreachable for a source-based artifact (every fetch failed, or no network) | U1 | "I cannot reach the official documentation, so I will not write from memory. Paste the relevant official excerpts, or supply source material, and I'll continue." |
| 5 | A needed fact — a name, number, limit, default, or version — is absent from every available source | U1 or U2 | Name the fact, name the sources you checked, and ask for it. Never substitute a plausible-sounding value. |
| 6 | A derived artifact needs a fact no sibling note contains | U1 or U2 | Name the fact and the topic note it belongs in. Ask whether to drop the point or pause and author it into that note first. |
| 7 | The topic is really two or more topics (the Coverage Plan will not decompose into one note) | U1 or U2 | Say what the two topics are and ask whether to split the stub. Splitting is a scope decision, not yours to make silently. |
| 8 | The 800-word prose floor cannot be reached with genuine explanation | U2 or U3 | Report the measured word count and the gap. Ask for more source material or a wider scope. Do **not** pad — padding is a gate failure, not a workaround. |
| 9 | Two sibling notes contradict each other on something a derived artifact must state | U1 or U2 | Quote both claims and their filenames. Ask which is correct. Do not silently pick a side. |
| 10 | The subject is a closed enumerable set, but its **complete** membership cannot be confirmed from an authoritative source | U1 or U2 | Name the set, the source you read, and the members you could confirm. Say that a partial list teaches the reader the rest do not exist, so you will not publish one. Ask for the authoritative list. |
| 11 | The **source member count** cannot be established, or the source count and the Coverage Plan count disagree and the discrepancy cannot be resolved | U1, U2 or U3 | Report both numbers (or say which one is unavailable) and the source and date you read. Ask which count is authoritative. Never split the difference and never guess the count. |

**How to stop:** do not write a partial file and report success. State (a) exactly what is missing, (b) what you checked, (c) what you need in order to continue. Then hand control back and wait.

---

## Workflow

The units run in order U0 → U4. Three of them are STOP GATES that hand control back for confirmation (U0 scope, U1 research brief, U2 draft review); the rest are self-verified by the doer. Do not skip the STOP GATES and do not combine a gate with the next unit in one response.

### Unit U0 — Resolve artifact type, locate the authoring contract & confirm scope

- **Goal/scope**: determine **what kind of file** this is, find the rules it must follow, confirm the derived-artifact prerequisites are met, and lock the exact target file — all before writing anything.
- **Inputs**: the file path or chapter/topic name the user named.
- **Do**: run steps 1–8 in order. Do not skip step 2 or step 4.

  **1. Resolve the exact target path.** Confirm one file path. If the user named a chapter or topic but not a file, glob the folder, list the candidate stub(s), and ask which one. Do not guess when two candidates match.

  **2. Read the target and classify it.** Open the file and count what is in it:

    | The file contains | Classification |
    |---|---|
    | Nothing, or a single HTML comment line (e.g. `<!-- stub: ... -->`) | **Stub** — safe to populate |
    | A `> **Status:** STUB` marker | **Stub** |
    | Only an H1 title, with or without a metadata line | **Stub** |
    | Only template placeholder brackets (`[Topic Title]`) or `TODO`/`TBD`/`STUB` | **Stub** |
    | Too little written to build on — no explanatory paragraph anywhere | **Stub** |
    | Anything more: at least one real explanatory paragraph | **Has real content** — do not overwrite silently (STOP GATE case (a)) |

  **3. Resolve the ARTIFACT TYPE from the filename.** Match the filename against this table and **write the result down**. It determines the template, the depth rules, the research mode in U1, and which quality-gate rubric applies in U3:

    | Filename pattern | Artifact type |
    |---|---|
    | `00-intro.md`, `intro.md` | **Chapter intro** (DERIVED — authored last) |
    | `NN-<slug>.md` — numbered, not `00` or `99` (e.g. `01-<topic-slug>.md`) | **Topic note** (authored first) |
    | `interview-prep.md` | **Interview prep** (authored alongside the topic notes) |
    | `thought-leadership.md` | **Thought leadership** (authored alongside the topic notes) |
    | `99-podcast.md`, `podcast.md` | **Podcast** (DERIVED — authored last) |
    | anything unrecognised | **Default to topic note** — and say so explicitly at the gate, so the user can correct the assumption |

  **4. Find the contract by walking up the tree.** Start in the target file's directory and walk toward the filesystem root, at each level looking for:
    1. `AGENTS.md` — depth rules, naming style, answer format.
    2. `templates/` — the section menus and the per-artifact authoring procedures.
    3. `templates/authoring-guidelines.md` — voice, adaptive-structure, and authoring-order rules.

    Stop at the first level that has `templates/`. Read every one you found. Then resolve which contract applies using the **authoring contract** table in shared reference material.

  **5. Select the template for the resolved artifact type** using the per-artifact template table in shared reference material — `topic-notes-template` / `chapter-intro-template` / `chapter-podcast-template` / `interview-prep-template` / `thought-leadership-template` — tolerating a repo that names them differently. If the repo has no `templates/`, or has no template for this artifact type, fall back to `reference/quality-gate.md` and use its filename → rubric **routing table** ("How to use this file") to pick the section menu and gate. Record which file you selected; U2 will read it in full before drafting.

  **6. SIBLING-READINESS GATE — chapter intro and podcast only.** Derived artifacts are authored last, so before planning anything:
    1. Glob the chapter folder. Read the **actual** filenames — do not work from the chapter title or from memory.
    2. Write down every numbered topic note found, plus `interview-prep.md` and `thought-leadership.md` if present.
    3. Open **each** numbered topic note and classify it with the same test as step 2: **Authored** (at least one genuine explanatory paragraph, enough to synthesise from) or **Stub/thin**.
    4. Record the tally as `N authored / N stub`.
    5. **Decision rule:** every numbered topic note Authored → continue to step 7. **One or more Stub/thin → stop and refuse** at this unit's gate. Do not warn and continue. Do not proceed to U1. Do not offer a reduced-scope derived artifact.
    6. If you stopped: report the exact stub filenames and that this same skill can author them.

    (Skip this step entirely for topic notes, interview prep, and thought leadership — they are authored *first* and have no such prerequisite.)

  **7. Gather chapter context.** Read the parent section/module index (if present) for the chapter's declared exam objective, topic scope, and estimated time. Read 1–2 already-authored siblings (if any) to match voice, depth, and formatting. Note the repo's naming style (ALLCAPS-underscore vs lowercase-hyphen) and answer-format convention (inline `<details>` vs separate key) so the draft matches.

  **8. Present the STOP GATE below.** Do not start research in the same response.
- **Self-verify**: a single target file is selected and classified; the **artifact type is resolved** (and any fallback-to-topic-note assumption is flagged); the contract source is resolved (repo `templates/`+`AGENTS.md`, partial, or built-in fallback) along with the template for this artifact type; for derived artifacts, the sibling-readiness classification is complete and every topic note is Authored; naming style and answer format are noted.
- **STOP GATE (hand back)**: present target file, resolved artifact type, contract source + selected template, and topic/objective, and **stop to confirm** before research. Three cases force this gate:
  - (a) the target **has real content** — ask whether to rewrite, extend, or leave it; never overwrite authored content silently;
  - (b) the folder is loose (no `AGENTS.md`/`templates/`) — state "I'll author using the built-in standard structure (`reference/quality-gate.md`)" and get confirmation before continuing;
  - (c) **sibling-readiness failed** for a derived artifact — refuse and stop with wording like:

    > "`00-intro.md` and `99-podcast.md` are derived artifacts: they may only summarise what the topic notes already say, so I can only author them once every topic note in this chapter is complete. These are still stubs or too thin: [list]. Please author them first — this same `author-chapter` skill does that — then re-run me on [target]. I will not write a chapter intro or podcast over stubs, because it would be guesswork rather than a synthesis."

    → Hand control back for the authoring decision. Do not offer a reduced-scope derived artifact; a partial synthesis of a chapter is not a valid artifact.

  → Otherwise, hand control back to the user/orchestrator for the scope/contract decision.
- **Report contract**: `target: <path> (<stub | has-content>) | artifact type: <topic note | chapter intro | podcast | interview prep | thought leadership> (<from filename | defaulted>) | contract: <repo templates/AGENTS.md | partial | built-in fallback> | template: <selected template or fallback rubric> | siblings: <n-a | N authored / N stub> | topic/objective: <...> | awaiting: <scope confirmation | topic notes to be authored first>`.

### Unit U1 — Build the source brief (live research, or derived synthesis)

- **Goal/scope**: ground the file in the right source and present a plan for approval. The **artifact type resolved in U0 decides which source is correct** — and using the wrong one is a defect, not a shortcut.
- **Inputs**: confirmed target, artifact type, and contract from U0; the topic/objective.
- **Do**: pick the branch from the artifact type resolved in U0. Run one branch only.

  **Branch A — source-based artifacts: topic note, interview prep, thought leadership.** Research live. Never write technical content from training data alone — product names, interfaces, and exam objectives drift.

  1. **List the fetch targets before fetching.** Write down (a) the **official documentation** page for the topic (primary source for mechanism and parameters); (b) **the exam/objective wording** if a certification is involved; (c) the **changelog / "what's new"** page if the topic is fast-evolving.
  2. **Fetch them in parallel** with `webfetch`, in one message. Record URL + retrieval date for each.
  3. **Judge each result** as one of three outcomes and act on it:

     | Fetch outcome | Do this |
     |---|---|
     | Full page returned | Keep it. Note the URL + today's date. |
     | Truncated (page too long) | Fetch a more specific sub-page, or delegate a targeted read to the `explore` agent. Never author from truncated output. |
     | Thin (a landing page, a redirect, a table of contents, no mechanism) | Retry once with a more specific sub-page URL. |
     | Failed / unreachable | Retry once with a more specific sub-page URL. |

  4. **Retry rule.** One targeted retry per failed or thin fetch. If the retry also fails or is still thin, do **not** substitute training data and do **not** substitute a non-official source. Go to step 5.
  5. **Fallback rule (STOP).** If official sources cannot be reached for the topic, **stop** — see STOP CONDITIONS row 4. Tell the user and offer two paths: (a) paste the relevant official-doc excerpts into the chat, or (b) run `create-learning-repo`'s Phase 1 fallback AI-query prompts elsewhere and paste the results back. Only resume once cited source material is available.
  6. **Apply source hygiene** (shared reference material) to every source and link. Reject any third-party blog, video, forum, or aggregator outright — it is not a citable source, however good it looks.
  7. **Quote any exam objective verbatim.** Copy it character for character. Never paraphrase it.
  8. **Enumerate the Coverage Plan sub-concepts** from what the sources actually say. Name real mechanisms, stages, settings, failure modes, and confusable neighbours — not vague buckets like "basics" or "key concepts". If a sub-concept has no supporting source, it must be dropped or asked about, never invented.

  9. **CLOSED-ENUMERABLE-SET EXTRACTION — do this before any drafting.** Ask one question and write the answer down: **is this topic's subject a closed enumerable set?** A closed enumerable set is a subject whose members are a finite, documented list. Answer **yes** if any of these holds: the subject *is* one of these kinds of list (permitted values, result or status codes, selectable options, lifecycle or workflow states, error categories, allowed roles, supported units, taxonomic ranks, statutory articles or subsections, treaty signatories, named periods or dynasties, musical modes, grammatical cases, classification tiers, official grades or rankings); the source documents the subject *as* a list a reader could count; or a reader would reasonably ask "what are all of them?".

     **If yes, all four are mandatory before you draft a single sentence:**
     1. Open the authoritative source and **extract the COMPLETE member list**. Not the common ones. Not the ones you happen to remember. All of them.
     2. **Record the source URL, the retrieval date (YYYY-MM-DD), and the SOURCE MEMBER COUNT** — the number of members that source lists — into the brief, and later into the Coverage Plan.
     3. List every member in the brief **exactly as the source names them**, character for character.
     4. Plan for **one complete table** in the body with **one row per member**. A member mentioned only in passing in prose does not satisfy this.

     **CAUTION — do not widen the set. A related-but-distinct item is NOT a set member.** Only what the source lists as a member is a member. A neighbouring concept, control, or setting that merely *influences* the set is not part of it. Naming such a neighbour as a member is a factual error that teaches the reader something false, and it is a common one: the neighbour usually appears on the same page as the list, so it feels like it belongs. Check membership against **the source's own list**, not against the page it appears on. Genuine neighbours go in "deliberately out of scope" or a "commonly confused with" note.

     **If no,** record one line in the brief saying why this subject has no finite member list.

     If you cannot confirm the complete membership or establish the source member count, **stop** — see STOP CONDITIONS rows 10 and 11.

  10. **Assemble the research brief:**
     ```
     ## Research Brief — [Artifact type] — [Topic]

     **Objective covered:** [verbatim objective or topic scope]
     **Sources:**
     - [url] — verified [date] — [what it provides]

     **Coverage Plan (sub-concepts to explain):**
     1. [Sub-concept A] — mechanism + why it matters
     2. [Sub-concept B] — ...
     3. [Sub-concept C] — ...

     **Closed enumerable set:** [yes / no — if no, one line on why this subject has no finite member list]
     - If yes — Source: [url] — retrieved [YYYY-MM-DD]
     - If yes — SOURCE MEMBER COUNT: [n]
     - If yes — Members, exactly as the source names them: [name, name, name, ...]
     - If yes — Related but NOT members (do not put these in the table): [name — what it does instead]

     **REQUIRED-IF trigger answers (all of T1-T11, none skipped):** [T1 yes/no — ...]

     **Sections planned (from the template menu, in teaching order):** [list]
     **Sections deliberately omitted (for the Adaptation Note):** [section — topic-specific reason]
     **Fast-evolving flags:** [list or "none"]
     ```

  **Branch B — DERIVED artifacts: chapter intro, podcast.** **SKIP live research entirely.** Their source is the sibling topic notes, not the web. Researching the web here is wrong: it is how a derived artifact acquires facts its chapter never taught.

  1. **List the chapter folder again** and write down the exact filenames of every numbered topic note. U0's sibling-readiness gate already confirmed they are all authored.
  2. **Read every sibling topic note in full** — the whole note, not the headings. Add `interview-prep.md` and `thought-leadership.md` where they inform the connective story. You cannot synthesise a note you skimmed.
  3. **Write down a per-sibling inventory row as you read each note.** This inventory is the raw material for the brief and **must be written down before any drafting**. One row per note, in file order:
     `[filename] | [title, in the note's own words] | [the one idea it teaches, in one sentence]`
     If you cannot state the one idea in a single sentence, re-read the note — you have not understood it yet.
  4. **Derive the connections from the inventory**, not from general knowledge. For each pair of topics that genuinely relate, write one line naming the real relationship: A is a prerequisite for B *because …*, C and D are alternatives traded off on *…*, E is the failure mode B creates. A restated topic list is not a connection map.
  5. **Decide the reading order and write the reason.** Default to file order; depart from it only when a later-numbered topic is plainly a prerequisite for an earlier one.
  6. **Podcast only: build one segment plan row per topic** — the angle, the everyday analogy, the question the other speaker pushes back with, the takeaway line. The number of rows must equal the number of numbered topic files.
  7. **Collect the "facts wanted but not present" list.** Any point the intro or podcast seems to need that no sibling note contains goes on this list. **No fact may appear in a derived artifact that is absent from the sibling topic notes.** The correct action is to **add that fact to the proper topic note first** — a separate authoring task, run through this skill on that file — never to invent it here or fetch it from the web. Surface the list at the gate rather than quietly filling the hole.
  8. **Reduce web use to link verification only.** The only permitted fetch is re-verifying an external link carried over from a sibling note, to refresh its `*verified YYYY-MM-DD*` date. Do not fetch new sources, and add no citation the topic notes do not already carry.
  9. **Assemble the derived brief:**
     ```
     ## Derived Brief — [Chapter intro | Podcast] — [Chapter]

     **Sibling notes read (all confirmed authored):**
     - [file] — covers: [one line, in the note's own terms]

     **Topic inventory:** [each topic + the single idea it contributes to the chapter]

     **Connections to explain:** [A is a prerequisite for B because ... | C and D are
     alternatives, traded off on ... | E is the failure mode B creates]

     **Suggested reading order + why:** [order — reason]

     **Segment plan (PODCAST ONLY):** one segment per topic —
     - [Topic] — angle, the everyday analogy to use, the question the other speaker
       pushes back with, the takeaway line
     **Framing / wrap-up beats (PODCAST ONLY):** [cold open hook, how-it-fits, wrap-up]

     **Facts wanted but NOT present in any sibling note:** [list — each must be added to
     the relevant topic note first, or dropped. Never invented here.] or "none"

     **Links carried over (re-verified):** [url] — verified [date] | or "none"
     ```
- **Self-verify**:
  - *Branch A:* at least the official documentation source was fetched and cited with a retrieval date; any exam objective is quoted verbatim; no source is a non-official blog/video; the brief lists a concrete Coverage Plan and the planned/omitted sections.
  - *Branch B:* every sibling topic note was read in full; no new source was fetched beyond link re-verification; the brief's topic inventory covers every topic file; the connections are real dependencies or trade-offs rather than a restated topic list; the "facts wanted but not present" list is either empty or surfaced for a decision; for a podcast, every topic has a segment plan.
- **STOP GATE (hand back)**: present the brief (research or derived) and **stop**. For Branch A, ask the user to confirm the sources and the Coverage Plan, or adjust it. For Branch B, ask the user to confirm the topic inventory, the connections, the reading order, and — if the "facts wanted but not present" list is non-empty — to decide whether to drop those points or pause and author them into the relevant topic note first. **Do not draft until confirmed.** → Hand control back for the research/plan decision.
- **Report contract**: `mode: <live research | derived from siblings> | sources: <N official (dated) | n-a — derived> | siblings read: <N | n-a> | objective quoted: <yes/n-a> | planned sub-concepts or segments: <N> | missing facts flagged: <N | none> | awaiting: brief approval`.

### Unit U2 — Draft the file, write it, then hand back for review

- **Goal/scope**: write the sections this artifact and topic genuinely need, to the depth the contract requires, **write the draft to the target file**, then hand back a short pointer for review — never the body.
- **Inputs**: approved brief (research or derived) + resolved artifact type, template, and naming/answer-format conventions from U0.
- **Do**:

  **The drafting procedure lives in the TEMPLATE, not here.** The on-disk template selected in U0 carries its own numbered authoring phases — orient, build the plan, choose sections, draft-and-check, map the plan to the body, run the self-audit, stop conditions. **Read that phase block in full and follow it.** This skill does not restate it: a restated copy would drift, and a drifted copy is worse than none. In fallback mode (no repo template for this artifact type), use `reference/quality-gate.md` as the section menu and gate instead.

  **The ordering rule that matters most: draft section by section, checking each section as you finish it.** Do **not** draft the whole file and audit at the end. Checking one section against a handful of tests while it is in front of you is reliable and takes seconds. Auditing a finished 900-word file against the same tests is not — you will skim it and tick rows you did not check.

  Run these steps in order:

  1. **Read the template's own authoring-procedure block in full**, plus its section menu and its self-audit table. Note anything in it that overrides this skill; the template wins.
  2. **Build the plan the template asks for** — the Coverage Plan for a topic note, the connection map for a chapter intro, the segment plan for a podcast — using the approved brief from U1 as its input. Write it into the file's scaffolding block where the template keeps one, so U3 can read it back.
  3. **Choose the sections, then order them.** Select from the template's **suggested menu** (or the fallback rubric's menu) only the sections *this* artifact and *this* topic genuinely need. There is **no fixed section list and no fixed order** — do not include a section merely because the menu lists it, and do invent a section the menu never anticipated if the topic calls for one. Name every sub-heading after the real domain concept it discusses. Order them so that each section makes the next one easier to read.
  4. **Draft and check, one section at a time.** For each section: write it, then immediately check it against the template's per-section tests before starting the next. At minimum, confirm the heading names a real domain concept; every sentence adds a mechanism, reason, consequence, constraint, name, or number; no sentence runs past ~25 words; every acronym used here is expanded at its first appearance in the file; every jargon term is defined in plain words in the same sentence or the next; the explanation sits in paragraphs, not bullets; and any diagram, table, or snippet is explained by the prose around it. Keep a running word count of explanatory prose as you go — U3 needs the total.
  5. **Run Unit U3 (the quality gate) on the draft**, using the rubric for this artifact type, and record a measured value for every row.
  6. **Fix every ✗ row**, then re-run that specific check, then re-run the whole gate. The draft is not ready to write until the gate passes or its unresolvable ✗ rows are surfaced explicitly.
  7. **Write the draft to the confirmed target path** (from U0) with the `Write` tool. This is the draft under review — writing it now is expected and is exactly the file the user will open. Writing the draft first is what keeps the full body out of chat. (The overwrite protection for *pre-existing authored content* was already settled at U0's gate before U1; see the write/overwrite discipline in U4.)
  8. **Hand back a pointer only** — the path, the artifact type, the gate result, the section tally, and the headline depth figure. Never paste the body into chat.

  While drafting, these apply throughout:
  - **Record every omitted suggested section in the Adaptation Note**, each with a one-line reason specific to this topic. "Not needed" is not acceptable — say what about *this* topic made the section unhelpful. Silent omission is a gate failure.
  - **Meet the four hard requirements — non-negotiable for topic notes** (see shared reference material): (1) the **Coverage Plan** is filled in before the body is written and every sub-concept it enumerates is genuinely explained; (2) the explanatory body as a whole clears the **800-word floor** of real explanation, with no padding; (3) **reading level and prose-first** — bright 14-year-old, short sentences, acronyms expanded and jargon defined inline on first use, explanation carried by prose rather than lists, every sub-heading named after the real domain concept it discusses; (4) **source fidelity** — every exact proper name, designation, and term of art spelled as the authoritative source spells it, plus every quantity, date, threshold, limit, unit, range, and closed set of permitted values the source states, and every artifact whose REQUIRED-IF trigger fired actually present. An analogy may illustrate a mechanism; it may never substitute for a real name, a real number, or an enumerated set.
  - Apply the **universal voice and prose-first rules** and the artifact's **distinctive bar** (shared reference material) — for a derived artifact this includes introducing **no fact absent from the sibling topic notes**, and for a podcast it includes zero code blocks.
  - **Keep only the surviving scaffolding blocks, and delete every other one outright** — do not leave a trimmed or summarised version. The template carries a **survival manifest**; obey it. For a topic note, exactly three scaffolding blocks are still in the finished file, filled in and still inside HTML comments: **1. Coverage Plan  2. Adaptation Note  3. Final Self-Audit**. Every other block must be gone before the file is written: the template's header block (including the four hard requirements and the manifest itself), **HOW TO AUTHOR THIS FILE** (all phases), **HOW TO MEASURE THE FOUR HARD REQUIREMENTS** (all recipes), the **WORKED MICRO-EXAMPLE**, the **SUGGESTED SECTIONS MENU**, the **VOICE AND PROSE-QUALITY ILLUSTRATIONS**, the **FURTHER READING — SOURCE HYGIENE** guidance block (the Further Reading section you wrote stays), and **VERSION HISTORY**. Also delete the placeholder first-section heading and every square-bracket placeholder you did not replace. **No `## Version History` heading may appear in a finished note.** Where another artifact type's template carries its own manifest, that manifest governs instead — read it and follow it.
  - Apply **draft discipline** (shared reference material): match naming style and answer format; leave zero TODO/TBD/STUB or bracket placeholders; respect the depth calibration.
  - Apply **source hygiene** to any links. For derived artifacts, add no citation the sibling notes do not already carry.
  - If any STOP CONDITION fires mid-draft — a missing fact, an unreachable floor, a topic that is really two — stop and ask. Do not fabricate to finish.
- **Self-verify**: the U3 gate for this artifact type ran (PASS, or its ✗ rows surfaced) and the draft has been written to the target path.
- **STOP GATE (hand back)**: **do NOT paste the full body into chat.** Present ONLY a short pointer + summary and **stop**: the target file path, the artifact type and rubric used, the U3 quality-gate result (`PASS`, or the specific flagged/unresolved rows), the sections included and those omitted-with-reason, and the headline depth figure for this artifact type (e.g. explanatory word count for a topic note, segment count for a podcast). Instruct the user to **open the file to review** content, section choice and order, depth, and examples, then approve or give corrections. On a **correction request**, re-edit the target file in place and re-point to it — never re-dump the body into chat. → Hand control back for draft review. (If running non-interactively, note the gate result and proceed to U4 with the written draft as-is.)
- **Report contract**: `draft written to <path>, awaiting review | artifact type: <...> | sections: <N included> (<N omitted, recorded in Adaptation Note>) | depth: <explanatory words | segments | Q&A pairs, as fits the artifact> | quality gate: <PASS | N flagged, fixed | N flagged, unresolved> | review by opening the file — full body not pasted`.

### Unit U3 — Quality gate (self-audit, run inside U2 before any hand-back)

- **Goal/scope**: self-audit the draft against the rubric **for its artifact type** before it is shown or written. This is the doer's own verification step — the mandatory gate that guarantees consistency.
- **Inputs**: the drafted file + the artifact type resolved in U0 + the applicable rubric (the repo's `AGENTS.md`/`templates/` rules, else `reference/quality-gate.md`).
- **Do**: run steps 1–5 in order. **Reporting PASS without measuring is the single most common failure of this skill.**

  **1. Select the rubric by artifact type.** Do not run a one-size checklist. Take the rubric from the repo's contract if it has one for this artifact type; otherwise use `reference/quality-gate.md`, which holds **five separate per-artifact gates** — topic note, chapter intro, podcast, interview prep, thought leadership — reached through the filename → rubric **routing table** in its "How to use this file" section. Always run the applicable artifact gate **plus** that file's **Universal rules**. An unrecognised filename runs the topic-note gate, as U0 resolved.

  **2. Run each check and record the actual measured value.** Work through the rubric row by row. For each row, perform the measurement, then write the number, filename, or quoted line you found into the Evidence column. Only then mark the result.

  **3. Mark rows only from recorded evidence.** A row ticked without a recorded measurement **is a failed row**. "Yes", "done", "OK", and "verified" are not evidence — a number, a filename, or a quoted line is.

  **4. For every ✗: fix it, then re-run that specific check** and record the new value. When all the individual fixes are in, re-run the **whole** gate, not just the rows you touched — a fix in one place often breaks another row.

  **5. Declare PASS only when every row has evidence and every result is ✓.** Otherwise report the specific ✗ rows and why they could not be fixed.

  **The gate table.** One row per check in the selected rubric. The rows come from the rubric, not from this skill; the shape looks like this:

    | Check (from the selected artifact rubric) | Measured evidence | Result |
    |---|---|---|
    | [first check for this artifact type] | [the number / filename / quoted line found] | ✓ |
    | [next check…] | [what the measurement actually showed] | ✗ |
    | [universal rule check…] | [evidence] | ✓ |

  **HOW TO MEASURE — do these mechanically, do not estimate.** Apply only the rows that match this artifact type; these mirror the **Deterministic checks** table in `reference/quality-gate.md` and the measurement recipes in the templates.

  - **Placeholder markers (all artifacts).** Search the file for `TODO`, `TBD`, `STUB`, `FIXME`, and unfilled `[bracket]` template markers. Record the hit count outside authoring comments. Required: **0**.

  - **Explanatory word count vs the 800-word floor (topic notes).** Do not eyeball it.
    1. List the explanatory prose paragraphs in body order: P1, P2, P3, …
    2. **Count these:** words inside explanatory prose paragraphs; prose captions under a diagram or table; prose inside a `<details>` answer that explains *why* an answer is right.
    3. **Exclude these:** the `# Title` and every heading and sub-heading; the metadata line; anything inside an HTML comment (including the Coverage Plan and the Adaptation Note); fenced code blocks and diagrams; every table cell; bulleted and numbered list items; the link/further-reading list; the self-audit table.
    4. Count each paragraph's words and write them down individually — "P1 = 74, P2 = 118, …".
    5. Sum them. That sum is the recorded evidence for this row.
    6. Sum ≥ 800 → ✓. Under 800 → ✗, and **do not pad**. Return to the Coverage Plan: usually a sub-concept got one line where it needed a paragraph, a mechanism was asserted without its cause, or a consequence was named without saying who it hurts and when. Explain more; never restate. If genuine explanation cannot close the gap, stop and ask (STOP CONDITIONS row 8).

  - **Unexpanded acronyms (all artifacts).** Scan the file for every token of two or more consecutive capital letters. For each, find its **first** occurrence and confirm the full expansion appears there, not later. Record: acronyms found `[n]`, already expanded `[n]`, fixed `[n]`. Any acronym whose expansion appears after its first bare use is ✗ until fixed.

  - **Paragraph-to-bullet-list ratio (all artifacts).** 
    1. Count the explanatory prose paragraphs in the body. Call it **P**.
    2. Count the bulleted or numbered lists **inside the explanation**. Call it **L**. Do not count as L: the further-reading list, a parameters table, a definitions table, a checklist, a set of options being compared, or the self-check questions.
    3. Apply the rule and record `P = n, L = n`:

       | Result | Verdict |
       |---|---|
       | L = 0 | ✓ |
       | P is at least 3 × L | ✓ — prose is carrying the explanation |
       | P is less than 3 × L | ✗ — the explanation is living in bullets |
       | Any list whose items **are** the explanation of a mechanism | ✗, whatever the ratio |

    4. To fix a ✗: rewrite one offending list as a paragraph that states each point **and** why it is true. Then recount.

  - **Coverage Plan reconciliation (topic notes).** Read the Coverage Plan back out of the file. Take each enumerated sub-concept in turn and find the specific sub-heading or paragraph in the body that explains it. Name that location next to the item. Not found → either write the missing explanation, or delete the item and record one line saying why it does not belong here. Record `[n] of [n] mapped`. An item marked done with no location named is a failed row.

  - **Domain-named sub-headings (all artifacts).** List every sub-heading in the file. For each, ask whether it names a real thing in this subject or only a generic slot ("Overview", "How does it work?", "Key Concepts", "Details", "Background"). Record `headings [n], generic [n]`. Required generic count: **0**.

  - **Source fidelity (topic notes — requirement 4).** Three counts, all recorded, none estimated.
    1. **Exact names.** List every proper name, designation, term of art, and identifier in the draft (a statute section, a species name, a place name, a grade, a field or parameter name). Check each one **character by character** against the source that supplies it. Record `names checked [n], mismatches fixed [n]`.
    2. **Real numbers.** List every quantity, date, threshold, limit, unit, range, and closed set of permitted values the source states for this topic. Confirm each one appears in the note. Record `source-stated values [n], present in note [n]` — the two must be equal. Any value in the note that no source states is an invention: delete it and record `untraceable dropped [n]`, which must reach **0**.
    3. **Delivered artifacts.** Count the REQUIRED-IF triggers answered **yes**, then count how many of those artifacts are actually in the body. Record `triggers fired [n], delivered [n]` — the two must be equal. Fix by writing the missing artifact, or by changing the answer to no with a reason specific to this topic.
    Every subject has names and dates, so this row is never "not applicable". An analogy never counts as a name, a number, or a set.

  - **REQUIRED-IF trigger answers (topic notes).** Read the Adaptation Note back out of the file and check the triggers **T1 through T11** one at a time. Record `answered [n] of 11`; required: **11 of 11**, every one an explicit yes or no. Then record `yes [n], each naming the section that satisfies it [n of n]` and `no [n], each with a reason specific to this topic [n of n]`. A missing answer, a "yes" that names no section, and a "no" whose reason would read identically in a note on any other subject are each a failed row.

  - **Closed-enumerable-set count equality (topic notes whose subject is a closed enumerable set).** Write down three numbers and compare them: (a) the **source member count** recorded in the Coverage Plan, (b) the number of members listed in the Coverage Plan, (c) the number of member rows in the rendered table in the body. Record `source [n] == plan [n] == table rows [n]`. All three equal → ✓. Any disagreement → ✗: re-read the source list, and if the discrepancy will not resolve, stop and ask (STOP CONDITIONS row 11). Also confirm no row is a related-but-distinct neighbour the source does not list as a member. If the subject is not a closed enumerable set, record the one line from the brief saying why, and mark the row not applicable.

  - **Scaffolding survival (all artifacts).** Search the finished draft for the blocks the template's survival manifest says must be gone — its header/requirements block, the authoring phases, the measurement recipes, the worked micro-example, the sections menu, the voice illustrations, the manifest itself, and any `## Version History` heading. Record `non-surviving blocks found [n]`; required: **0**. Then confirm the surviving blocks are present and filled in: `Coverage Plan [y/n], Adaptation Note [y/n], Final Self-Audit [y/n]`. A missing survivor and a leaked non-survivor are each a failed row.

  - **Speaker turns and code fences (podcasts).**
    1. Count `###` topic segments. Compare to the number of numbered topic files. The two must be the same number; record both.
    2. For **each** segment, count `**Host:**` turns and `**Expert:**` turns. Record per segment, e.g. `S1: 4/5, S2: 3/4`. A segment where the questioning speaker appears fewer than 3 times is a monologue → ✗, add real questions.
    3. Confirm the two labels are byte-identical everywhere, including the bold markers and the colon. Search for label drift — `Guest`, `Interviewer`, `Speaker 1`, `Speaker 2`, `Narrator`, `Moderator` — and record the hit count. Required: **0**. No invented person names, no real people.
    4. Count fenced code blocks in the transcript body by searching for lines beginning with three backticks. Record the count. Required: **0**.

  - **Relative links resolve (chapter intro, podcast).** Take each relative link in the file in turn. Check that the path it points to **exists on disk** from the file's own directory. Record `links checked [n], resolved [n], broken [n]`. Any broken link is ✗ until fixed. Do not assume a link is right because you wrote the filename from the folder listing — re-check it against the listing.

  - **Siblings non-stub (chapter intro, podcast).** Re-run U0's sibling classification against the final draft: read every numbered topic note in the chapter and confirm none is a stub or thin. Record `checked [n] notes, [n] stubs`. Anything but 0 stubs means this file should never have been authored — stop and report.

  - **External URLs live (all artifacts with external links).** Re-fetch each external URL. Confirm it is reachable and that its content matches the citation title and the claim it supports. Record `links [n], fetched live [n], non-official rejected [n]`. Never keep a link you could not fetch.

  - **No invented content (all artifacts).** Take every name, number, limit, default, version, and quoted objective in the draft and name the source it came from — a URL for a source-based artifact, a sibling filename for a derived one. Record `traced [n], dropped for lack of a source [n]`. Anything you cannot trace must be cut or asked about, never kept.
- **Self-verify**: the rubric selected matches the artifact type from U0; every row is ✓, or every remaining ✗ is surfaced explicitly with the reason it could not be fixed.
- **Report contract**: folded into U2's report (`quality gate: PASS` or the flagged/fixed/unresolved counts), naming which artifact rubric was run.

### Unit U4 — Finalize and report

- **Goal/scope**: confirm the approved, gated draft is the file's content and report compliance. (The file was already written in U2; correction rounds updated it in place.)
- **Inputs**: approved draft that passed the U3 gate + target path from U0.
- **Do**: run steps 1–5 in order.

  **1. Apply the write/overwrite discipline (reconciled).**
    - The draft-write of **this run** to the confirmed target — the initial write in U2 and any in-place re-edits during correction rounds — is expected and is not what the idempotency guard below is about.
    - **Pre-existing authored content is still protected:** if the target already *had* real authored content (not a stub) at U0, the decision to rewrite/extend was made at U0's STOP GATE before any write. That "never overwrite authored content without confirmation" guardrail remains in force — U2 only wrote because U0's gate authorized it.
    - **Idempotency guard (genuine external/parallel edits only):** re-read the target file. If it was changed *outside this run* (e.g. a parallel edit by someone else since U0) such that its content diverges from the draft this run wrote, **stop and ask** before overwriting. This guard is about foreign edits, not the skill's own draft write of this run.

  **2. Confirm the file at the target path holds the approved + gated draft.** Re-write in place only if a correction round or the guard above requires it.

  **3. Re-confirm the U3 gate was PASS** — every row ✓ with recorded evidence — before reporting anything as finalized. If any row is still ✗, report that instead of a PASS.

  **4. Report, filling every field with the actual value:**
    ```
    Authored:      [path]
    Artifact type: [topic note | chapter intro | podcast | interview prep | thought leadership]
    Contract:      [repo templates/AGENTS.md | partial | built-in fallback]
    Template:      [template or fallback rubric used]
    Sections:      [N included] ([N omitted, each with a reason in the Adaptation Note])
    Depth:         [explanatory word count vs floor | segments | Q&A pairs — as fits the artifact]
    Source:        [N official links verified | derived from N sibling topic notes]
    Quality gate:  PASS ([artifact] rubric — all checks ✓)
    ```

  **5. Suggest the next logical stub in the same chapter, respecting authoring order** — topic notes, `interview-prep.md`, and `thought-leadership.md` first; `00-intro.md` and `99-podcast.md` only once every topic note is complete. Name it; do **not** author it without a new request.
- **Self-verify**: the file exists at the expected path, matches the approved+gated draft, and the U3 gate for this artifact type was PASS (all rows ✓) before finalizing.
- **Report contract**: `finalized: <exact path> | artifact type: <...> | contract: <source> | quality gate: PASS | next stub suggested: <path or none>`.

---

## WORKED EXAMPLE — the shape of one full run

**ILLUSTRATION ONLY.** The subject is a placeholder (`NN-<topic-slug>.md`, "[topic]"). Copy the **shape** of the run, never the content.

```
Target named by user:  <chapter-folder>/03-<topic-slug>.md
U0 step 2  Read it: one line, `<!-- stub: [topic] -->`     -> STUB, safe to populate
U0 step 3  Filename is numbered, not 00 or 99              -> ARTIFACT TYPE: topic note
U0 step 4  Walked up 2 levels: found AGENTS.md + templates/ -> contract: repo (authoritative)
U0 step 5  Selected templates/topic-notes-template.md
U0 step 6  Skipped — sibling-readiness applies to derived artifacts only
U0 GATE    Handed back: target, type, contract, template. User confirmed.

U1  Branch A (source-based). Fetched 2 official pages in parallel; 1 was thin,
    retried a specific sub-page, got it. Coverage Plan: 5 sub-concepts.
U1 GATE    Handed back the Research Brief. User approved.

U2  Read the template's phase block. Built the Coverage Plan into the file.
    Chose 7 sections from the menu, omitted 3 with topic-specific reasons.
    Drafted and checked one section at a time.
U3  Ran the TOPIC-NOTE gate. Measured, not judged:
      prose floor: P1..P11 summed = 912 (>= 800)  ✓
      coverage: 5 of 5 items mapped to named sub-headings  ✓
      acronyms: 4 found, 3 expanded, 1 fixed  ✓
      prose-first: P = 11, L = 2 -> 11 >= 6  ✓
      source fidelity: 14 names checked (1 fixed), 9 of 9 source values present,
                       triggers fired 6 / delivered 6  ✓
      triggers: 11 of 11 answered (6 yes, each naming a section; 5 no with reasons)  ✓
      enumerable set: source 8 == plan 8 == table rows 8  ✓
      scaffolding: non-surviving blocks found 0; Coverage Plan / Adaptation Note /
                   Final Self-Audit all present  ✓
      placeholders: 0 hits | external links: 2 fetched live  ✓
U2  Wrote the file. Handed back a POINTER ONLY, no body.

U4  Final report: 03-<topic-slug>.md | topic note | repo contract |
    7 sections (3 omitted, logged) | 912 words vs 800 floor |
    2 official links verified | gate PASS. Next stub named: 04-<topic-slug>.md
```


This skill is written in the `SKILL.md` format for OpenCode. The workflow and rules are platform-agnostic.

| Platform | How to use |
|---|---|
| **Google Antigravity** | Drop the whole `author-chapter/` folder into `~/.gemini/config/skills/` — same `SKILL.md` standard (YAML frontmatter required, `name` optional) |
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
