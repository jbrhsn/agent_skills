---
name: medium-article-writer
description: Use when the user wants to turn a source draft, notes file, or rough points into a publish-ready Medium article, OR to score and refine a finished Medium story for reach and Boost-worthiness. It has two paths. The WRITE path turns source notes/draft into medium_article.md, applying Medium-specific craft grounded in Medium's official Distribution Guidelines, AI-content policy, and earnings mechanics (title+subtitle+cover as a unit, read-ratio-driven scannability, first-hand originality, relevant tagging, soft value-tied CTAs, paywall recommendation) behind mandatory review gates. The REVIEW/SCORE path scores an existing article out of 100 across 5 distribution-aligned dimensions and produces one refined medium_article_reviewed.md with an itemized change list. Trigger the write path on "write a Medium article from this", "turn these notes into a Medium article", "draft a Medium post/story"; trigger the review path on "review this Medium article", "score this Medium article", "will this get Boosted", "refine this Medium story".
---

# Medium Article Writer

Turn a source draft, a notes file, or rough bullet points into a publish-ready Medium article, or take a finished article and score + refine it for reach and Boost-worthiness. Both paths apply platform-specific craft grounded in how Medium's distribution system, curation, and Partner Program actually reward content — not generic copywriting advice. The verified facts are baked into the rubric below; an executor does not need external research.

## Two paths

- **WRITE path** — source notes/draft/points into a publish-ready `medium_article.md`. Use when the user has raw material and wants an article built from it.
- **REVIEW/SCORE path** — an existing finished article scored out of 100 and rewritten once into `medium_article_reviewed.md` with an itemized change list. Use when the user already has an article and wants it scored, reviewed, or refined.

Pick the path from the trigger. If ambiguous (e.g. the user points at a file that already looks like a finished article and just says "make this better"), state which path you're taking with one line of reasoning and confirm before proceeding.

## When to use

- WRITE: user points to a file with notes, bullets, or a rough draft, or pastes raw notes, and wants a Medium-ready article.
- REVIEW/SCORE: user has a finished Medium article (typically `medium_article.md`) and wants it scored, reviewed, or refined. Works on any file or pasted text, not only this skill's own output.
- Not for LinkedIn, Twitter/X, or other platforms — this skill is **Medium-specific**. Medium's rules (title+subtitle+cover unit, read-ratio, three-tier human curation, member-read paywall economics) do not match LinkedIn's feed-algorithm rules; do not import them.
- Not for cover/inline image generation — that's `medium-image-prompts` (run after this skill).

## Input

The user must point to a source file (any path, any text format — `.md`, `.txt`, etc.): notes/draft/points for the WRITE path, or a finished article for the REVIEW/SCORE path. **If no file is given, ask for one before doing anything else.** Raw pasted text in the conversation is also acceptable in place of a file, but note in that case there is no source directory to colocate output with — ask the user where to write the output.

## Output

- WRITE path: `medium_article.md`
- REVIEW/SCORE path: `medium_article_reviewed.md`, containing, in this order: the score table, the refined article text, then the itemized change list.

Both are written in the **same directory as the source file**. Never write to a fixed `medium/` or `drafts/` folder — always colocate with the input.

**Write-first, then review (both paths).** The full article/refined body is **written to its file FIRST — as a draft** — and only then handed back for review. The review gate carries **only a pointer to the file plus a short summary; the full body is NEVER pasted into chat.** On an edit/another-pass request, re-edit the file **in place** and re-point to it — do not re-dump the body into chat.

**Overwrite policy (both paths).** The **first draft write of this run** to the canonical name (`medium_article.md` / `medium_article_reviewed.md`) is expected — it is the draft under review — and subsequent edit rounds update that same file **in place**. This does **not** trigger the overwrite prompt. The overwrite prompt applies only when a file of that name **already exists from a PRIOR run/session** at the first write: never silently overwrite it — ask to overwrite, write a `-v2` variant (`medium_article-v2.md` / `medium_article_reviewed-v2.md`), or pick a new name. (Once you have chosen the working file for this run, in-place edits within the run proceed without re-prompting.)

