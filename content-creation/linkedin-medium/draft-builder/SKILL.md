---
name: draft-builder
description: Use when the user has rough bullets, a messy paragraph, a half-finished draft, or a drafts/ stub and wants it turned into one clean, platform-neutral source draft. Auto-detects how much cleanup vs expansion is needed, matches voice from voice-tone/, enforces claim integrity with a linter (no invented facts), and stops for review. Trigger on "turn this into a draft", "clean up these notes", "build a draft from".
---

# Draft Builder

Take messy input and produce ONE clean, platform-neutral **source draft**, a complete, well-structured piece of thinking before any platform formatting.

Because everything downstream trusts this draft as the source of truth, this skill is the pipeline's **fact-origination point**. Its most important guarantee is therefore not style. It is **claim integrity: never fabricate a fact, statistic, quote, or study.** That guarantee is *enforced by a linter*, not left to good intentions.

## When to use
- User has rough bullets, a messy paragraph, or a half-finished draft.
- User points at a `drafts/<slug>.md` stub (from `seed-expander`) and says "build this out".

## Folder conventions (resolve relative to CWD)
- `drafts/`: source drafts live here; stubs from seed-expander are read from and updated here.
- `voice-tone/`: voice samples + explicit style instructions.

If `drafts/` is needed but missing, STOP and ask the user how to proceed. Never silently create folders.

### Voice handling (mandatory)
Before drafting, look for `voice-tone/`:
- If `voice-tone/profile.md` exists, read it first (fast, consistent voice read). Otherwise read the raw samples + any instruction files.
- Adapt sentence rhythm, vocabulary, and structural habits to match, adapting to the CONTENT, not a rigid template.
- If `voice-tone/` does NOT exist, STOP and ask the user how to proceed: point to samples, paste style rules, or explicitly proceed with a neutral professional voice.

## Claim-integrity contract (the core rule)

In **Expansion mode** especially, the model develops sparse notes into full prose, which is exactly where invented statistics, fake studies, and made-up attributions creep in. To make "don't fabricate" enforceable rather than aspirational, every **risky claim** in the drafting prose MUST be explicitly accounted for by one of three inline markers during authoring and review:

| Marker | Meaning | Use when |
|---|---|---|
| `[source: <url-or-ref>]` | Cited | You have a real source for the claim. Use the URLs already in the stub's `## Research sources` where possible. |
| `[UNVERIFIED]` | Knowingly unbacked | You want to keep a claim you cannot source. Ships honestly labeled. |
| `[personal]` | First-hand anecdote | It's your own experience, not a public fact. |

A **risky claim** is any sentence containing a number, percentage, money figure, multiplier, dated statistic, appeal to research/data ("studies show", "a survey found"), a named attribution ("X says/estimates"), or an absolute factual superlative ("never", "always", "the largest", "proven"). Pure rhetoric ("everyone races to build the model") is NOT a risky claim and needs no marker.

**Absolute rule: never invent a citation to satisfy the linter.** If a claim cannot be sourced, flag it `[UNVERIFIED]` or cut it. Fabricating a URL is worse than an unbacked claim.

**On persist (final step 5), all markers are stripped.** The inline markers exist only during authoring and review to enforce integrity at the source. When the draft is finalized, markers are removed from the prose and consolidated into a structured `## Claim ledger` section, so downstream skills receive clean prose with full provenance recorded separately. This ensures the draft is readable while maintaining complete claim traceability.

## Workflow

### 1. Intake + detect mode
Read the input. Auto-detect how much work it needs:
- **Cleanup mode**: input is already a near-complete draft: tighten, restructure, fix flow. Preserve the user's words where they work.
- **Expansion mode**: input is bullets/sparse notes: develop the thinking, add connective tissue, but do NOT invent facts or fake anecdotes. Mark every risky claim per the contract above.
- **Mixed**: some sections solid, others thin. Handle each accordingly.

State which mode you detected and why (one line). Expansion and Mixed modes carry the highest fabrication risk. Apply the claim contract most strictly there.

**For Expansion and Mixed modes: clarifying-questions gate.** Before building the draft, pause and ask the user a focused batch of clarifying questions (5–8 questions max, not an endless round) to gather missing facts, numbers, sources, anecdotes, and context. Purpose: fill sparse areas with real information rather than placeholders, and reduce the number of `[UNVERIFIED]` claims by converting guesses into either real cited facts or explicit `[personal]` anecdotes. Cleanup mode skips this. If running non-interactively, skip the questions, note "clarifying-questions gate skipped — non-interactive mode," and proceed.

### 2. Build the source draft
Structure every source draft as: **hook → point → evidence/story → takeaway.**
- Keep it platform-neutral: no LinkedIn line-break formatting, no Medium subheadings yet. Just clean, complete prose with a clear spine.
- Match the voice profile.
- Apply the claim-integrity contract as you write: cite from the stub's research sources, flag `[UNVERIFIED]`, or mark `[personal]`.
- Length: whatever the idea genuinely needs. This is the raw material, not the final cut.

### 3. Claim-integrity gate (MANDATORY, run before review)
This is a hard gate: before showing the draft to the user, every risky claim must be accounted for. Run the linter on the drafting prose:

Resolve `SKILL_DIR` to this skill's directory (project-local `.opencode/skills/draft-builder` or global `~/.config/opencode/skills/draft-builder`).

```
python3 $SKILL_DIR/scripts/claim_lint.py drafts/<slug>.md --section Draft
```
(Use `--section Draft` when linting a stub whose new prose lives under `## Draft`; omit it, or point at a standalone file, when the whole file is the draft.)

