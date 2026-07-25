# Sync Scripts

Automated scripts to sync skills from this repository to global OpenCode and IBM Bob configurations.

## Scripts

### `sync_all.py` (Recommended)
Syncs skills to both OpenCode and IBM Bob configurations in one command.

**Usage:**
```bash
python3 scripts/sync_all.py                # Sync to both
python3 scripts/sync_all.py --dry-run      # Preview before syncing
python3 scripts/sync_all.py --opencode-only # Sync only to OpenCode
python3 scripts/sync_all.py --bob-only     # Sync only to Bob
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

All 19 skills from the repository:
- **7 Content Creation**: carousel-builder, content-tracker, draft-builder, editorial-reviewer, linkedin-writer, medium-imager, medium-writer
- **3 Learning**: author-chapter, create-learning-repo, generate-practice-exam
- **4 Development**: lean-coder, project-planner, repo-docs-publisher, ui-ux-designer
- **2 Agent Management**: end-session, init-session
- **3 Other**: seed-expander, tutorial-verifier, voice-profiler

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
4. **Verify installation** in both locations:
   ```bash
   ls ~/.config/opencode/skills/
   ls ~/.bob/skills/
   ```

## Environment Setup

### For Development
Edit skills directly in this repository, then sync.

### For Users
After syncing, skills are available in:
- OpenCode: `~/.config/opencode/skills/`
- IBM Bob: `~/.bob/skills/`

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
BOB_SKILLS=/custom/path python3 scripts/sync_bob_skills.py
```

## Maintenance

- Scripts are maintained in `scripts/` directory of the repository
- Keep them in sync with the main SKILLS list if new skills are added
- Document any changes to the sync behavior in this README
