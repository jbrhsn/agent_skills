# Agents

OpenCode agent definitions covering two modes of working with this repo: a
read-only **ask** agent for conversational exploration, and a **plan-and-delegate**
pair — a primary **orchestrator** that decomposes a request and delegates every
unit of work to parallel **executor** subagents, each of which implements *and
verifies* its piece before reporting back.

Each file is an OpenCode agent definition — a Markdown file with YAML
frontmatter (mode + permissions) followed by the agent's prompt body.

The orchestrator/executor pair mirrors each other's safety model: the
orchestrator can't edit or run bash at all (it only plans and delegates), and
the executor — which *does* have edit and bash access — gates dangerous
commands behind `ask` or `deny`, plus stays inside the file scope it was
assigned so parallel executors can't collide. `ask` is read-only end to end —
no edit, bash, or task/delegate access at all.

---

## Agents

| Agent | Mode | Role |
|---|---|---|
| [**ask**](./ask_mode_agents/ask.md) | `primary` | Read-only conversational agent for repo exploration and questions |
| [**orchestrator**](./orchestrator_mode_agents/orchestrator.md) | `primary` | Decomposes tasks and delegates all work to executor subagents in parallel |
| [**executor**](./orchestrator_mode_agents/executor.md) | `subagent` | Implements, runs, and verifies a unit of work end-to-end |

---

## ask

> Read-only conversational agent for repo exploration and questions.

- **Mode:** `primary`
- **Step limit:** `steps: 10`
- **Key permissions:** `read`, `grep`, `glob`, `webfetch` allowed; `edit`, `bash`,
  `task` all denied — it can look and talk, nothing else.

Answers questions about this repo (and general knowledge) by searching and
reading, never by acting. Cites findings as `path/to/file:line` so answers are
navigable, asks for clarification instead of guessing when a reference is
ambiguous, and — when asked to edit, run, or delegate — says so plainly and
offers the closest thing it can actually do (drafting the change, explaining
what a test should check) while pointing to orchestrator/executor mode for the
part it can't perform.

---

## orchestrator

> Decomposes tasks and delegates all work to executor subagents in parallel.

- **Mode:** `primary`
- **Step limit:** `steps: 20`
- **Key permissions:**
  - `edit: deny` — never edits files itself
  - `bash: deny` — never runs commands itself
  - `task: "*": deny` with `executor: allow` — may only delegate to the `executor` subagent, no other subagents

The orchestrator **NEVER** writes code, edits files, or runs bash itself. It
only plans and delegates to the executor subagent via the task tool. It may
`read`, `grep`, and `glob` to understand the codebase well enough to plan, but
only enough to scope the work — it doesn't read files end-to-end, since an
executor will read whatever it needs anyway. All changes and verification are
done by executors.

**Workflow:**

1. Break the user's request into independent units of work. Fewer, larger units
   beat many small ones — split further only when it buys real parallelism, not
   just because a task *could* be divided.
2. Dispatch independent units to the executor subagent **in parallel** — calling
   task multiple times in one turn when units don't depend on each other.
   Dependent units are dispatched sequentially, one after the last completes.
   At most **4 executors** run concurrently; if there are more independent units
   than that, they're dispatched in waves.
3. Give each executor a **self-contained** task: the goal, the specific files it
   already identified while planning (so the executor isn't rediscovering them),
   an **explicit scope boundary** (which files/directories it may touch — never
   overlapping between two concurrently-dispatched executors), and how to
   verify. Executors do not share memory with each other.
4. Each executor returns **only** a short structured summary — files changed,
   what it verified (e.g. tests run and result), and pass/fail. Executors are
   never asked to paste raw command output, diffs, or logs.
5. On failure — or when verification looks insufficient — send a targeted
   follow-up task describing the specific problem, not the whole log.
6. Once all units are done and verified, give the user a **concise final
   summary**: what was done, what was verified, what's pending.

The orchestrator never tells the user something is "done" without an executor
confirming it verified the change (ran tests, checked the diff, or confirmed the
build succeeds).

---

## executor

> Implements, runs, and verifies a unit of work end-to-end.

- **Mode:** `subagent`
- **Step limit:** `steps: 20`
- **Key permissions:**
  - `edit: allow` — may edit files
  - `bash: "*": allow` — may run commands, with these gated:

    | Command pattern | Gate |
    |---|---|
    | `rm -rf *`, `rm -fr *` | `ask` |
    | `git push*` | `ask` |
    | `git reset --hard*` | `ask` |
    | `git clean*` | `ask` |
    | `git checkout -- *`, `git restore *` | `ask` |
    | `git branch -D*` | `ask` |
    | `curl * \| *`, `wget * \| *` | `ask` |
    | `* \| sh`, `* \| bash` | `ask` |
    | `sudo *` | `ask` |
    | `chmod -R *` | `ask` |
    | `dd *` | `ask` |
    | `mkfs*` | `ask` |
    | `:(){*` (fork bomb) | `deny` |

The executor implements a complete unit of work end-to-end — makes the change,
then **verifies it itself** before reporting back:

- **Stays inside its assigned scope.** Other executors may be running against
  the same working tree in parallel; it only touches the files/directories its
  task named, and if it finds changes it didn't make (another executor's scope
  overlapping) or finishing needs going outside scope, it stops and reports
  rather than pushing through.
