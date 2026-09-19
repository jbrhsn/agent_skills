<div align="center">

# Agent Skills

**Skills, agents, and plugins for AI coding agents — tested in real sessions, ready to install.**

Repeatable, high-quality behavior for OpenCode, Claude Code, Codex/ChatGPT, Google Antigravity, and IBM Bob. One repo is the source of truth; sync scripts push it to every platform.

**11 skills** · **3 base agents** · **1 opt-in plugin**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

</div>

---

## What's here

| Layer | What it is | Where it syncs |
|---|---|---|
| **Skills** | Prompt playbooks the agent loads on demand ([`skills/`](./skills/)) | All five platforms |
| **Agents** | Per-mode agent definitions with permission models ([`agents/`](./agents/)) | OpenCode, Claude Code, Antigravity |
| **Plugins** | Runtime tools bundled with the agent overlays that govern them ([`plugins/`](./plugins/)) | OpenCode only, opt-in |

---

## Skills

### [Session Management](./skills/agent_session_management/)

> Load and save project context across agent sessions.

| Skill | What it does |
|---|---|
| [**init-session**](./skills/agent_session_management/init-session/README.md) | Restore project context at session start — reads the handoff log and delivers a concise briefing of open items and last state |
| [**end-session**](./skills/agent_session_management/end-session/README.md) | Write a high-signal handoff at session end — compacted on every write, never appended to, so read cost stays flat |

### [Learning](./skills/learning/)

> Scaffold a learning repository, then fill it in chapter by chapter.

| Skill | What it does |
|---|---|
| [**create-learning-repo**](./skills/learning/create-learning-repo/README.md) | Turn a learning goal into a folder structure of briefed stubs — interviews, researches gaps, drafts a plan (sections → modules → chapters), shows the tree for approval, then scaffolds six files per chapter on a domain-matched tier ladder. Structure and assignment only, no content |
| [**author-chapter**](./skills/learning/author-chapter/README.md) | Populate one Markdown file that teaches a topic to expert level — takeaway first, the vital 20% marked, cut into self-contained ~5-minute units, with evidence standards and a tier ladder matched to the domain rather than forced into one format |

### [Development](./skills/development/)

> Write, review, and plan software.

| Skill | What it does |
|---|---|
| [**lean-coder**](./skills/development/lean-coder/README.md) | Implement, review, optimize, and debug production software with focused language and domain guidance for web, data, Web3, and mobile |
| [**project-planner**](./skills/development/project-planner/README.md) | Turn project or feature requirements into adaptable interface contracts, implementation plans, and verification/release guidance |

### [Content Creation](./skills/content-creation/)

> Research, draft, revise, and plan visuals with adaptable guidance and traceable evidence.

| Skill | What it does |
|---|---|
| [**idea-research**](./skills/content-creation/Common/idea-research/README.md) | Research and prioritize audience-relevant angles with traceable evidence and optional source scaffolds |
| [**keyword-research**](./skills/content-creation/Common/keyword-research/README.md) | Search intent and discovery phrasing for drafts or topics, with transparent provenance and heuristic limitations |
| [**linkedin-post-writer**](./skills/content-creation/Linkedin/linkedin-post-writer/README.md) | Draft or revise LinkedIn posts in the author's voice, with factual support and flexible editorial choices |
| [**medium-article-writer**](./skills/content-creation/Medium/medium-article-writer/README.md) | Develop and package long-form articles with coherent structure, source fidelity, and current publication checks |
| [**medium-image-prompts**](./skills/content-creation/Medium/medium-image-prompts/README.md) | Plan useful article visuals and prompts, distinguishing editorial art from exact diagrams, screenshots, and data |

---

## Agents

Three base definitions in [`agents/`](./agents/), built around a safety split: the planner holds no edit or bash power, the implementer does and gates destructive commands.

| Agent | Mode | Role |
|---|---|---|
| **orchestrator** | `primary` | Decomposes a request, delegates every unit of work to executors (≤4 in parallel). Never edits, never runs bash |
| **executor** | `subagent` | Implements *and verifies* one unit end-to-end. Edit + bash, with `rm -rf`, `git push`, `sudo` and friends behind `ask` |
| **ask** | `primary` | Read-only conversational exploration. No edit, bash, or delegation |

Only `executor` translates to a Claude Code subagent (`~/.claude/agents/`) — Claude Code's own top-level session is the primary-agent equivalent. Antigravity has no per-mode agent files, so [`agents/ANTIGRAVITY_AGENTS.md`](./agents/ANTIGRAVITY_AGENTS.md) carries the equivalent standing rules into its one global instructions file. See [`agents/README.md`](./agents/README.md).

## Plugins

