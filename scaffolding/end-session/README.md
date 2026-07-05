# end-session

> Write a high-signal handoff at the end of any work session — a refreshed rolling project summary plus a detailed session entry — so any agent or human can resume exactly where you left off.

---

## When to use

**Trigger phrases** — say one of these to activate this skill:

```
"End session"
"Wrap up"
"Write a handoff"
"Save my progress"
"Log what we did today"
"I'm done for today"
"/end-session"
```

**Conditions where this skill applies:**
- You're finishing a work session and want to preserve context for next time
- You made decisions or encountered issues that a future agent should know about
- You want a clean record of what changed before closing out

**Do NOT use this skill when:**
- You want to commit or push code (this skill only writes the handoff file)
- You're in the middle of a session and just want a quick status — use `init-session` to read state

---

## How it works

This skill runs in 4 phases:

| Phase | Name | What happens |
|---|---|---|
| 1 | Inspect repo | Runs `git status`, `git diff`, `git log` to ground the handoff in evidence |
| 2 | Read existing handoff | Reads `.agent_docs/handoff.md` to preserve continuity (creates it if missing) |
| 3 | Write updated handoff | Rewrites the rolling summary; appends a new detailed session entry |
| 4 | Confirm | Prints a one-line confirmation of what was written |

No confirmation gates — runs in one response and produces the file.

---

## Example

**You say:**
```
End session — we implemented the rate limiter and deferred the Redis migration.
```

**Agent does:**
```
Phase 1: Runs git status, git diff --stat, git log.
         Sees: 3 files changed, rate-limiter.ts added, tests updated.

Phase 2: Reads .agent_docs/handoff.md.
         Finds existing rolling summary and last session entry.

Phase 3: Rewrites rolling summary:
         "Now: rate limiter complete; Redis migration deferred to next session."
         Appends new entry for today with:
         - Completed: rate-limiter.ts, updated integration tests
         - Decisions: used in-memory store as interim (Redis deferred — too risky before deploy)
         - Next steps: 1) Redis migration  2) Load test rate limiter under prod traffic

Phase 4: "Handoff written: rolling summary updated to 'rate limiter complete';
          session entry logged for 2026-07-05."
```

**Result:**
`.agent_docs/handoff.md` is updated. The next session starts with `init-session` and gets a complete briefing instantly.

---

## Customization

**To change the handoff file location:**
Edit Phase 2 in `SKILL.md` — change `.agent_docs/handoff.md` to your preferred path (e.g. `PROGRESS.md`). Make sure `init-session` is updated to match.

**To add custom sections to the detailed entry:**
Edit the detailed entry template in Phase 3 of `SKILL.md`. Add rows to the template — e.g. `### Architecture decisions` or `### Metrics / benchmarks`.

**To enforce stricter next-action sourcing:**
The next-action sourcing rule in Phase 3 is already strict. You can add a note to your team in `AGENTS.md` reminding contributors of the rule, so all agents on the project follow the same standard.

**To install globally** (available in all your projects):
```bash
cp -r agent_skills/scaffolding/end-session ~/.config/opencode/skills/
```

**To install per-project** (available only in the current project):
```bash
cp -r agent_skills/scaffolding/end-session .opencode/skills/
```

---

## Related skills

| Skill | How it complements this one |
|---|---|
| [scaffolding/init-session](../init-session/README.md) | Reads the handoff that `end-session` writes — use at the start of every session |
| [scaffolding/create-learning-repo](../create-learning-repo/README.md) | After scaffolding a repo, use `end-session` at the end of each content-authoring session |

---

## Known limitations

- **Does not commit or push.** The handoff file is written to disk but not staged or committed. You need to include it in your next commit manually, or add `.agent_docs/` to your tracked files.
- **Git-dependent accuracy.** Phase 1 relies on `git diff` and `git log`. If changes are not tracked by git (e.g. files in `.gitignore`), they won't appear in the diff and may be missed.
- **Rolling summary can drift.** If `end-session` is skipped for several sessions (e.g. agent crashes, session abandoned), the rolling summary will be out of date. Run `end-session` retroactively with session notes in `$ARGUMENTS` to recover.
