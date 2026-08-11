# author-chapter

Turns a blank stub (or thin file) into one fully contract-compliant learning file. Resolves the target's artifact type from its filename, then either researches live official sources (topic notes, interview prep, thought leadership) or synthesises strictly from the sibling topic notes (chapter intro, podcast). Drafts the sections the topic genuinely needs, runs the matching artifact quality gate as a self-audit, and writes the file only after every check passes.

---

## Trigger phrases

| Input | Example |
|---|---|
| Populate a stub | "populate this chapter", "fill in this stub" |
| Author by name | "author the notes for [topic]" |
| By file path | "write `01-<section>/01-<chapter>/02-<topic-slug>.md`" |
| Derived artifact | "write the chapter intro (`00-intro.md`) now the topics are done", "write `99-podcast.md`" |
| Auxiliary artifact | "author `interview-prep.md` / `thought-leadership.md` for this chapter" |
| Template-aware | "write the [chapter name] topic notes following the template" |

Do **not** trigger this skill to create a new repo (use `create-learning-repo`) or to generate a quiz/exam (use `generate-practice-exam`).

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
| **U0 — Resolve artifact type, locate contract & confirm scope** | Identifies the target file; **resolves its artifact type from the filename**; walks up the tree to find `AGENTS.md` + `templates/` and selects the template for that artifact type; classifies the file as stub vs. has-content; for a chapter intro or podcast, runs the **sibling-readiness gate**. **STOP GATE**: confirms target + artifact type + contract source before research (and never silently overwrites authored content or a loose-folder fallback) |
| **U1 — Build the source brief** | **Branch A (source-based)** — for topic notes, interview prep, and thought leadership: fetches official documentation, exam objective wording, and changelog in parallel; stops rather than author from training data if sources are unreachable. **Branch B (derived)** — for chapter intro and podcast: skips live research entirely and reads every sibling topic note in full instead. **STOP GATE**: presents a compact research or derived brief — Coverage Plan and planned sections, or topic inventory, connections, and reading order — for approval |
| **U2 — Draft, write, hand back** | Picks the sections this artifact and topic genuinely need from the template's suggested **menu**, orders them to teach best, records omissions in the Adaptation Note; runs Unit U3 as its Self-verify, then writes the draft to the target file. **STOP GATE**: hands back only a short pointer + summary — never the full body — and asks you to open the file to review |
| **U3 — Quality gate (self-audit)** | The doer's own verification, run inside U2 before any hand-back: selects the rubric **for this artifact type**, self-audits the draft row by row plus the universal rules; any ✗ blocks completion; fixes failures and re-runs the whole gate until every row is ✓ |
| **U4 — Finalize and report** | Idempotency guard against foreign edits, confirms the file holds the approved and gated draft, reports a structured completion summary, and suggests the next stub **respecting authoring order** |

---

## Sibling-readiness refusal (derived artifacts)

Because a chapter intro and a podcast can only summarise what the topic notes already say, U0 **refuses outright** to author either one while any sibling topic note in that chapter is still a stub or too thin to synthesise from. It enumerates the chapter's files, classifies each as Authored or Stub/thin, and on failure stops at its gate, names the files that must be authored first, and hands control back — it does not warn and continue, and it does not offer a reduced-scope partial synthesis.

In **derived-content mode** (Branch B of U1) the skill also does no live research at all: fetching the web there is precisely how a derived artifact acquires facts its chapter never taught. The only permitted fetch is re-verifying a link carried over from a sibling note. If the intro or podcast seems to need a fact the notes do not contain, the skill surfaces it at the gate so it can be added to the proper topic note first — never invented here.

---

## Contract-first design

The section menu and depth rules are **read from the target repo's own files at runtime** — not hardcoded into this skill:

| Situation | Contract used |
|---|---|
| `AGENTS.md` + `templates/` both found | Reads and follows them — they win. Reads the template matching the resolved artifact type (`topic-notes-template.md`, `chapter-intro-template.md`, `chapter-podcast-template.md`, `interview-prep-template.md`, `thought-leadership-template.md`), tolerating a repo that names them differently |
| Neither found (loose Markdown folder) | Asks confirmation, then falls back to built-in `reference/quality-gate.md`, using its filename → rubric routing table |
| Only one found | Uses what is present, falls back for the missing piece; tells you which contract applies |

This makes the skill portable across repos with different templates and standards.

---

## Adaptive structure and the three hard requirements

There is **no fixed section list and no fixed section order.** The template supplies a **menu of suggested sections**; the skill picks the ones this artifact and this topic genuinely need, arranges them in the order that teaches best, names every sub-heading after the real domain concept it discusses (generic headings like "Overview" or "Key Concepts" are non-compliant), and may invent a section the menu never anticipated. Every omitted menu section is recorded in the **Adaptation Note** with a reason specific to this topic — omission is fine, silent omission is a gate failure.

Only three structural floors survive, and for topic notes they are non-negotiable:

1. **Coverage** — the sub-concepts are enumerated up front in a **Coverage Plan** that stays in the finished file, and every one is verified as genuinely explained in the body before the file is written.
2. **Prose floor** — the explanatory body as a whole reaches at least **800 words** of genuine explanation. Padding, hedging, or restatement is a violation, not a way to meet it.
3. **Reading level / prose-first** — written for a **bright 14-year-old**: short sentences, one idea each, every acronym expanded and every piece of jargon defined inline in plain words on first use, and the explanation carried by **prose paragraphs** rather than bullet lists. Lists are for genuine enumerations only.

