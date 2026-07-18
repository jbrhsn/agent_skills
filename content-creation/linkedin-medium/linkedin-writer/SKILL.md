---
name: linkedin-writer
description: Use when the user wants to write, format, or sharpen a LinkedIn post or article from a source draft or raw idea. Applies deep LinkedIn-specific craft — hook engineering, body structure, scannability, CTA — for Short Posts, Long Posts, and Articles. Produces posting-ready output with a mandatory review gate before writing. Trigger on "write a LinkedIn post", "turn this into a LinkedIn post", "LinkedIn version", "make this shareable on LinkedIn".
---

# LinkedIn Writer

Take a source draft, a rough idea, or raw notes and produce a posting-ready LinkedIn piece, applying deep platform craft: hook engineering, body structure for scrolling readers, voice alignment, and a sharp closing question. Output is formatted specifically for LinkedIn's rendering, fold mechanics, and algorithm behavior.

This skill handles three LinkedIn content types: **Short Post**, **Long Post**, and **Article**. Carousel copy and carousel image rendering are outside this skill's scope — use `carousel-builder`, which authors and renders carousel slides.

## When to use

- User has a `drafts/<slug>.md` source draft and wants a LinkedIn-ready version.
- User pastes raw notes, bullets, or a rough idea and says "make this a LinkedIn post".
- User wants to sharpen or rewrite an existing LinkedIn post with better craft.
- This skill is for LinkedIn only. For Medium content, use a Medium-specific skill.
- Carousel copy and carousel image rendering are not in scope for this skill — use `carousel-builder`, which authors and renders carousel slides.

## Folder conventions (cwd-relative)

- `drafts/`: source drafts read from here.
- `linkedin/`: finished LinkedIn files written here.
- `voice-tone/`: voice samples + style instructions.

If `linkedin/` is needed but missing, STOP and ask the user how to proceed. Never silently create folders.

## Content types

| Type | Target length | Primary use |
|---|---|---|
| Short Post | 100–300 words, 8–15 lines | Single sharp insight, story beat, or opinion |
| Long Post | 600–1200 words, 25–45 lines | Narrative, lesson, or argument — native feed, no images |
| Article | 1000–2500 words | Native LinkedIn Publishing; headers, structured sections |

If the user has not specified a type, detect the best fit from the input substance, state your reasoning in one line, then ASK for confirmation before writing. Never silently default.

## Voice handling

Before writing anything:
- If `voice-tone/profile.md` exists, read it. Use the `### LinkedIn` subsection of `## Per-Platform Notes` if present — this is the most specific voice signal.
- If only raw samples exist in `voice-tone/`, read them and infer rhythm, vocabulary, and structural habits.
- If `voice-tone/` does NOT exist, note this to the user in one line ("No voice-tone/ found — proceeding with neutral professional voice") and continue. Do not block the skill.

Voice adapts to the content type: Short Posts are more punchy and personal; Long Posts allow more narrative and texture; Articles allow a more considered, essayistic tone while still being direct.

---

## LinkedIn craft rules (apply to all content types)

These are the non-negotiable mechanics of writing well for LinkedIn. Apply every rule on every piece.

### 1. Hook engineering (first 1–3 lines)

LinkedIn truncates posts at roughly 150–200 characters on mobile, showing only the first 1–3 lines before a "see more" button. If the hook does not earn the tap, nothing else matters.

**Hook mechanics:**
- Write the hook LAST, not first. Draft the body, then mine it for the single most surprising sentence — that is usually the real hook, buried in paragraph three.
- Apply the **cold-read test**: copy only the first 1–2 lines into a blank note and read them in isolation. Ask honestly: would you tap "see more"? If you can already predict what comes next, the hook explains too much — trim until it withholds something.
- Write **5 hook variants** before choosing one. Cover all five modes:
  1. **Contrarian**: "[Common belief] is wrong. Here's what I've actually seen."
  2. **Curiosity gap**: "There's one thing that kills [outcome] and almost nobody talks about it."
  3. **Number + contrast**: "[Specific small input]. [Specific large outcome]. Here's what happened in between."
  4. **Confession**: "I was wrong about [X] for [specific time]. Here's what changed my mind."
  5. **Mid-scene open**: Drop the reader into a specific moment already in progress, no setup.

