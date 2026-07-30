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
| **U0 — Intake & intent logic** | Collects topic, learning goals, level, time budget, naming preference, and seed URLs, then decides which per-chapter file types to generate |
| **U1 — Research** | Fetches the official exam blueprint, documentation, and changelog in parallel; presents a structured, cited research summary for approval |
| **U2 — Structure design** | Designs the full folder + file tree with budget reconciliation, domain mapping, and naming-convention enforcement; awaits approval |
| **U3 — Template manifest** | Confirms the set of template files to be generated, based on detected goals |
| **U4 — Write AGENTS.md + templates** | Copies templates verbatim from `reference/` to `templates/`, writes the repo's `AGENTS.md` with the 9 content-depth rules (`author-chapter` and `generate-practice-exam` enforce these rules via their quality gates) |
| **U5 — Scaffold stubs + README** | Creates every folder and one-line blank-stub file, writes the root `README.md`, runs a planned-vs-actual verification pass |
| **U6 — Git init** | Checks for `.git`; prints the first-commit command — runs automatically after U5 |

Every unit runs in its own response — no two units are combined. U0–U5 end with a STOP GATE you must approve before the next unit runs; U6 follows automatically once U5 is confirmed.

---

## What gets created

- A `templates/` directory — the **only** directory with real file content
- `AGENTS.md` — authoring rules and the 9 content-depth standards for the repo (the same standards `author-chapter` drafts to and its quality gate checks)
- `README.md` — populated with repo metadata, learning path table, and section summaries
- Blank one-line stubs for every content file (`<!-- stub: populate using templates/ -->`)

**What does NOT get created:** any learning notes, explanations, or exam questions — those are added later with `author-chapter`.

---

## Key design decisions

**Budget reconciliation** — the skill computes `chapters × 1.5 hrs` to `chapters × 3.0 hrs` and flags if your stated time budget is more than 25% outside the range, proposing specific structural fixes before proceeding.

**Slug derivation** — a deterministic 6-step algorithm (lowercase → clean → collapse → trim → 40-char cap → style) ensures consistent naming and prevents silent Windows MAX_PATH failures.

**Filename lock** — after U5, all file and folder names are locked. Authored chapters may forward-link to not-yet-written stubs; those links resolve when the stub is populated. Renaming breaks every reference.

**Intent-based file types** — the set of files generated per chapter depends on your goals:
- Certification / personal mastery → `notes.md` stubs only
- Thought leadership goal → also generates `thought-leadership.md` stubs
- Career / interview goal → also generates `interview-prep.md` stubs

---

## Inputs (Unit U0)

| Question | Required | Notes |
|---|---|---|
| Topic / certification name | Yes | Exact name; drives all naming and research |
| Learning goal(s) | Yes | a) exam, b) career, c) thought leadership, d) mastery |
| Current level | Yes | Beginner / Some exposure / Adjacent expert / Practitioner |
| Time budget (hours) | Yes | Used for budget reconciliation in U2 |
| Naming preference | Optional | Preferred repo folder name; derived from topic if omitted |
| Naming style | Optional | Lowercase-hyphen (default) or ALLCAPS_UNDERSCORE |
| Seed URLs | Optional | Official docs, exam guides; the skill finds them if omitted |

---

## Outputs

A complete repo skeleton on disk with:
- `AGENTS.md` (fully populated with authoring rules)
- `templates/` (fully populated with real template content)
- `README.md` (fully populated with repo metadata)
- All section, module, chapter, and auxiliary files as one-line stubs
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

- **`author-chapter`** — populates stub notes files created by this skill
- **`generate-practice-exam`** — builds mock exams from authored chapters
