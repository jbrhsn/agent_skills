---
name: linkedin-post-writer
description: Use when the user wants to turn a source draft, notes file, or rough points into a posting-ready LinkedIn post, OR to score and refine a finished post for virality. It has two paths. The WRITE path turns source notes/draft into linkedin_post.md, applying 2026 LinkedIn algorithm-aware craft (hook engineering, scroll-first structure, no-link-in-body discipline, engagement-bait avoidance) behind mandatory review gates. The REVIEW/REFINE path scores an existing post out of 100 across 5 algorithm-aligned dimensions and produces one refined linkedin_post_revised.md with an itemized change list. Trigger the write path on "write a LinkedIn post from this", "turn these notes into a LinkedIn post", "draft a LinkedIn post"; trigger the review path on "review this LinkedIn post", "score this for virality", "how shareable is this", "refine this post".
---

# LinkedIn Post Writer

Turn a source draft, a notes file, or rough bullet points into a posting-ready LinkedIn post, or take a finished post and score + refine it for virality. Both paths apply platform-specific craft grounded in how LinkedIn's 2026 algorithm actually ranks content — not generic copywriting advice.

## Two paths

- **WRITE path** — source notes/draft/points into a posting-ready `linkedin_post.md`. Use when the user has raw material and wants a post built from it.
- **REVIEW/REFINE path** — an existing finished post scored out of 100 and rewritten once into `linkedin_post_revised.md` with an itemized change list. Use when the user already has a post and wants it scored, reviewed, or refined.

Pick the path from the trigger. If ambiguous (e.g. the user points at a file that already looks like a finished post and just says "make this better"), state which path you're taking with one line of reasoning and confirm before proceeding.

## When to use

- WRITE: user points to a file with notes, bullets, or a rough draft, or pastes raw notes, and wants a LinkedIn-ready post.
- REVIEW/REFINE: user has a finished LinkedIn post (typically `linkedin_post.md`) and wants it scored or refined. Works on any file or pasted text, not only this skill's own output.
- Not for Medium, Twitter/X, or other platforms — this skill is LinkedIn-specific.
- Not for carousel image generation — that's `linkedin-image-prompts` (run after this skill).

## Input

The user must point to a source file (any path, any text format — `.md`, `.txt`, etc.): notes/draft/points for the WRITE path, or a finished post for the REVIEW/REFINE path. **If no file is given, ask for one before doing anything else.** Raw pasted text in the conversation is also acceptable in place of a file, but note in that case there is no source directory to colocate output with — ask the user where to write the output.

## Output

- WRITE path: `linkedin_post.md`
- REVIEW/REFINE path: `linkedin_post_revised.md`, containing, in this order: the score table, the refined post text, then the itemized change list.

Both are written in the **same directory as the source file**. Never write to a fixed `linkedin/` or `drafts/` folder — always colocate with the input.

**Overwrite policy (both paths)**: never silently overwrite. If the target file already exists in that directory, ask: overwrite, write a `-v2` variant (`linkedin_post-v2.md` / `linkedin_post_revised-v2.md`), or pick a new name.

---

## Algorithm mechanics and rubric (shared — defined once, referenced by both paths)

LinkedIn's ranking in 2026 is semantic (reads for meaning, not hashtag density) and favors relevance over recency — a good post can keep surfacing for weeks. Ranking signals, in order of reach impact: **saves** (~5x the reach of a like), **comments** (~2x), then likes. Dwell time (how long someone reads before scrolling on) is a major passive signal. Links in the post body tank dwell time because they invite the reader off-platform. Engagement bait ("comment YES if you agree") is actively detected and suppressed, not rewarded. These facts drive every rule and rubric dimension below — they are not arbitrary style preferences.

The mechanics group into **5 dimensions**. The WRITE path's craft rules produce these qualities; the REVIEW/REFINE path scores them (20 pts each, /100 total); the shared self-audit checks them. Both paths reference this one definition — do not restate it.