---

## Distribution mechanics and rubric (shared — defined once, referenced by both paths)

Medium distributes stories through **three tiers**: **Network** (your followers and topic feeds), **General Distribution** (recommended broadly across the site to non-followers), and **Boost** (the human-curated top tier that gets the widest reach). Curators are human; automated eligibility gates sit under them. Earnings in the Partner Program come **only from paying-member reads on paywalled ("member-only") stories** — driven by member read time (a member reading ≥30s) plus engagement points from members (claps, highlights, replies), with a Boost bonus, a +5% external-traffic bonus (higher for search and email referrals), and a one-time conversion bonus when a non-member subscribes specifically to read a story. Publications and self-publishing use the **identical payout formula** — a publication only helps reach, it does not change the math. These facts drive every rule and rubric dimension below; they are not arbitrary style preferences. (Source basis: Medium's official Distribution Guidelines updated 2026-06-29, its AI-content policy, and its stats/earnings help pages; retrieved 2026-07-30.)

**CRITICAL GUARDRAIL — never fabricate earnings figures.** No live source verified current per-read or per-story dollar amounts. This skill must never promise, quote, or invent specific income numbers ("$500/month", "$0.05 per read", etc.). Describe the *mechanics* of how earnings work; never a dollar amount.

**CRITICAL TRAP — "about Medium" = Network-only.** Stories whose subject is Medium itself, or making money on Medium, are forced to **Network-only distribution** regardless of quality. If a drafted or reviewed article's core topic is Medium/Medium-earnings, flag it explicitly: it cannot reach General Distribution or Boost, and the writer should know that before publishing.

**WRITING AUTHENTICITY.** Undisclosed AI-generated *writing* is capped at Network-only, cannot be paywalled, and risks Partner Program removal. This skill is a **human-authorship aid**, not an AI ghostwriter: it structures, sharpens, and tightens the writer's own material and lived experience. It must **never fabricate first-hand experience, quotes, or facts**. (Image disclosure — AI-generated images must be caption-disclosed — is real but is `medium-image-prompts`' job; only the writing-authenticity rule is enforced here.)

The mechanics group into **5 dimensions**. The WRITE path's craft rules produce these qualities; the REVIEW/SCORE path scores them (20 pts each, /100 total); the shared self-audit checks them. Both paths reference this one definition — do not restate it.

### Dimension 1 — Title + subtitle + cover as a unit / Hook
Medium judges the **title, subtitle, and cover image together** as the entry unit; curation weighs whether they invite the reader in *and* whether the body delivers on that promise. **Overpromising / clickbait is the #1 curation failure** — a title the body doesn't pay off gets demoted, not Boosted.
- Effective title patterns: **curiosity gap, benefit-driven, numbered list, how-to, contrarian, specific-result.** The sweet spot is **clarity + a specific promise + exactly one turn of intrigue** — not maximum mystery.
- **Subtitle must pay off the title, not repeat it** — add the angle, stakes, or specificity the title withheld.
- Title norms: roughly **≤60 characters**, **Title Case**, no all-caps and no emoji-stuffing.
- **Opening (first 1–3 sentences)**: a startling fact, a pull question, or an in-media-res drop — short and tension-loaded. A weak first line loses most readers before they reach the point (bounce), which craters the read ratio (Dimension 2).
- Review deduction: title/body mismatch (overpromise), a subtitle that merely restates the title, all-caps/emoji clickbait, or a flat throat-clearing opener.

