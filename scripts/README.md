# Sync Scripts

Automated scripts to sync skills, agents, and plugins from this repository to global OpenCode, IBM Bob, Antigravity, and Claude Code configurations.

## Scripts

### `sync_all.py` (Recommended)
Syncs everything to all four platforms in one command, running the per-platform scripts in order:

| Target | Scripts run |
|---|---|
| `opencode` | `sync_opencode_skills.py`, `sync_opencode_plugins.py`, `sync_opencode_agents.py` |
| `bob` | `sync_bob_skills.py` |
| `antigravity` | `sync_antigravity_skills.py`, `sync_antigravity_agents.py` |
| `claude` | `sync_claude_skills.py`, `sync_claude_agents.py` |

Plugins run before agents on the OpenCode side: `--verify` inspects resolved tools, which needs the runtime already installed.

The four `--*-only` flags are mutually exclusive. With none of them passed, all four targets sync.

Run everything with **`uv run`** — the scripts carry PEP 723 headers declaring `pyyaml`.

**Usage:**
```bash
uv run scripts/sync_all.py                     # Sync to all four targets
uv run scripts/sync_all.py --dry-run           # Preview before syncing
uv run scripts/sync_all.py --opencode-only     # Skills + agents + plugins
uv run scripts/sync_all.py --claude-only       # Skills + the executor subagent
uv run scripts/sync_all.py --antigravity-only  # Skills + AGENTS.md
uv run scripts/sync_all.py --bob-only          # Skills

uv run scripts/sync_all.py --list-plugins                     # List available plugins
uv run scripts/sync_all.py --plugins search-internet --verify # Install a plugin, then verify
uv run scripts/sync_all.py                                    # Omit --plugins to uninstall
```

**Plugin flags:**
- `--plugins <a,b>` — install these plugins' runtime files *and* agent overlays (OpenCode only). Omitting the flag uninstalls: previously-synced plugin files are pruned.
- `--list-plugins` — print available plugins and exit.
- `--verify` — after syncing, verify SHA-256 checksums and exact file parity for all skills across all platforms, verify agent files, and run `opencode debug agent` on OpenCode agents to assert resolved permissions match composition.

### `sync_opencode_skills.py`
Syncs skills to OpenCode global config (`~/.config/opencode/skills`).

**Usage:**
```bash
uv run scripts/sync_opencode_skills.py           # Sync
uv run scripts/sync_opencode_skills.py --dry-run # Preview
```

**Environment variables:**
- `OPENCODE_SKILLS` — Override destination (default: `~/.config/opencode/skills`)

### `sync_opencode_agents.py`
Composes and syncs agent definitions to the OpenCode global agent directory (`~/.config/opencode/agent` — note the singular `agent`). The `agents/README.md` is not synced.

Base agents come from `agents/*/*.md`. When `--plugins` is passed, each selected plugin's overlays are merged in: frontmatter is deep-merged, and the overlay body is appended as a `## Capability: <plugin>` section. Agents with no overlay are copied verbatim. Composition happens in memory — nothing is written back into the repo.

**Usage:**
```bash
uv run scripts/sync_opencode_agents.py                                    # Base agents only
uv run scripts/sync_opencode_agents.py --dry-run                          # Preview
uv run scripts/sync_opencode_agents.py --plugins search-internet --verify # Compose + verify
uv run scripts/sync_opencode_agents.py --plugins search-internet \
    --print-composed orchestrator                                         # Inspect, write nothing
```

**Environment variables:**
- `OPENCODE_AGENTS` — Override destination (default: `~/.config/opencode/agent`)

### `sync_opencode_plugins.py`
Syncs the runtime files (e.g. `web-search.js`) of the plugins named in `--plugins` to `~/.config/opencode/plugin` (singular). Reads each plugin's `plugin.json` manifest; with no `--plugins`, installs nothing and prunes anything previously installed.

Running this alone installs a tool **without** the agent overlays that constrain it — the script warns about this. Prefer `sync_all.py`, which drives both.

**Usage:**
```bash
uv run scripts/sync_opencode_plugins.py --plugins search-internet
uv run scripts/sync_opencode_plugins.py --dry-run
```

**Environment variables:**
- `OPENCODE_PLUGINS` — Override destination (default: `~/.config/opencode/plugin`)

### `plugins.py`
Not a sync script — the composition engine imported by the two above. Handles plugin discovery and manifest validation, frontmatter deep-merge with cross-plugin conflict detection, body-section appending, and manifest-scoped pruning.

### `common.py`
Shared helpers: destination resolution with env-var overrides, skill auto-discovery, the generic skill-copy routine, and exclusion patterns.

### `sync_bob_skills.py`
Syncs skills to IBM Bob global config (`~/.bob/skills`).

