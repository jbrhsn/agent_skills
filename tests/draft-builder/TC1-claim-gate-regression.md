# TC1: Claim-Integrity Gate Regression Test

## Objective

Verify that the existing claim-integrity gate (step 3 of the workflow) continues to function correctly after the Goal 1 and Goal 2 improvements. This regression test ensures:

1. The linter correctly **detects unaccounted risky claims** in prose
2. The linter correctly **passes lint-clean drafts** with all claims properly marked
3. Exit codes are correct (0 = clean, 1 = fail, 2 = usage error)
4. The `--json` output format is valid and correct
5. Scoping (`--section`, code blocks, scaffolding) is respected

---

## Test Criteria (Weighted Rubric: 100 points)

### 1. Exit Codes Correct (40 points)
- **Clean fixture → exit 0** (15 points)
  - `tc1-clean.md` with all risky claims properly marked should exit 0
  - Output contains "PASS"
  
- **Dirty fixture → exit 1** (15 points)
  - `tc1-dirty.md` with unaccounted claims should exit 1
  - Output contains "FAIL" and lists each unaccounted claim
  
- **Usage error → exit 2** (10 points)
  - Missing or invalid file argument should exit 2
  - Example: `claim_lint.py nonexistent.md` → exit 2 + "error: file not found"

### 2. Claims Detected (30 points)
- **Every unaccounted claim is flagged** (20 points)
  - `tc1-dirty.md` contains 4 intentionally unaccounted claims (numbers, percentages, research appeals, superlatives)
  - Linter must flag all 4 (and only those 4)
  - Each flag includes the line number and a helpful hint (e.g., "a percentage — cite it or flag it")
  
- **No false positives in clean fixture** (10 points)
  - `tc1-clean.md` has all claims properly marked
  - Linter exits 0 with no flags
  - Pure rhetoric (unscored risky words) in clean fixture should not trigger false positives

### 3. JSON Output Shape & Correctness (15 points)
- `--json` flag produces valid JSON (5 points)
  - Parseable JSON structure (no syntax errors)
  
- Correct JSON keys and counts (10 points)
  - Clean fixture: `{"ok": true, "file": "...", "unaccounted_claims": [], "count": 0}`
  - Dirty fixture: `{"ok": false, "file": "...", "count": 4}` + entries in `unaccounted_claims`
  - Counts match actual flagged claims

### 4. Scoping Rules Respected (15 points)
- **Code blocks skipped** (5 points)
  - `tc1-clean.md` includes a code block with `[unaccounted numbers]`
  - Linter ignores code blocks (no false flags)
  
- **`--section Draft` isolates section** (5 points)
  - Linter only checks the `## Draft` section body when `--section Draft` is used
  - Other sections (e.g., "Raw notes", "Research sources") are skipped
  
- **Blockquotes and scaffolding skipped** (5 points)
  - Lines starting with `>` (blockquotes) are skipped
  - Stub metadata (`**Status:** ...`, `**Hook:** ...`) is skipped

---

## Test Steps

### Setup
```bash
export SKILL_DIR="./content-creation/linkedin-medium/draft-builder"  # or ~/.config/opencode/skills/draft-builder
cd tests/draft-builder
```

### Step 1: Run linter on clean fixture (expect exit 0)
```bash
python3 $SKILL_DIR/scripts/claim_lint.py fixtures/tc1-clean.md --section Draft
```

**Expected output:**
- Exit code: **0**
- Output includes: `CLAIM LINT: PASS — no unaccounted risky claims`
- Output includes: `Every risky claim is cited [source: ...], flagged [UNVERIFIED], or marked [personal].`

**Scoring:** If any of the above fails, deduct 5 points from the "Clean fixture → exit 0" criterion (max 15 points).

### Step 2: Run linter on dirty fixture (expect exit 1, flags all 4 claims)
```bash
python3 $SKILL_DIR/scripts/claim_lint.py fixtures/tc1-dirty.md --section Draft
```

