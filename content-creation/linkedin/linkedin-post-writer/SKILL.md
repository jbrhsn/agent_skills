---
name: linkedin-post-writer
description: Use when the user wants to turn a source draft, notes file, or rough points into a posting-ready LinkedIn post. Applies 2026 LinkedIn algorithm-aware craft — hook engineering, scroll-first structure, no-link-in-body discipline, engagement-bait avoidance — with a mandatory review gate before writing. Writes linkedin_post.md next to the source file. Trigger on "write a LinkedIn post from this", "turn these notes into a LinkedIn post", "draft a LinkedIn post".
---

# LinkedIn Post Writer

Turn a source draft, a notes file, or rough bullet points into a posting-ready LinkedIn post. Applies platform-specific craft grounded in how LinkedIn's 2026 algorithm actually ranks content — not generic copywriting advice.

## When to use

- User points to a file with notes, bullets, or a rough draft and wants a LinkedIn-ready post.
- User pastes raw notes directly and asks for a LinkedIn post.
- Not for Medium, Twitter/X, or other platforms — this skill is LinkedIn-specific.
- Not for carousel image generation — that's `linkedin-image-prompts` (run after this skill).

## Input

The user must point to a source file (any path, any text format — `.md`, `.txt`, etc.) containing the draft, notes, or points to work from. **If no file is given, ask for one before doing anything else.** Raw pasted text in the conversation is also acceptable in place of a file, but note in that case there is no source directory to colocate output with — ask the user where to write `linkedin_post.md`.

## Output

`linkedin_post.md`, written in the **same directory as the source file**. Never write to a fixed `linkedin/` or `drafts/` folder — always colocate with the input.

**Overwrite policy**: never silently overwrite. If `linkedin_post.md` already exists in that directory, ask: overwrite, write `linkedin_post-v2.md`, or pick a new name.

---

## Why these rules (2026 LinkedIn algorithm context)

LinkedIn's ranking in 2026 is semantic (reads for meaning, not hashtag density) and reads on relevance over recency — a good post can keep surfacing for weeks. Ranking signals, in order of reach impact: **saves** (~5x the reach of a like), **comments** (~2x), then likes. Dwell time (how long someone reads before scrolling on) is a major passive signal. Links in the post body tank dwell time because they invite the reader off-platform. Engagement bait ("comment YES if you agree") is actively detected and suppressed, not rewarded. These facts drive every rule below — they are not arbitrary style preferences.

---

## Content types

| Type | Target length | Best fit |
|---|---|---|
| Short Post | 100–300 words, 8–15 lines | Single sharp insight, story beat, opinion |
| Long Post | 600–1200 words, 25–45 lines | Narrative, lesson, or argument, native feed |
| Article | 1000–2500 words | Structured argument with multiple distinct sections |

If the user hasn't specified a type, detect the best fit from the source substance, state the detected type with one line of reasoning, and **stop to confirm** before drafting. Never silently default.

---

## Craft rules (apply to every post)

### 1. Hook engineering (first 1–3 lines, mandatory gated step)

LinkedIn truncates at roughly 150–210 characters on mobile before "see more." The hook is the single biggest lever on whether the post gets read at all.

- Generate **5 hook variants**, one per mode:
  1. **Contrarian**: "[Common belief] is wrong. Here's what I've actually seen."
  2. **Curiosity gap / number+contrast**: a specific small input leading to a specific large outcome.
  3. **Confession**: "I was wrong about [X] for [time]. Here's what changed my mind."
  4. **Mid-scene open**: drop the reader into a specific moment already in progress, no setup.
  5. **Problem-naming**: name the reader's specific pain more precisely than they'd name it themselves.
- Use **exact numbers, not round ones** ("847 to 22,400" reads as credible; "20K" reads as marketing).
- Delete all throat-clearing on sight: "Excited to share…", "I've been thinking about…", "In today's post…".
- Apply the **cold-read test**: read only the first 1–2 lines in isolation. Would you tap "see more"? If you can already predict what comes next, trim until it withholds something.
- The cut must land at a point of unresolved tension, ideally mid-thought, never at a full stop.
- **Stop here.** Present only the 5 hooks, labeled by mode, with the 1–2 strongest marked. Let the user pick one or mix elements. Do not draft the body until a hook is selected.

### 2. Narrative frame

Pick the frame that matches what actually happened — never bend a real detail to fit a better-looking template.

