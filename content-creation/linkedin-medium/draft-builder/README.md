# draft-builder

Takes messy input (rough bullets, a half-finished paragraph, or a `drafts/` stub) and produces ONE clean, platform-neutral **source draft**: a complete, well-structured piece of thinking before any platform formatting. This is the single source of truth that `linkedin-writer` and `medium-writer` later reshape into platform versions and that `tutorial-verifier` runs code from. As the pipeline's fact-origination point, its most important guarantee is not style but **claim integrity: never fabricate a fact, statistic, quote, or study**, enforced by a linter, not left to good intentions.

---

## Trigger phrases

| Input | Example |
|---|---|
| Build a draft | "turn this into a draft", "build a draft from" |
| Clean up notes | "clean up these notes" |
| Build out a stub | "build this out" while pointing at a `drafts/<slug>.md` stub from `seed-expander` |

Do **not** use it to generate the ideas themselves (use `seed-expander`), to reshape the finished draft into LinkedIn/Medium versions (use `linkedin-writer` or `medium-writer`), or to verify tutorial code (use `tutorial-verifier`). This skill stops at the platform-neutral source draft on purpose.

---

## What it does

- **Intakes and auto-detects mode.** Reads the input and detects how much work it needs, then states which mode it chose and why (one line):
  - **Cleanup mode**: input is a near-complete draft. Tighten, restructure, fix flow, preserve the user's words where they work.
  - **Expansion mode**: input is bullets/sparse notes. Develop the thinking and add connective tissue, but invent no facts or anecdotes.
  - **Mixed**: some sections solid, others thin; handle each accordingly.
- **Clarifying-questions gate (Expansion/Mixed only).** Before drafting sparse input, pause and ask 5–8 focused clarifying questions to gather missing facts, numbers, sources, and anecdotes. Purpose: convert guesses into real cited facts or explicit `[personal]` anecdotes, reducing `[UNVERIFIED]` claims and producing a fuller draft. Cleanup mode skips this.
- **Matches voice (mandatory).** Before drafting, looks for `voice-tone/`. If `voice-tone/profile.md` exists it reads that first; otherwise it reads the raw samples plus any instruction files, and adapts sentence rhythm, vocabulary, and structural habits to the content. If `voice-tone/` does not exist, it stops and asks how to proceed (point to samples, paste style rules, or explicitly proceed with a neutral professional voice).
- **Builds a platform-neutral source draft.** Structures every draft as **hook → point → evidence/story → takeaway**, with no LinkedIn line-break formatting or Medium subheadings yet, just clean, complete prose with a clear spine. Length is whatever the idea genuinely needs.
- **Enforces claim integrity with a linter.** Runs `scripts/claim_lint.py` as a hard gate before review; every risky claim must be accounted for by an inline marker (see Claim-integrity contract below).
- **Review-first (mandatory stop).** Presents the lint-clean draft plus a one-line claim audit, then stops for edits/approval. Iterates in place, re-running the gate after any change that touches a claim, and never hands off to the writer skills automatically.
- **Persists after approval.** Runs a voice-compliance gate, then runs the final claim-integrity gate on the marked draft, then strips all markers and builds a `## Claim ledger` for clean, marker-free prose. Fills the stub's `## Draft` section (or creates a new file with the same structure), sets `**Status:** drafted`. Downstream skills consume clean prose with provenance recorded in the ledger.

---

## Claim-integrity contract

Because everything downstream trusts this draft, "don't fabricate" is made enforceable. Every **risky claim** in the drafting prose must be explicitly accounted for during authoring and review by one of three inline markers:

| Marker | Meaning | Use when |
|---|---|---|
| `[source: <url-or-ref>]` | Cited | You have a real source for the claim. Prefer the URLs already in the stub's `## Research sources`. |
| `[UNVERIFIED]` | Knowingly unbacked | You want to keep a claim you cannot source. Ships honestly labeled. |
| `[personal]` | First-hand anecdote | It is your own experience, not a public fact. |

A **risky claim** is any sentence containing a number, percentage, money figure, multiplier, dated statistic, appeal to research/data ("studies show", "a survey found"), a named attribution ("X says/estimates"), or an absolute factual superlative ("never", "always", "the largest", "proven"). Pure rhetoric ("everyone races to build the model") is not a risky claim and needs no marker.

**Absolute rule: never invent a citation to satisfy the linter.** If a claim cannot be sourced, flag it `[UNVERIFIED]` or cut it. Fabricating a URL is worse than an unbacked claim. Expansion and Mixed modes carry the highest fabrication risk. The contract is applied most strictly there.

**Markers exist only during authoring.** On persist, all markers are stripped from the prose and consolidated into a structured `## Claim ledger` section. This keeps the final draft clean and readable while preserving full provenance. Downstream skills see marker-free prose and can reference the ledger for claim context.

---

## Scripts

