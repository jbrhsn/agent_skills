# init-session

> Rebuild full project context at the start of any work session — reads the handoff log and project docs, runs an alignment check, and produces a concise operational briefing. Read-only; never modifies project code.

---

## When to use

**Trigger phrases** — say one of these to activate this skill:

```
"Start a new session"
"Init session"
"Where did we leave off?"
"Reload context"
"Catch me up on this project"
"/init-session"
```

**Conditions where this skill applies:**
- You're beginning a new work session and want to resume from the last known state
- You're picking up a project you haven't touched in days or weeks
- A new agent is taking over and needs to get oriented quickly

**Do NOT use this skill when:**
- You want to make code changes (orientation first, then work)
- You want a handoff written (use `end-session` for that)

---

## How it works

This skill runs in 5 phases:

| Phase | Name | What happens |
|---|---|---|
| 1 | Read baseline docs | Reads handoff log, README, and AGENTS.md in parallel |
| 2 | Alignment check | Verifies the three docs tell a consistent story |
| 3 | Escalation (if needed) | Runs git + targeted file checks only if docs disagree |
| 4 | Briefing | Outputs a structured summary: progress, state, open issues, next steps |
| 5 | .gitignore hygiene | Adds agent reference files to .gitignore if missing |

No confirmation gates — the entire skill runs in one response.

---

## Example

**You say:**
```
Init session — I'm picking up the API redesign work.
```

**Agent does:**
```
Phase 1: Reads .agent_docs/handoff.md, README.md, and AGENTS.md in parallel.

Phase 2: Runs alignment check — all 5 checks pass. Docs are aligned.

Phase 4: Produces briefing:
  - Overall progress: 3 bullets from rolling summary
  - Project state: currently mid-Phase 2, auth endpoints complete
  - Last session: "Implemented POST /login and POST /refresh; deferred rate limiting"
  - Open issues: none (docs aligned)
  - Next steps: 1) Add rate limiting to /login  2) Write integration tests

Phase 5: Checks .gitignore — AGENTS.md already listed, no change needed.
```

**Result:**
You have a complete picture of where the project stands in under 30 seconds. The agent is ready to start work immediately.

---

## Customization

**To point the skill at a different handoff file location:**
Edit Phase 1 Step 1 in `SKILL.md` — change `.agent_docs/handoff.md` to wherever your handoff lives (e.g. `PROGRESS.md`, `docs/handoff.md`).

**To add more baseline docs to the alignment check:**
Add rows to the Phase 2 alignment table in `SKILL.md`. Any doc you add will be read in Phase 1 and checked in Phase 2.

**To suppress the .gitignore update:**
Remove Phase 4 from `SKILL.md` if your team manages `.gitignore` manually and doesn't want auto-additions.

**To install globally** (available in all your projects):
```bash
cp -r agent_skills/scaffolding/init-session ~/.config/opencode/skills/
```

**To install per-project** (available only in the current project):
```bash
cp -r agent_skills/scaffolding/init-session .opencode/skills/
```

---

## Related skills

| Skill | How it complements this one |
|---|---|
| [scaffolding/end-session](../end-session/README.md) | Use at the end of every session to write the handoff that `init-session` will read next time |
| [scaffolding/create-learning-repo](../create-learning-repo/README.md) | After scaffolding a repo, use `init-session` at the start of each content-authoring session |

---

## Known limitations

- **Requires a maintained handoff log.** If `.agent_docs/handoff.md` doesn't exist or was never written, the briefing falls back to README + AGENTS.md only — which may be stale.
- **Read-only scope.** The skill does not verify that described files actually exist on disk unless docs disagree. For a deeper audit, run `git status` manually after the briefing.
- **Does not resolve conflicts.** If docs are misaligned, the skill flags the discrepancies — it does not fix them. You need to correct the stale doc yourself.
