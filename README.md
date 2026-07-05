<div align="center">

# Agent Skills

**Structured workflows for AI coding agents — tested in real sessions, ready to install.**

Give agents like OpenCode, Claude Code, and Cursor repeatable, high-quality behavior for common development tasks. Each skill is a prompt file your agent loads and follows like a playbook.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

</div>

---

## Skills

### Scaffolding

> Session management and project scaffolding workflows.

| Skill | What it does |
|---|---|
| [**create-learning-repo**](./scaffolding/create-learning-repo/README.md) | Scaffold a structured learning repository for any topic or certification — phased intake, live research, folder design, templates, and file generation |
| [**init-session**](./scaffolding/init-session/README.md) | Rebuild full project context at the start of a session — reads handoff log, README, and AGENTS.md, runs an alignment check, and produces a concise briefing |
| [**end-session**](./scaffolding/end-session/README.md) | Write a high-signal handoff at the end of a session — refreshed rolling project summary plus a detailed session entry for the next agent |

---

## Getting started

### Install with OpenCode

Copy any skill into your OpenCode skills directory:

```bash
# Global — available in all your projects
cp -r scaffolding/<skill-name> ~/.config/opencode/skills/

# Per-project — available only in the current project
cp -r scaffolding/<skill-name> .opencode/skills/
```

To install all three skills at once:

```bash
cp -r scaffolding/create-learning-repo scaffolding/init-session scaffolding/end-session \
  ~/.config/opencode/skills/
```

OpenCode loads skills automatically. Once installed, describe what you want and the agent invokes the right skill.

### Use with other agents

Each skill's `SKILL.md` contains an **Adapting to Other Agents** section with exact instructions per platform:

| Platform | How to load the skill |
|---|---|
| **Claude Code** | Add content to `CLAUDE.md` under a named section |
| **Cursor** | Add as `.cursor/rules/<skill-name>.mdc`, type `Agent Requested` |
| **GitHub Copilot** | Add content to `.github/copilot-instructions.md` |
| **ChatGPT / Claude (web)** | Paste the skill content as your opening message |

The workflow phases and constraints are platform-agnostic — only the loading mechanism differs.

---

## Adding new skills

Each skill lives in a `category/skill-name/` folder with exactly two files:

```
category/
└── skill-name/
    ├── SKILL.md     ← agent-facing skill (OpenCode format with frontmatter)
    └── README.md    ← human-readable guide: triggers, workflow, examples, limitations
```

Start from the templates in [`templates/`](./templates/):

| Template | Use it to |
|---|---|
| [`SKILL.md.template`](./templates/SKILL.md.template) | Author a new agent-facing skill with frontmatter, phases, and constraints |
| [`skill-readme.template.md`](./templates/skill-readme.template.md) | Write the human-readable README for a skill |

> Only tested skills belong here. New skills are added after they've been run in real sessions.

---

## License

MIT — see [LICENSE](./LICENSE) for details.

---

<div align="center">

Made by [jbrhsn](https://github.com/jbrhsn)

</div>
