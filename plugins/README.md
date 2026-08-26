# Plugins

Optional OpenCode plugins. Each one bundles a **runtime tool** with the **agent
instructions** that tell agents how to use it responsibly — installed together,
as one unit, or not at all.

Skills and base agents sync by default. Plugins never do: you opt in per sync
with `--plugins`.

## Available

| Plugin | What it adds |
|---|---|
| [`search-internet`](search-internet/) | `web_search_tool` — live web search via Tavily → Firecrawl → self-hosted fallback, plus a `researcher` subagent that keeps raw results out of the orchestrator's context |

```bash
uv run scripts/sync_all.py --list-plugins
```

## Installing

```bash
# preview
uv run scripts/sync_all.py --opencode-only --plugins search-internet --dry-run

# install, then assert OpenCode resolved the agents as composed
uv run scripts/sync_all.py --opencode-only --plugins search-internet --verify

# uninstall: omit the flag — the plugin's files are pruned automatically
uv run scripts/sync_all.py --opencode-only
```

## How agent composition works

The base agents in [`agents/`](../agents/) are canonical and are **never edited by a
plugin**. A plugin instead ships small *overlays* that are merged into a base agent
in memory at sync time:

```
plugins/<name>/
├── plugin.json                  # manifest: runtime files, overlays, new agents, env
├── plugin/<tool>.js             # the OpenCode tool itself
└── agents/
    ├── overlays/<agent>.md      # frontmatter delta + a section appended to that base agent
    └── <new-agent>.md           # net-new agent, copied verbatim
```

- **Frontmatter** is deep-merged into the base agent's.
- **Body** is appended as a titled `## Capability: <plugin>` section — never spliced
  into the middle. The base can be rewritten freely without breaking overlays.
- Composition is **order-independent** (plugins apply sorted). If two plugins set the
  same key to different values, the sync **fails loudly** rather than silently picking
  one — permissions are security-relevant.
- Nothing composed is written back into the repo; merged files exist only in
  `~/.config/opencode/agent/`.

### Why runtime and overlays install together

A plugin-provided tool is **allowed by default in every agent** unless a permission
explicitly denies it (verified against OpenCode 1.18.23). So installing a tool without
its overlays would silently hand it to the orchestrator — exactly the context blowout
the `researcher` delegation pattern exists to prevent. `--plugins` therefore drives
both halves; running the plugin sync alone prints a warning.

## Uninstall safety

Each destination directory gets a `.agent_skills_manifest.json` listing only the files
this tooling wrote. Pruning consults that manifest, so deselecting a plugin removes its
files and **never touches** anything you or another tool placed in
`~/.config/opencode/` — these are shared config directories, not ours alone.

## Adding a plugin

1. `mkdir -p plugins/<name>/{plugin,agents/overlays}`
2. Write the tool (see the [OpenCode plugin docs](https://opencode.ai/docs/plugins/)).
3. Write `plugin.json` declaring `runtime`, `agents.new`, and `agents.overlays`.
4. Add an overlay for each base agent whose behavior or permissions must change —
   in particular, **deny the tool on `orchestrator`** unless it is genuinely cheap.
5. `uv run scripts/sync_all.py --opencode-only --plugins <name> --dry-run`, then
   `--verify` on the real run.

Manifest paths are validated on every sync: a missing file or an overlay targeting a
non-existent base agent fails immediately.