| Frame | Fill-in |
|---|---|
| Before → After → Bridge | "I used to [struggle]. Now [result]. Here's what changed." |
| Mistake → Realization → Shift | "I did [X] for years. Then [moment] made me realize [Y]." |
| Challenge → Action → Result | "[I] was stuck on [problem]. Here's what we tried, here's what happened." |
| Contrarian stance | "[Widely accepted belief]. I disagree. Here's why." |

State which frame was picked and why, in one line.

### 3. Body structure (scroll-first, phone-first)

- **One idea per line.** Any line with more than one idea gets split.
- **Paragraph cap**: 1–3 lines max, blank line between every paragraph. No exceptions for Long Posts or Articles.
- **Line-count gut check** (Short/Long Posts): under 10 lines is likely thin; over 18, cut a paragraph that explains something the reader can infer.
- **Bullet-ize 3+ parallel items** rather than burying them in a sentence.
- Replace vague nouns with real, textured detail (industry, size, specific number) — anonymize names, not texture.

### 4. Engagement design (comments > likes, no bait)

- End with a **sharp, specific closing question** — not "Thoughts?", not yes/no. Draft 3 candidates, mark the recommended one. It should be narrow enough to answer in one sentence but interesting enough that you'd genuinely want to read the replies.
- **Never use engagement-bait phrasing** ("Comment YES if...", "Tag someone who...", "Repost if..."). LinkedIn's 2026 spam filter actively detects and suppresses this — it reduces reach, it does not increase it.
- Favor content that is worth **saving** (a framework, checklist, or reusable insight), not just liking — saves currently drive roughly 5x the reach of a like.

### 5. Link discipline (dwell-time protection)

- **No URLs in the post body**, ever. A link invites the reader off-platform, which tanks dwell time — a core ranking signal.
- Write the post to be completely valuable with zero external clicks.
- If a source or link matters, tell the user to add it as the **first comment** immediately after publishing, or name the source in prose instead of linking it ("I read a good piece on this by [person]").

### 6. Sound human, not generated

- **Crutch-phrase hunt**: cut "it's important to note", "in today's fast-paced world", "at the end of the day", "dive deep", "game-changer", "leverage" (as a verb), "delve into".
- Read the draft aloud (coffee test) — rewrite any sentence that would sound stilted said to a colleague's face.
- Leave one rough edge in: a sentence starting with "And," a fragment, a slightly-too-long line. A perfectly symmetrical post reads as manufactured.

### 7. Hashtags

- Zero to three relevant hashtags, placed at the end. Hashtag stuffing is a spam signal under the 2026 semantic algorithm, not a reach booster.

---

## Workflow

### Step 1 — Intake and type selection
Read the source file (or pasted text). Detect the content type if unspecified, state it with one line of reasoning, and **stop to confirm** before proceeding.

### Step 2 — Hook engineering (mandatory stop)
Generate the 5 hook variants per the rules above. Present them alone. Stop and wait for the user's pick or mix. Do not proceed to drafting until this is resolved.

### Step 3 — Draft the full piece
Using the selected hook:
- State the narrative frame chosen and why (one line).
- Write the body applying: one-idea-per-line, paragraph cap, specificity, no links, no crutch phrases.
- Draft 3 closing-question candidates, mark the recommended one.
- Add 0–3 hashtags if relevant.

### Step 4 — Self-audit (run before showing the user)
Check internally and report PASS or FLAGGED with a one-line note for each:

| Check | Pass criteria |
|---|---|
| Hook fold test | First 1–3 lines under ~210 chars; ends on unresolved tension |
| Line density | No paragraph over 3 lines; blank line between paragraphs |
| Specificity | No vague nouns where a real detail was available |
| Crutch-phrase scan | None of the banned phrases present |
| Link discipline | Zero URLs in body |
| Engagement-bait scan | No "comment YES", "tag someone", "repost if" phrasing |
| Closing question | Specific, not yes/no, not "Thoughts?" |

Fix all FLAGGED items once. If something still fails after the fix, flag it to the user instead of looping silently.

### Step 5 — Review-first stop
Present: the full draft, the self-audit results, the frame used, and the content type. **Stop.** Ask the user to approve, request edits, or reject. Do not write any file yet. If running non-interactively, note the gate as "skipped — auto-proceeding with output as drafted" and continue rather than silently omitting it.

### Step 6 — Persist
After approval, write `linkedin_post.md` in the same directory as the source file. Apply the overwrite policy above. Confirm the exact written path back to the user.

## Handoff

After writing `linkedin_post.md`, mention that `linkedin-image-prompts` can generate carousel/image prompts from this file, and `linkedin-post-reviewer` can score and refine it further — both write their output to the same folder.