### Dimension 1 — Hook strength
LinkedIn truncates at roughly 150–210 characters on mobile before "see more." The hook is the single biggest lever on whether the post gets read at all.
- The first 1–3 lines must earn the tap. **Cold-read test**: read only those lines in isolation — is there tension, specificity, or a withheld promise? If you can already predict what comes next, it fails.
- Use **exact numbers, not round ones** ("847 to 22,400" reads as credible; "20K" reads as marketing).
- No throat-clearing ("Excited to share…", "I've been thinking about…", "In today's post…").
- The cut must land at a point of unresolved tension, ideally mid-thought, never at a full stop.
- Review deduction: throat-clearing, round numbers where exact ones were available, or a hook that resolves too neatly.

### Dimension 2 — Structure & scannability
- **One idea per line.** Any line with more than one idea gets split.
- **Paragraph cap**: 1–3 lines max, blank line between every paragraph. No exceptions for Long Posts or Articles.
- Readable at phone width, not just desktop. **Bullet-ize 3+ parallel items** rather than burying them in a sentence.
- **Do not use em-dashes in writing.**
- Review deduction: dense paragraphs, walls of text, or 3+ parallel items buried in a sentence.

### Dimension 3 — Specificity & save-worthiness
- Real, textured detail (industry, size, specific number) vs. generic statements a stranger could have written. Anonymize names, not texture.
- Does the post contain something reusable — a framework, checklist, or specific insight — worth **saving** for later? Saves drive roughly 5x the reach of a like, more than double a comment — this is the highest-leverage dimension to get right.
- Review deduction: vague nouns, unanchored claims, or insight so generic it earns a like but nothing more.

### Dimension 4 — Engagement design
- Close with a **sharp, specific question** — answerable in one sentence, genuinely interesting, not "Thoughts?" and not yes/no.
- **Never use engagement-bait phrasing** ("Comment YES if...", "Tag someone who...", "Repost if..."). LinkedIn's 2026 spam filter actively detects and suppresses this — it reduces reach, it does not increase it.
- Review deduction: treat any detected engagement-bait phrase as a near-disqualifier for this dimension.

### Dimension 5 — Platform mechanics
- **Zero URLs in the post body**, ever. A link invites the reader off-platform, which tanks dwell time. If a source or link matters, it goes in the **first comment**, or is named in prose ("I read a good piece on this by [person]").
- **No AI-voice crutch phrases**: "it's important to note", "in today's fast-paced world", "at the end of the day", "dive deep", "delve into", "game-changer", "leverage" (as a verb).
- **Hashtags**: 0–3, relevant, placed at the end. Stuffing is a spam signal under the semantic algorithm, not a reach booster.
- Review deduction: any body URL, crutch phrase, or hashtag stuffing.

### Sound-human overlay (applies while writing/refining)
- Read the draft aloud (coffee test) — rewrite any sentence that would sound stilted said to a colleague's face.
- Leave one rough edge in: a sentence starting with "And," a fragment, a slightly-too-long line. A perfectly symmetrical post reads as manufactured.

---

## WRITE path

### Content types

| Type | Target length | Best fit |
|---|---|---|
| Short Post | 100–300 words, 8–15 lines | Single sharp insight, story beat, opinion |
| Long Post | 600–1200 words, 25–45 lines | Narrative, lesson, or argument, native feed |
| Article | 1000–2500 words | Structured argument with multiple distinct sections |

### Narrative frames
Pick the frame that matches what actually happened — never bend a real detail to fit a better-looking template.

| Frame | Fill-in |
|---|---|
| Before → After → Bridge | "I used to [struggle]. Now [result]. Here's what changed." |
| Mistake → Realization → Shift | "I did [X] for years. Then [moment] made me realize [Y]." |
| Challenge → Action → Result | "[I] was stuck on [problem]. Here's what we tried, here's what happened." |
| Contrarian stance | "[Widely accepted belief]. I disagree. Here's why." |

### Unit W1 — Intake & type selection
- **Goal/scope**: read the source and lock the content type.
- **Inputs**: source file path or pasted text; user's stated type if any.
- **Do**: read the source. If no source is given, stop and ask. Detect the content type from the source substance if unspecified, state it with one line of reasoning.
- **Self-verify**: confirm a source was actually read and a single type is selected.
- **STOP GATE (hand back)**: present the detected type + reasoning and **stop to confirm** before drafting. Never silently default. → Hand control back to the user/orchestrator for the type decision.
- **Report contract**: `source read: <path> | type: <type> (<reason>) | awaiting: type confirmation`.

