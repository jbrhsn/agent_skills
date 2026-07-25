# TC2: Strip Markers & Build Claim Ledger Test

## Objective

Verify that the new `--strip` mode correctly removes all inline claim markers from prose and builds a valid `## Claim ledger` section. This test validates Goal 2 (marker stripping for downstream consumption):

1. All `[source: ...]` markers are removed from prose
2. All `[UNVERIFIED]` markers are removed from prose
3. All `[personal]` markers are removed from prose
4. A structured `## Claim ledger` is created with all claims recorded
5. Ledger entries correctly classify each claim (cited + source, unverified, or personal)
6. The `--in-place` flag writes the stripped version to the file
7. Non-target sections (code blocks, other sections) are preserved

---

## Test Criteria (Weighted Rubric: 100 points)

### 1. Markers Fully Removed from Prose (30 points)

- **No `[source: ...]` remaining** (10 points)
  - All inline citations are stripped from the prose
  - Example: "According to research [source: https://example.com]" becomes "According to research"
  - No partial markers left (e.g., stray `[source:` or `]`)

- **No `[UNVERIFIED]` remaining** (10 points)
  - All unverified claim flags are stripped from prose
  - Example: "This claim [UNVERIFIED]" becomes "This claim"

- **No `[personal]` remaining** (10 points)
  - All personal anecdote markers are stripped from prose
  - Example: "I did this [personal]" becomes "I did this"

**Scoring:** Use `grep` to count marker occurrences in output. If any markers remain in the prose section:
- Markers found: deduct full 10 points for that marker type
- Markers not found: full 10 points earned

### 2. Claim Ledger Present & Formatted (25 points)

- **`## Claim ledger` section exists** (5 points)
  - Output contains exactly one `## Claim ledger` heading
  - Positioned after the main prose content

- **Correct number of entries** (10 points)
  - Ledger should have 4 entries (matching the 4 marked claims in tc2-marked.md)
  - Each entry is a bullet point (`-`)
  - Count with: `grep -c "^- " output` should equal 4

- **Correct Markdown format** (10 points)
  - Each entry is formatted as: `- **status** — cleaned_text`
  - Cited entries include: `Source: <url>` on next line (indented)
  - No malformed Markdown; each status is bold; URLs are plain text

**Scoring:**
- Ledger heading missing: -5 points
- Entry count wrong: -10 points
- Malformed Markdown: -5 to -10 points (depending on severity)

### 3. Claim Status Classification (25 points)

- **Cited claims show status + source URL** (10 points)
  - Claims marked `[source: <url>]` appear in ledger as: `- **cited** — <cleaned_text> \n  Source: <url>`
  - URLs are accurately extracted (no truncation, no extra characters)
  - Example: `[source: https://example.com/report]` → ledger shows `Source: https://example.com/report`

- **Unverified claims marked correctly** (8 points)
  - Claims marked `[UNVERIFIED]` appear in ledger as: `- **unverified** — <cleaned_text>`
  - No source field (unverified entries are single-line)

- **Personal claims marked correctly** (7 points)
  - Claims marked `[personal]` appear in ledger as: `- **personal** — <cleaned_text>`
  - No source field (personal entries are single-line)

**Scoring:**
- Cited claims with wrong status or missing URL: -3 to -5 points per claim
- Unverified claims with wrong format: -2 points per claim
- Personal claims with wrong format: -2 points per claim

### 4. In-Place Mode (`--in-place` flag) (10 points)

- **File is rewritten** (5 points)
  - `--in-place` flag causes the file to be updated in place
  - Original file should be modified (timestamp changed)

- **Success message & claim count printed** (5 points)
  - Output contains: `CLAIM STRIP: stripped markers and wrote ledger to <file>`
  - Output contains: `(N claim(s) recorded in ## Claim ledger)`
  - Where N = 4 (the number of claims in tc2-marked.md)

**Scoring:**
- File not modified: -5 points
- Success message missing: -2 points
- Claim count incorrect: -2 points

### 5. Non-Target Sections Untouched (10 points)

- **`## Research sources` preserved** (3 points)
  - The `## Research sources` section is left unchanged
  - URLs and formatting intact

- **Code blocks preserved** (3 points)
  - Fenced code blocks (```...```) are not processed for stripping
  - Content inside code blocks is unchanged

- **Other sections untouched** (4 points)
  - Sections like `## Metadata`, `## Notes` pass through unchanged
  - Only the target section (specified by `--section` or default draft sections) is processed

**Scoring:**
- Non-target section modified: -3 to -5 points per section affected

---

## Test Steps

### Setup
```bash
export SKILL_DIR="./content-creation/linkedin-medium/draft-builder"  # or ~/.config/opencode/skills/draft-builder
cd tests/draft-builder

# IMPORTANT: Reset the fixture before running TC2 (in case TC2 was run before)
git checkout fixtures/tc2-marked.md 2>/dev/null || echo "Fixture OK"
```

### Step 1: Run strip to stdout (verify output format)
```bash
python3 $SKILL_DIR/scripts/claim_lint.py fixtures/tc2-marked.md --section Draft --strip
```

**Expected output:**
- Exit code: **0**
- Prose section with NO markers (`[source:]`, `[UNVERIFIED]`, `[personal]`)
- A `## Claim ledger` section at the end with 4 bullet entries
- Each entry shows: `- **cited|unverified|personal** — <claim text>`

