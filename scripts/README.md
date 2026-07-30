# Sync Scripts

Automated scripts to sync skills, agents, and plugins from this repository to global OpenCode and IBM Bob configurations.

## Scripts

### `sync_all.py` (Recommended)
Syncs everything to both OpenCode and IBM Bob configurations in one command. On the OpenCode side it runs `sync_opencode_skills.py`, `sync_opencode_agents.py`, and `sync_opencode_plugins.py`; on the Bob side it runs `sync_bob_skills.py`.

**Usage:**
```bash
python3 scripts/sync_all.py                # Sync to both
python3 scripts/sync_all.py --dry-run      # Preview before syncing
python3 scripts/sync_all.py --opencode-only # Sync only to OpenCode (skills, agents, plugins)
python3 scripts/sync_all.py --bob-only     # Sync only to Bob (skills)
```

### `sync_opencode_skills.py`
Syncs skills to OpenCode global config (`~/.config/opencode/skills`).

**Usage:**
```bash
python3 scripts/sync_opencode_skills.py           # Sync
python3 scripts/sync_opencode_skills.py --dry-run # Preview
```

**Environment variables:**
- `OPENCODE_SKILLS` — Override destination (default: `~/.config/opencode/skills`)

### `sync_opencode_agents.py`
Syncs the repo's agent definitions (`agents/orchestrator_mode_agents/orchestrator.md` and `agents/orchestrator_mode_agents/executor.md`) to the OpenCode global agent directory (`~/.config/opencode/agent` — note the singular `agent`). The `agents/README.md` is not synced.

**Usage:**
```bash
python3 scripts/sync_opencode_agents.py           # Sync
python3 scripts/sync_opencode_agents.py --dry-run # Preview
```

**Environment variables:**
- `OPENCODE_AGENTS` — Override destination (default: `~/.config/opencode/agent`)

### `sync_opencode_plugins.py`
Syncs the repo's TypeScript plugins (`plugins/token_saving/*.ts`, currently `token-guard.ts`) to the OpenCode global plugin directory (`~/.config/opencode/plugin` — note the singular `plugin`). The `plugins/README.md` is not synced.

**Usage:**
```bash
python3 scripts/sync_opencode_plugins.py           # Sync
python3 scripts/sync_opencode_plugins.py --dry-run # Preview
```

**Environment variables:**
- `OPENCODE_PLUGINS` — Override destination (default: `~/.config/opencode/plugin`)

### `sync_bob_skills.py`
Syncs skills to IBM Bob global config (`~/.bob/skills`).

**Usage:**
```bash
python3 scripts/sync_bob_skills.py           # Sync
python3 scripts/sync_bob_skills.py --dry-run # Preview
```

**Environment variables:**
- `BOB_SKILLS` — Override destination (default: `~/.bob/skills`)

## What Gets Synced

### Skills

All 13 skills from the repository (synced to both OpenCode and Bob):
- **2 Agent Session Management**: end-session, init-session
- **2 Content Creation (LinkedIn)**: linkedin-post-writer, linkedin-image-prompts
- **2 Content Creation (Medium)**: medium-article-writer, medium-image-prompts
- **4 Development**: lean-coder, project-planner, repo-docs-publisher, ui-ux-designer
- **3 Learning**: author-chapter, create-learning-repo, generate-practice-exam

### Agents (OpenCode only)

- `orchestrator.md`, `executor.md` → `~/.config/opencode/agent/`

### Plugins (OpenCode only)

- `token-guard.ts` (all `plugins/*.ts`) → `~/.config/opencode/plugin/`

## Build Artifacts Excluded

The following are automatically excluded to save space (~2.5GB total):
- `.venv/` — Python virtual environments
- `__pycache__/` — Python bytecode
- `*.pyc` — Compiled Python files
- `.pytest_cache/` — Test artifacts
- `node_modules/` — JavaScript dependencies
- `.git/` — Git metadata
- `.DS_Store` — macOS metadata
- `*.egg-info/`, `dist/`, `build/` — Package build artifacts

## Dry-Run Mode

All scripts support `--dry-run` to preview what would be synced without modifying files:

```bash
python3 scripts/sync_all.py --dry-run
```

## Typical Workflow

1. **Make changes** to skills in the repository
2. **Preview changes:**
   ```bash
   python3 scripts/sync_all.py --dry-run
   ```
3. **Sync when ready:**
   ```bash
   python3 scripts/sync_all.py
   ```
4. **Verify installation** in all locations:
   ```bash
   ls ~/.config/opencode/skills/
   ls ~/.config/opencode/agent/
   ls ~/.config/opencode/plugin/
   ls ~/.bob/skills/
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

## Troubleshooting

### Permission Denied
Make sure the script is executable:
```bash
chmod +x scripts/sync_all.py
```

### Python Not Found
Use `python3` instead of `python`:
```bash
python3 scripts/sync_all.py
```

### Destination Directory Doesn't Exist
Scripts automatically create destination directories if they don't exist. If you get permission errors, ensure you have write access to `~/.config/` and `~/.bob/`.

### Override Destination Paths
Use environment variables to sync to custom locations:
```bash
OPENCODE_SKILLS=/custom/path python3 scripts/sync_opencode_skills.py
OPENCODE_AGENTS=/custom/path python3 scripts/sync_opencode_agents.py
OPENCODE_PLUGINS=/custom/path python3 scripts/sync_opencode_plugins.py
BOB_SKILLS=/custom/path python3 scripts/sync_bob_skills.py
```

## Maintenance

- Scripts are maintained in `scripts/` directory of the repository
- Keep them in sync with the main `SKILLS`/`AGENTS` lists if new skills or agents are added (plugins are auto-discovered from `plugins/*.ts`)
- Document any changes to the sync behavior in this README