**For deeper hook engineering**, read `$SKILL_DIR/reference/hook-writing-guide.md` (resolve `$SKILL_DIR` to this skill's directory). It contains the full framework: curiosity gap theory, four psychological levers, five hook types, platform-specific mechanics, a 7-dimension scoring rubric, and a naturalness check. Apply those tools to generate and score the 5 variants if hook quality is the focus of the session. This skill works without that guide — the five modes above are sufficient for most sessions.
- Use **exact numbers, not round ones**. "847 to 22,400 followers" reads as credible; "20K" reads as marketing. Specificity is a trust signal.
- **Delete throat-clearing without exception**: any version of "I've been thinking about…", "Excited to share…", "In today's post…", "I wanted to take a moment to…". Cut on sight, every time.
- The hook must have **at least one of**: tension (contradicts expectation), specificity (a real detail), or a withheld promise (reader must keep reading to resolve it).

**Fold awareness:**
- The "see more" cut lands after ~150–200 characters on mobile. Count characters on the hook lines. The cut must land at a point of maximum unresolved tension — ideally mid-thought, never at a full stop.
- On desktop the cut is slightly later, but design for mobile.

### 2. Body structure for scrolling readers

LinkedIn is a scroll-first, phone-first platform. Dense paragraphs are skipped even by interested readers.

**Structure rules:**
- **One idea per line.** After drafting, go line by line: if a line contains more than one idea, break it in two. This roughly doubles line count without adding length.
- **Paragraph cap**: 1–3 lines maximum per paragraph, with a blank line between every paragraph. No exceptions for Long Posts or Articles.
- **The 10–18 line gut check (Short/Long Posts)**: count lines, not words. Under 10: likely too thin. Over 18: find the paragraph that explains something the reader can already infer, and cut it.
- **Bullet-ize 3+ parallel items**: if you're writing "first… second… also…" in a sentence, that is a bullet list trying to escape a paragraph.
- **Scroll momentum**: end each short paragraph on a slightly incomplete thought. A paragraph that resolves too neatly gives the reader permission to stop scrolling.
- **Preview on mobile before publishing**: paste into LinkedIn's own post box (don't publish — just inspect the preview) or into a Notes app at phone width. What looks clean on desktop becomes a wall on mobile. Instruct the user to do this before posting.

### 3. Narrative frame

A frame gives the piece a shape to fill. Pick the frame that matches what actually happened — do not force content into a frame it doesn't fit.

| Frame | Fill-in structure |
|---|---|
| Before → After → Bridge | "I used to [struggle]. Now [result]. Here's what actually changed." |
| Mistake → Realization → Shift | "I did [X] for years. Then [specific moment] made me realize [Y]. Now I [new behavior]." |
| Challenge → Action → Result | "[Person/I] was stuck on [specific problem]. Here's exactly what we tried. Here's what happened." |
| Contrarian stance | "[Widely accepted belief]. I disagree. Here's why — and what I do instead." |

**Frame selection discipline**: ask "did I mess up and learn something?", "did I go from bad to better?", "did I see something counterintuitive?". The honest answer points to the frame. Never bend a real memory to fit a better-looking template.

### 4. Say something only you could say

Generic insight gets a like. A specific, lived take gets shared to someone's team with "this is what I mean."

**Specificity rules:**
- Replace every vague noun with a real, textured detail: not "a client" but what industry, what size, what went wrong. Anonymize names, not texture.
- Before writing each paragraph, ask: "could a stranger who has never met me have written this exact sentence?" If yes, make it more specific to the actual experience.
- Write the version you'd be slightly nervous to post — not reckless, just a genuine opinion instead of a safe one. If every sentence would get unanimous agreement from anyone in the field, nothing has been said yet.
- **Mine disagreements**: the gap between what you said in a meeting and what you actually thought is usually the best post material.

