<div align="center">

# Agent Skills

**Structured workflows for AI coding agents — tested in real sessions, ready to install.**

Give agents like OpenCode, IBM Bob, Google Antigravity, Claude Code, and Cursor repeatable, high-quality behavior for common development tasks. Each skill is a prompt file your agent loads and follows like a playbook.

**11 skills** across session management, learning, development, and content creation.

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

> Scaffold learning repositories and populate complete chapters.

Use **create-learning-repo** to structure your learning (goal → plan → empty stubs), then use **author-chapter** to fill in content one chapter at a time. Two complementary skills.

| Skill | What it does |
|---|---|
| [**create-learning-repo**](./skills/learning/create-learning-repo/README.md) | Turn a learning goal into a folder structure with blank stub files — interviews for the goal, researches to fill gaps, drafts a plan (sections → modules → chapters → topics), shows you the tree for approval, then scaffolds the repo and tracking files. Creates structure only; no content written. |
| [**author-chapter**](./skills/learning/author-chapter/README.md) | Populate one complete Markdown file that teaches a topic from zero to architect-level mastery — covers all prerequisite concepts, worked examples, failure modes, misconceptions, and Socratic checkpoints. Use this to fill in stubs created by create-learning-repo, or to author standalone modules. |

### Development

> Write, refactor, and plan software projects.

| Skill | What it does |
|---|---|
| [**lean-coder**](./skills/development/lean-coder/README.md) | A "lazy senior developer" discipline for coding work — the least code that correctly and safely solves the problem; adds `/review-diff` and `/audit-repo` workflows for finding over-engineering |
| [**project-planner**](./skills/development/project-planner/README.md) | Plan and spec a project before coding — produces spec, design, roadmap, and backlog docs under `docs/` (`/plan-project`) |

### Content Creation

> Turn source notes into a posting-ready piece (with built-in review/refine) and generate matching visual prompts — for LinkedIn and Medium.

**LinkedIn** — `skills/content-creation/Linkedin/`

| Skill | What it does |
|---|---|
| [**linkedin-post-writer**](./skills/content-creation/Linkedin/linkedin-post-writer/README.md) | Turn source notes or a rough draft into a posting-ready LinkedIn post — hook engineering, scroll-first structure, no-link-in-body discipline, mandatory review gate. Writes `linkedin_post.md` next to the source file. Also scores a finished post across 5 algorithm-aligned dimensions and produces one refined version with an itemized change list in `linkedin_post_revised.md` |

**Medium** — `skills/content-creation/Medium/`

| Skill | What it does |
|---|---|
| [**medium-article-writer**](./skills/content-creation/Medium/medium-article-writer/SKILL.md) | Turn source notes or a draft into a publish-ready `medium_article.md`, applying Medium-specific craft grounded in Medium's Distribution Guidelines, AI-content policy, and earnings mechanics — title+subtitle+cover as a unit, read-ratio-driven scannability, first-hand originality, relevant tagging, soft value-tied CTAs, paywall recommendation — behind mandatory review gates. Also scores a finished article out of 100 across 5 distribution-aligned dimensions and writes one refined `medium_article_reviewed.md` with an itemized change list |
| [**medium-image-prompts**](./skills/content-creation/Medium/medium-image-prompts/SKILL.md) | Generate image-generation prompts for a finished Medium article — one featured/cover prompt plus one in-article visual per major section that earns one (Medium is not a carousel platform), each with alt text, a caption including credit and the mandatory AI-disclosure line, and a rationale. Writes `medium_image_prompts.md` next to the source article — prompt text only, no rendering |

**Common** — `skills/content-creation/Common/`

| Skill | What it does |
|---|---|
| [**idea-research**](./skills/content-creation/Common/idea-research/README.md) | Generate ranked, evidence-backed content ideas for Medium, LinkedIn, and Reddit from live public sources — fetches from Hacker News, Reddit, Google Trends, Medium tags, then clusters by beat, scores by recency+velocity+fit+gap, and scaffolds a source.md per approved idea |
| [**keyword-research**](./skills/content-creation/Common/keyword-research/README.md) | Run keyless keyword research for a drafted article and write a kresearch.md next to its source.md — search intent, long-tail keywords, Medium tags, article optimization tips, and related topics from Google Autocomplete, related searches, and Medium's tag index |

---

## Getting started

### Sync everything (recommended)

The sync scripts install all 11 skills to every supported destination in one command. Run from the repo root:

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

# Development skills
cp -r skills/development/lean-coder ~/.config/opencode/skills/
cp -r skills/development/project-planner ~/.config/opencode/skills/

# Content creation skills (LinkedIn)
cp -r skills/content-creation/Linkedin/linkedin-post-writer ~/.config/opencode/skills/

# Content creation skills (Medium)
cp -r skills/content-creation/Medium/medium-article-writer ~/.config/opencode/skills/
cp -r skills/content-creation/Medium/medium-image-prompts ~/.config/opencode/skills/

# Content creation skills (Common)
cp -r skills/content-creation/Common/idea-research ~/.config/opencode/skills/
cp -r skills/content-creation/Common/keyword-research ~/.config/opencode/skills/
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
