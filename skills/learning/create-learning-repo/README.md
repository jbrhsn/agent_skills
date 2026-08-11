# create-learning-repo

Scaffolds a complete, structured Markdown learning repository for any topic or certification. Runs a delegation-model workflow of confirmed, self-contained units — intake, live-source research, folder-hierarchy design, template generation, AGENTS.md authoring, and blank-stub scaffolding — each handed back for approval before the next runs.

---

## Trigger phrases

| Input | Example |
|---|---|
| Topic/cert focus | "create a learning repo for Kubernetes" |
| Certification prep | "build a certification prep repo for AWS SAA-C03" |
| General study | "scaffold a study guide for machine learning" |
| Expertise goal | "set up a knowledge base to become an expert in Rust" |

Do **not** trigger this skill to populate an existing repo's content — use `author-chapter` for that.

---

## What it does

Runs a delegation-model workflow of **seven self-contained units** (U0 → U6) to produce a ready-to-author skeleton repo. Each unit has a Goal/scope, Inputs, Do, a Self-verify step, and a terse Report contract; U0–U5 each end with an explicit **STOP GATE** that hands control back to you for approval before the next unit runs:

| Unit | What happens |
|---|---|
| **U0 — Intake** | Collects topic, learning goals, level, time budget, naming preference, labs preference, and seed URLs. Learning goals shape *emphasis* only — every chapter gets all five artifact types regardless |
| **U1 — Research** | Fetches the official exam blueprint, documentation, and changelog in parallel; presents a structured, cited research summary for approval |
| **U2 — Structure design** | **Decomposes every chapter into 2–6 topics** derived from the approved U1 research (each with a name and one-line scope, becoming the `NN-<topic-slug>.md` filenames), then designs the full folder + file tree with budget reconciliation, domain mapping, and naming-convention enforcement; the topic names are presented for approval before being locked |
| **U3 — Template manifest** | Confirms the set of template files to be generated — every "Always" template, plus `lab-template.md` only if labs were requested |
| **U4 — Write AGENTS.md + templates** | Copies templates verbatim from `reference/` to `templates/`, writes the repo's `AGENTS.md` with the adaptive authoring rules — an adaptive section menu rather than a fixed order, plus the **three hard requirements** (Coverage Plan, 800-word prose floor, bright-14-year-old reading level) and the authoring order for derived artifacts (`author-chapter` and `generate-practice-exam` enforce these rules via their quality gates) |
| **U5 — Scaffold stubs + README** | Creates every folder and one-line blank-stub file — including all five artifact types in every chapter — writes the root `README.md`, runs a planned-vs-actual verification pass |
| **U6 — Git init** | Checks for `.git`; prints the first-commit command — runs automatically after U5 |

Every unit runs in its own response — no two units are combined. U0–U5 end with a STOP GATE you must approve before the next unit runs; U6 follows automatically once U5 is confirmed.

---

## What gets created

- A `templates/` directory — the **only** directory with real file content. It holds `topic-notes-template.md`, `chapter-intro-template.md`, `chapter-podcast-template.md`, `interview-prep-template.md`, `thought-leadership-template.md`, `section-index-template.md`, `module-index-template.md`, `authoring-guidelines.md`, `capstone-template.md`, a `templates/README.md` index, and `lab-template.md` if labs were requested
- `AGENTS.md` — authoring rules for the repo: the adaptive section menu, the three hard requirements (Coverage Plan, 800-word prose floor, bright-14-year-old reading level), the template → destination mapping, and the authoring order (the same standards `author-chapter` drafts to and its quality gates check)
- `README.md` — populated with repo metadata, learning path table, and section summaries
- Blank one-line stubs for every content file (`<!-- stub: populate using templates/ -->`) — including, in **every** chapter folder, all five artifact types: `00-intro.md`, 2–6 `NN-<topic-slug>.md` topic notes, `interview-prep.md`, `thought-leadership.md`, and `99-podcast.md`

**What does NOT get created:** any learning notes, explanations, or exam questions — those are added later with `author-chapter`.

---

## Key design decisions

**Budget reconciliation** — the skill computes `chapters × 1.5 hrs` to `chapters × 3.0 hrs` and flags if your stated time budget is more than 25% outside the range, proposing specific structural fixes before proceeding.

**Slug derivation** — a deterministic 6-step algorithm (lowercase → clean → collapse → trim → 40-char cap → style) ensures consistent naming and prevents silent Windows MAX_PATH failures.

**Filename lock** — after U5, all file and folder names are locked (including the topic names approved in U2, which became topic-note filenames). Authored chapters may forward-link to not-yet-written stubs; those links resolve when the stub is populated. Renaming breaks every reference.

