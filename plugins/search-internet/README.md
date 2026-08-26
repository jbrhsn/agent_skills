# search-internet

Live web search for OpenCode agents, exposed as the **`web_search_tool`** tool, with a
multi-tier fallback chain and a `researcher` subagent that keeps raw search output out
of the orchestrator's context window.

## Install

```bash
# from the repo root
uv run scripts/sync_all.py --opencode-only --plugins search-internet --verify
```

This installs, as one unit:

| File | Destination |
|---|---|
| `plugin/web-search.js` | `~/.config/opencode/plugin/` |
| `researcher.md` (net-new agent) | `~/.config/opencode/agent/` |
| overlays merged into `orchestrator` / `executor` / `ask` | `~/.config/opencode/agent/` |

To uninstall, sync without the flag — the plugin's files are pruned automatically:

```bash
uv run scripts/sync_all.py --opencode-only
```

## Fallback chain

```
web_search_tool(query)
        │
        ├─ in-memory cache (10 min TTL, max 200 entries)
        │
        ├─ Tier 1: Tavily  ⇄  Firecrawl v2      ← order randomized per call;
        │                                          if one fails, the other is tried
        └─ Tier 2: local tavily-open            ← SearXNG + Crawl4AI, self-hosted
                   POST {TAVILY_OPEN_URL}/tavily/search
```

Result snippets are capped at 1,500 characters each to bound context cost.

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `TAVILY_API_KEY` | Tavily cloud search | — |
| `FIRECRAWL_API_KEY` | Firecrawl v2 cloud search | — |
| `TAVILY_OPEN_URL` | Self-hosted fallback base URL | `http://localhost:8000` |

Keys are read from `process.env` first, then from `~/.secrets` (`export KEY="..."` or
plain `KEY=...` lines). At least one cloud key **or** a running local instance is
required. Optional local fallback:

```bash
git clone https://github.com/jianjungki/tavily-open.git
cd tavily-open && docker compose up -d
```

## The subagent pattern

> **Web search runs inside a subagent. Only synthesized findings reach the orchestrator.**

Raw search output is bulky — markdown extracts, boilerplate, URLs. Injecting it straight
into a primary agent degrades multi-turn reasoning and triggers early context compaction.
So responsibilities split: the **orchestrator** decides *what* needs investigating; the
**researcher** executes the search, filters the noise, and returns a short brief.

The plugin enforces this through permissions rather than convention:

| Agent | `web_search_tool` | Why |
|---|---|---|
| `orchestrator` | **deny** | Protects planning context; must delegate to `researcher` |
| `researcher` | allow | Dedicated research subagent — searches, filters, returns a brief |
| `executor` | allow | Targeted lookups for cryptic third-party errors, incidental to its task |
| `ask` | allow | Conversational Q&A about things outside the repo |

**The `deny` on `orchestrator` is the load-bearing one.** Plugin-provided tools are
*allowed by default* in every agent, so without that overlay the orchestrator would
silently gain the tool. This is why the runtime file and the overlays install together.

Verify the resolved state at any time:

```bash
opencode debug agent orchestrator   # → tools.web_search_tool: false
opencode debug agent researcher     # → tools.web_search_tool: true
```

## Tool reference

**`web_search_tool`**

| Arg | Type | Notes |
|---|---|---|
| `query` | string, required | The search query |
| `max_results` | number, optional | Clamped to 1–10, default 5 |

Returns formatted text: provider, query, optional synthesized answer, numbered results
(title / URL / truncated content), and credit usage.

## Layout

```
search-internet/
├── plugin.json                     # manifest consumed by the sync scripts
├── plugin/web-search.js            # the OpenCode tool
├── agents/
│   ├── researcher.md               # net-new subagent
│   └── overlays/
│       ├── orchestrator.md         # denies the tool, permits the researcher subagent
│       ├── executor.md             # permits targeted lookups
│       └── ask.md                  # permits conversational search
└── README.md
```

See [../README.md](../README.md) for how overlay composition works in general.

## Requirements

`@opencode-ai/plugin` must be resolvable from `~/.config/opencode/`. Verified against
OpenCode 1.18.23 with `@opencode-ai/plugin` 1.18.11.
