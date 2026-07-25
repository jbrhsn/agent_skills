# Draft-Builder Skill Test Suite

## Overview

This test suite validates the two major improvements made to the `draft-builder` skill:

1. **Goal 1: Clarifying-questions gate** — Sparse input triggers a focused batch of clarifying questions before drafting (Expansion/Mixed modes only).
2. **Goal 2: Marker stripping** — On persist, inline claim markers are stripped and consolidated into a structured `## Claim ledger` so downstream skills receive clean prose.

Additionally, all tests verify that **existing functionality (claim-integrity gate) remains unaffected** (regression test).

---

## Test Cases

| ID | Name | Type | Location |
|---|---|---|---|
| **TC1** | Claim-integrity gate regression | Script-verifiable | `draft-builder/TC1-claim-gate-regression.md` |
| **TC2** | Strip markers + build ledger | Script-verifiable | `draft-builder/TC2-strip-and-ledger.md` |
| **TC3** | Clarifying-questions gate (Goal 1) | Behavioral/manual | `draft-builder/TC3-clarifying-questions.md` |

---

## How to Run

### Setup
Resolve `$SKILL_DIR` to the draft-builder skill directory:
```bash
export SKILL_DIR="$(cd "$(dirname "$0")/../content-creation/linkedin-medium/draft-builder" && pwd)"
# or if running from a different location:
export SKILL_DIR="/home/jbrhsn/.config/opencode/skills/draft-builder"  # installed version
# or
export SKILL_DIR="./content-creation/linkedin-medium/draft-builder"   # repo source from agent_skills root
```

### TC1: Claim-integrity gate regression
```bash
cd tests/draft-builder
python3 $SKILL_DIR/scripts/claim_lint.py fixtures/tc1-clean.md --section Draft
# Expected: exit 0, output contains "PASS"

python3 $SKILL_DIR/scripts/claim_lint.py fixtures/tc1-dirty.md --section Draft
# Expected: exit 1, output lists unaccounted claims

python3 $SKILL_DIR/scripts/claim_lint.py fixtures/tc1-dirty.md --section Draft --json
# Expected: exit 1, JSON output with {"ok": false, "count": N}
```

### TC2: Strip markers + build ledger
```bash
cd tests/draft-builder
python3 $SKILL_DIR/scripts/claim_lint.py fixtures/tc2-marked.md --section Draft --strip
# Expected: exit 0, output shows clean prose + ## Claim ledger

python3 $SKILL_DIR/scripts/claim_lint.py fixtures/tc2-marked.md --section Draft --strip --in-place
# Expected: exit 0, modifies fixtures/tc2-marked.md in place
# Inspect file: grep -c "Claim ledger" fixtures/tc2-marked.md should be 1
# Reset fixture: git checkout fixtures/tc2-marked.md
```

### TC3: Clarifying-questions gate
```bash
# Read the behavioral spec in TC3-clarifying-questions.md
# Run the skill interactively with fixtures/tc3-sparse-input.md
# Evaluate based on the rubric criteria listed in the spec
```

---

## Scoring Model

Each test uses a **weighted rubric** with criteria summing to **100 points**. 

### Overall Pass Threshold
- **≥ 80 points → PASS**
- **< 80 points → FAIL**

Script tests (TC1, TC2) are expected to score **100/100** (all assertions pass). Behavioral tests (TC3) use judgment-based scoring against the rubric.

### TC1 Rubric (100 points)
| Criterion | Points | Scoring |
|---|---|---|
| **Exit codes correct** | 40 | Clean fixture → exit 0 (15), dirty fixture → exit 1 (15), usage error → exit 2 (10) |
| **Claims detected** | 30 | Every unaccounted claim in dirty fixture flagged (20), no false positives in clean fixture (10) |
| **JSON output shape** | 15 | `{"ok": ..., "count": N, ...}` present; counts correct |
| **Scoping (sections, code blocks)** | 15 | Code blocks / blockquotes / scaffolding skipped correctly; `--section Draft` isolates only that section |

**Total: 100 points**

### TC2 Rubric (100 points)
| Criterion | Points | Scoring |
|---|---|---|
| **Markers fully removed from prose** | 30 | No `[source: ...]` remaining (10), no `[UNVERIFIED]` (10), no `[personal]` (10) |
| **Claim ledger present & formatted** | 25 | `## Claim ledger` section exists (5), correct number of entries (10), correct Markdown format (10) |
| **Claim status classification** | 25 | Cited claims show status + source URL (10), unverified claims marked correctly (8), personal claims marked correctly (7) |
| **In-place mode** | 10 | `--in-place` flag rewrites file (5), success message with claim count printed (5) |
| **Non-target sections untouched** | 10 | `## Research sources`, code blocks, other sections unaffected by strip |

**Total: 100 points**

### TC3 Rubric (100 points)
| Criterion | Points | Scoring |
|---|---|---|
| **Gate triggers in Expansion/Mixed** | 25 | Sparse input triggers questions (15), near-complete input skips (10) |
| **Question batch is focused** | 20 | Asks ≤ ~8 questions (5), questions are distinct/non-repetitive (8), prompts are clear (7) |
| **Questions target claim-risky gaps** | 30 | Questions address numbers/statistics that would become [UNVERIFIED] (12), ask for sources (10), ask for anecdote context (8) |
| **Skips in Cleanup mode** | 15 | Near-complete input auto-detected as Cleanup (8), clarifying gate is skipped (7) |
| **Non-interactive fallback** | 10 | Non-interactive runs skip questions with documented note (7), documented in SKILL.md step 1 (3) |

**Total: 100 points**

---

## Test Fixtures

All fixtures are stored in `draft-builder/fixtures/` and are minimal, purpose-built for each test:

| Fixture | Size | Purpose |
|---|---|---|
| `tc1-clean.md` | ~150 lines | All risky claims properly marked → gate should PASS (exit 0) |
| `tc1-dirty.md` | ~150 lines | Multiple unaccounted risky claims → gate should FAIL (exit 1) |
| `tc2-marked.md` | ~120 lines | Markers present (`[source:]`, `[UNVERIFIED]`, `[personal]`) → strip should clean & build ledger |
| `tc3-sparse-input.md` | ~60 lines | Sparse bullets/notes (Expansion mode) → should trigger clarifying-questions gate before draft |

---

## Notes

- **TC1 & TC2 are fully automatable** — assert exit codes and output patterns. A reviewer can copy/paste the commands above and verify deterministically.
- **TC3 is behavioral** — the skill's instruction to ask clarifying questions lives in SKILL.md step 1 and must be observed during interaction. The rubric guides evaluation but requires human judgment.
- **Fixtures are NOT reset between runs** — TC2's `--in-place` modifies `tc2-marked.md`. To re-run TC2, reset the fixture: `git checkout tests/draft-builder/fixtures/tc2-marked.md`.
- **Scoring is cumulative** — all criteria within a test must be met to earn full points; partial credit is possible for borderline cases.

---

## Pass/Fail Decision

- **All 3 tests must score ≥ 80/100** to declare the skill improvements as **validated**.
- If any test scores < 80/100, the spec lists the failed criteria and remediation is needed.
