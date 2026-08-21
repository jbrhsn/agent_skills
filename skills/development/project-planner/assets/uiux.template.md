Three variants in one file. Use the one matching the surface type from Stage 0 and
delete the rest. Output goes to `docs/uiux.md`.

---
# VARIANT A — visual surfaces (web / mobile / desktop)
---

# <Project name> — UI/UX Specification

**Status:** Draft | Approved
**Last updated:** <YYYY-MM-DD>
**Surface:** web | mobile | desktop
**PRD:** [prd.md](prd.md) · **Plan:** [plan/overview.md](plan/overview.md)

Behavior, not visuals. No wireframes, no colours, no measurements — this document says
what exists, what state it can be in, and what moves it between states.

## 1. Surface summary

<Two or three sentences: what kind of interface this is, the navigation model, and the
single most important thing a user does with it.>

## 2. Requirement → surface map

| Requirement | Where it surfaces |
|---|---|
| FR-01 | SC-02 (<name>), CMP-03 (<name>) |
| FR-02 | <…> |

<Note any FR that deliberately surfaces nowhere, and why.>

## 3. Screens

### SC-01 — <Screen name>
**Covers:** FR-01
**Reached from:** <entry point, or "app launch">
**Leads to:** <SC-0n on success; where it goes on failure>

**Purpose**
<One sentence: what the user accomplishes here.>

**What's on it**
- CMP-01 — <name>
- CMP-02 — <name> *(conditional: <when>)*

**Screen states**
- **<State>** — <what is true, what is active, what is disabled.>
- **<State>** — <…>

**Not on this screen**
- <Thing a reader would assume is here> — SC-0n.

---

### SC-02 — <Screen name>

<Same shape.>

## 4. Components

### CMP-01 — <Component name>
**Used on:** SC-01, SC-02
**Covers:** FR-01

**Purpose**
<One sentence.>

**States**

| State | When it shows | What the user sees | What they can do |
|---|---|---|---|
| Default | <…> | <…> | <…> |
| Loading | <…> | <…> | <…> |
| Empty | <…> | <…> | <…> |
| Error | <…> | <…> | <…> |
| Disabled | <…> | <…> | <…> |

**Behavior rules**
- <Rule that is not obvious from the state table.>

**Edge cases**
- <What happens at the boundary.>

---

### CMP-02 — <Component name>

<Same shape.>

## 5. Flows

### FLOW-01 — <Happy path name>
**Covers:** FR-01, FR-03
SC-01 → <action> → SC-02 (<state>) → <action> → SC-03

**Where it can break**
- <Failure> → <state>, picked up by FLOW-02.

---

### FLOW-02 — <Failure path name>

<Same shape. At least one failure flow is required.>

## 6. Cross-cutting rules

- **Responsive / platform:** <what the user stated>
- **Accessibility floor:** <keyboard reach, focus visibility, labels, contrast>
- **Loading convention:** <spinner | skeleton | blocking, applied where>
- **Error convention:** <inline | banner | toast, and tone>
- **Empty-state convention:** <what a fresh install shows>

## 7. Open questions

| # | Question | Who answers |
|---|---|---|
| 1 | <…> | <…> |

---
# VARIANT B — conversational surfaces (CLI / chatbot)
---

# <Project name> — Interaction Specification

**Status:** Draft | Approved
**Last updated:** <YYYY-MM-DD>
**Surface:** conversational (CLI | chatbot | voice)
**PRD:** [prd.md](prd.md) · **Plan:** [plan/overview.md](plan/overview.md)

## 1. Surface summary

<What kind of interface, how a session starts and ends, and the one thing it is for.>

## 2. Requirement → surface map

| Requirement | Where it surfaces |
|---|---|
| FR-01 | CS-02 (<command/intent>) |

## 3. Commands and intents

### CS-01 — <What the user is trying to do>
**Covers:** FR-01
**Invoked by:** `<command syntax>` / "<natural phrasing>", "<variant>"

**Inputs it needs**
- <Input> — <what happens if it is missing: ask, default, or refuse.>

**Responses**

| Situation | What comes back | Session state after |
|---|---|---|
| <Valid input> | <…> | <…> |
| <Missing input> | <…> | Awaiting input |
| <Invalid input> | <…> | <…> |
| <Wrong state> | <…> | Unchanged |

**Behavior rules**
- <Rule, especially anything about never partially succeeding.>

---

### CS-02 — <…>

<Same shape.>

## 4. Session state model

| State | Meaning | Entered by | Exits to |
|---|---|---|---|
| Idle | <…> | <…> | <…> |
| Awaiting input | <…> | <…> | <…> |
| Working | <…> | <…> | <…> |
| Errored | <…> | <…> | <…> |

**Persists across turns:** <…>
**Resets each turn:** <…>
**Persists across sessions:** <…>

## 5. Turn flows

### FLOW-01 — <Happy session>
1. User: <…> → system: <…> → state: <…>
2. <…>

### FLOW-02 — <Session that goes wrong and recovers>
<Same shape. Required.>

<Sample wording is illustrative, not fixed copy.>

## 6. Output and invocation conventions

- **Format:** <plain text | tables | structured output>
- **Verbosity:** <levels, and the default>
- **Machine-readable mode:** <flag/behavior, or "none">
- **Non-interactive / piped invocation:** <what differs>
- **Accessibility:** <screen-reader friendliness, colour independence>

## 7. Open questions

| # | Question | Who answers |
|---|---|---|
| 1 | <…> | <…> |

---
# VARIANT C — headless (library / API / pipeline)
---

# <Project name> — Interaction Contract

**Status:** Draft | Approved
**Last updated:** <YYYY-MM-DD>
**Surface:** headless
**PRD:** [prd.md](prd.md) · **Plan:** [plan/overview.md](plan/overview.md)

No end-user interface. This document is the contract a caller programs against, in plain
terms — no schemas, no type signatures, no code.

## 1. Surface summary

<What consumes this, and how.>

## 2. Requirement → surface map

| Requirement | Where it surfaces |
|---|---|
| FR-01 | CS-01 (<entry point>) |

## 3. Interfaces

### CS-01 — <Entry point name>
**Covers:** FR-01
**Called by:** <who or what, and when>

**Takes**
<What the caller supplies, described in plain terms.>

**Returns**
<What comes back on success.>

**Failure behavior**

| Failure | What the caller gets | Side effects |
|---|---|---|
| <…> | <…> | <…> |

**Behavior rules**
- <Idempotency, ordering, partial-success semantics.>

---

### CS-02 — <…>

<Same shape.>

## 4. Cross-cutting rules

- **Error signalling:** <exceptions | codes | result objects>
- **Versioning:** <how breaking changes are handled, or "v1 only">
- **Observability:** <what is logged or emitted, if the user cares>
- **Configuration surface:** <env vars, config file, arguments>

## 5. Open questions

| # | Question | Who answers |
|---|---|---|
| 1 | <…> | <…> |
