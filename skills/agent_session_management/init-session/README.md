# init-session

Restores full project context at the start of an agent session. Reads the rolling handoff log and delivers a concise briefing covering last session state and open items — so you can start working immediately without re-reading every file.

---

## Trigger phrases

| Input | Example |
|---|---|
| Slash command | `/init-session` |
| Natural language | "start session", "load handoff", "restore context", "what was I working on" |

---

## What it does

1. **Reads `.agent_docs/handoff.md`** (Unit I1) — the rolling session log written by `end-session`. If not found, reports the path and stops with instructions to run `end-session` first.
2. **Reads `AGENTS.md`** at the workspace root (Unit I2) — internalizes authoritative project rules (naming conventions, file paths, known gotchas) that take precedence over handoff content.
3. **Internalizes the handoff** (Unit I3) — loads the Project Summary, Session Log, Open Items, and Quick Reference into working context.
4. **Delivers a structured briefing** (Unit I4) — a compact session-initialized message with the project description, last session summary, and a checklist of open items.
5. **Checks for a stale/ambiguous handoff** (Unit I5) — hands back for confirmation only if the handoff is clearly outdated or self-contradictory; otherwise no gate fires.

The skill is **read-only** — it never modifies any files.

---

## Workflow

Structured as self-contained delegation-model units. The skill runs **fully automatically as a single read-and-report pass — there is no routine confirmation gate** (it writes nothing). The only hand-back is a *conditional* stop gate that fires solely when the handoff looks stale or internally contradictory. Shared conventions (the `.agent_docs/handoff.md` path/format, `AGENTS.md` precedence, the missing-content rule, the briefing format) are defined once in a shared-reference section and referenced by every unit.

```
Unit I1 — Locate & read the handoff (stops cleanly if absent)
Unit I2 — Read project rules (AGENTS.md, optional; overrides on conflict)
Unit I3 — Internalize handoff sections into working context
Unit I4 — Deliver the structured briefing
Unit I5 — Stale/ambiguous handoff check (conditional STOP GATE only)
```

Each unit carries a Goal/scope, Inputs, Do, Self-verify, and a terse Report contract. Every read/load unit self-verifies that it actually found and loaded the expected content, reporting cleanly rather than failing when something is missing.

**Output format:**

```
## Session Initialized

**Project:** <one-line description>

**Last session (<date>):** <what was done and what state it was left in>

**Open items carrying over:**
- [ ] <item>
- [ ] <item>

**Ready.** <next logical action>
```

---

## Inputs

| Input | Required | Description |
|---|---|---|
| `.agent_docs/handoff.md` | Yes | Written by `end-session`. Must exist at the workspace root. |
| `AGENTS.md` | Optional | If present, its rules override handoff content on conflicts. |

---

## Outputs

A session briefing message in the conversation. No files are written or modified.

---

## Limitations

- **Requires a prior `end-session` run.** If `.agent_docs/handoff.md` does not exist, the skill stops and tells you to create it first.
- **Context depth is bounded by the handoff.** The skill only knows what `end-session` captured — it does not independently re-read the entire codebase.
- **Rolling 2-session window.** Handoff logs retain the last two sessions. Work older than two sessions is not surfaced unless it appears in the Project Summary.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global — available in all projects (Linux/macOS)
cp -r agent_session_management/init-session ~/.config/opencode/skills/

# Per-project only
cp -r agent_session_management/init-session .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse agent_session_management\init-session "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a named section |
| **Cursor** | Paste into `.cursor/rules/init-session.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your opening message |

---

## Companion skill

Use **`end-session`** at the end of every session to write the handoff that this skill reads.
