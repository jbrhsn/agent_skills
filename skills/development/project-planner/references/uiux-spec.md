# UIUX spec

Write to `docs/uiux.md`, only after the PRD is approved. Start from the template variant
in `assets/uiux.template.md` that matches the surface type from Stage 0.

## Why this document exists

An agent handed "FR-04 | A user can retry a failed import" and nothing else will invent a
screen, invent the states that screen can be in, and invent a different set of both next
session. This document removes that freedom. It is the layer between *what the product
does* (PRD) and *when it gets built* (plan).

It is a **behavior specification, not a visual design**. No wireframes, no ASCII layouts,
no hex codes, no pixel values, no component library names, no code. If the user has strong
visual opinions, record them as constraints in prose ("dense table layout, not cards") and
move on. Anything you cannot state as observable behavior does not belong here.

## ID scheme

- Screens / pages / views: `SC-01`, `SC-02`, …
- Components: `CMP-01`, … (numbered globally, not per screen — a component reused on
  three screens keeps one ID)
- Conversation states or command surfaces: `CS-01`, …
- Flows: `FLOW-01`, …

Same permanence rule as the PRD: IDs never get renumbered. Removed items are marked
`(removed)` and left in place, because plan units cite them.

## Required structure — visual surfaces (web / mobile / desktop)

### 1. Surface summary
Two or three sentences: what kind of interface this is, the navigation model, and the
single most important thing the user does with it.

### 2. Requirement → surface map
A table, before any detail, so a reader can see coverage at a glance:

| Requirement | Where it surfaces |
|---|---|
| FR-01 | SC-02 (Import screen), CMP-03 (File picker) |
| FR-04 | SC-02, CMP-05 (Retry banner) |

Every FR with a user-facing effect appears here. An FR that surfaces nowhere is either
genuinely background work (say so explicitly in a note) or a hole in this document.

### 3. Screen inventory
One entry per screen, in the order a first-time user meets them:

```markdown
### SC-02 — Import
**Covers:** FR-01, FR-03, FR-04
**Reached from:** SC-01 (Dashboard) via the "New import" action
**Leads to:** SC-03 (Import result) on success; stays on SC-02 on failure

**Purpose**
One sentence: what the user accomplishes here.

**What's on it**
- CMP-03 — File picker
- CMP-04 — Preview table
- CMP-05 — Retry banner (conditional: only after a failed attempt)

**Screen states**
- **Empty** — no file chosen yet. Only the file picker is active; the import action is
  disabled.
- **Preview** — file parsed. Preview table shows the first 5 rows; import action enabled.
- **Working** — import running. Both the picker and the import action are disabled;
  progress is visible.
- **Error** — import failed. Retry banner appears with the reason; the chosen file is
  still held so the user does not re-upload.

**Not on this screen**
- Import history — SC-04.
```

### 4. Component inventory
One entry per component. This is where agentic code most often goes wrong, so each
component names **every state it can be in and what triggers each transition**:

```markdown
### CMP-05 — Retry banner
**Used on:** SC-02
**Covers:** FR-04

**Purpose**
One sentence.

**States**
| State | When it shows | What the user sees | What they can do |
|---|---|---|---|
| Hidden | No failed attempt in this session | — | — |
| Error | Import returned a failure | Failure reason in plain language | Retry, or dismiss |
| Retrying | Retry pressed | Banner stays, action disabled | Nothing until it resolves |

**Behavior rules**
- Dismissing does not clear the chosen file.
- A second failure replaces the message; it does not stack banners.

**Edge cases**
- Failure with no reason available → generic message, never a blank banner.
```

Cover, at minimum, for anything that fetches or submits: **default, loading, empty,
error, success, disabled**. Omit a state only when it genuinely cannot occur, and say why
in one line rather than leaving it out silently.

### 5. Flows
End-to-end paths across screens, including the unhappy ones:

```markdown
### FLOW-01 — First successful import
**Covers:** FR-01, FR-03
SC-01 → "New import" → SC-02 (Empty) → choose file → SC-02 (Preview) → confirm →
SC-02 (Working) → SC-03 (Result)

**Where it can break**
- File unparseable → SC-02 (Error), FLOW-02 picks up from there.
```

At least one failure flow. A UIUX doc with only happy paths is the thing this document
exists to prevent.

### 6. Cross-cutting rules
Only what the user actually stated or confirmed:
- Responsive / breakpoint expectations (web), or platform conventions (mobile/desktop)
- Accessibility floor — keyboard reachability, focus visibility, contrast, labels
- Loading convention — spinner vs skeleton vs blocking, applied consistently
- Error message tone and where errors appear (inline vs banner vs toast)
- Empty-state convention — what a fresh install looks like before any data exists

### 7. Open questions
Same rule as the PRD. An unanswered interaction detail is an open question, never a
silently invented state.

## Required structure — conversational surfaces (CLI / chatbot)

Same rigor, different vocabulary. Replace sections 3–5 with:

### 3. Command / intent inventory
One entry per command, intent, or input the system handles:

```markdown
### CS-02 — Import a file
**Covers:** FR-01
**Invoked by:** `import <path>` (CLI) / "import this file", "load my CSV" (chatbot)

**Inputs it needs**
- A file path. If absent, the system asks for it rather than failing.

**Responses**
| Situation | What comes back | Session state after |
|---|---|---|
| Valid file | Row count and first rows, then a confirm prompt | Awaiting confirmation |
| Path missing | A question asking for the path | Awaiting input |
| File unreadable | Reason plus a suggested fix | Idle |
| Already importing | Refusal explaining one import runs at a time | Unchanged |

**Behavior rules**
- Never partially imports and reports success.
```

### 4. Session state model
The states a session can be in (idle, awaiting input, working, errored), what moves it
between them, and what survives across turns versus what resets. Agentic code gets
conversational state wrong constantly — this section is the fix.

### 5. Turn flows
A sample session as an ordered turn list — user turn, system turn, resulting state — plus
at least one session that goes wrong and recovers. Sample text is illustrative wording,
not fixed copy; say so.

Also include, in place of section 6: output formatting conventions (plain text, tables,
structured output), verbosity levels, whether output is expected to be machine-parseable,
and what a non-interactive/piped invocation does differently.

## Required structure — headless

A short **interaction contract**. Sections 1, 2, 6, 7 as above, and in place of 3–5:

### 3. Interface inventory
One entry per public entry point (function, endpoint, CLI flag, queue topic, event):

```markdown
### CS-01 — Trigger an import
**Covers:** FR-01
**Called by:** the scheduler, or a manual invocation

**Takes**
A file location and an import mode, described in plain terms — no schema, no types.

**Returns**
An outcome plus a count of rows accepted and rejected.

**Failure behavior**
| Failure | What the caller gets | Side effects |
|---|---|---|
| Source unreachable | A retryable error | None; nothing partially written |
| Malformed rows | Success with a rejected-row count | Good rows written |
```

Keep it to what a caller must know to use it correctly. Two pages is plenty.

## Length

Visual surfaces: typically 2–5 pages for a v1. Conversational: 2–4. Headless: 1–2. If a
visual UIUX doc is running past 8 pages, v1 has too many screens — say so and propose
moving screens to the PRD's Later section rather than writing a longer document.

## Learning mode

No change to the structure. The curriculum in `learnings/` picks up UI/UX topics from
this document at Stage 9; do not put teaching material here.