### Unit W2 — Hook engineering
- **Goal/scope**: produce 5 hook variants and hand back for selection.
- **Inputs**: confirmed content type + source substance.
- **Do**: generate **5 hook variants**, one per mode, applying Dimension 1 (cold-read test, exact numbers, no throat-clearing, cut on unresolved tension):
  1. **Contrarian**: "[Common belief] is wrong. Here's what I've actually seen."
  2. **Curiosity gap / number+contrast**: a specific small input leading to a specific large outcome.
  3. **Confession**: "I was wrong about [X] for [time]. Here's what changed my mind."
  4. **Mid-scene open**: drop the reader into a specific moment already in progress, no setup.
  5. **Problem-naming**: name the reader's specific pain more precisely than they'd name it themselves.
- **Self-verify**: each variant passes the cold-read test and ends on unresolved tension; the 1–2 strongest are marked.
- **STOP GATE (hand back)**: present **only** the 5 hooks, labeled by mode, strongest marked. **Do not draft the body until a hook is selected or mixed.** → Hand control back for hook selection.
- **Report contract**: `5 hooks produced (modes: contrarian/curiosity/confession/mid-scene/problem) | strongest: #N,#M | awaiting: hook pick or mix`.

### Unit W3 — Draft
- **Goal/scope**: write the full piece from the selected hook.
- **Inputs**: the **selected hook** (or mix) + confirmed content type. Selecting a narrative frame is part of this unit.
- **Do**:
  - State the narrative frame chosen and why (one line).
  - Write the body applying Dimensions 2, 3, 5 and the sound-human overlay: one-idea-per-line, 1–3 line paragraphs, specificity over vague nouns, no body links, no crutch phrases. Line-count gut check on Short/Long Posts (under ~10 lines is likely thin; over ~18, cut a paragraph the reader can infer).
  - Draft **3 closing-question candidates** (Dimension 4), mark the recommended one.
  - Add 0–3 hashtags if relevant.
- **Self-verify**: run **Unit W4 (self-audit)** before reporting — the draft is not "done" until the audit passes or its flags are surfaced.
- **Report contract**: `draft complete | frame: <frame> | closing-question candidates: 3 (rec: #N) | self-audit: <PASS | N flagged, fixed | N flagged, unresolved>`.

### Unit W4 — Self-audit (run inside W3, before any hand-back)
- **Goal/scope**: verify the draft against the shared 5 dimensions before showing the user. This is the doer's own verification step.
- **Inputs**: the drafted post.
- **Do**: check each row and record PASS or FLAGGED with a one-line note. Fix all FLAGGED items **once**. If something still fails after the fix, surface it to the user rather than looping silently.

| Check | Pass criteria | Dimension |
|---|---|---|
| Hook fold test | First 1–3 lines under ~210 chars; ends on unresolved tension | 1 |
| Line density | No paragraph over 3 lines; blank line between paragraphs | 2 |
| Specificity | No vague nouns where a real detail was available | 3 |
| Engagement-bait scan | No "comment YES", "tag someone", "repost if" phrasing | 4 |
| Closing question | Specific, not yes/no, not "Thoughts?" | 4 |
| Link discipline | Zero URLs in body | 5 |
| Crutch-phrase / em-dash scan | None of the banned phrases; no em-dashes | 5 |

- **Report contract**: folded into W3's report (`self-audit: PASS` or the flagged/unresolved counts).

### Unit W5 — Review-first (hand back before persisting)
- **Goal/scope**: get human approval before writing any file.
- **Inputs**: full draft + W4 audit results + frame + content type.
- **STOP GATE (hand back)**: present all of the above and **stop**. Ask the user to approve, request edits, or reject. **Do not write any file yet.** → Hand control back for approval. If running non-interactively, note the gate as "skipped — auto-proceeding with output as drafted" and continue rather than silently omitting it.
- **Report contract**: `awaiting: approve / edit / reject | nothing written yet`.

