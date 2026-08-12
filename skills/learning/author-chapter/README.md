# author-chapter

Turns a blank stub (or thin file) into one fully contract-compliant learning file. Resolves the target's artifact type from its filename, then either researches live official sources (topic notes, interview prep, thought leadership) or synthesises strictly from the sibling topic notes (chapter intro, podcast). Drafts the sections the topic genuinely needs, runs the matching artifact quality gate as a self-audit, and writes the file only after every check passes. It is subject-neutral: the same contract governs a note on a dynasty's marriage strategy, on sharpening a knife, on a statute, on a species, on a musical mode, or on a piece of software.

**Trigger phrases:** "populate this chapter" / "fill in this stub"; "author the notes for [topic]"; a bare file path such as `01-<section>/01-<chapter>/02-<topic-slug>.md`; "write the chapter intro now the topics are done"; "write `99-podcast.md`"; "author `interview-prep.md` / `thought-leadership.md` for this chapter". Do **not** trigger it to create a new repo (use `create-learning-repo`) or to generate a quiz or exam (use `generate-practice-exam`).

---

## The five per-chapter artifact types

A chapter folder holds five kinds of file, and this skill authors any one of them. The filename resolves the artifact type, and the artifact type then selects the template, the depth rules, the research mode, and the quality-gate rubric:

| Filename pattern | Artifact type | Source | Order |
|---|---|---|---|
| `00-intro.md`, `intro.md` | Chapter intro — overview plus **how the topics interconnect** | Derived from sibling topic notes | **Last** |
| `NN-<slug>.md` (not `00`/`99`) | Topic note — the primary teaching artifact, 2–6 per chapter | Live official sources | First |
| `interview-prep.md` | Interview prep — role-targeted Q&A | Live official sources | Alongside the topic notes |
| `thought-leadership.md` | Thought leadership — one original, defensible argument | Live official sources | Alongside the topic notes |
| `99-podcast.md`, `podcast.md` | Podcast — two-speaker conversational transcript, zero code blocks | Derived from sibling topic notes | **Last** |
| anything unrecognised | Defaults to topic note — the assumption is stated at the U0 gate | Live official sources | — |

**Derived artifacts** (`00-intro.md`, `99-podcast.md`) may introduce **no fact absent from the sibling topic notes**. They synthesise; they do not add.

---

## What it does

Runs a sequence of discrete **units** (U0 → U4). Each unit has a Goal/scope, Inputs, Do, a Self-verify step, and a terse Report contract. Three units are **STOP GATES** that hand control back for confirmation; the mandatory quality gate is expressed as the doer's own self-audit run before the draft is written:

| Unit | What happens |
|---|---|
| **U0 — Resolve artifact type, locate contract & confirm scope** | Identifies the target file; **resolves its artifact type from the filename**; walks up the tree to find `AGENTS.md` + `templates/` and selects the template for that artifact type; classifies the file as stub vs. has-content; for a chapter intro or podcast, runs the **sibling-readiness gate**. **STOP GATE**: confirms target + artifact type + contract source before research, and never silently overwrites authored content or assumes a loose-folder fallback |
| **U1 — Build the source brief** | **Branch A (source-based)** — for topic notes, interview prep, and thought leadership: fetches official documentation, exam objective wording, and changelog in parallel; stops rather than author from training data if sources are unreachable. **Branch B (derived)** — for chapter intro and podcast: skips live research entirely and reads every sibling topic note in full instead. **STOP GATE**: presents a compact brief — Coverage Plan, the eleven trigger answers, and planned sections, or else topic inventory, connections, and reading order — for approval |
| **U2 — Draft, write, hand back** | Picks the sections this artifact and topic genuinely need from the template's suggested **menu**, adds every artifact a trigger required, orders them to teach best, records omissions in the Adaptation Note; runs Unit U3 as its Self-verify, then writes the draft. **STOP GATE**: hands back only a short pointer + summary — never the full body — and asks you to open the file to review |
| **U3 — Quality gate (self-audit)** | The doer's own verification, run inside U2 before any hand-back: selects the rubric **for this artifact type**, self-audits the draft row by row plus the universal rules, carrying evidence on every row — a measured number, a name, or a location. A tick with no evidence is a failed row; any ✗ blocks completion, and the **whole** gate re-runs after each fix |
| **U4 — Finalize and report** | Idempotency guard against foreign edits, confirms the file holds the approved and gated draft, reports a structured completion summary, and suggests the next stub **respecting authoring order** |

