<div align="center">

# Agent Skills

**Structured workflows for AI coding agents — tested in real sessions, ready to install.**

Give agents like OpenCode, IBM Bob, Google Antigravity, Claude Code, and Cursor repeatable, high-quality behavior for common development tasks. Each skill is a prompt file your agent loads and follows like a playbook.

**14 skills** across session management, learning, development, and content creation.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

</div>

---

## Skills

### Session Management

> Load and save project context across agent sessions.

| Skill | What it does |
|---|---|
| [**init-session**](./skills/agent_session_management/init-session/README.md) | Restore full project context at session start — reads the handoff log and delivers a concise briefing of open items and last state |
| [**end-session**](./skills/agent_session_management/end-session/README.md) | Write a high-signal handoff at session end — rolling project summary, session log, and filtered open items for the next agent |

### Learning

> Create and populate Markdown-based learning repositories built on a five-artifact-per-chapter layout.

Every chapter folder holds the same five artifact types. `00` and `99` are reserved slots:

| File | Artifact | Authored |
|---|---|---|
| `00-intro.md` | Chapter intro — overview plus how the topics interconnect | **Last** (derived from the topic notes) |
| `01..NN-<topic-slug>.md` | Topic notes — the primary teaching artifact, 2–6 per chapter | **First**, from live official sources |
| `interview-prep.md` | Interview prep — role-targeted Q&A | Alongside the topic notes |
| `thought-leadership.md` | Thought leadership — one original, defensible argument | Alongside the topic notes |
| `99-podcast.md` | Podcast — two-speaker conversational transcript | **Last** (derived from the topic notes) |

Derived artifacts (`00-intro.md`, `99-podcast.md`) may introduce **no fact absent from the sibling topic notes** — they synthesise, they do not add.

| Skill | What it does |
|---|---|
| [**create-learning-repo**](./skills/learning/create-learning-repo/README.md) | Scaffold a structured learning repository for any topic or certification — phased intake, live research, decomposition of every chapter into 2–6 topics, template generation, and blank stubs for all five artifact types in every chapter |
| [**author-chapter**](./skills/learning/author-chapter/README.md) | Populate one blank stub into a fully contract-compliant file — resolves the artifact type from the filename, researches live official sources (topic notes, interview prep, thought leadership) or synthesises from sibling topic notes (intro, podcast), then runs the matching quality gate before writing |
| [**generate-practice-exam**](./skills/learning/generate-practice-exam/README.md) | Generate a blueprint-weighted mock exam or targeted drill from already-authored chapter content, with per-option answer rationale |

### Development

> Plan, build, design, and document software projects.

| Skill | What it does |
|---|---|
| [**lean-coder**](./skills/development/lean-coder/README.md) | A "lazy senior developer" discipline for coding work — the least code that correctly and safely solves the problem; adds `/review-diff` and `/audit-repo` workflows for finding over-engineering |
| [**project-planner**](./skills/development/project-planner/README.md) | Plan and spec a project before coding — produces spec, design, roadmap, and backlog docs under `docs/` (`/plan-project`) |
| [**repo-docs-publisher**](./skills/development/repo-docs-publisher/README.md) | Prepare a repo to go public — scans the code and checks for secrets first, then writes README, HOW_TO_USE, CONTRIBUTING, LICENSE, and optional community/GitHub docs |
| [**ui-ux-designer**](./skills/development/ui-ux-designer/README.md) | Design user flows, screens, and a design system into `docs/ux-design.md` (`/design-ux`) — detects non-UI projects (CLI/API/backend) and stops rather than fabricating screens |

### Content Creation

> Turn source notes into a posting-ready piece (with built-in review/refine) and generate matching visual prompts — for LinkedIn and Medium.

**LinkedIn** — `skills/content-creation/Linkedin/`

| Skill | What it does |
|---|---|
| [**linkedin-post-writer**](./skills/content-creation/Linkedin/linkedin-post-writer/README.md) | Turn source notes or a rough draft into a posting-ready LinkedIn post — hook engineering, scroll-first structure, no-link-in-body discipline, mandatory review gate. Writes `linkedin_post.md` next to the source file. Also scores a finished post across 5 algorithm-aligned dimensions and produces one refined version with an itemized change list in `linkedin_post_revised.md` |
| [**linkedin-image-prompts**](./skills/content-creation/Linkedin/linkedin-image-prompts/README.md) | Generate image-generation prompts (single hero image or full carousel) for a finished post, chosen from its structure. Writes `image_prompts.md` next to the source post — prompt text only, no rendering |

**Medium** — `skills/content-creation/Medium/`

| Skill | What it does |
|---|---|
| [**medium-article-brainstorm**](./skills/content-creation/Medium/medium-article-brainstorm/SKILL.md) | Brainstorm article ideas grounded in the user's examples and experience — interview-driven ideation, pattern parsing, web research for current facts, and one source.md seed per idea so the user writes the article themselves. Scaffolds ideas as folders or series. |
| [**medium-article-writer**](./skills/content-creation/Medium/medium-article-writer/SKILL.md) | Turn source notes or a draft into a publish-ready `medium_article.md`, applying Medium-specific craft grounded in Medium's Distribution Guidelines, AI-content policy, and earnings mechanics — title+subtitle+cover as a unit, read-ratio-driven scannability, first-hand originality, relevant tagging, soft value-tied CTAs, paywall recommendation — behind mandatory review gates. Also scores a finished article out of 100 across 5 distribution-aligned dimensions and writes one refined `medium_article_reviewed.md` with an itemized change list |
| [**medium-image-prompts**](./skills/content-creation/Medium/medium-image-prompts/SKILL.md) | Generate image-generation prompts for a finished Medium article — one featured/cover prompt plus one in-article visual per major section that earns one (Medium is not a carousel platform), each with alt text, a caption including credit and the mandatory AI-disclosure line, and a rationale. Writes `medium_image_prompts.md` next to the source article — prompt text only, no rendering |

