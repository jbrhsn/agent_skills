# Skill Name

> One-sentence value proposition — what problem does this skill solve for a developer using an AI coding agent?

---

## When to use

**Trigger phrases** — say one of these (or something close) to activate this skill:

```
"[Exact example trigger phrase 1]"
"[Exact example trigger phrase 2]"
"[Exact example trigger phrase 3]"
```

**Conditions where this skill applies:**
- [Situation 1]
- [Situation 2]

**Do NOT use this skill when:**
- [Misfire scenario 1 — what looks similar but isn't]
- [Misfire scenario 2]

---

## How it works

This skill runs in [N] phases:

| Phase | Name | What happens |
|---|---|---|
| 0 | Intake | Agent asks [N] questions to understand context |
| 1 | [Phase name] | [One-line description] |
| 2 | [Phase name] | [One-line description] |
| N | [Phase name] | [One-line description — final output] |

Each phase ends with a confirmation gate — the agent shows you output and waits before proceeding.

---

## Example

**You say:**
```
[Realistic example prompt from a developer]
```

**Agent does:**
```
Phase 0: Asks clarifying questions about [X, Y, Z]

Phase 1: [Describes what it produces — e.g. "Generates a list of..."]

Phase 2: [Describes what it produces — e.g. "Creates files at..."]

Final output: [What the user ends up with]
```

**Result:**
[2–3 sentence description of the concrete outcome — what exists that didn't before, what problem is solved.]

---

## Customization

**To adapt this skill for your context:**

1. **[Common customization 1]:** [How to do it — e.g. "Edit the Phase 1 prompt block to include your team's specific standards."]
2. **[Common customization 2]:** [How to do it.]
3. **[Common customization 3]:** [How to do it.]

**To install globally** (available in all your projects):
```bash
cp -r agent_skills/[category]/[skill-name] ~/.config/opencode/skills/
```

**To install per-project** (available only in the current project):
```bash
cp -r agent_skills/[category]/[skill-name] .opencode/skills/
```

---

## Related skills

| Skill | How it complements this one |
|---|---|
| [[category/skill-name]](../../[category]/[skill-name]/README.md) | [One sentence: use X before/after/alongside this skill because...] |
| [[category/skill-name]](../../[category]/[skill-name]/README.md) | [One sentence.] |

---

## Known limitations

- **[Limitation 1]:** [What the skill doesn't handle and why — be honest and specific.]
- **[Limitation 2]:** [Where human judgment is still required.]
- **[Limitation 3]:** [Edge case or context where the skill may produce suboptimal results.]