**Sibling-readiness refusal (derived artifacts).** Because a chapter intro and a podcast can only summarise what the topic notes already say, U0 **refuses outright** to author either one while any sibling topic note in that chapter is still a stub or too thin to synthesise from: it enumerates the chapter's files, classifies each as Authored or Stub/thin, and on failure stops at its gate, names the files that must be authored first, and hands control back — it does not warn and continue, and it does not offer a reduced-scope partial synthesis. In **derived-content mode** (Branch B of U1) it also does no live research at all, because fetching the web there is precisely how a derived artifact acquires facts its chapter never taught; the only permitted fetch is re-verifying a link carried over from a sibling note. If the intro or podcast seems to need a fact the notes do not contain, the skill surfaces it at the gate so it can be added to the proper topic note first — never invented here.

**Contract-first design.** The section menu, depth rules, and gate rubric are **read from the target repo's own files at runtime**, not hardcoded here. When `AGENTS.md` and `templates/` are both found they win, and the skill reads the template matching the resolved artifact type (`topic-notes-template.md`, `chapter-intro-template.md`, `chapter-podcast-template.md`, `interview-prep-template.md`, `thought-leadership-template.md`), tolerating a repo that names them differently. When only one is found it uses what is present, falls back for the missing piece, and tells you which contract applies. When neither is found — a loose Markdown folder — it asks for confirmation, then falls back to the built-in `reference/quality-gate.md` and its filename → rubric routing table. **That file is the authoritative statement of the requirements and the gate; everything below is a summary of it.**

---

## Adaptive structure and the four hard requirements

There is **no fixed section list and no fixed section order.** The template supplies a **menu of suggested sections**; the skill picks the ones this artifact and this topic genuinely need, arranges them in the order that teaches best, names every sub-heading after the real domain concept it discusses (generic headings like "Overview" or "Key Concepts" are non-compliant), and may invent a section the menu never anticipated. Every omitted menu section is recorded in the **Adaptation Note** with a reason specific to this topic — omission is fine, silent omission is a gate failure.

Exactly four hard requirements survive, and for topic notes they are non-negotiable:

1. **Coverage** — the sub-concepts are enumerated up front in a **Coverage Plan** that stays in the finished file, and every one is verified as genuinely explained in the body before the file is written. If the subject is a closed enumerable set, coverage means *every member of that set*.
2. **Prose floor** — the explanatory body as a whole reaches at least **800 words** of genuine explanation. Padding, hedging, or restatement is a violation, not a way to meet it.
3. **Reading level / prose-first** — written for a **bright 14-year-old**: short sentences, one idea each, every acronym expanded and every piece of jargon defined inline in plain words on first use, and the explanation carried by **prose paragraphs** rather than bullet lists. Lists are for genuine enumerations only.
4. **Source fidelity** — every exact proper name, designation, or term of art is spelled as the authoritative source spells it (a rank, a statute section, a species name, a place name, a field name); every quantity, date, threshold, limit, unit, range, and closed set of permitted values the source states, the note states too; and every artifact whose **REQUIRED-IF trigger** fired is actually present. An analogy may *illustrate* a mechanism but may **never substitute** for naming the real thing, stating a real number, or enumerating a set. This requirement is graded **independently** of the 800-word prose floor: artifacts neither count toward the floor nor against it, so adding a table or a diagram can never reduce compliance with the floor.

**REQUIRED-IF triggers T1–T11 are binding, not recommendations.** Each is a yes/no question about *this* topic: does it have ordered stages (T1); settings the reader chooses, such as proportions, grades, quantities, or thresholds (T2); a real decision with consequences (T3); a competing approach the reader will meet (T4); a concrete artifact, procedure, or worked calculation the reader would actually produce or follow (T5); a tempting wrong intuition (T6); a true everyday analogy for something abstract (T7); one mechanism much harder than the rest (T8); terms the reader will meet again later (T9); something the reader must be able to do afterwards (T10); an authoritative source (T11). Where the condition is true of the topic, that artifact is **REQUIRED**, not recommended. All eleven get an explicit yes or no in the Adaptation Note, and omitting one means **citing the trigger ID** plus a reason naming something specific about this topic that makes the artifact impossible or actively misleading. A reason that would read identically in a note on a completely different subject is boilerplate and fails, as does any reason about the author's own effort, time, or uncertainty.