### 5. Closing question

A vague "Thoughts?" gets ignored. A sharp, specific question gets people typing paragraphs — and comments carry more algorithmic weight than likes.

**Closing question rules:**
- Ask a question you would genuinely want to know the answer to. If you wouldn't be curious about the replies, don't ask it.
- Make it answerable in one sentence but interesting to answer — narrow enough to answer immediately, with enough personality to invite a real reply.
- Avoid yes/no. Avoid engagement-bait phrasing ("Comment YES if you agree") — this reads as manipulative and is increasingly suppressed.
- Draft 3 closing questions. Delete the safest one. The slightly too-specific or slightly too-personal option usually generates the best replies.
- Example of a weak close: *"What do you think? Let me know in the comments!"*
- Example of a strong close: *"What's a piece of 'best practice' advice in your field that you've quietly stopped following?"*

### 6. Sound human, not generated

Over-polished text measurably underperforms. Readers and the algorithm both detect it.

**Human voice checks (apply before finalizing):**
- **Coffee test**: read the draft aloud. Any sentence that would sound stilted said to a colleague's face — rewrite it in the words you'd actually use.
- **Crutch-phrase hunt**: scan for "it's important to note", "in today's fast-paced world", "at the end of the day", "clear, concise, and compelling", "dive deep", "game-changer", "leverage". Cut or rewrite each one.
- **Break a rule on purpose**: start one sentence with "And." Use one sentence fragment. Real speech is not grammatically tidy — one slightly imperfect rhythm reads more human than a uniformly polished post.
- **Leave one rough edge in**: a perfectly symmetrical post reads as manufactured. An aside in parentheses, a sentence that trails with an em-dash, a line that's slightly longer than the rest — consider keeping it.
- **Write the first draft fast, edit slow**: first-pass speed preserves actual voice. Voice is much harder to add back to something over-polished from the start.

### 7. Link placement

A link in the post body invites the reader to leave the platform, which tanks dwell time — the signal LinkedIn uses to decide how widely to distribute the post.

**Link rules:**
- Write the post so it is completely valuable with zero external clicks. If the post is a teaser for a link, rewrite it as a standalone complete idea; the link is bonus for readers who want more.
- Delete any URL from the post body. Publish the post first. Then add the link as the **first comment** on your own post immediately after.
- If referencing something, name it instead of linking it: "I read a good piece on this by [person] this week" carries nearly the same value without the reach penalty.

---

## Workflow

### Step 1 — Intake and type selection
Read the input (source draft, file, or pasted notes). If a content type has not been specified:
- Detect the best fit from the substance (single sharp insight → Short Post; layered narrative with a clear arc → Long Post; structured argument with multiple distinct sections → Article).
- State your recommendation in one line with brief reasoning.
- STOP and ask the user to confirm the type before proceeding.

### Step 2 — Hook engineering (mandatory)
Before drafting the body:
- Generate **5 hook variants**, one per mode (Contrarian, Curiosity gap, Number+contrast, Confession, Mid-scene). Label each.
- Apply the cold-read test mentally to each. Mark the 1–2 strongest with a brief note on why.
- STOP and present only the hooks to the user. Ask them to pick one, or mix elements from two.
- Do NOT draft the full body until a hook is selected.

### Step 3 — Draft the full piece
Using the selected hook and the craft rules above:
- Select the narrative frame that fits the content honestly. State which frame and why (one line).
- Write the body applying: one-idea-per-line, paragraph cap, scroll momentum, specificity rules.
- Write 3 closing question candidates. Mark the recommended one.
- Apply link discipline — no URLs in the body.
- Apply the human-voice checks as you write, not only at the end.

Do NOT present the draft yet — proceed to Step 4 first.

### Step 4 — Self-audit (run before review)
Before showing the draft to the user, run these checks internally and report the results:

