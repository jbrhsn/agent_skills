# Sync Scripts

Automated scripts to sync skills, agents, and plugins from this repository to global OpenCode, IBM Bob, and Antigravity configurations.

## Scripts

### `sync_all.py` (Recommended)
Syncs everything to the OpenCode, IBM Bob, and Antigravity configurations in one command. On the OpenCode side it runs `sync_opencode_skills.py`, `sync_opencode_agents.py`, and `sync_opencode_plugins.py`; on the Bob side it runs `sync_bob_skills.py`; on the Antigravity side it runs `sync_antigravity_skills.py`.

The three `--*-only` flags are mutually exclusive. With none of them passed, all three targets sync.

**Usage:**
```bash
python3 scripts/sync_all.py                     # Sync to all three targets
python3 scripts/sync_all.py --dry-run           # Preview before syncing
python3 scripts/sync_all.py --opencode-only     # Only OpenCode (skills, agents, plugins)
python3 scripts/sync_all.py --bob-only          # Only Bob (skills)
python3 scripts/sync_all.py --antigravity-only  # Only Antigravity (skills)
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



### `sync_bob_skills.py`
Syncs skills to IBM Bob global config (`~/.bob/skills`).

**Usage:**
```bash
python3 scripts/sync_bob_skills.py           # Sync
python3 scripts/sync_bob_skills.py --dry-run # Preview
```

**Environment variables:**
- `BOB_SKILLS` — Override destination (default: `~/.bob/skills`)

### `sync_antigravity_skills.py`
Syncs skills to the Antigravity (Google Antigravity IDE) global config (`~/.gemini/config/skills`). Antigravity uses the same directory-of-skill-folders standard as OpenCode and Bob, so the same 13 skill folders are copied verbatim.

**Usage:**
```bash
python3 scripts/sync_antigravity_skills.py           # Sync
python3 scripts/sync_antigravity_skills.py --dry-run # Preview
```

**Environment variables:**
- `ANTIGRAVITY_SKILLS` — Override destination (default: `~/.gemini/config/skills`)

## What Gets Synced

### Skills

All 13 skills from the repository (synced to OpenCode, Bob, and Antigravity):
- **2 Agent Session Management**: end-session, init-session
- **2 Content Creation (LinkedIn)**: linkedin-post-writer, linkedin-image-prompts
- **2 Content Creation (Medium)**: medium-article-writer, medium-image-prompts
- **4 Development**: lean-coder, project-planner, repo-docs-publisher, ui-ux-designer
- **3 Learning**: author-chapter, create-learning-repo, generate-practice-exam

### Agents (OpenCode only)

- `orchestrator.md`, `executor.md` → `~/.config/opencode/agent/`

### Plugins (OpenCode only)

No plugins are currently maintained in this repository.

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
   ls ~/.bob/skills/
   ls ~/.gemini/config/skills/
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
Scripts automatically create destination directories if they don't exist. If you get permission errors, ensure you have write access to `~/.config/`, `~/.bob/`, and `~/.gemini/`.

### The Antigravity Destination Shares a Parent With Other Gemini Config
`~/.gemini/config/` is **not** a skills-only directory — it also holds `AGENTS.md`, `config.json`, `mcp_config.json`, `projects/`, and `sidecars/`, which belong to other Gemini tooling. `sync_antigravity_skills.py` therefore only ever removes an *individual* destination skill folder immediately before re-copying that one skill. Never add a "clean" step that deletes the whole `~/.gemini/config/skills/` directory or its parent `~/.gemini/config/` — doing so would destroy unrelated Gemini configuration.

### Override Destination Paths
Use environment variables to sync to custom locations:
```bash
OPENCODE_SKILLS=/custom/path python3 scripts/sync_opencode_skills.py
OPENCODE_AGENTS=/custom/path python3 scripts/sync_opencode_agents.py
BOB_SKILLS=/custom/path python3 scripts/sync_bob_skills.py
ANTIGRAVITY_SKILLS=/custom/path python3 scripts/sync_antigravity_skills.py
```

## Maintenance

- Scripts are maintained in `scripts/` directory of the repository
- Keep them in sync with the main `SKILLS`/`AGENTS` lists if new skills or agents are added
- Document any changes to the sync behavior in this README
