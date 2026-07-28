<div align="center">

# Agent Skills

**Structured workflows for AI coding agents — tested in real sessions, ready to install.**

Give agents like OpenCode, Claude Code, and Cursor repeatable, high-quality behavior for common development tasks. Each skill is a prompt file your agent loads and follows like a playbook.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

</div>

---

## Skills

### Session Management

> Load and save project context across agent sessions.

| Skill | What it does |
|---|---|
| [**init-session**](./agent_session_management/init-session/README.md) | Restore full project context at session start — reads the handoff log and delivers a concise briefing of open items and last state |
| [**end-session**](./agent_session_management/end-session/README.md) | Write a high-signal handoff at session end — rolling project summary, session log, and filtered open items for the next agent |

### Learning

> Create and populate Markdown-based learning repositories.

| Skill | What it does |
|---|---|
| [**create-learning-repo**](./learning/create-learning-repo/README.md) | Scaffold a structured learning repository for any topic or certification — phased intake, live research, folder design, templates, and stub generation |
| [**author-chapter**](./learning/author-chapter/README.md) | Populate a stub chapter with fully template-compliant content — live-sourced research, every section written to spec, quality gate before write |
| [**generate-practice-exam**](./learning/generate-practice-exam/README.md) | Generate a blueprint-weighted mock exam or targeted drill from already-authored chapter content, with per-option answer rationale |

### Development

> Plan, build, design, and document software projects.

| Skill | What it does |
|---|---|
| [**lean-coder**](./development/lean-coder/README.md) | A "lazy senior developer" discipline for coding work — the least code that correctly and safely solves the problem; adds `/review-diff` and `/audit-repo` workflows for finding over-engineering |
| [**project-planner**](./development/project-planner/README.md) | Plan and spec a project before coding — produces spec, design, roadmap, and backlog docs under `docs/` (`/plan-project`) |
| [**repo-docs-publisher**](./development/repo-docs-publisher/README.md) | Prepare a repo to go public — scans the code and checks for secrets first, then writes README, HOW_TO_USE, CONTRIBUTING, LICENSE, and optional community/GitHub docs |
| [**ui-ux-designer**](./development/ui-ux-designer/README.md) | Design user flows, screens, and a design system into `docs/ux-design.md` (`/design-ux`) — detects non-UI projects (CLI/API/backend) and stops rather than fabricating screens |

### Content Creation

> Skills for creating LinkedIn content — from source notes to a posting-ready piece, visual prompts, and a virality review.

| Skill | What it does |
|---|---|
| [**linkedin-post-writer**](./content-creation/linkedin/linkedin-post-writer/README.md) | Turn source notes or a rough draft into a posting-ready LinkedIn post — hook engineering, scroll-first structure, no-link-in-body discipline, mandatory review gate. Writes `linkedin_post.md` next to the source file |
| [**linkedin-image-prompts**](./content-creation/linkedin/linkedin-image-prompts/README.md) | Generate image-generation prompts (single hero image or full carousel) for a finished post, chosen from its structure. Writes `image_prompts.md` next to the source post — prompt text only, no rendering |
| [**linkedin-post-reviewer**](./content-creation/linkedin/linkedin-post-reviewer/README.md) | Score a finished post across 5 algorithm-aligned dimensions and produce one refined version with an itemized change list. Writes `linkedin_post_revised.md` next to the source file |

---

## Getting started

### Install with OpenCode

Copy any skill into your OpenCode skills directory. Run these commands from the repo root:

```bash
# Global — available in all your projects

# Session management skills
cp -r agent_session_management/init-session ~/.config/opencode/skills/
cp -r agent_session_management/end-session ~/.config/opencode/skills/

# Learning skills
cp -r learning/create-learning-repo ~/.config/opencode/skills/
cp -r learning/author-chapter ~/.config/opencode/skills/
cp -r learning/generate-practice-exam ~/.config/opencode/skills/

# Development skills
cp -r development/lean-coder ~/.config/opencode/skills/
cp -r development/project-planner ~/.config/opencode/skills/
cp -r development/repo-docs-publisher ~/.config/opencode/skills/
cp -r development/ui-ux-designer ~/.config/opencode/skills/

# Content creation skills (LinkedIn pipeline)
cp -r content-creation/linkedin/linkedin-post-writer ~/.config/opencode/skills/
cp -r content-creation/linkedin/linkedin-image-prompts ~/.config/opencode/skills/
cp -r content-creation/linkedin/linkedin-post-reviewer ~/.config/opencode/skills/
```

```bash
# Per-project — available only in the current project
cp -r agent_session_management/init-session .opencode/skills/
cp -r learning/create-learning-repo .opencode/skills/
cp -r development/lean-coder .opencode/skills/
cp -r content-creation/linkedin/linkedin-post-writer .opencode/skills/
```

OpenCode loads skills automatically. Once installed, describe what you want and the agent invokes the right skill.

> **Content-creation skills ship helper scripts** (under `scripts/`) that run on **standard-library Python 3** — no install needed. Optional PNG export in `carousel-builder` uses `cairosvg` or a headless browser if present, and degrades gracefully if not.

### Use with other agents

Each skill's `README.md` has an **Other platforms** section with exact instructions per platform:

| Platform | How to load the skill |
|---|---|
| **Claude Code** | Add content to `CLAUDE.md` under a named section |
| **Cursor** | Add as `.cursor/rules/<skill-name>.mdc`, type `Agent Requested` |
| **GitHub Copilot** | Add content to `.github/copilot-instructions.md` |
| **ChatGPT / Claude (web)** | Paste the skill content as your opening message |

The workflow phases and constraints are platform-agnostic — only the loading mechanism differs.

---

## Skill structure

Each skill lives in a `category/skill-name/` folder:

```
category/
└── skill-name/
    ├── SKILL.md       ← agent-facing skill (OpenCode format with frontmatter)
    ├── README.md      ← human-readable guide: triggers, workflow, examples, limitations
    └── support/       ← optional runtime files the skill reads or runs
```

The optional support directory varies by category:

| Category | Support dir | Contents |
|---|---|---|
| `learning/`, `agent_session_management/` | `reference/` (singular) | Templates, rubrics, quality gates |
| `development/` | `references/` (plural) | Templates, checklists, command references |
| `content-creation/linkedin/` | none (self-contained) | No support folder — craft rules are inlined directly in each `SKILL.md` |

> **Only tested skills belong here.** Skills are added only after being exercised in a real session — no untested stubs.

---

## License

MIT — see [LICENSE](./LICENSE) for details.

---

<div align="center">

Made by [jbrhsn](https://github.com/jbrhsn)

</div>