---

## Getting started

### Sync everything (recommended)

The sync scripts install all 14 skills to every supported destination in one command. Run from the repo root:

```bash
python3 scripts/sync_all.py                     # Sync to all three targets
python3 scripts/sync_all.py --dry-run           # Preview without writing anything
python3 scripts/sync_all.py --opencode-only     # Only OpenCode (skills, agents, plugins)
python3 scripts/sync_all.py --bob-only          # Only IBM Bob (skills)
python3 scripts/sync_all.py --antigravity-only  # Only Google Antigravity (skills)
```

The three `--*-only` flags are **mutually exclusive**. With none of them passed, all three targets sync.

### Destinations

| What | Destination | Env override |
|---|---|---|
| OpenCode skills | `~/.config/opencode/skills/` | `OPENCODE_SKILLS` |
| OpenCode agents | `~/.config/opencode/agent/` (note the singular `agent`) | `OPENCODE_AGENTS` |
| IBM Bob skills | `~/.bob/skills/` | `BOB_SKILLS` |
| Google Antigravity skills | `~/.gemini/config/skills/` | `ANTIGRAVITY_SKILLS` |

```bash
# Sync a single target to a custom location
OPENCODE_SKILLS=/custom/path python3 scripts/sync_opencode_skills.py
BOB_SKILLS=/custom/path python3 scripts/sync_bob_skills.py
ANTIGRAVITY_SKILLS=/custom/path python3 scripts/sync_antigravity_skills.py
```

See [`scripts/README.md`](./scripts/README.md) for per-script details.

### Install manually

Prefer to copy only the skills you want? Run these from the repo root. Swap the destination for `~/.bob/skills/` or `~/.gemini/config/skills/` to target Bob or Antigravity instead — all three use the same skill-folder layout.

```bash
# Global — available in all your projects

# Session management skills
cp -r skills/agent_session_management/init-session ~/.config/opencode/skills/
cp -r skills/agent_session_management/end-session ~/.config/opencode/skills/

# Learning skills
cp -r skills/learning/create-learning-repo ~/.config/opencode/skills/
cp -r skills/learning/author-chapter ~/.config/opencode/skills/
cp -r skills/learning/generate-practice-exam ~/.config/opencode/skills/

# Development skills
cp -r skills/development/lean-coder ~/.config/opencode/skills/
cp -r skills/development/project-planner ~/.config/opencode/skills/
cp -r skills/development/repo-docs-publisher ~/.config/opencode/skills/
cp -r skills/development/ui-ux-designer ~/.config/opencode/skills/

# Content creation skills (LinkedIn pipeline)
cp -r skills/content-creation/Linkedin/linkedin-post-writer ~/.config/opencode/skills/
cp -r skills/content-creation/Linkedin/linkedin-image-prompts ~/.config/opencode/skills/

# Content creation skills (Medium pipeline)
cp -r skills/content-creation/Medium/medium-article-writer ~/.config/opencode/skills/
cp -r skills/content-creation/Medium/medium-image-prompts ~/.config/opencode/skills/
```

```bash
# Per-project (OpenCode) — available only in the current project
cp -r skills/agent_session_management/init-session .opencode/skills/
cp -r skills/learning/create-learning-repo .opencode/skills/
cp -r skills/development/lean-coder .opencode/skills/
cp -r skills/content-creation/Linkedin/linkedin-post-writer .opencode/skills/
cp -r skills/content-creation/Medium/medium-article-writer .opencode/skills/
```

OpenCode, Bob, and Antigravity all load skills automatically. Once installed, describe what you want and the agent invokes the right skill.

> **Content-creation skills ship helper scripts** (under `scripts/`) that run on **standard-library Python 3** — no install needed. Optional PNG export in `carousel-builder` uses `cairosvg` or a headless browser if present, and degrades gracefully if not.

### Use with other agents

Each skill's `README.md` has an **Other platforms** section with exact instructions per platform:

| Platform | How to load the skill |
|---|---|
| **Google Antigravity** | Drop the skill folder into `~/.gemini/config/skills/` — same `SKILL.md` standard, loaded automatically |
| **Claude Code** | Add content to `CLAUDE.md` under a named section |
| **Cursor** | Add as `.cursor/rules/<skill-name>.mdc`, type `Agent Requested` |
| **GitHub Copilot** | Add content to `.github/copilot-instructions.md` |
| **ChatGPT / Claude (web)** | Paste the skill content as your opening message |

The workflow phases and constraints are platform-agnostic — only the loading mechanism differs.

---

## Skill structure

Each skill lives in a `skills/category/skill-name/` folder:

```
skills/
└── category/
    └── skill-name/
        ├── SKILL.md       ← agent-facing skill (SKILL.md format with YAML frontmatter)
        ├── README.md      ← human-readable guide: triggers, workflow, examples, limitations
        └── support/       ← optional runtime files the skill reads or runs
```

The optional support directory varies by category:

| Category | Support dir | Contents |
|---|---|---|
| `skills/learning/`, `skills/agent_session_management/` | `reference/` (singular) | Templates, rubrics, quality gates |
| `skills/development/` | `references/` (plural) | Templates, checklists, command references |
| `skills/content-creation/Linkedin/`, `skills/content-creation/Medium/` | none (self-contained) | No support folder — craft rules are inlined directly in each `SKILL.md` |

> **Only tested skills belong here.** Skills are added only after being exercised in a real session — no untested stubs.

---

## License

MIT — see [LICENSE](./LICENSE) for details.

---

<div align="center">

Made by [jbrhsn](https://github.com/jbrhsn)

</div>