- **`scripts/claim_lint.py`**: scans a draft for risky claims (numbers, percentages, money, multipliers, dated stats, research appeals, named attributions, factual superlatives) that are NOT accounted for by `[source: ...]`, `[UNVERIFIED]`, or `[personal]`. Skips code blocks, headings, blockquotes, and stub scaffolding by default. Standard-library Python only.

  Resolve `$SKILL_DIR` to the skill's directory (project-local `.opencode/skills/draft-builder` or global `~/.config/opencode/skills/draft-builder`).

  **Modes and usage:**

  *Gate before review (step 3):*
  ```bash
  python3 $SKILL_DIR/scripts/claim_lint.py drafts/<slug>.md --section Draft
  ```

  *Final gate + strip (step 5):*
  ```bash
  # Confirm draft is still clean
  python3 $SKILL_DIR/scripts/claim_lint.py drafts/<slug>.md --section Draft
  # Then strip markers and build ledger
  python3 $SKILL_DIR/scripts/claim_lint.py drafts/<slug>.md --section Draft --strip --in-place
  ```

  **Flags:**
  | Flag | Effect |
  |---|---|
  | `--section <heading>` | Lint only that section body (use `--section Draft` when the new prose lives under `## Draft`) |
  | `--whole-file` | Lint the entire file including scaffolding |
  | `--json` | Emit machine-readable output |
  | `--strip` | Remove all markers and build a `## Claim ledger`. Draft must be lint-clean (exit 0) for best results. |
  | `--in-place` | With `--strip`, write to the file instead of stdout. |

  **Exit codes:**
  | Code | Meaning | Action |
  |---|---|---|
  | `0` | PASS: clean | Proceed to review (or strip succeeded) |
  | `1` | FAIL: unaccounted risky claims found | For each one, cite, flag `[UNVERIFIED]`, or reword/cut (never invent a source), then re-run until clean |
  | `2` | Usage error | Fix the invocation |

  The linter is a heuristic safety net and can over- or under-flag. Over-flagging is resolved cheaply by adding a marker; if a flag is a genuine false positive, reword to remove ambiguity rather than disabling the gate.

---

## Workflow

| Step | What happens |
|---|---|
| **1. Intake + detect mode** | Read the input; detect Cleanup / Expansion / Mixed and state which and why (one line) |
| **1a. Clarifying-questions gate (Expansion/Mixed only)** | If Expansion or Mixed, ask 5–8 focused questions to gather missing facts, numbers, sources, anecdotes. Cleanup mode skips this. Non-interactive runs skip silently. |
| **2. Build the source draft** | Write hook → point → evidence/story → takeaway, platform-neutral, voice-matched, applying the claim contract inline with markers |
| **3. Claim-integrity gate** | Run `claim_lint.py`; resolve every FAIL by citing/flagging/rewording; re-run until exit 0 |
| **4. Review-first (stop)** | Present the lint-clean draft + one-line claim audit; iterate in place until approved; no auto-handoff |
| **5. Persist** | Run voice-compliance gate → run final claim-integrity gate (confirm clean) → strip markers and build `## Claim ledger` → write to `drafts/<slug>.md`, set `**Status:** drafted`; confirm the path |

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Messy input | Yes | Rough bullets, a messy paragraph, a half-finished draft, or a `drafts/<slug>.md` stub |
| `voice-tone/` folder | Yes (or explicit opt-out) | Voice samples / `profile.md` / style rules; if missing, the skill stops and asks how to proceed |
| `drafts/` folder | For persistence | Source drafts live and are updated here; the skill asks how to proceed if it is missing |
| Research sources | Optional | URLs from the stub's `## Research sources`, reused to satisfy `[source: ...]` markers |

---

## Outputs

- **A clean, platform-neutral source draft** structured hook → point → evidence/story → takeaway, voice-matched, with all inline markers stripped and provenance recorded in a `## Claim ledger` section.
- **A one-line claim audit** ("N risky claims: X cited, Y flagged UNVERIFIED, Z personal") plus the lint result (PASS, or the FAIL list and how each item was resolved).
- **The persisted draft** at `drafts/<slug>.md` with `**Status:** drafted`, marker-free prose, a `## Claim ledger` recording all claim sources and statuses, and a confirmed path. Downstream skills receive clean, readable prose with full provenance traceable.

---

## Limitations

- **Never fabricates** a fact, statistic, quote, study, or citation. The linter is a hard gate, not a suggestion.
- **The linter is heuristic** and can over- or under-flag; it must not be disabled to avoid the work.
- **Never silently creates folders** and **never silently overwrites**. It asks how to proceed if `drafts/` is missing or a target file exists.
- **Requires a voice signal.** If `voice-tone/` is absent it stops and asks rather than guessing a voice.
- **Stops at the platform-neutral draft.** It does not produce LinkedIn/Medium versions or verify code.
- **Tracker updates are prompted, not automatic.** If a `content-log.md`/`content-log.json` tracker exists, the skill asks in one line whether to update it after writing; a missing tracker never blocks the skill.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global, available in all projects (Linux/macOS)
cp -r content-creation/linkedin-medium/draft-builder ~/.config/opencode/skills/

# Per-project only
cp -r content-creation/linkedin-medium/draft-builder .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse content-creation\linkedin-medium\draft-builder "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/draft-builder.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before the content task |

Note: on non-opencode platforms the `claim_lint.py` gate must be run manually (`python3 scripts/claim_lint.py ...`), since those platforms will not invoke it automatically.

---

## Companion skills

`draft-builder` is the second stage of the LinkedIn/Medium content pipeline: **seed-expander → draft-builder → {linkedin-writer, medium-writer} → {carousel-builder, medium-imager, tutorial-verifier} → editorial-reviewer**, with `voice-profiler` and `content-tracker` as cross-cutting support.

- **`seed-expander`**: produces the approved stubs this skill builds out (the previous stage)
- **`linkedin-writer`** / **`medium-writer`**: reshape this skill's marker-free source draft into platform-specific versions (the next stage). They consume clean prose and can reference the `## Claim ledger` for context.
- **`tutorial-verifier`**: runs and verifies code from tutorial drafts
- **`carousel-builder`**: renders carousel slide copy into image files
- **`editorial-reviewer`**: produces edited variants of a version
- **`voice-profiler`**: builds the `voice-tone/` profile this skill reads to match voice
- **`content-tracker`**: tracks each piece's status (`idea` → `drafted` → ...) across the pipeline