**Scoring:**
- Run the command and capture output: `python3 $SKILL_DIR/scripts/claim_lint.py fixtures/tc2-marked.md --section Draft --strip > /tmp/tc2_output.txt`
- Check for markers: `grep -c '\[source:\|UNVERIFIED\|personal\]' /tmp/tc2_output.txt` (should be 0 in main prose, but OK in the marker-removal verification below)
- Manually verify: `grep "## Claim ledger" /tmp/tc2_output.txt` should return the heading

**Detailed checks for Step 1:**
```bash
# Check no markers in main prose (before ledger)
grep -B 1000 "## Claim ledger" /tmp/tc2_output.txt | grep -c '\[source:\|\[UNVERIFIED\|\[personal\]'
# Expected: 0 (or very low, only in comments explaining what was stripped)

# Check ledger exists
grep "## Claim ledger" /tmp/tc2_output.txt
# Expected: found

# Count ledger entries
grep "^- " /tmp/tc2_output.txt | tail -n +1 | wc -l
# Expected: 4
```

Earn full criterion points if all checks pass.

### Step 2: Run strip with `--in-place` (verify file rewrite)
```bash
# Backup the original fixture
cp fixtures/tc2-marked.md fixtures/tc2-marked.md.bak

# Run strip in-place
python3 $SKILL_DIR/scripts/claim_lint.py fixtures/tc2-marked.md --section Draft --strip --in-place
```

**Expected output:**
- Exit code: **0**
- Output includes: `CLAIM STRIP: stripped markers and wrote ledger to fixtures/tc2-marked.md`
- Output includes: `(4 claim(s) recorded in ## Claim ledger)`

**Scoring:**
- Check exit code: `echo $?` should be 0
- Check output message: `grep "CLAIM STRIP" /tmp/tc2_output.txt` should find it
- Check file was modified: `diff fixtures/tc2-marked.md.bak fixtures/tc2-marked.md` should show differences (markers removed, ledger added)

Earn full 10 points if all checks pass.

### Step 3: Verify markers are gone from the file
```bash
# Check the modified file
grep -n '\[source:\|\[UNVERIFIED\|\[personal\]' fixtures/tc2-marked.md | grep -v "## Claim ledger" | head -5
# Expected: only matches in the Claim ledger section (not in main prose)
```

**Scoring:**
- If markers found in prose sections (before `## Claim ledger`): deduct appropriate points from criterion 1
- If no markers found outside ledger: earn full criterion points

### Step 4: Inspect the Claim ledger format
```bash
# Show the ledger section
tail -n 30 fixtures/tc2-marked.md
```

**Expected format:**
```
## Claim ledger
- **cited** — Claim text here
  Source: https://example.com

- **unverified** — Another claim here

- **personal** — Third claim here
```

**Scoring:**
- Each cited entry has `Source:` line: +3 points per entry found
- Each unverified entry is single-line: +2 points per entry
- Each personal entry is single-line: +2 points per entry
- Markdown format correct (bold status, em-dash separator): +5 points

### Step 5: Verify non-target sections are untouched
```bash
# Compare the Research sources section
diff <(grep -A 5 "## Research sources" fixtures/tc2-marked.md.bak) <(grep -A 5 "## Research sources" fixtures/tc2-marked.md)
# Expected: no differences

# Compare any code blocks (should be unchanged)
grep -A 2 "^\`\`\`" fixtures/tc2-marked.md
# Expected: unchanged from original fixture
```

**Scoring:**
- If differences found: deduct 3-5 points from criterion 5
- If sections match: earn full criterion points

### Step 6: Reset fixture for next runs
```bash
git checkout fixtures/tc2-marked.md
rm fixtures/tc2-marked.md.bak
```

---

## Expected Outcomes Summary

| Checkpoint | Check | Expected | Points |
|---|---|---|---|
| **Step 1: stdout output** | Markers in prose? | 0 found | 30 |
| **Step 1: stdout output** | Ledger section? | Present | 15 |
| **Step 1: stdout output** | Ledger entries? | 4 entries | 10 |
| **Step 2: --in-place** | Exit code? | 0 | 5 |
| **Step 2: --in-place** | Success message? | "CLAIM STRIP: ..." | 3 |
| **Step 2: --in-place** | Claim count? | "(4 claim(s) ...)" | 2 |
| **Step 3: Ledger format** | Cited + Source? | Correct | 10 |
| **Step 3: Ledger format** | Unverified format? | Correct | 8 |
| **Step 3: Ledger format** | Personal format? | Correct | 7 |
| **Step 5: Non-target** | Research sources? | Unchanged | 3 |
| **Step 5: Non-target** | Code blocks? | Unchanged | 3 |
| **Step 5: Non-target** | Other sections? | Unchanged | 4 |

**Total: 100 points**

---

## Passing Criteria

- **Score ≥ 80/100 → PASS** — Marker stripping works correctly; downstream skills will receive clean prose with full provenance in ledger.
- **Score < 80/100 → FAIL** — Stripping is broken or incomplete; review the failed checkpoints and remediate.

---

## Notes

- **Fixture reset required:** Always reset `tc2-marked.md` before re-running TC2 (`git checkout fixtures/tc2-marked.md`).
- **Deterministic checks:** All criteria are script-verifiable via grep and diff.
- **Ledger is line-based:** The ledger records claim text at the line level (same as the linter's heuristic). Multi-sentence lines with two claims will have one ledger entry for the whole line.