**Unconditional per-chapter artifacts** — every chapter folder gets the same five artifact types, and none of them is conditional on the learning goals collected in U0:

```
<chapter>/
  00-intro.md              <- chapter overview + how the topics interconnect (DERIVED — authored last)
  01-<topic-slug>.md       <- topic note; 2-6 per chapter, count derived in U2
  02-<topic-slug>.md
  ...
  interview-prep.md        <- always created, unnumbered
  thought-leadership.md    <- always created, unnumbered
  99-podcast.md            <- two-speaker conversational transcript (DERIVED — authored last)
```

`00` and `99` are **reserved slots**, so topic notes always occupy the contiguous range `01`…`NN` with `NN` ≤ `06`; the two auxiliary files carry no number and cannot collide. A chapter that appears to need more than 6 topics is too large — split the chapter.

**Derived-artifact authoring order** — `00-intro.md` and `99-podcast.md` may only be authored once **every** topic note in that chapter is complete and non-stub, and must introduce **no fact absent from those sibling notes**. Topic notes, `interview-prep.md`, and `thought-leadership.md` are authored first, from live sources; the two derived artifacts synthesise and connect them.

**Derived topic counts** — the number of topic notes per chapter is never asked for and never defaulted. U2's topic-decomposition step splits each chapter into the 2–6 topics the approved U1 research actually shows it contains, gives each a name and a one-line scope, and traces each back to a blueprint objective or documented concept.

**Adaptive structure over a fixed template** — `topic-notes-template.md` is a **menu of suggested sections, not a running order**. The author picks the sections the topic genuinely needs, orders them to teach best, names every sub-heading after a real domain concept, may invent sections the menu never anticipated, and records each omission with a topic-specific reason in the template's **Adaptation Note**. Only three hard requirements survive: a **Coverage Plan** of sub-concepts verified as genuinely explained, an **800-word floor** of real explanatory prose per topic note (padding is a violation, not a way to meet it), and the reading level below.

**Reading level pitched at a bright 14-year-old** — short sentences, one idea each, acronyms expanded on first use, jargon defined inline in plain words, and explanation carried by prose paragraphs rather than bullet lists. This is a requirement in `AGENTS.md` and `authoring-guidelines.md`, not a style preference.

---

## Inputs (Unit U0)

| Question | Required | Notes |
|---|---|---|
| Topic / certification name | Yes | Exact name; drives all naming and research |
| Learning goal(s) | Yes | a) exam, b) career, c) thought leadership, d) mastery. Shapes **emphasis only** — what U1 researches hardest and how `README.md` frames the repo. It does not decide which files are created |
| Current level | Yes | Beginner / Some exposure / Adjacent expert / Practitioner |
| Time budget (hours) | Yes | Used for budget reconciliation in U2 |
| Naming preference | Optional | Preferred repo folder name; derived from topic if omitted |
| Naming style | Optional | Lowercase-hyphen (default) or ALLCAPS_UNDERSCORE |
| Seed URLs | Optional | Official docs, exam guides; the skill finds them if omitted |

**Not asked here:** which per-chapter file types to create (all five are unconditional) and how many topic notes each chapter gets (derived from the U1 research during U2's topic decomposition). The only conditional input is whether you want hands-on lab files.

---

## Outputs

A complete repo skeleton on disk with:
- `AGENTS.md` (fully populated with the adaptive authoring rules, the three hard requirements, and the authoring order)
- `templates/` (fully populated with real template content, plus a `templates/README.md` index)
- `README.md` (fully populated with repo metadata)
- All section, module, and chapter files as one-line stubs — every chapter carrying `00-intro.md`, its 2–6 `NN-<topic-slug>.md` topic notes, `interview-prep.md`, `thought-leadership.md`, and `99-podcast.md`
- `progress-tracker.md` and `00-roadmap/learning-roadmap.md` as stubs

---

## Limitations

- **No content is written.** The skill creates structure only. Populate stubs with `author-chapter`.
- **Live research required.** U1 makes real web requests. If official sources are unavailable, the skill provides fallback AI-assistant prompts.
- **Blueprint changes.** Exam blueprints change over time — always re-fetch the official blueprint before final exam prep.
- **Windows MAX_PATH.** Folder component names are capped at 40 characters. Any truncation is noted in the relevant index file.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global — available in all projects (Linux/macOS)
cp -r learning/create-learning-repo ~/.config/opencode/skills/

# Per-project only
cp -r learning/create-learning-repo .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse learning\create-learning-repo "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/create-learning-repo.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before describing the topic |

---

## Companion skills

- **`author-chapter`** — populates any of the five per-chapter artifact stubs created by this skill (topic notes, chapter intro, podcast, interview prep, thought leadership)
- **`generate-practice-exam`** — builds mock exams from authored chapters
