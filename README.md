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
```

```bash
# Per-project — available only in the current project
cp -r agent_session_management/init-session .opencode/skills/
cp -r learning/create-learning-repo .opencode/skills/
```

OpenCode loads skills automatically. Once installed, describe what you want and the agent invokes the right skill.

### Use with other agents

Each skill's `SKILL.md` contains a **Portability** section with exact instructions per platform:

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
    └── reference/     ← optional: runtime files the skill reads (templates, rubrics)
        └── *.md
```

> **Only tested skills belong here.** Skills are added only after being exercised in a real session — no untested stubs.

---

## License

MIT — see [LICENSE](./LICENSE) for details.

---

<div align="center">

Made by [jbrhsn](https://github.com/jbrhsn)

</div>