### Unit W6 — Persist
- **Goal/scope**: write the approved post to disk.
- **Inputs**: approved draft + source directory.
- **Do**: after approval, write `linkedin_post.md` in the same directory as the source file. Apply the overwrite policy.
- **Self-verify**: confirm the file exists at the expected path and matches the approved text.
- **Report contract**: `wrote: <exact path> | overwrite policy: <applied choice>`.

---

## REVIEW/REFINE path

### Unit R1 — Intake
- **Goal/scope**: read the finished post to be reviewed.
- **Inputs**: source file path or pasted text.
- **Do**: read the source post. If none given, stop and ask. If pasted text, ask where to write the output.
- **Self-verify**: confirm the source was read and an output directory is known.
- **Report contract**: `source read: <path> | output dir: <dir>`.

### Unit R2 — Diagnose & score
- **Goal/scope**: score the post against the shared 5 dimensions.
- **Inputs**: the source post + the shared rubric (Dimensions 1–5 above).
- **Do**: for each of the 5 dimensions, give a brief diagnostic — what's strong, what's weak, one-line reason grounded in that dimension. Do not skip a dimension even if clearly strong ("no issues" is fine). Score each out of 20 and sum to /100. Present as a table.
- **Self-verify**: all 5 dimensions scored; sum equals the /100 total.
- **Report contract**: `scored: <X>/100 | flagged dimensions: <list or none>`.

### Unit R3 — Refine
- **Goal/scope**: produce **one** refined version fixing every flagged weakness.
- **Inputs**: the source post + the flags from R2.
- **Do**: rewrite once to fix every weakness flagged in R2, without introducing new ones. If a fix would require information not in the source (e.g. a real statistic the post lacks), flag it as a note rather than inventing a fact. This path scores and rewrites — it does **not** offer multiple stylistic variants.
- **Self-verify (self-audit against own output)**: re-run the shared 5-dimension rubric against the **refined** version before finalizing. If the rewrite introduced a regression on any dimension, fix it before proceeding.
- **Report contract**: `refined version produced | re-checked rubric on refined text: <PASS | fixed N regressions> | unfixable-for-lack-of-info: <list or none>`.

### Unit R4 — Itemize changes
- **Goal/scope**: account for every flagged weakness.
- **Inputs**: R2 flags + R3 refined version.
- **Do**: list each change, one line each, as **what changed → why** (tied to the specific dimension it improves). Every weakness flagged in R2 must be accounted for — if flagged but not fixed, say so explicitly and why (e.g. "insufficient information in source to add a specific number here").
- **Self-verify**: every R2 flag maps to either a change line or an explicit not-fixed note.
- **Report contract**: `change list: N items | R2 flags all accounted for: yes`.

### Unit R5 — Present & confirm (hand back)
- **Goal/scope**: show results and get a lightweight go-ahead before writing.
- **Inputs**: score table, diagnostics, refined version, change list.
- **STOP GATE (hand back, lightweight)**: present all of the above. This is a **lightweight confirm**, not a full review-first block. If the user asks for another pass, treat the just-refined version as the new input and repeat R2–R4. → Hand control back for confirm-or-another-pass.
- **Report contract**: `presented: score + refined + changes | awaiting: confirm or another pass`.

### Unit R6 — Write
- **Goal/scope**: persist the review artifact.
- **Inputs**: confirmed refined version + output directory.
- **Do**: write `linkedin_post_revised.md` containing, in order: the score table, the refined post, then the itemized change list. Apply the overwrite policy.
- **Self-verify**: confirm the file exists at the expected path with the three sections in the correct order.
- **Report contract**: `wrote: <exact path> | sections: score → refined → changes | overwrite policy: <applied choice>`.

### Output format (`linkedin_post_revised.md`)

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

---

## Handoff

- After the WRITE path writes `linkedin_post.md`, mention the built-in **REVIEW/REFINE path** can score and refine it further into `linkedin_post_revised.md` in the same folder.
- After either path, mention that `linkedin-image-prompts` can generate carousel/image prompts from the output file (`linkedin_post.md` or `linkedin_post_revised.md`) — it writes its output to the same folder.
