# Agent Skills

A curated collection of skills for AI coding agents — structured workflows that give agents like OpenCode, Claude Code, and Cursor repeatable, high-quality behavior for common development tasks.

Each skill is a prompt file your agent loads and follows like a playbook. Every skill in this repo has been authored and tested in real sessions.

---

## Skills

### scaffolding

| Skill | Description |
|---|---|
| [create-learning-repo](./scaffolding/create-learning-repo/README.md) | Scaffold a structured learning repository for any topic or certification — phased intake, live research, folder design, templates, and file generation |
| [init-session](./scaffolding/init-session/README.md) | Rebuild full project context at the start of a session — reads handoff log, README, and AGENTS.md, runs an alignment check, and produces a concise briefing |
| [end-session](./scaffolding/end-session/README.md) | Write a high-signal handoff at the end of a session — refreshed rolling project summary plus a detailed session entry for the next agent |

---

## How to use

### With OpenCode (primary)

**Global install** — skill available in all your projects:
```bash
cp -r scaffolding/create-learning-repo ~/.config/opencode/skills/
```

**Per-project install** — skill available only in the current project:
```bash
cp -r scaffolding/create-learning-repo .opencode/skills/
```

OpenCode loads skills automatically. Once installed, just describe what you want and the agent will invoke the right skill.

### With other agents

Each skill's `SKILL.md` includes an **Adapting to Other Agents** table with exact instructions for:

| Platform | Mechanism |
|---|---|
| **Claude Code** | Add content to `CLAUDE.md` under a named section |
| **Cursor** | Add as a `.cursor/rules/*.mdc` file, type `Agent Requested` |
| **GitHub Copilot** | Add content to `.github/copilot-instructions.md` |
| **ChatGPT / Claude (web)** | Paste the skill content as your opening system message |

The workflow phases and constraints are platform-agnostic — only the loading mechanism differs.

---

## Adding new skills

Each skill lives in a `category/skill-name/` folder with exactly two files:

```
category/
└── skill-name/
    ├── SKILL.md     ← the agent-facing skill (OpenCode format)
    └── README.md    ← human-readable guide: triggers, workflow, examples, related skills
```

Use the templates in [`templates/`](./templates/) as your starting point:
- `SKILL.md.template` — full skill structure with frontmatter, phases, and constraints
- `skill-readme.template.md` — per-skill README with all required sections

Only tested skills belong in this repo. New skills are added after they've been run in real sessions.

---

## License

MIT — see [LICENSE](./LICENSE) for details.

---

<div align="center">
Made by <a href="https://github.com/jbrhsn">jbrhsn</a>
</div>