**Closed-enumerable-set ratchet.** When the subject's members are a finite documented list — taxonomic ranks, statutory articles, treaty signatories, musical modes, official grades, permitted values, lifecycle states — the skill extracts the **complete** list from the authoritative source before writing, records the source URL, the retrieval date, and the **source member count**, renders one row per member using the source's own spelling, and confirms **source count == Coverage Plan count == table row count**. A related-but-distinct item that merely influences the set is **not** a member of it; genuine neighbours go in a deliberately-out-of-scope or commonly-confused note.

**Scaffolding survival.** Exactly **three** scaffolding blocks survive into a finished topic note — **Coverage Plan**, **Adaptation Note**, **Final Self-Audit** — each filled in. Every other scaffolding block is **deleted outright**, not trimmed or summarised, and no `## Version History` heading appears in a finished note.

The voice and reading-level target applies to **every** artifact type, not just topic notes. Prose explanation and worked examples carry the teaching load; artifacts — diagrams, tables, concrete examples, questions — support it and never stand in for it. The reverse also holds: prose never stands in for an artifact a trigger required. Deliver both.

---

## Quality gate checks (Unit U3)

There is no single one-size checklist. The gate selects the rubric **for the resolved artifact type** and always runs it **plus the universal rules**. In a structured repo the rubric comes from the repo's own `AGENTS.md` / `templates/`; in fallback mode it comes from `reference/quality-gate.md`, which holds **five separate per-artifact gates** reached through its filename → rubric routing table and carries the authoritative wording. Any ✗ blocks completion — the failure is fixed and the whole gate re-runs:

| Rubric | Representative checks |
|---|---|
| **Universal (every artifact)** | Bright-14-year-old reading level; every acronym expanded and jargon defined inline on first use; explanation carried by prose, not lists; sub-headings named after real domain concepts; official documentation only, each link live with a `*verified YYYY-MM-DD*` date; nothing invented; zero TODO/TBD/STUB/bracket markers |
| **Topic note** | Coverage Plan reconciled against the body; 800-word prose floor met with real explanation; all eleven T1–T11 triggers answered in the Adaptation Note, every omission citing its trigger ID with a topic-specific reason that survives the blocklist categories. **Artifacts are judged two-sided:** every artifact *present* — a diagram, a table, a worked example, a concrete example or artifact — earns its place and has prose around it saying what to take away, **and** every artifact *required* by a fired trigger is actually delivered; **triggers fired must equal artifacts delivered**, and a note containing **zero** artifacts **FAILS** unless every one of T1–T11 is a "no" whose reason survives the blocklist categories. Enumerable-set counts agree (source == Coverage Plan == table rows) with no member the source does not list; **source fidelity two-sided** — exact names spelled as the source spells them, and every source-stated quantity, date, threshold, limit, unit, and permitted-value set present; only the three surviving scaffolding blocks remain |
| **Chapter intro** | Every topic file represented with a working relative link; the "how the topics connect" explanation is genuine prose about dependencies and motivation, not a restated topic list; a suggested reading order with a stated reason; no fact absent from the sibling notes; every sibling topic note was non-stub before authoring |
| **Podcast** | One clearly delineated segment per topic; genuine back-and-forth rather than two monologues; consistent generic role labels, never invented personalities; an everyday analogy per segment; **zero code blocks**; no fact absent from the sibling notes; every sibling topic note was non-stub before authoring |
| **Interview prep** | Questions realistic for the stated role and seniority, not trivia; answers a candidate could say out loud, with the reasoning behind them so a follow-up is survivable; weak-answer traps specific to this subject matter, not generic interview advice; everything grounded in the chapter's actual content |
| **Thought leadership** | A specific, non-obvious claim in the opening lines; no throat-clearing cliché opener; defensible rather than unfalsifiable claims; at least one concrete example or number anchoring the argument; the strongest counterargument stated fairly and answered; a clear original angle and a concrete takeaway |