### Dimension 2 — Read-ratio & scannability / structure
Medium stat definitions: a **View** = reader stayed ≥5s; a **Read** = reader stayed ≥30s (this is also the earnings-relevant member-read threshold). **Read ratio = Reads / Views** is the key implicit quality signal — the whole structure exists to keep a reader past 30 seconds and moving down the page.
- Rewarded structure: **section headings, short paragraphs, blockquotes / pull quotes, bulleted lists, scannable formatting.** Medium states correct formatting is one of many indicators of good craftsmanship and is an explicit curation signal.
- **Length**: the famous "7-minute" figure is 2013 pre-paywall data — **heuristic only, never a target.** Medium's current line is "the right length for the job." Treat **~4–8 minutes** as a practical range, not a goal; cut anything that doesn't earn its place.
- Review deduction: walls of text, no headings/subheads, no scannable elements across a long piece, or padding that lowers the likely read ratio.

### Dimension 3 — Originality & first-hand value (share-worthiness)
Boost-worthy content is defined by Medium as content that **makes someone happy to pay for their membership and/or want to share it**, with readers **still thinking about the story days later**.
- **First-hand experience and originality beat generic listicles and rehash.** Both emotional resonance *and* practical utility qualify; leaving the reader with **multiple possible takeaways** increases impact.
- **Avoid unconstructive negativity / rage-bait** — it is explicitly disqualified from General Distribution.
- Enforce **writing authenticity** (see guardrail above): never manufacture lived experience or facts to look more original — flag the gap instead.
- Review deduction: rehash a stranger could have written, no first-hand angle, single thin takeaway, or rage-bait framing.

### Dimension 4 — Distribution & tagging
The three tiers (Network → General → Boost) gate reach; eligibility rules matter as much as craft.
- **≤5 topics/tags, and they must be genuinely relevant.** Irrelevant tag-spam, or roughly ~20 @-mentions, **disqualifies from General Distribution.**
- **"About Medium" trap** (see above): a story about Medium or Medium-earnings is forced to Network-only — flag it.
- **Writing authenticity** (see above): undisclosed AI-written text caps at Network-only and blocks the paywall — this dimension is where that self-referential distribution penalty lives.
- Review deduction: >5 tags, irrelevant/spammy tags, @-mention flooding, an unflagged "about Medium" topic, or writing that reads as machine-generated and undisclosed.

### Dimension 5 — Monetization & endings (CTA + paywall)
Earnings flow **only from paying-member reads on paywalled stories** (see mechanics above). So monetization is a real, checkable property of the draft.
- **Recommend enabling the paywall / "member-only"** when the writer wants to earn, and prompt them to consider it — with the one caveat that undisclosed-AI or "about Medium" pieces can't be paywalled/monetized normally.
- **Endings/CTAs must be soft, single, and value-tied.** Medium **demotes self-serving sales-pitch endings** and stories whose primary purpose is gathering signups, selling, or soliciting. A genuine, single follow/subscribe invite tied to the article's value is fine; a hyped multi-link pitch is a demotion risk.
- **Never fabricate earnings figures** (see guardrail) — no dollar amounts anywhere.
- Review deduction: hard/multi-link sales pitch ending, a story whose main point is soliciting signups, any invented income number, or no paywall recommendation where monetization is a stated goal.

### Sound-human overlay (applies while writing/refining)
- Read the draft aloud — rewrite any sentence that sounds machine-flat or padded. Medium rewards a real voice, and authentic writing is a distribution requirement, not a nicety.
- Do not sand off the writer's specific voice and lived detail in the name of polish — texture is what makes Dimension 3 pass.

---

## WRITE path

### Article types

| Type | Best fit |
|---|---|
| Personal essay / story | A lived experience with a turn; strongest for first-hand originality (Dim 3) |
| How-to / tutorial | Reader can act on it; strong practical-utility share-worthiness |
| Listicle with substance | Numbered structure, but each item carries real first-hand value (not filler) |
| Opinion / contrarian | A specific stance with earned reasoning; constructive, not rage-bait |
| Analysis / deep-dive | Structured argument across distinct sections; leans on Dim 2 structure |

