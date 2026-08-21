# PRD spec

Write to `docs/prd.md`. Start from `assets/prd.template.md` — copy it, then fill it.
Do not compose the structure from memory; the template exists so the section set is
identical across projects.

The PRD does not reference `docs/uiux.md` yet — that file does not exist until Stage 6.
The plan link in the template header is enough at this point; leave the UIUX link out
rather than pre-writing a path that might change.

## Requirement IDs

- Functional: `FR-01`, `FR-02`, … Non-functional: `NFR-01`, … Constraints: `CON-01`, …
- IDs are permanent. When a requirement is removed, mark it `(removed)` and leave the ID
  in place — the plan files reference these IDs and renumbering silently breaks traceability.
- Two digits, zero-padded, so they sort correctly.

## Writing a requirement

Each line is one requirement, in this shape:

```
FR-03 | A user can retry a failed import without re-uploading the file.
        Verify: after a forced failure, the retry button re-runs the import and the
        original file is still available.
```

The `Verify` line is what makes the requirement testable. If you cannot write one, the
requirement is too vague — it belongs in Open Questions until the user pins it down.

**Good:** `NFR-02 | A 10,000-row import completes in under 5 seconds on the dev machine.`
**Bad:** `NFR-02 | The import should be fast.` — nothing to test against.

## Section rules

- **Problem and goal** — the user's words, tightened. Not a marketing paragraph.
- **Users and jobs** — who, and the job they hire this for. Skip personas.
- **Scope for v1** — the smallest shippable version. If the user described something
  larger, put the rest under Later, not v1.
- **Out of scope** — explicit. This section prevents scope arguments during the build.
- **Functional requirements** — grouped by area if there are more than ~8.
- **Non-functional requirements** — performance, security, reliability, accessibility.
  Only include ones the user actually cares about; a boilerplate NFR nobody will check
  is noise.
- **Technical constraints** — decided stack, required infra, forbidden choices. If the
  stack is open, say "open — to be decided in Phase 1" rather than picking one silently.
  In learn-by-building mode, the target language/framework is a constraint: record it here.
- **Data model sketch** — entities and relationships, prose or a list. No schemas, no DDL.
- **Success criteria** — how the user will know v1 worked.
- **Open questions** — everything unresolved, each with who needs to answer it.
- **Assumptions** — anything you inferred rather than asked. Keep this list short and
  honest; it is the record of where you filled a gap.

## Length

A v1 PRD for a solo project is typically 1–3 pages. If it is running longer, the scope
is too big for v1 — say so and propose cutting requirements to Later.
