---
name: draft-builder
description: Use when the user has rough bullets, a messy paragraph, a half-finished draft, or a drafts/ stub and wants it turned into one clean, platform-neutral source draft. Auto-detects how much cleanup vs expansion is needed, matches voice from voice-tone/, enforces claim integrity with a linter (no invented facts), and stops for review. Trigger on "turn this into a draft", "clean up these notes", "build a draft from".
---

# Draft Builder

Take messy input and produce ONE clean, platform-neutral **source draft** — a complete, well-structured piece of thinking before any platform formatting. This is the single source of truth that `platform-adapter` later reshapes for LinkedIn and Medium, and that `tutorial-verifier` runs code from.

Because everything downstream trusts this draft as the source of truth, this skill is the pipeline's **fact-origination point**. Its most important guarantee is therefore not style — it is **claim integrity: never fabricate a fact, statistic, quote, or study.** That guarantee is *enforced by a linter*, not left to good intentions.

## When to use
- User has rough bullets, a messy paragraph, or a half-finished draft.
- User points at a `drafts/<slug>.md` stub (from `seed-expander`) and says "build this out".

## Folder conventions (resolve relative to CWD)
- `drafts/` — source drafts live here; stubs from seed-expander are read from and updated here.
- `voice-tone/` — voice samples + explicit style instructions.

If `drafts/` is needed but missing, STOP and ask the user how to proceed. Never silently create folders.

### Voice handling (mandatory)
Before drafting, look for `voice-tone/`:
- If `voice-tone/profile.md` exists, read it first (fast, consistent voice read). Otherwise read the raw samples + any instruction files.
- Adapt sentence rhythm, vocabulary, and structural habits to match — adapt to the CONTENT, not a rigid template.
- If `voice-tone/` does NOT exist, STOP and ask the user how to proceed: point to samples, paste style rules, or explicitly proceed with a neutral professional voice.

## Claim-integrity contract (the core rule)

In **Expansion mode** especially, the model develops sparse notes into full prose — which is exactly where invented statistics, fake studies, and made-up attributions creep in. To make "don't fabricate" enforceable rather than aspirational, every **risky claim** in the drafting prose MUST be explicitly accounted for by one of three inline markers:

| Marker | Meaning | Use when |
|---|---|---|
| `[source: <url-or-ref>]` | Cited | You have a real source for the claim. Use the URLs already in the stub's `## Research sources` where possible. |
| `[UNVERIFIED]` | Knowingly unbacked | You want to keep a claim you cannot source. Ships honestly labeled. |
| `[personal]` | First-hand anecdote | It's your own experience, not a public fact. |

A **risky claim** is any sentence containing a number, percentage, money figure, multiplier, dated statistic, appeal to research/data ("studies show", "a survey found"), a named attribution ("X says/estimates"), or an absolute factual superlative ("never", "always", "the largest", "proven"). Pure rhetoric ("everyone races to build the model") is NOT a risky claim and needs no marker.

**Absolute rule: never invent a citation to satisfy the linter.** If a claim cannot be sourced, flag it `[UNVERIFIED]` or cut it. Fabricating a URL is worse than an unbacked claim.

Markers live inline in the draft body during authoring. On persistence you may either keep inline `[source: ...]` markers or consolidate them into the stub's `## Research sources` list (see step 5) — but every risky claim must remain traceable to a source or an explicit `[UNVERIFIED]` / `[personal]` label.

## Workflow

### 1. Intake + detect mode
Read the input. Auto-detect how much work it needs:
- **Cleanup mode** — input is already a near-complete draft: tighten, restructure, fix flow. Preserve the user's words where they work.
- **Expansion mode** — input is bullets/sparse notes: develop the thinking, add connective tissue, but do NOT invent facts or fake anecdotes. Mark every risky claim per the contract above.
- **Mixed** — some sections solid, others thin. Handle each accordingly.

State which mode you detected and why (one line). Expansion and Mixed modes carry the highest fabrication risk — apply the claim contract most strictly there.