Optional, OpenCode-only, opt-in per sync. A plugin ships a runtime tool **plus** the agent overlays that constrain it — installed together, since a plugin tool is otherwise allowed in every agent by default.

| Plugin | What it adds |
|---|---|
| [`search-internet`](./plugins/search-internet/) | `web_search_tool` (Tavily → Firecrawl → self-hosted fallback) and a `researcher` subagent that keeps raw results out of the orchestrator's context |

Base agents are never edited by a plugin — overlays are merged in memory at sync time. See [`plugins/README.md`](./plugins/README.md).

---

## Getting started

Requires [`uv`](https://docs.astral.sh/uv/) — the scripts carry PEP 723 headers and resolve their own dependencies. A bare `python3` invocation fails on `ModuleNotFoundError: yaml`.

```bash
uv run scripts/sync_all.py                     # everything, to all five platforms
uv run scripts/sync_all.py --dry-run           # preview, write nothing
uv run scripts/sync_all.py --opencode-only     # one platform (flags are mutually exclusive)

uv run scripts/sync_all.py --list-plugins                       # what's available
uv run scripts/sync_all.py --plugins search-internet --verify   # install a plugin + assert resolved config
uv run scripts/sync_all.py                                      # omit --plugins = uninstall, files pruned
```

### Destinations

| What | Destination | Env override |
|---|---|---|
| OpenCode skills | `~/.config/opencode/skills/` | `OPENCODE_SKILLS` |
| OpenCode agents | `~/.config/opencode/agent/` (singular) | `OPENCODE_AGENTS` |
| OpenCode plugins | `~/.config/opencode/plugin/` (singular) | `OPENCODE_PLUGINS` |
| Claude Code skills | `~/.claude/skills/` | `CLAUDE_SKILLS` |
| Claude Code agents | `~/.claude/agents/` | `CLAUDE_AGENTS` |
| Codex / ChatGPT skills | `~/.agents/skills/` | `CODEX_SKILLS` |
| Antigravity skills | `~/.gemini/config/skills/` | `ANTIGRAVITY_SKILLS` |
| Antigravity agent rules | `~/.gemini/config/AGENTS.md` | `ANTIGRAVITY_AGENTS` |
| IBM Bob skills | `~/.bob/skills/` | `BOB_SKILLS` |

```bash
OPENCODE_SKILLS=/custom/path uv run scripts/sync_opencode_skills.py
```

Bob gets skills only — its custom-agent config format isn't publicly documented enough to target confidently. Per-script details: [`scripts/README.md`](./scripts/README.md).

> These are **shared** config directories, not ours alone. Syncing only ever replaces individual skill folders, and agent/plugin pruning is scoped to a `.agent_skills_manifest.json` recording what this tooling wrote. `~/.gemini/config/AGENTS.md` is the one full-overwrite exception — edit it in this repo, not in place.

### Install manually

Any skill folder works as-is in any of the five platforms — same `SKILL.md` layout everywhere.

```bash
cp -r skills/development/lean-coder ~/.config/opencode/skills/   # or ~/.claude/skills/,
                                                                 # ~/.agents/skills/,
                                                                 # ~/.gemini/config/skills/, ~/.bob/skills/
cp -r skills/development/lean-coder .opencode/skills/            # per-project (OpenCode)
```

Agents are one level deeper, under `agents/orchestrator_mode_agents/` and `agents/ask_mode_agents/`:

```bash
cp agents/orchestrator_mode_agents/orchestrator.md \
   agents/orchestrator_mode_agents/executor.md \
   agents/ask_mode_agents/ask.md \
   ~/.config/opencode/agent/
```

### Other harnesses

Skills load natively on OpenCode, Claude Code, Antigravity, and Bob. Elsewhere:

| Platform | How to load a skill |
|---|---|
| **Cursor** | Add as `.cursor/rules/<skill-name>.mdc`, type `Agent Requested` |
| **GitHub Copilot** | Append to `.github/copilot-instructions.md` |
| **ChatGPT / Claude (web)** | Paste `SKILL.md` as your opening message |

The workflow phases and constraints are platform-agnostic — only the loading mechanism differs.

---

## Layout

```
skills/{category}/{skill-name}/
├── SKILL.md        ← agent-facing prompt, YAML frontmatter + body
├── README.md       ← human guide: triggers, workflow, limitations
├── references/     ← optional: guides, checklists, rubrics the skill loads on demand
├── assets/         ← optional: templates the skill writes from
└── scripts/        ← optional: stdlib-only Python the skill runs
```

Helper scripts shipped inside skills run on **standard-library Python 3** — no install needed.

> **Only tested skills belong here.** Nothing is added until it has been exercised in a real session.

---

## License

MIT — see [LICENSE](./LICENSE).

---

<div align="center">

Made by [jbrhsn](https://github.com/jbrhsn)

</div>