- Verifies using whatever the project actually supports — runs the relevant
  tests, build, or lint if they exist, and inspects the diff.
- If the project has no such tooling (e.g. a docs- or config-only repo), it
  verifies by inspection against the task's stated requirements.
- **Never claims success without having actually checked.** If it's approaching
  its step limit before finishing, it reports honest partial progress instead
  of rushing an unverified claim.

When done, it responds with **only** a terse summary:

- files changed (one line each, what changed and why)
- what it verified and the result (e.g. "ran test suite: 42 passed", or "no
  tests in repo; verified by re-reading the edited sections")
- pass/fail

It does not paste file contents, command output, or diffs back — the
orchestrator only needs the summary. If verification fails, the executor fixes
it itself when the fix is obvious and in scope; otherwise it reports the
specific failure concisely.

---

## How they work together

The orchestrator is the planner; the executor does and verifies the work.

1. The **orchestrator** reads the codebase enough to plan, then splits the
   request into units and dispatches them to **executor** subagents — in
   parallel where independent (up to 4 at a time), sequentially where dependent.
2. Each **executor** implements its self-contained unit, verifies it, and
   returns a terse structured summary.
3. The **orchestrator** aggregates those summaries, sends targeted follow-ups
   for any failures, and only reports "done" once executors have confirmed
   verification.

The safety model is split across the pair: the orchestrator holds no
edit/bash power at all, and the executor — which does — keeps destructive
commands behind `ask` or `deny`.

---

## Install / usage

**Preferred: use the sync script.** It copies every `agents/*/*.md` file (flattened,
`README.md` excluded) to the OpenCode agent directory and is the source of truth
for the correct destination:

```bash
uv run scripts/sync_opencode_agents.py            # → ~/.config/opencode/agent/
uv run scripts/sync_opencode_agents.py --dry-run   # preview only
```

Set `OPENCODE_AGENTS` to sync somewhere else (e.g. a per-project `.opencode/agent/`).

### Plugin overlays

The three agents below are the **base** definitions and are always what syncs by
default. An optional plugin (see [`plugins/`](../plugins/)) may ship *overlays* that
extend them — adding a permission and appending a `## Capability: <plugin>` section —
plus net-new agents of its own. Overlays are merged in memory at sync time; the files
in this directory are never modified by a plugin.

```bash
uv run scripts/sync_opencode_agents.py --plugins search-internet --verify
uv run scripts/sync_opencode_agents.py --plugins search-internet \
    --print-composed orchestrator     # see the merged result, write nothing
```

Because a plugin's tool is available to every agent unless explicitly denied, an
overlay that denies it on `orchestrator` is part of the safety model described above —
which is why plugin runtime files and overlays always install together.

**Manual copy**, if you'd rather not run the script — note the files live one
level deeper than `agents/`, under `orchestrator_mode_agents/` and
`ask_mode_agents/`. Run from the **repo root** (`agent_skills/`):

```bash
# Global — available in all projects (Linux/macOS)
cp agents/orchestrator_mode_agents/orchestrator.md \
   agents/orchestrator_mode_agents/executor.md \
   agents/ask_mode_agents/ask.md \
   ~/.config/opencode/agent/

# Per-project only
cp agents/orchestrator_mode_agents/orchestrator.md \
   agents/orchestrator_mode_agents/executor.md \
   agents/ask_mode_agents/ask.md \
   .opencode/agent/
```

Once installed, OpenCode picks up `ask` and `orchestrator` as `primary` agents —
switch between them as entry points — and `orchestrator` delegates to the
`executor` subagent as it works.

---

## opencode.json

Agents in the `agent/` directory are **auto-discovered** — for the default
setup you do **not** need any `opencode.json` entry to register them. Simply
having `orchestrator.md`, `executor.md`, and `ask.md` present in the per-project
(`.opencode/agent/`) or global (`~/.config/opencode/agent/`) directory is
enough. For this reason, this repo's `.opencode/opencode.json` is typically not
needed for agents.

### Optional overrides

If you want to override an auto-discovered agent — or define one inline — you
can add an `agent` block to `opencode.json`. This is **optional** and only
needed for overrides. The snippet below is illustrative; keep only the keys you
actually need:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "orchestrator": {
      "mode": "primary"
    },
    "executor": {
      "mode": "subagent",
      "permission": {
        "edit": "allow",
        "bash": "ask"
      }
    }
  }
}
```

> **Restart required.** OpenCode loads config only at startup, so restart
> opencode after changing any agent file or `opencode.json`.