**Usage:**
```bash
uv run scripts/sync_bob_skills.py           # Sync
uv run scripts/sync_bob_skills.py --dry-run # Preview
```

**Environment variables:**
- `BOB_SKILLS` — Override destination (default: `~/.bob/skills`)

### `sync_antigravity_skills.py`
Syncs skills to the Antigravity (Google Antigravity IDE) global config (`~/.gemini/config/skills`). Antigravity uses the same directory-of-skill-folders standard as OpenCode and Bob, so the same 11 skill folders are copied verbatim.

**Usage:**
```bash
uv run scripts/sync_antigravity_skills.py           # Sync
uv run scripts/sync_antigravity_skills.py --dry-run # Preview
```

**Environment variables:**
- `ANTIGRAVITY_SKILLS` — Override destination (default: `~/.gemini/config/skills`)

### `sync_claude_skills.py`
Syncs skills to Claude Code global config (`~/.claude/skills`). Claude Code auto-discovers skills placed here across all projects and exposes them as slash commands or automatic capabilities.

**Usage:**
```bash
uv run scripts/sync_claude_skills.py           # Sync
uv run scripts/sync_claude_skills.py --dry-run # Preview
```

**Environment variables:**
- `CLAUDE_SKILLS` — Override destination (default: `~/.claude/skills`)

### `sync_claude_agents.py`
Translates OpenCode `mode: subagent` agents into Claude Code's own subagent format and syncs them to `~/.claude/agents`. Only `executor.md` qualifies today — `orchestrator`/`ask` are `mode: primary`, and Claude Code's own top-level session is that equivalent, governed by `CLAUDE.md` rather than an agent file.

The translation maps `description` verbatim and `steps` → `maxTurns`. Claude Code subagent frontmatter has no per-command bash permission map, so the granular allow/ask/deny gates `executor.md` carries can't be represented there; a plain-language "ask before destructive commands" note is appended to the body instead.

**Usage:**
```bash
uv run scripts/sync_claude_agents.py           # Sync
uv run scripts/sync_claude_agents.py --dry-run # Preview
```

**Environment variables:**
- `CLAUDE_AGENTS` — Override destination (default: `~/.claude/agents`)

### `sync_antigravity_agents.py`
Copies the canonical `agents/ANTIGRAVITY_AGENTS.md` to Antigravity's single global instructions file (`~/.gemini/config/AGENTS.md`), fully overwriting it. Antigravity has no per-mode agent files the way OpenCode/Claude Code do — one flat file governs every agent session in the workspace, so it carries the same execution/verification standards as `executor.md` plus the mandatory `lean-coder` instruction, phrased as standing rules rather than a per-agent prompt.

**Usage:**
```bash
uv run scripts/sync_antigravity_agents.py           # Sync
uv run scripts/sync_antigravity_agents.py --dry-run # Preview
```

**Environment variables:**
- `ANTIGRAVITY_AGENTS` — Override destination (default: `~/.gemini/config/AGENTS.md`)

## What Gets Synced

### Skills

All 11 skills from the repository (synced to OpenCode, Bob, Antigravity, and Claude Code):
- **2 Agent Session Management**: end-session, init-session
- **1 Content Creation (LinkedIn)**: linkedin-post-writer
- **2 Content Creation (Medium)**: medium-article-writer, medium-image-prompts
- **2 Content Creation (Common)**: idea-research, keyword-research
- **2 Development**: lean-coder, project-planner
- **2 Learning**: author-chapter, create-learning-repo

### Agents

**OpenCode** — base agents, always synced → `~/.config/opencode/agent/`:
- `orchestrator.md` (primary), `executor.md` (subagent), `ask.md` (primary)

Plus, when a plugin is selected, that plugin's net-new agents and its overlays merged into the base agents above.

**Claude Code** — `executor.md` translated to Claude Code's subagent format → `~/.claude/agents/executor.md`. `orchestrator`/`ask` have no target (Claude Code's own session is the primary-agent equivalent).

**Antigravity** — one global file, `agents/ANTIGRAVITY_AGENTS.md`, synced verbatim → `~/.gemini/config/AGENTS.md`.

**IBM Bob** — not synced. Bob's custom-agent config format isn't documented publicly enough to target confidently; only skills sync there today.

### Plugins (OpenCode only, opt-in)

| Plugin | Adds | Agents affected |
|---|---|---|
| `search-internet` | `web_search_tool` (Tavily → Firecrawl → self-hosted fallback) | new `researcher`; overlays on `orchestrator` (deny), `executor`, `ask` |

Plugins sync **only** when named in `--plugins`. See `plugins/README.md` for the composition model.

