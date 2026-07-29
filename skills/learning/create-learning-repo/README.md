# create-learning-repo

Scaffolds a complete, structured Markdown learning repository for any topic or certification. Runs phased intake, fetches live sources for curriculum design, designs the folder hierarchy, writes content templates, and generates blank stubs for every content file.

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

Guides you through **six confirmed phases** to produce a ready-to-author skeleton repo:

| Phase | What happens |
|---|---|
| **Phase 0 — Intake** | Collects topic, learning goals, level, time budget, naming preference, and seed URLs |
| **Phase 1 — Research** | Fetches the official exam blueprint, documentation, and changelog in parallel; presents a structured research summary for approval |
| **Phase 2 — Structure** | Designs the full folder + file tree with budget reconciliation, domain mapping, and naming-convention enforcement; awaits approval |
| **Phase 3 — Templates** | Confirms the set of template files to be generated, based on detected goals |
| **Phase 4 — Write AGENTS.md + templates** | Copies templates from `reference/` to `templates/`, writes the repo's `AGENTS.md` with the 9 content-depth rules (`author-chapter` and `generate-practice-exam` enforce these rules via their quality gates) |
| **Phase 5 — Scaffold stubs + README** | Creates every folder and one-line stub file, writes the root `README.md`, runs a planned-vs-actual verification pass |
| **Phase 6 — Git init** | Checks for `.git`; prints the first-commit command — runs automatically after Phase 5 |

Every phase (except Phase 6) ends with an explicit "proceed" gate — you approve before the next phase runs.

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

**Filename lock** — after Phase 5, all file and folder names are locked. Authored chapters may forward-link to not-yet-written stubs; those links resolve when the stub is populated. Renaming breaks every reference.

**Intent-based file types** — the set of files generated per chapter depends on your goals:
- Certification / personal mastery → `notes.md` stubs only
- Thought leadership goal → also generates `thought-leadership.md` stubs
- Career / interview goal → also generates `interview-prep.md` stubs

---

## Inputs (Phase 0)

| Question | Required | Notes |
|---|---|---|
| Topic / certification name | Yes | Exact name; drives all naming and research |
| Learning goal(s) | Yes | a) exam, b) career, c) thought leadership, d) mastery |
| Current level | Yes | Beginner / Some exposure / Adjacent expert / Practitioner |
| Time budget (hours) | Yes | Used for budget reconciliation in Phase 2 |
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
- **Live research required.** Phase 1 makes real web requests. If official sources are unavailable, the skill provides fallback AI-assistant prompts.
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
