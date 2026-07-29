---
name: linkedin-post-reviewer
description: Use when the user wants to review, score, or refine a finished LinkedIn post for virality and shareability. Scores the piece across 5 algorithm-aligned dimensions (hook, structure, save-worthiness, engagement design, platform mechanics), produces one refined version, and writes both the score and an itemized list of changes to linkedin_post_revised.md next to the source file. Trigger on "review this LinkedIn post", "score this for virality", "how shareable is this", "refine this post".
---

# LinkedIn Post Reviewer

Score a finished LinkedIn post against 2026 algorithm-aligned virality dimensions, then produce **one refined version** that fixes the flagged weaknesses. This skill scores and rewrites — it does not offer multiple stylistic variants (that's a different job; for multiple angle options, a separate editorial-variants skill would apply).

## When to use

- User has a finished LinkedIn post (typically `linkedin_post.md`) and wants it scored, reviewed, or refined for virality/shareability.
- Works on any pasted text or file, not only output from `linkedin-post-writer`.

## Input

A file path to the finished post. If not given, ask. Pasted text is also acceptable — in that case ask where to write the output, since there's no source directory to colocate with.

## Output

`linkedin_post_revised.md`, written in the **same directory as the source file**. Contains, in this order: the score table, the refined post text, and an itemized list of improvements made.

**Overwrite policy**: never silently overwrite. If `linkedin_post_revised.md` already exists, ask: overwrite, write `linkedin_post_revised-v2.md`, or pick a new name.

---

## Scoring rubric (5 dimensions, 20 points each, /100 total)

Grounded in how LinkedIn's 2026 algorithm actually ranks posts — not generic writing-quality heuristics.

### 1. Hook strength (20 pts)
- Does the first 1–3 lines (~150–210 characters before "see more") earn the tap?
- Cold-read test: read only those lines in isolation — is there tension, specificity, or a withheld promise?
- Deduct for throat-clearing ("Excited to share…", "I wanted to…"), round numbers where exact ones were available, or a hook that resolves too neatly (no reason to keep reading).

### 2. Structure & scannability (20 pts)
- One idea per line; paragraphs capped at 1–3 lines with blank lines between.
- Readable at phone width, not just desktop.
- Deduct for dense paragraphs, walls of text, or 3+ parallel items buried in a sentence instead of bulleted.
- Do not use em-dashes in writing.

### 3. Specificity & save-worthiness (20 pts)
- Real, textured detail vs. generic statements a stranger could have written.
- Does the post contain something reusable — a framework, checklist, or specific insight — worth **saving** for later? Saves currently drive roughly 5x the reach of a like in LinkedIn's ranking, more than double a comment — this is the highest-leverage dimension to get right.
- Deduct for vague nouns, unanchored claims, or insight so generic it earns a like but nothing more.

### 4. Engagement design (20 pts)
- Closing question: specific, answerable in one sentence, genuinely interesting — not "Thoughts?" and not yes/no.
- No engagement-bait phrasing ("Comment YES if...", "Tag someone who...", "Repost if you agree") — LinkedIn's 2026 spam filter actively detects and suppresses this pattern; it costs reach rather than helping it.
- Deduct heavily (treat as a near-disqualifier) for any detected engagement-bait phrase.

### 5. Platform mechanics (20 pts)
- Zero URLs in the post body (links tank dwell time, a core ranking signal — should be in the first comment instead, if needed at all).
- No AI-voice crutch phrases ("delve into", "it's important to note", "in today's fast-paced world", "game-changer", "leverage" as a verb).
- Hashtags: 0–3, relevant, not stuffed.
- Deduct for any body URL, crutch phrase, or hashtag stuffing.

**Overall score** = sum of the 5 dimensions, out of 100.

---

## Workflow

### Step 1 — Intake
Read the source post (file or pasted text). If not given, ask.

### Step 2 — Diagnose
For each of the 5 dimensions, give a brief diagnostic: what's strong, what's weak, with a one-line reason grounded in the rubric above. Do not skip a dimension even if it's clearly strong — a short "no issues" note is fine.

### Step 3 — Score
Score each dimension out of 20, sum to the overall /100. Present as a table.

### Step 4 — Refine
Produce **one refined version** that fixes every flagged weakness from Step 2. Do not introduce new weaknesses while fixing others — re-check the rubric against the refined version before finalizing. If a fix would require information not present in the source (e.g. a real statistic the post is missing), flag it as a note rather than inventing a fact.

### Step 5 — Itemize changes
List each change made, one line each, in the form: **what changed → why** (tie back to the specific dimension it improves). This list must account for every weakness flagged in Step 2 — if something was flagged but not fixed, say so explicitly and why (e.g. "insufficient information in source to add a specific number here").

### Step 6 — Present and confirm
Show the score table, diagnostics, refined version, and change list to the user. This is a **lightweight confirm**, not a full review-first block — but if the user asks for another pass, treat the just-refined version as the new input and repeat Steps 2–5.

### Step 7 — Write
Write `linkedin_post_revised.md` containing, in order: the score table, the refined post, and the itemized change list. Apply the overwrite policy above. Confirm the exact path to the user.

---

## Output format (`linkedin_post_revised.md`)

```markdown
# LinkedIn Post Review

## Score

| Dimension | Score | Notes |
|---|---|---|
| Hook strength | X/20 | ... |
| Structure & scannability | X/20 | ... |
| Specificity & save-worthiness | X/20 | ... |
| Engagement design | X/20 | ... |
| Platform mechanics | X/20 | ... |
| **Overall** | **X/100** | |

## Refined Version

<full refined post text>

## Improvements Made

- <change> → <why, tied to dimension>
- ...
```

## Handoff

If the refined version needs new visuals, `linkedin-image-prompts` can generate prompts from `linkedin_post_revised.md` the same way it would from the original.