> A plugin tool is allow-by-default in every agent unless denied, so runtime files and overlays must install together. `--plugins` guarantees this.

## Build Artifacts Excluded

Never copied into a destination: `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `node_modules/`, `.git/`, `.DS_Store`, `*.egg-info/`, `dist/`, `build/` (the set lives in `EXCLUSIONS` in `common.py`).

## Typical Workflow

Every script supports `--dry-run`.

1. **Make changes** to skills in the repository
2. **Preview changes:**
   ```bash
   uv run scripts/sync_all.py --dry-run
   ```
3. **Sync when ready:**
   ```bash
   uv run scripts/sync_all.py
   ```
4. **Verify installation** in all locations:
   ```bash
   ls ~/.config/opencode/skills/
   ls ~/.config/opencode/agent/
   ls ~/.bob/skills/
   ls ~/.gemini/config/skills/ && cat ~/.gemini/config/AGENTS.md
   ls ~/.claude/skills/ && ls ~/.claude/agents/
   ```

## Environment Setup

### For Development
Edit skills, agents, and plugins directly in this repository, then sync.

### For Users
After syncing, content is available in:
- OpenCode skills: `~/.config/opencode/skills/`
- OpenCode agents: `~/.config/opencode/agent/`
- OpenCode plugins: `~/.config/opencode/plugin/`
- IBM Bob skills: `~/.bob/skills/`
- Antigravity skills: `~/.gemini/config/skills/`
- Antigravity global agent instructions: `~/.gemini/config/AGENTS.md`
- Claude Code skills: `~/.claude/skills/`
- Claude Code agents: `~/.claude/agents/`

## Troubleshooting

### Python / dependency errors
Run through `uv`, which resolves the PEP 723 dependency headers automatically:
```bash
uv run scripts/sync_all.py
```
A bare `python3` invocation fails with `ModuleNotFoundError: yaml` unless `pyyaml` is installed in the active environment.

### Plugin conflict error
`Plugin conflict on '<key>'` means two selected plugins set the same frontmatter key to different values. This is deliberate — permissions are security-relevant, so the sync refuses to silently pick one. Reconcile the overlays, or select only one of the two plugins.

### A plugin's tool isn't available in OpenCode
Confirm the runtime file landed and the agent resolves it:
```bash
ls ~/.config/opencode/plugin/
opencode debug agent researcher   # look for tools.web_search_tool
```
`@opencode-ai/plugin` must be resolvable from `~/.config/opencode/package.json`.

### Destination Directory Doesn't Exist
Scripts automatically create destination directories if they don't exist. If you get permission errors, ensure you have write access to `~/.config/`, `~/.bob/`, `~/.gemini/`, and `~/.claude/`.

### Shared Parent Directories Caution
`~/.gemini/config/` and `~/.claude/` are **not** skills-only directories — they hold configs, history, and state used by other tooling. Sync scripts therefore only ever remove *individual* destination skill folders immediately before re-copying each skill. Never add a "clean" step that deletes the whole `~/.gemini/config/skills/` or `~/.claude/skills/` parent tree indiscriminately.

The same applies to agent and plugin pruning: each agent destination (`~/.config/opencode/agent/`, `~/.claude/agents/`) holds a `.agent_skills_manifest.json` recording only the files this tooling wrote, and pruning is restricted to that list. Nothing you or another tool placed there is ever touched.

`~/.gemini/config/AGENTS.md` is the one exception: it's a single file, not a directory of many, and syncing it is a full overwrite by design (a deliberate choice — see `sync_antigravity_agents.py`). If you hand-edit that file directly, your edits will be lost on the next sync; edit `agents/ANTIGRAVITY_AGENTS.md` in this repo instead.

### Override Destination Paths
Use environment variables to sync to custom locations:
```bash
OPENCODE_SKILLS=/custom/path uv run scripts/sync_opencode_skills.py
OPENCODE_AGENTS=/custom/path uv run scripts/sync_opencode_agents.py
OPENCODE_PLUGINS=/custom/path uv run scripts/sync_opencode_plugins.py
BOB_SKILLS=/custom/path uv run scripts/sync_bob_skills.py
ANTIGRAVITY_SKILLS=/custom/path uv run scripts/sync_antigravity_skills.py
ANTIGRAVITY_AGENTS=/custom/path/AGENTS.md uv run scripts/sync_antigravity_agents.py
CLAUDE_SKILLS=/custom/path uv run scripts/sync_claude_skills.py
CLAUDE_AGENTS=/custom/path uv run scripts/sync_claude_agents.py
```

## Maintenance

- Scripts are maintained in `scripts/` directory of the repository
- Skills, agents, and plugins are all auto-discovered — there are no hardcoded lists to update when adding one
- Document any changes to the sync behavior in this README
