# TC3: Clarifying-Questions Gate Behavioral Test

## Objective

Verify that the skill's new clarifying-questions gate (Goal 1) works as designed in the workflow:

1. **Triggers for Expansion/Mixed mode** — When input is sparse (bullets/notes), the skill pauses and asks clarifying questions before building the draft
2. **Skips for Cleanup mode** — When input is near-complete (already a draft), the gate is skipped
3. **Questions are focused** — Asks 5–8 targeted questions about facts, numbers, sources, anecdotes, audience, and takeaway
4. **Questions target claim-risky gaps** — Questions address gaps that would otherwise become `[UNVERIFIED]` claims
5. **Non-interactive fallback** — In non-interactive mode, the gate is skipped with a documented note
6. **Documented in SKILL.md** — Step 1 of the workflow clearly states when and how the gate triggers

---

## Test Criteria (Weighted Rubric: 100 points)

### 1. Gate Triggers in Expansion/Mixed Modes (25 points)

- **Sparse input detected as Expansion** (15 points)
  - When given `tc3-sparse-input.md` (rough bullets/notes), the skill detects mode = Expansion
  - The skill outputs: `Detected mode: Expansion — input is sparse bullets/notes`
  - The gate asks clarifying questions before drafting
  - **Evidence:** Interaction shows questions asked before "Building the draft..." message

- **Near-complete input detected as Cleanup** (10 points)
  - When given a near-complete draft (e.g., already a well-formed paragraph), the skill detects mode = Cleanup
  - The skill skips the clarifying-questions gate
  - **Evidence:** Interaction shows drafting starts immediately without questions

**Scoring:**
- Expansion mode correctly detected: +8 points
- Clarifying-questions gate actually triggered: +7 points
- Cleanup mode correctly detected: +5 points
- Cleanup gate skipped: +5 points

### 2. Question Batch is Focused (20 points)

- **Asks ≤ ~8 questions** (5 points)
  - The skill asks no more than 8 questions (ideally 5–7)
  - Questions are distinct (no repetition)
  - **Evidence:** Count the questions in the interaction transcript

- **Questions are distinct & non-repetitive** (8 points)
  - Each question asks for different information (not duplicate intent)
  - No circular or redundant phrasing
  - **Evidence:** Read through and verify no two questions ask the same thing

- **Prompts are clear & actionable** (7 points)
  - Questions are worded clearly (no ambiguity)
  - Each question has a clear intent (gather a specific fact, source, or context)
  - Questions use conversational tone, not overly formal
  - **Evidence:** Questions are understandable and specific

**Scoring:**
- If ≤ 8 questions: +5 points (full); if 9–12 questions: +2 points; if > 12: +0 points
- Distinct questions: +8 points (full); if some repetition: +4–6 points
- Clear & actionable: +7 points (full); if vague or unclear: +3–5 points

### 3. Questions Target Claim-Risky Gaps (30 points)

- **Address statistics/numbers that would become `[UNVERIFIED]`** (12 points)
  - The fixture contains sparse claims like "70% of startups" and "5x growth"
  - The skill asks: "Do you have a source for the 70% statistic?" or "Can you cite the 5x growth claim?"
  - Goal: convert guesses into either real cited facts or explicit `[UNVERIFIED]` labels
  - **Evidence:** Questions directly reference numbers/stats in the input

- **Ask for sources (URLs, references)** (10 points)
  - For any statistical or authoritative claim, the skill asks "Where did this come from?" or "Do you have a link?"
  - Intent: provide citations (`[source: ...]`) rather than shipping unbacked claims
  - **Evidence:** At least 2–3 questions ask for sources or citations

- **Ask for anecdote context (personal experience clarity)** (8 points)
  - If the input mentions personal experience (e.g., "I saw this happen"), the skill asks clarifying details
  - Example: "Can you describe what you observed?" or "When did this happen in your context?"
  - Intent: convert vague anecdotes into concrete `[personal]` claims
  - **Evidence:** Questions ask about first-hand experience or observational context

**Scoring:**
- Questions address numbers/stats: +12 points (full); if only vaguely: +6–9 points; if not at all: +0
- Questions ask for sources: +10 points (full); 1–2 questions only: +5–7 points; none: +0
- Questions ask about anecdotes: +8 points (full); vague: +4–5 points; none: +0

### 4. Skips in Cleanup Mode (15 points)

- **Near-complete input auto-detected as Cleanup** (8 points)
  - When given input that is already a mostly-complete draft (e.g., full paragraphs with flow), the skill detects Cleanup mode
  - **Evidence:** Skill outputs "Detected mode: Cleanup — input is already near-complete"
  - Skill does NOT ask clarifying questions

- **Clarifying-questions gate is skipped** (7 points)
  - No pause for questions occurs; drafting begins immediately
  - **Evidence:** Interaction shows "Building draft..." message without intervening questions

**Scoring:**
- Cleanup auto-detected: +8 points (full); if detected but gate not skipped: +4 points
- Gate skipped: +7 points (full); if some questions asked anyway: +3 points

### 5. Non-Interactive Fallback (10 points)

- **Non-interactive runs skip questions with a note** (7 points)
  - When run in non-interactive mode (e.g., piped input, no TTY), the skill detects this
  - The skill outputs: `clarifying-questions gate skipped — non-interactive mode`
  - Drafting proceeds without waiting for user input
  - **Evidence:** Non-interactive run completes without hanging or error

- **Behavior documented in SKILL.md step 1** (3 points)
  - SKILL.md section 1 (Intake + detect mode) clearly states the fallback: "If running non-interactively, skip the questions, note 'clarifying-questions gate skipped — non-interactive mode,' and proceed."
  - **Evidence:** Text found in SKILL.md