### Unit W1 — Intake & article-type selection
- **Goal/scope**: read the source and lock the article type.
- **Inputs**: source file path or pasted text; user's stated type if any.
- **Do**: read the source. If no source is given, stop and ask. Detect the article type from the source substance if unspecified, state it with one line of reasoning. Note early if the topic is "about Medium" (Network-only trap).
- **Self-verify**: confirm a source was actually read and a single type is selected.
- **STOP GATE (hand back)**: present the detected type + reasoning (and any "about Medium" flag) and **stop to confirm** before drafting. Never silently default. → Hand control back to the user/orchestrator for the type decision.
- **Report contract**: `source read: <path> | type: <type> (<reason>) | about-Medium trap: <yes/no> | awaiting: type confirmation`.

### Unit W2 — Title + subtitle + hook engineering
- **Goal/scope**: produce 5 title+subtitle variants (as a unit) and hand back for selection, plus the opening hook.
- **Inputs**: confirmed article type + source substance.
- **Do**: generate **5 title+subtitle pairs**, each across a different pattern from Dimension 1 (curiosity gap, benefit-driven, numbered list, how-to, contrarian, specific-result). For each: title ≤~60 chars, Title Case, no all-caps/emoji; subtitle **pays off** the title (adds angle/stakes/specificity, never repeats). Apply the anti-clickbait rule — every promise must be one the body can deliver. Mark the 1–2 strongest. Then draft the **opening hook** (first 1–3 sentences: startling fact / pull question / in-media-res) for the marked-strongest pair.
- **Self-verify**: each pair passes clarity + specific promise + one turn of intrigue; no overpromise; subtitle adds rather than repeats; opening is tension-loaded and short.
- **STOP GATE (hand back)**: present **only** the 5 title+subtitle pairs (labeled by pattern, strongest marked) and the drafted opening hook. **Do not draft the body until a title+subtitle is selected or mixed.** → Hand control back for selection.
- **Report contract**: `5 title+subtitle pairs produced (patterns listed) | strongest: #N,#M | opening hook drafted | awaiting: title/subtitle pick or mix`.

### Unit W3 — Draft
- **Goal/scope**: write the full article from the selected title+subtitle+hook.
- **Inputs**: the **selected title+subtitle+hook** (or mix) + confirmed article type. Selecting a narrative frame is part of this unit.
- **Do**:
  - State the narrative frame chosen and why (one line).
  - Write the body applying Dimensions 2 and 3 and the sound-human overlay: section headings, short paragraphs, blockquotes/pull quotes and bulleted lists where they earn their place, first-hand specificity over rehash, ~4–8 min as a loose range (never padded to hit it). Never fabricate lived experience or facts.
  - Draft **3 closing/CTA candidates** (Dimension 5): each soft, single, value-tied (e.g. a genuine follow/subscribe invite) — no multi-link hype, no signup-farming ending, no earnings figures. Mark the recommended one.
  - Pick **≤5 relevant tags**.
  - **Recommend paywall on/off with a one-line reason** (on if monetization is a goal and the piece is authentic/not "about Medium"; off otherwise).
  - Flag the Network-only "about Medium" trap if the topic falls into it.
- **Self-verify**: run **Unit W4 (self-audit)** before reporting — the draft is not "done" until the audit passes or its flags are surfaced.
- **Report contract**: `draft complete | frame: <frame> | CTA candidates: 3 (rec: #N) | tags: <n, listed> | paywall rec: <on/off + reason> | about-Medium: <yes/no> | self-audit: <PASS | N flagged, fixed | N flagged, unresolved>`.

### Unit W4 — Self-audit (run inside W3, before any hand-back)
- **Goal/scope**: verify the draft against the shared 5 dimensions before showing the user. This is the doer's own verification step.
- **Inputs**: the drafted article (title+subtitle+body+tags+CTA+paywall rec).
- **Do**: check each row and record PASS or FLAGGED with a one-line note. Fix all FLAGGED items **once**. If something still fails after the fix, surface it to the user rather than looping silently.