**Expected output:**
- Exit code: **1**
- Output includes: `CLAIM LINT: FAIL — 4 unaccounted risky claim(s)`
- Output lists line numbers and hints for:
  1. **Line with unaccounted percentage** (e.g., "87% of developers")
  2. **Line with unaccounted research appeal** (e.g., "studies show")
  3. **Line with unaccounted superlative** (e.g., "the largest")
  4. **Line with unaccounted bare number** (e.g., "> 50 examples")

**Scoring:** 
- Each expected claim flagged: +5 points (4 × 5 = 20 points max)
- No false positives: +0 (already counted in criterion 2)
- If count ≠ 4 or output format broken: deduct 10 points from "Claims detected" criterion

### Step 3: Run linter on dirty fixture with `--json` (expect exit 1, valid JSON)
```bash
python3 $SKILL_DIR/scripts/claim_lint.py fixtures/tc1-dirty.md --section Draft --json
```

**Expected output:**
- Exit code: **1**
- Output is valid JSON (parseable, no syntax errors)
- `"ok": false`
- `"count": 4`
- `"unaccounted_claims"` array has 4 entries, each with `"line"`, `"text"`, `"risks"` fields

**Scoring:**
- Valid JSON: +5 points
- Correct `ok`, `count`, keys: +10 points

### Step 4: Verify scoping with code block (expect exit 0, code skipped)
```bash
python3 $SKILL_DIR/scripts/claim_lint.py fixtures/tc1-clean.md --section Draft
```

**Expected behavior:**
- The `## Draft` section contains a fenced code block with `[not a real claim: 999]`
- Linter skips the code block and does NOT flag this
- Overall exit 0 (all real claims in prose are marked)

**Scoring:** +5 points if code block is correctly skipped

### Step 5: Verify `--section` flag (only lints specified section)
```bash
# Lint only the Draft section
python3 $SKILL_DIR/scripts/claim_lint.py fixtures/tc1-clean.md --section Draft
# Exit 0, lints only ## Draft section

# Try a different section (should skip it if it doesn't exist)
python3 $SKILL_DIR/scripts/claim_lint.py fixtures/tc1-clean.md --section "Raw notes"
# Should skip (or output no claims) since Raw notes are scaffolding
```

**Scoring:** +5 points if `--section Draft` correctly isolates and lints only that section

### Step 6: Test usage error (missing file)
```bash
python3 $SKILL_DIR/scripts/claim_lint.py nonexistent.md --section Draft
```

**Expected output:**
- Exit code: **2**
- Output contains: `error: file not found: nonexistent.md`

**Scoring:** +10 points if exit code is 2 and error message is present

---

## Expected Outcomes Summary

| Scenario | Exit Code | Output | Points (if all pass) |
|---|---|---|---|
| **tc1-clean.md** | 0 | PASS + no flags | 15 |
| **tc1-dirty.md** | 1 | FAIL + 4 flags | 15 |
| **tc1-dirty.md --json** | 1 | Valid JSON, `count: 4` | 10 |
| **Code block skipped** | 0 | Code not flagged | 5 |
| **--section Draft works** | 0/1 | Only Draft section linted | 5 |
| **Blockquotes skipped** | 0 | Blockquotes ignored | 5 |
| **Usage error** | 2 | "error: file not found" | 10 |

**Total: 100 points**

---

## Passing Criteria

- **Score ≥ 80/100 → PASS** — The claim-integrity gate regression is clear; no regressions introduced.
- **Score < 80/100 → FAIL** — The gate has degraded or broken; review the spec and remediate.

---

## Notes

- All criteria are **deterministic and script-verifiable** — copy/paste the commands and check exit codes and output patterns.
- Fixtures are stable (never modified by TC1).
- If any command fails unexpectedly, check that `$SKILL_DIR` is correctly resolved and the script exists at `$SKILL_DIR/scripts/claim_lint.py`.