**Scoring:**
- Non-interactive skip + message: +7 points (full); if skipped but no message: +3 points; if hangs or errors: +0
- Documented in SKILL.md: +3 points (full); if not documented: +0

---

## Test Steps

### Setup
The skill is invoked interactively (e.g., via the OpenCode agent interface or directly as a function call). The fixture `tc3-sparse-input.md` contains sparse bullets simulating user input.

### Step 1: Interactive run with sparse input (Expansion mode)
**Context:** Simulate a user providing sparse bullet notes and asking the skill to build a draft.

**Input:**
```
- React is very popular
- I think 70% of startups use it
- My company switched from Vue
- Performance improved a lot
- TypeScript adoption is high
```

**Expected interaction flow:**
1. Skill reads input
2. Outputs: `Detected mode: Expansion — input is sparse bullets/notes; building draft`
3. **Pauses and asks 5–8 clarifying questions before drafting**, for example:
   - "Do you have a source for the 70% statistic?"
   - "When did your company switch from Vue to React?"
   - "Can you quantify 'improved a lot'? (e.g., faster render times, smaller bundle?)"
   - "Who is your target audience for this draft?"
   - "What's your core takeaway? (e.g., why React won, how to migrate, performance benefits?)"
   - "Any specific TypeScript benefits from your experience?"
4. User provides answers
5. Skill builds the draft with answers incorporated, minimizing `[UNVERIFIED]` claims

**Scoring:**
- Expansion mode detected: +8 points
- Clarifying-questions gate triggered: +7 points
- Questions follow the 5–8 count: +5 points (or proportional deduction)
- Questions address numbers/sources: +12 points (or proportional)
- Questions ask for anecdote details: +8 points (or proportional)

### Step 2: Interactive run with near-complete input (Cleanup mode)
**Context:** Provide a near-complete draft paragraph.

**Input:**
```
React has emerged as the dominant JavaScript framework for building user interfaces. 
Many organizations are adopting it, and performance benefits are significant. 
In my experience at Company X, we saw measurable improvements after migrating from Vue.
```

**Expected interaction flow:**
1. Skill reads input
2. Outputs: `Detected mode: Cleanup — input is already near-complete`
3. **Skips the clarifying-questions gate**
4. Proceeds directly to: `Building the source draft...`
5. Builds the draft without asking clarifying questions

**Scoring:**
- Cleanup mode detected: +5 points
- Clarifying-questions gate skipped: +7 points

### Step 3: Verify SKILL.md documentation
**Check:** Open SKILL.md and navigate to **step 1: "Intake + detect mode"**

**Expected text:**
```
**For Expansion and Mixed modes: clarifying-questions gate.** 
Before building the draft, pause and ask the user a focused batch 
of clarifying questions (5–8 questions max, not an endless round) 
to gather missing facts, numbers, sources, anecdotes, and context. 
... If running non-interactively, skip the questions, note 
"clarifying-questions gate skipped — non-interactive mode," and proceed.
```

**Scoring:**
- Step 1 mentions the gate: +1 point
- Mentions Expansion/Mixed only: +1 point
- Specifies 5–8 questions: +1 point
- Non-interactive fallback documented: +0 points (already scored in Step 5)

---

## Expected Outcomes Summary

| Scenario | Expected Behavior | Evidence | Points |
|---|---|---|---|
| **Sparse input (tc3-sparse-input.md)** | Expansion mode detected | "Detected mode: Expansion" | 8 |
| **Sparse input** | Clarifying questions asked | 5–8 questions appear | 7 |
| **Sparse input** | Questions focused | Distinct, ≤8 total | 5 |
| **Sparse input** | Questions target gaps | Ask about 70%, sources, experience | 30 |
| **Near-complete input** | Cleanup mode detected | "Detected mode: Cleanup" | 5 |
| **Near-complete input** | Gate skipped | No questions asked | 7 |
| **SKILL.md step 1** | Gate documented | Text found in SKILL.md | 3 |
| **Non-interactive** | Gate skipped + message | Message in output (if applicable) | 7 |

**Total: 100 points**

---

## Passing Criteria

- **Score ≥ 80/100 → PASS** — The clarifying-questions gate is working as designed; Goal 1 is validated.
- **Score < 80/100 → FAIL** — The gate is missing, incomplete, or not triggered correctly; review the failed steps and remediate.

---

## Evaluation Guidelines (Rubric Notes)

This test is **behavioral and judgment-based**, unlike TC1 and TC2 (which are script-verifiable). The evaluator should:

1. **Run the skill interactively** with the sparse fixture and observe whether questions are actually asked
2. **Count and categorize questions** against the rubric criteria
3. **Assess question quality** (clarity, relevance to claim-risky gaps)
4. **Verify documentation** in SKILL.md
5. **Check for the fallback behavior** if running non-interactively (or document that it was not tested)

**Scoring discretion:**
- If questions are 7 out of 8 criteria-perfect, deduct at most 5–10 points (not a full criterion loss)
- If questions address most but not all claim-risky gaps, award 20–25 points (not full 30)
- If documentation is present but unclear, award 1–2 points (not full 3)

---

## Notes

- **Behavioral test:** Unlike TC1 and TC2, this test requires active skill interaction and human judgment. No automated harness can verify that questions are "focused" or "clearly worded."
- **Fixture fixture:** `tc3-sparse-input.md` contains realistic rough bullets simulating what a user might provide.
- **Real-world validation:** The best validation is a reviewer running the skill with the sparse fixture and evaluating the interaction against the rubric.
- **Documentation check:** SKILL.md must explicitly state when and how the gate triggers, which can be verified objectively.