The voice and reading-level target applies to **every** artifact type, not just topic notes. Prose explanation and worked examples carry the teaching load; snippets, diagrams, tables, and questions support it and never stand in for it.

---

## Quality gate checks (Unit U3)

There is no single one-size checklist. The gate selects the rubric **for the resolved artifact type** and always runs it **plus the universal rules**. In a structured repo the rubric comes from the repo's own `AGENTS.md` / `templates/`; in fallback mode it comes from `reference/quality-gate.md`, which holds **five separate per-artifact gates** reached through its filename → rubric routing table. Any ✗ blocks completion — the failure is fixed and the **whole** gate re-runs:

| Rubric | Representative checks |
|---|---|
| **Universal (every artifact)** | Bright-14-year-old reading level; every acronym expanded and jargon defined inline on first use; explanation carried by prose, not lists; sub-headings named after real domain concepts; official documentation only, each link live with a `*verified YYYY-MM-DD*` date; nothing invented; zero TODO/TBD/STUB/bracket markers |
| **Topic note** | Coverage Plan reconciled against the body; 800-word prose floor met with real explanation; Adaptation Note records every omission with a topic-specific reason; any diagram/table/snippet earns its place and is explained; any snippet opens with a comment naming the real problem it solves; any parameter table gives actionable decision rules; any self-check answer explains why the correct answer is right and why the tempting wrong ones fail |
| **Chapter intro** | Every topic file represented with a working relative link; the "how the topics connect" explanation is genuine prose about dependencies and motivation, not a restated topic list; a suggested reading order with a stated reason; no fact absent from the sibling notes; every sibling topic note was non-stub before authoring |
| **Podcast** | One clearly delineated segment per topic; genuine back-and-forth rather than two monologues; consistent generic role labels, never invented personalities; an everyday analogy per segment; **zero code blocks**; no fact absent from the sibling notes; every sibling topic note was non-stub before authoring |
| **Interview prep** | Questions realistic for the stated role and seniority, not trivia; answers a candidate could say out loud, with the reasoning behind them so a follow-up is survivable; weak-answer traps specific to this subject matter, not generic interview advice; everything grounded in the chapter's actual content |
| **Thought leadership** | A specific, non-obvious claim in the opening lines; no throat-clearing cliché opener; defensible rather than unfalsifiable claims; at least one concrete example or number anchoring the argument; the strongest counterargument stated fairly and answered; a clear original angle and a concrete takeaway |

**Deterministic checks** are run mechanically, keyed by artifact type: grep for residual placeholder markers (all); acronym-expansion scan (all); prose-to-list ratio (all); external URLs re-fetched (all); word count against the 800-word floor and Coverage Plan reconciliation (topic notes); speaker-label consistency and a zero code-fence count (podcast); every sibling topic note non-stub and every relative link resolving on disk (chapter intro and podcast).

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Target file path (or chapter/topic name) | Yes | The stub or thin file to populate; its filename resolves the artifact type |
| `AGENTS.md` + `templates/` | Preferred | Authoritative authoring contract; skill falls back to built-in if absent |
| Live web access | Yes for source-based artifacts | Unit U1 Branch A fetches official docs. Derived artifacts (chapter intro, podcast) need only the sibling topic notes on disk, plus the web for link re-verification |
| Completed sibling topic notes | Yes for derived artifacts | A chapter intro or podcast is refused while any topic note in the chapter is still a stub |

---

## Outputs

A single fully-authored Markdown file at the target path. The draft is written to the file first and reviewed by opening it — the body is never pasted into chat. Completion report:

```
Authored:      path/to/file.md
Artifact type: topic note | chapter intro | podcast | interview prep | thought leadership
Contract:      repo templates/AGENTS.md  (or partial, or built-in fallback)
Template:      template or fallback rubric used
Sections:      N included (N omitted, each with a reason in the Adaptation Note)
Depth:         explanatory word count vs floor | segments | Q&A pairs
Source:        N official links verified | derived from N sibling topic notes
Quality gate:  PASS (artifact rubric — all checks ✓)
```

---

## Limitations

- **One file per invocation.** The skill authors only the file you explicitly name. It does not batch-populate a chapter or module unless you ask for each file separately.
- **Stubs only, freely.** For files with existing authored content, the skill stops and asks before proceeding.
- **Derived artifacts come last.** `00-intro.md` and `99-podcast.md` cannot be authored until every topic note in the chapter is complete and non-stub — the skill refuses rather than guessing.
- **Official sources only.** External links use only official documentation — no third-party blogs, Medium, or YouTube.
- **Live research required for source-based artifacts.** Unit U1 Branch A makes real web requests for topic notes, interview prep, and thought leadership. Avoid running those in offline environments. If official sources are unreachable, the skill stops rather than authoring from training data — paste doc excerpts directly, or use `create-learning-repo`'s Phase 1 fallback prompts and share the results. Derived artifacts are exempt: they read the sibling topic notes instead.
- **No exam/quiz generation.** Use `generate-practice-exam` for that.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global — available in all projects (Linux/macOS)
cp -r learning/author-chapter ~/.config/opencode/skills/

# Per-project only
cp -r learning/author-chapter .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse learning\author-chapter "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/author-chapter.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before naming the chapter to author |

---

## Companion skills

- **`create-learning-repo`** — scaffolds the repo, templates, and the five per-chapter artifact stubs that this skill populates
- **`generate-practice-exam`** — builds mock exams from chapters authored by this skill
