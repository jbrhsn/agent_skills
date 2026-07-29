# Plugins

OpenCode plugins that shape how the agent behaves at the tool and session level — the runtime counterpart to the skills in this repo. Where a skill is a prompt the agent loads and follows, a plugin hooks directly into OpenCode's execution flow (before/after tool calls, session compaction) to enforce behavior the agent can't opt out of.

---

## What's here

| Plugin | What it does |
|---|---|
| [**token-guard.ts**](./token-guard.ts) | Keeps large tool output from flooding the agent's context window — truncates oversized `bash`/`webfetch` output, blocks whole-file dump commands, and forces terse session-compaction summaries |

---

## token-guard.ts

A "token guard" for the agent's context window. Large command output, fetched pages, and verbose compaction summaries quietly burn context; this plugin caps that spend without disrupting the tool-result flow.

It exposes one configurable option, `maxOutputChars` (default `4000`), and installs three hooks.

### The three hooks

- **`tool.execute.after` — truncate large output.** When a `bash` or `webfetch` result exceeds `maxOutputChars`, it is truncated with a **head+tail** strategy: the budget is split in half, keeping the head (command context) and the tail (errors/stack traces), with the elision marked as `...[truncated N chars]...`. The `read` tool is deliberately **not** truncated (see design notes).
- **`tool.execute.before` — block whole-file dumps.** Bash commands that dump entire files or streams into context are rejected before they run. A deliberately broad regex matches `cat`, `less`, `more`, `tail`, and `head` — allowing a leading path, pipes, and pagers so it isn't trivially bypassed — and throws an error telling the agent to use the `read` tool with an offset/limit or `grep` for targeted lookups instead.
- **`experimental.session.compacting` — terse continuation summaries.** Replaces the compaction prompt so continuation summaries stay decision-focused. The summary must cover only: the current task and its status, key decisions and why, files touched with a one-line description each, and any pending verification. It explicitly **excludes** raw command output, full diffs, full file contents, and logs.

All three hooks are defensively wrapped so the guard never disrupts the normal tool-result flow — if anything goes wrong inside the guard, the tool result passes through untouched.

### Configuration

`maxOutputChars` defaults to `4000` and is overridable per-project via the tuple form of the `plugin` entry in `opencode.json`. The tuple form `["./path/to/plugin.ts", { ...options }]` passes options; the plain string form `"./path/to/plugin.ts"` uses defaults.

Dropping `token-guard.ts` into `.opencode/plugin/` alone loads it with **default** options (`maxOutputChars` 4000). To **override** options you must add the tuple entry to the `plugin` array in `opencode.json`.

Here is the complete minimal `opencode.json` that registers token-guard with `maxOutputChars` overridden to 8000 (this repo's actual file):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    ["./.opencode/plugin/token-guard.ts", { "maxOutputChars": 8000 }]
  ]
}
```

> OpenCode loads config only at startup, so restart opencode after editing `opencode.json` or the plugin.

### Design notes

- **Why `read` is excluded from truncation.** OpenCode's built-in `read` tool already truncates and spools full output to a file for offset/`grep` re-reads. Hard-slicing its output a second time here would break the "read a larger window" workflow, so `read` is left alone — only `bash` and `webfetch` are truncated.
- **Why the dump regex is broad.** Matching a leading path, pipes, and pagers keeps the block from being trivially bypassed, while still leaving small explicit reads (via the `read` tool) available.

---

## Install / usage

OpenCode loads plugins from `.opencode/plugin/` and via the `plugin` array in `opencode.json`. To use a plugin here:

- **Per-project (simple):** copy the file into your project's `.opencode/plugin/` directory. OpenCode picks it up automatically with **default** options (`maxOutputChars` 4000).

  ```bash
  cp plugins/token-guard.ts .opencode/plugin/
  ```

- **With options:** to override defaults, register it in `opencode.json`'s `plugin` array using the tuple form. The complete minimal file is:

  ```json
  {
    "$schema": "https://opencode.ai/config.json",
    "plugin": [
      ["./.opencode/plugin/token-guard.ts", { "maxOutputChars": 8000 }]
    ]
  }
  ```

Either way, OpenCode loads config only at startup — restart opencode after editing `opencode.json` or the plugin.

Consult the [OpenCode plugin documentation](https://opencode.ai/docs/) for the authoritative loading and configuration details for your version.