### 2. Build the source draft
Structure every source draft as: **hook → point → evidence/story → takeaway.**
- Keep it platform-neutral: no LinkedIn line-break formatting, no Medium subheadings yet. Just clean, complete prose with a clear spine.
- Match the voice profile.
- Apply the claim-integrity contract as you write: cite from the stub's research sources, flag `[UNVERIFIED]`, or mark `[personal]`.
- Length: whatever the idea genuinely needs — this is the raw material, not the final cut.

### 3. Claim-integrity gate (MANDATORY — run before review)
This is a hard gate, analogous to `tutorial-verifier` refusing to claim code works without running it. Before showing the draft to the user, run the linter on the drafting prose:

```
python3 .opencode/skills/draft-builder/scripts/claim_lint.py drafts/<slug>.md --section Draft
```
(Use `--section Draft` when linting a stub whose new prose lives under `## Draft`; omit it, or point at a standalone file, when the whole file is the draft.)

- **Exit 0 (PASS):** proceed to review.
- **Exit 1 (FAIL):** the linter lists each unaccounted risky claim. For EACH one, resolve it by citing, flagging `[UNVERIFIED]`, or rewording/cutting — **never by inventing a source** — then re-run until it passes. Only then continue.

The linter is a heuristic safety net (it can over- or under-flag). Over-flagging is resolved cheaply by adding a marker; do not disable the gate to avoid the work. If you genuinely believe a flag is a false positive (e.g. a number that is not a factual claim), reword to remove ambiguity rather than ignoring it.

Report the lint result (PASS, or the FAIL list and how you resolved each item) as part of the review so the user can see the claim audit.

### 4. Review-first (mandatory stop)
Present the source draft (now lint-clean) to the user, plus a one-line claim audit ("N risky claims: X cited, Y flagged UNVERIFIED, Z personal"). STOP.
Ask for edits/approval. Iterate on the draft in place — re-running the gate after any change that touches a claim — until the user approves. Do NOT hand off to platform-adapter automatically.

### 5. Persist (after approval)
Write/update the source draft in `drafts/<slug>.md`:
- If building from a stub, fill the `## Draft` section and set `**Status:** drafted`. Keep inline `[source: ...]` / `[UNVERIFIED]` / `[personal]` markers, or move cited URLs into the `## Research sources` list while leaving `[UNVERIFIED]`/`[personal]` markers inline.
- If new, create the file with the same stub structure (title, status, source notes, then the draft).
- Re-run the gate one final time on the persisted file to confirm it is still clean.

Confirm the file path to the user.

## Scripts reference
- `scripts/claim_lint.py` — scans a draft for risky claims (numbers, %, money, multipliers, dated stats, research appeals, named attributions, factual superlatives) that are NOT accounted for by `[source: ...]`, `[UNVERIFIED]`, or `[personal]`. Skips code blocks, headings, blockquotes, and stub scaffolding by default. Flags: `--section <heading>` (lint only that section body), `--whole-file`, `--json`. Exit `0` clean, `1` unaccounted claims found, `2` usage error. Standard-library Python only.

## Handoff
An approved, claim-clean source draft is the input to `platform-adapter` (LinkedIn/Medium versions) and, for tutorials, `tutorial-verifier`. Because the draft's claims are already cited or flagged, downstream skills inherit that provenance instead of guessing. This skill stops at the platform-neutral draft on purpose.

## Conventions

These are shared assumptions so the content skills interoperate. Each skill
still works standalone — none of these require another skill to be present.

- **Folders** (all cwd-relative): `drafts/`, `linkedin/`, `medium/`,
  `archive/`, `voice-tone/`. Never auto-create — ask the user if missing.
- **Slug**: lowercase, hyphenated, derived from the working title. Reused as
  the filename stem across skills so a piece is traceable.
- **Filenames**: `drafts/<slug>.md`, `linkedin/<slug>-<type>.md`,
  `medium/<slug>-<type>.md`, carousels at `linkedin/carousels/<slug>/`.
- **Overwrite policy**: never silently overwrite an existing file. If the
  target exists, ask the user: overwrite, write a `-v2` (then `-v3`...)
  variant, or pick a new name.
- **Status values** (if a tracker file like `content-log.md` or
  `content-log.json` exists at cwd): `idea` -> `drafted` -> `reviewed` ->
  `posted` -> `archived`. Updating the tracker is optional and best-effort;
  absence of a tracker must never block the skill.