| Check | Pass criteria |
|---|---|
| Hook fold test | First 1–3 lines under ~200 chars; ends on unresolved tension |
| Line density | No paragraph longer than 3 lines; blank line between every paragraph |
| Specificity scan | No vague nouns where a real detail is available |
| Crutch-phrase scan | None of the banned phrases present |
| Throat-clearing scan | No "Excited to share", "I wanted to", "In today's post", or equivalent |
| Link discipline | No URLs in body |
| Closing question | Not a yes/no; not "Thoughts?"; specific enough to earn a paragraph reply |

Report each check as PASS or FLAGGED with a one-line note. Fix all FLAGGED items before presenting to the user. Only one iteration of fixes is needed — if a check still fails after the fix, flag it for the user instead of looping silently.

### Step 5 — Review-first (mandatory stop)
Present:
1. The full draft.
2. The self-audit results (all checks + any fixes made).
3. A one-line note on the narrative frame used.

STOP. Ask the user to approve, request edits, or reject. Do NOT write any file yet. Iterate on the draft in place if edits are requested, re-running the self-audit after each significant change.
If running non-interactively (e.g. in a batch pipeline or scripted run), document this gate as "skipped — auto-proceeding with output as drafted" and continue; do not silently omit the gate from the output log.

### Step 6 — Persist (after approval)
**Voice compliance gate (before write).** If `voice-tone/profile.md` (or raw `voice-tone/` samples) is present, scan the approved text against its "Avoided Words & Phrases" and "Punctuation & Formatting Quirks" sections. Auto-fix mechanical violations (em-dashes, banned punctuation) and report what changed. Flag judgment-call violations (hype words, AI-voice markers) for the user. Never emit a banned pattern. If no voice-tone exists, skip silently.

**Pre-publish marker cleanup.** The source draft may contain inline `[source: ...]`, `[UNVERIFIED]`, and `[personal]` claim markers from draft-builder. These are provenance markers for the drafting phase — they must be stripped from the final LinkedIn file before publishing. Remove all `[source: ...]` and `[personal]` inline markers. Replace each `[UNVERIFIED]` claim with a softer hedge ("reportedly", "according to some practitioners") or cut the sentence — never publish an `[UNVERIFIED]` claim as a plain statement. Add any cited sources as the first comment on the post after publishing (links in the body tank reach).

Write the file:
- Short Post → `linkedin/<slug>-short.md`
- Long Post → `linkedin/<slug>-long.md`
- Article → `linkedin/<slug>-article.md`

**Overwrite policy**: never silently overwrite an existing file. If the target exists, ask: overwrite, write a `-v2` variant, or pick a new name.

Confirm the exact written path to the user.

If a `content-log.json` tracker exists at cwd, ask in one line whether to update the piece's status to `reviewed`.

## Handoff

This skill produces a complete, posting-ready LinkedIn file. Further polish passes, carousel image rendering, and Medium adaptations are outside this skill's scope.

## Conventions

These are shared assumptions so the content skills interoperate. Each skill
still works standalone. None of these require another skill to be present.

- **Folders** (all cwd-relative): `drafts/`, `linkedin/`, `medium/`,
  `archive/`, `voice-tone/`. Never auto-create: ask the user if missing.
- **Slug**: lowercase, hyphenated, derived from the working title. Reused as
  the filename stem across skills so a piece is traceable.
- **Filenames**: `drafts/<slug>.md`, `linkedin/<slug>-<type>.md`,
  `medium/<slug>-<type>.md`, carousels at `linkedin/carousels/<slug>/`.
- **Overwrite policy**: never silently overwrite an existing file. If the
  target exists, ask the user: overwrite, write a `-v2` (then `-v3`...)
  variant, or pick a new name.
- **Status values** (if a tracker file like `content-log.md` or
  `content-log.json` exists at cwd): `idea` -> `drafted` -> `reviewed` ->
  `posted` -> `archived`. If such a tracker exists, after writing or moving a
  file ASK the user in one line whether to update it to the new status.
  Absence of a tracker must never block the skill.