**Deterministic checks** are run mechanically, keyed by artifact type: grep for residual placeholder markers (all); acronym-expansion scan (all); prose-to-list ratio (all); external URLs re-fetched (all); **source-fidelity counts** — names checked character by character against the source, and source-stated values present in the note (all); word count against the 800-word floor, Coverage Plan reconciliation, **trigger completeness (11 of 11 answered)**, two-sided artifact delivery, **enumerable-set count equality**, the omission-reason blocklist test, and the **scaffolding-leak grep** including any `## Version History` heading (topic notes); speaker-label consistency and a zero code-fence count (podcast); every sibling topic note non-stub and every relative link resolving on disk (chapter intro and podcast).

**Stopping is a successful outcome.** The skill stops and asks rather than guess — for existing authored content, an unconfirmed fallback contract, stub siblings, unreachable sources, a missing fact, a topic that is really two, an unreachable prose floor, contradictory siblings, and two conditions specific to enumerable sets: the **complete membership of a closed set cannot be confirmed** from an authoritative source, or the **source member count cannot be established** (or it disagrees with the Coverage Plan count and the discrepancy cannot be resolved). A partial member list teaches the reader that the rest do not exist, so it is never published, and a count is never guessed or split.

---

## Inputs and outputs

**Inputs.** A target file path, or a chapter/topic name to resolve to one (required — its filename resolves the artifact type). The repo's `AGENTS.md` + `templates/` (preferred; the built-in fallback is used, with confirmation, if absent). Live web access (required for source-based artifacts, since U1 Branch A fetches official docs; derived artifacts need only the sibling notes on disk plus the web for link re-verification). Completed sibling topic notes (required for derived artifacts — a chapter intro or podcast is refused while any topic note in the chapter is still a stub).

**Output.** A single fully-authored Markdown file at the target path. The draft is written to the file first and reviewed by opening it — the body is never pasted into chat. Completion report:

```
Authored:      path/to/file.md
Artifact type: topic note | chapter intro | podcast | interview prep | thought leadership
Contract:      repo templates/AGENTS.md  (or partial, or built-in fallback)
Sections:      N included (N omitted, each citing a trigger ID and a topic-specific reason)
Triggers:      11 of 11 answered — N fired, N artifacts delivered
Depth:         explanatory word count vs floor | segments | Q&A pairs
Source:        N official links verified | derived from N sibling topic notes
Quality gate:  PASS (artifact rubric — every row ✓ with evidence)
```

---

## Limitations

- **One file per invocation.** The skill authors only the file you explicitly name; it does not batch-populate a chapter or module unless you ask for each file separately. Stubs are populated freely, but for a file with existing authored content it stops and asks first.
- **Derived artifacts come last.** `00-intro.md` and `99-podcast.md` cannot be authored until every topic note in the chapter is complete and non-stub — the skill refuses rather than guessing.
- **Official sources only, researched live.** External links use only official documentation — no third-party blogs or video. U1 Branch A makes real web requests for topic notes, interview prep, and thought leadership, so avoid running those offline. If official sources are unreachable it stops rather than authoring from training data: paste the official excerpts, or use `create-learning-repo`'s Phase 1 fallback prompts and share the results. Derived artifacts are exempt — they read the sibling notes instead.
- **No exam or quiz generation.** Use `generate-practice-exam` for that.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
cp -r learning/author-chapter ~/.config/opencode/skills/   # global, all projects
cp -r learning/author-chapter .opencode/skills/            # this project only
```

On Windows use `Copy-Item -Recurse learning\author-chapter "$env:USERPROFILE\.config\opencode\skills\"`. On other platforms, paste the skill content where that tool reads standing instructions: `CLAUDE.md` under a `## Workflows` heading (Claude Code), `.cursor/rules/author-chapter.mdc` set to `Agent Requested` (Cursor), `.github/copilot-instructions.md` under a labelled heading (GitHub Copilot), or as your first chat message before naming the chapter to author (web chat assistants).

---

## Companion skills

- **`create-learning-repo`** — scaffolds the repo, templates, and the five per-chapter artifact stubs that this skill populates
- **`generate-practice-exam`** — builds mock exams from chapters authored by this skill