| Check | Pass criteria | Dimension |
|---|---|---|
| Title-unit delivers on promise | Title+subtitle invite in, body pays it off; no overpromise/clickbait; subtitle adds not repeats | 1 |
| Read-ratio / scannability | Headings, short paragraphs, scannable elements; tension-loaded opener; no padding | 2 |
| First-hand value, not rehash | Real first-hand angle or original utility; not generic; not rage-bait; nothing fabricated | 3 |
| Tag relevance + traps | ≤5 relevant tags; no @-flooding; "about Medium" flagged if applicable; writing reads as authentic | 4 |
| Soft CTA + no fabricated earnings | Single, value-tied CTA; no hard/multi-link pitch or signup-farming; **zero invented dollar figures**; paywall recommended | 5 |

- **Report contract**: folded into W3's report (`self-audit: PASS` or the flagged/unresolved counts).

### Unit W5 — Persist draft (write to file first)
- **Goal/scope**: write the audited draft to disk **as a draft**, before the human review gate.
- **Inputs**: the W3 draft that has passed (or had its flags surfaced by) the W4 self-audit + source directory.
- **Do**: write `medium_article.md` in the same directory as the source file. Include title, subtitle, body, tags, and the paywall recommendation as a trailing note. **Overwrite policy:** this first draft write of the run to the canonical name is expected and needs no prompt; but if a `medium_article.md` already exists from a **prior run/session**, apply the overwrite policy (ask: overwrite / `-v2` / new name) before writing.
- **Self-verify**: confirm the file exists at the expected path and matches the drafted text (title, subtitle, body, tags, paywall note).
- **Report contract**: `draft written: <exact path> | overwrite policy: <n/a first-run write | applied choice> | self-audit: <PASS | N flagged>`.

### Unit W6 — Review-first (hand back to the file, not the chat)
- **Goal/scope**: get human approval on the draft that now lives in `medium_article.md`.
- **Inputs**: the written draft file path + W4 audit results + article type + narrative frame + tags + paywall recommendation + the 3 closing/CTA candidates.
- **STOP GATE (hand back)**: present **only** a short pointer + summary — the **file path**, the **article type**, the **chosen narrative frame**, the **W4 self-audit result** (PASS or the flags), the **≤5 tags**, the **paywall on/off recommendation + one-line reason**, the **"about Medium" Network-only flag** if applicable, and the **3 closing/CTA candidates** (short). **Do NOT paste the full article body into chat — point the user to `medium_article.md` to read it.** Ask the user to approve, request edits, or reject. → Hand control back for approval. If running non-interactively, note the gate as "skipped — auto-proceeding with the draft as written" and continue.
- **On an edit request**: re-edit `medium_article.md` **in place** and re-point the user to the file — do **not** re-dump the body into chat.
- **Report contract**: `draft written to <path>, awaiting review | awaiting: approve / edit / reject`.

---

## REVIEW/SCORE path

### Unit R1 — Intake
- **Goal/scope**: read the finished article to be reviewed.
- **Inputs**: source file path or pasted text.
- **Do**: read the source article. If none given, stop and ask. If pasted text, ask where to write the output.
- **Self-verify**: confirm the source was read and an output directory is known.
- **Report contract**: `source read: <path> | output dir: <dir>`.

### Unit R2 — Diagnose & score
- **Goal/scope**: score the article against the shared 5 dimensions.
- **Inputs**: the source article + the shared rubric (Dimensions 1–5 above).
- **Do**: for each of the 5 dimensions, give a brief one-line diagnostic — what's strong, what's weak, grounded in that dimension. Do not skip a dimension even if clearly strong ("no issues" is fine). Score each out of 20 and sum to /100. Present as a table. Explicitly note if the "about Medium" trap or a writing-authenticity concern applies.
- **Self-verify**: all 5 dimensions scored; sum equals the /100 total.
- **Report contract**: `scored: <X>/100 | flagged dimensions: <list or none> | about-Medium/authenticity flags: <list or none>`.