- **Exit 0 (PASS):** proceed to review.
- **Exit 1 (FAIL):** the linter lists each unaccounted risky claim. For EACH one, resolve it by citing, flagging `[UNVERIFIED]`, or rewording/cutting, **never by inventing a source**, then re-run until it passes. Only then continue.

The linter is a heuristic safety net (it can over- or under-flag). Over-flagging is resolved cheaply by adding a marker; do not disable the gate to avoid the work. If you genuinely believe a flag is a false positive (e.g. a number that is not a factual claim), reword to remove ambiguity rather than ignoring it.

Report the lint result (PASS, or the FAIL list and how you resolved each item) as part of the review so the user can see the claim audit.

### 4. Review-first (mandatory stop)
Present the source draft (now lint-clean) to the user, plus a one-line claim audit ("N risky claims: X cited, Y flagged UNVERIFIED, Z personal"). STOP.
If running non-interactively (e.g. in a batch pipeline or scripted run), document this gate as "skipped — auto-proceeding with output as drafted" and continue; do not silently omit the gate from the output log.
Ask for edits/approval. Iterate on the draft in place, re-running the gate after any change that touches a claim, until the user approves. Do NOT proceed to writing the final file automatically.

### 5. Persist (after approval)
After the user approves the draft, persist it in the following order:

1. **Voice compliance gate (before write).** If `voice-tone/profile.md` (or raw `voice-tone/` samples) is present, scan the draft against its "Avoided Words & Phrases" and "Punctuation & Formatting Quirks". Auto-fix mechanical violations (em-dashes to periods or commas, banned punctuation) and report what changed. Flag judgment calls (hype words, AI-voice markers) for the user. Never emit a banned pattern. If no voice-tone exists, skip silently.

2. **Final claim-integrity gate (before strip).** Run `claim_lint.py` on the **marked** draft to confirm it still passes (exit 0). This gate ensures no claim drift occurred since review. This is the last time the markers are validated.

3. **Strip markers and build ledger (write step).** Run `claim_lint.py --strip` to remove all inline markers (`[source:]`, `[UNVERIFIED]`, `[personal]`) from the prose and generate a structured `## Claim ledger` section at the end of the file. This produces clean, marker-free prose while recording every claim's provenance.

4. **Write/update the source draft** in `drafts/<slug>.md`:
   - If building from a stub, fill the `## Draft` section with the stripped prose and set `**Status:** drafted`. Keep the `## Claim ledger` at the end.
   - If new, create the file with the same stub structure (title, status, source notes, then the stripped draft, then the ledger).
   - The `## Claim ledger` section provides full provenance without polluting the prose: each entry records the claim text and its status (cited + source URL, unverified, or personal).

5. **Confirm the file path** to the user.

The stripped draft at `drafts/<slug>.md` is now ready for downstream skills. The prose contains no marker annotations, but the `## Claim ledger` preserves complete claim traceability.

## Scripts reference
- `scripts/claim_lint.py`: scans a draft for risky claims (numbers, %, money, multipliers, dated stats, research appeals, named attributions, factual superlatives) that are NOT accounted for by `[source: ...]`, `[UNVERIFIED]`, or `[personal]`. Skips code blocks, headings, blockquotes, and stub scaffolding by default. 

  **Flags:**
  | Flag | Effect |
  |---|---|
  | `--section <heading>` | Lint only that section body (e.g. `--section Draft`) |
  | `--whole-file` | Lint everything, including code blocks and scaffolding |
  | `--json` | Emit machine-readable JSON output |
  | `--strip` | Remove markers and build a `## Claim ledger`. Draft must be lint-clean (exit 0) for best results. |
  | `--in-place` | With `--strip`, write to the file instead of stdout |

  **Exit codes:**
  | Code | Meaning |
  |---|---|
  | `0` | PASS: no unaccounted claims (or strip succeeded) |
  | `1` | FAIL: unaccounted risky claims found (or strip failed) |
  | `2` | Usage error |

  **Typical usage (step 5: final gate, then strip):**
  ```bash
  # First, confirm draft is clean (final gate)
  python3 $SKILL_DIR/scripts/claim_lint.py drafts/<slug>.md --section Draft
  # Then strip markers and build ledger (final write)
  python3 $SKILL_DIR/scripts/claim_lint.py drafts/<slug>.md --section Draft --strip --in-place
  ```

## Handoff
An approved, claim-clean source draft at `drafts/<slug>.md` is the complete deliverable of this skill. The draft is marker-free prose with a `## Claim ledger` that records every claim's status (cited + source URL, unverified, or personal). Downstream skills (linkedin-writer, medium-writer, etc.) consume the clean prose and can reference the ledger for provenance context as needed. The claim-integrity gate was already satisfied during authoring; downstream skills do not re-run the linter.

## Conventions

These are shared assumptions so the content skills interoperate. Each skill
still works standalone. None of these require another skill to be present.

- **Folders** (all cwd-relative): `drafts/`, `linkedin/`, `medium/`,
  `archive/`, `voice-tone/`. Never auto-create, ask the user if missing.
- **Slug**: lowercase, hyphenated, derived from the working title. Reused as
  the filename stem across skills so a piece is traceable.
- **Filenames**: `drafts/<slug>.md`, `linkedin/<slug>-<type>.md`,
  `medium/<slug>-<type>.md`, carousels at `linkedin/carousels/<slug>/`.
- **Overwrite policy**: never silently overwrite an existing file. If the
  target exists, ask the user: overwrite, write a `-v2` (then `-v3`...)
  variant, or pick a new name.
- **Status values** (if a tracker file like `content-log.md` or `content-log.json` exists at cwd): `idea` -> `drafted` -> `reviewed` -> `posted` -> `archived`. If such a tracker exists, after writing or moving a file ASK the user in one line whether to update it to the new status. Absence of a tracker must never block the skill.