### Unit R3 — Refine
- **Goal/scope**: produce **one** refined version fixing every flagged weakness.
- **Inputs**: the source article + the flags from R2.
- **Do**: rewrite once to fix every weakness flagged in R2, without introducing new ones. **Do not invent facts, lived experience, or earnings numbers** — if a fix would require information not in the source (a real statistic, a first-hand detail, a specific outcome), flag it as a note rather than fabricating it. This path scores and rewrites — it does **not** offer multiple stylistic variants.
- **Self-verify (self-audit against own output)**: re-run the shared 5-dimension rubric against the **refined** version before finalizing. If the rewrite introduced a regression on any dimension, fix it before proceeding.
- **Report contract**: `refined version produced | re-checked rubric on refined text: <PASS | fixed N regressions> | unfixable-for-lack-of-info: <list or none>`.

### Unit R4 — Itemize changes
- **Goal/scope**: account for every flagged weakness.
- **Inputs**: R2 flags + R3 refined version.
- **Do**: list each change, one line each, as **what changed → why** (tied to the specific dimension it improves). Every weakness flagged in R2 must be accounted for — if flagged but not fixed, say so explicitly and why (e.g. "insufficient information in source to add a specific first-hand detail here" or "cannot add an earnings figure — no verified number").
- **Self-verify**: every R2 flag maps to either a change line or an explicit not-fixed note.
- **Report contract**: `change list: N items | R2 flags all accounted for: yes`.

### Unit R5 — Write reviewed file first
- **Goal/scope**: persist the review artifact to disk **before** the confirm gate.
- **Inputs**: score table + R3 refined version + R4 itemized change list + output directory.
- **Do**: write `medium_article_reviewed.md` containing, in order: the score table, the refined article, then the itemized change list. **Overwrite policy:** this first write of the run to the canonical name is expected and needs no prompt; but if a `medium_article_reviewed.md` already exists from a **prior run/session**, apply the overwrite policy (ask: overwrite / `-v2` / new name) before writing.
- **Self-verify**: confirm the file exists at the expected path with the three sections in the correct order.
- **Report contract**: `reviewed file written: <exact path> | sections: score → refined → changes | overwrite policy: <n/a first-run write | applied choice>`.

### Unit R6 — Present & confirm (hand back to the file, not the chat)
- **Goal/scope**: show the short, useful results and get a lightweight go-ahead.
- **Inputs**: score table + itemized change list + written file path + any flags.
- **STOP GATE (hand back, lightweight)**: present **inline only** the **score table** and the **itemized change list** (these are short and useful), plus the **file path pointer**, plus any **"about Medium" / writing-authenticity flags**. **Do NOT paste the full refined article body into chat — it lives in `medium_article_reviewed.md`; point the user there to read it.** Ask for confirm-or-another-pass. If the user asks for another pass, treat the just-refined version as the new input, repeat R2–R4, and re-edit the file **in place** (re-pointing to it, not re-dumping the body). → Hand control back for confirm-or-another-pass.
- **Report contract**: `reviewed file written to <path>, awaiting review | presented: score + change list (inline) | awaiting: confirm or another pass`.

### Output format (`medium_article_reviewed.md`)

```markdown
# Medium Article Review

## Score

| Dimension | Score | Notes |
|---|---|---|
| Title + subtitle + cover unit / Hook | X/20 | ... |
| Read-ratio & scannability / structure | X/20 | ... |
| Originality & first-hand value | X/20 | ... |
| Distribution & tagging | X/20 | ... |
| Monetization & endings (CTA + paywall) | X/20 | ... |
| **Overall** | **X/100** | |

## Refined Version

<full refined article: title, subtitle, body, tags, paywall note>

## Improvements Made

- <change> → <why, tied to dimension>
- ...
```

---

## Handoff

- After the WRITE path writes `medium_article.md`, mention the built-in **REVIEW/SCORE path** can score and refine it further into `medium_article_reviewed.md` in the same folder.
- After either path, mention that **`medium-image-prompts`** can generate cover and inline image prompts from the output file (`medium_article.md` or `medium_article_reviewed.md`) — it writes its output to the same folder, and it (not this skill) enforces the AI-image caption-disclosure rule.
