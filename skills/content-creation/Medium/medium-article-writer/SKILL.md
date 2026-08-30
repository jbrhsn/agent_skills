---
name: medium-article-writer
description: Turn a rough draft, notes, or dictated thoughts in source.md into a finished, publishable Medium article, plus title options, subtitle, tags, and cover/alt-text notes. Use this whenever the user mentions Medium, publishing an article or blog post, turning notes or a draft into an article, writing up an experience, tutorial, post-mortem, or opinion piece for readers, or is working inside a folder that contains a source.md. Also use when asked to restructure, retitle, tighten, or tag an existing article draft, even if Medium is not named explicitly.
---
# Medium Article

Convert the user's raw material into a finished article that could be pasted into
the Medium editor and published as-is. The user edits afterward; do not hand back
work-in-progress, do not annotate the draft, and do not leave placeholders.

The user is an AI/data engineer. Default assumption: the piece is technical and
the reader is a working practitioner. See `assets/article-structures.md` for the
non-technical modes.

## Folder contract

Each article lives in its own folder. Work only inside it.

```
<article-folder>/
  source.md    # written by the user: draft, bullets, thoughts, experience
  medium_brief.md      # you write: angle, reader, promise, outline, gaps
  medium_article.md    # you write: the finished piece
  medium_publish.md    # you write: titles, subtitle, tags, alt text, checklist
```

If `source.md` is missing, look for `draft.md` or any single markdown file in the
folder and confirm with the user before treating it as the source. Never
overwrite `source.md`.

## Workflow

### 1. Read and classify

Read `source.md` in full before doing anything else. Then decide:

- **Piece type** — tutorial, case study / post-mortem, opinion, explainer, or
  experience report. This determines structure. See `assets/article-structures.md`.
- **Voice** — read `references/voice-inference.md` now and build the six-line
  voice card it describes. The card goes in the brief. Do not defer this to
  drafting; register is decided before the first sentence, not adjusted after.
- **What is already the user's** — specific numbers, failures, decisions, turns of
  phrase, opinions, and above all lived experience. These are the load-bearing
  parts of the article. Everything you add is scaffolding around them. Inventory
  them; the coverage ledger in step 3 depends on this list being complete.
- **What is missing** — the gaps that, if you filled them yourself, would mean
  inventing the user's experience.

### 2. Gap interview

Ask up to five questions in a single batch. Target only what you must not invent:
concrete numbers, versions, what actually broke, what the user would tell a
colleague over coffee, why they chose X over Y.

Do not ask about structure, tone, or length — decide those yourself. Do not ask
questions the source already answers. If the source is rich enough, skip this
step entirely rather than manufacturing questions.

Wait for answers before drafting.

### 3. Brief

Write `medium_brief.md` from `assets/brief-template.md`: the angle in one sentence,
who the reader is, the promise, the voice card, a section outline, the coverage
ledger, anything proposed for omission, and any claim you could not verify.

Two sections of that template do the work the rest of the skill depends on:

- **Coverage ledger** — every load-bearing specific from `source.md` mapped to the
  section that carries it. A thin ledger is a piece that will read as
  generic no matter how well written.
- **Proposed to omit** — everything from `source.md` that is not in the ledger,
  with a reason. This is a question for the user, not a decision you have made.

**Stop and show the brief.** A rejected brief costs one minute; a rejected 2,000-word
draft costs an afternoon. This is also the gate where omissions get approved, so
call out the "Proposed to omit" list explicitly rather than letting the user find
it. If the user says to skip ahead, skip the brief — but still say in one line
what you propose to leave out, because that decision is theirs whether or not the
brief gets written.

### 4. Verify, do not research

You may search the web **only to check claims that are already in the user's
material** — version numbers, dates, pricing, whether a named tool still behaves as
described, whether a statistic is real. That is verification.

You may not search to find new sources, new arguments, new examples, or extra
material to pad the piece. The article's substance comes from the user.

When a claim fails verification or you cannot check it, do not write around it and
do not silently drop it. List it in `medium_brief.md` under "Unverified" and raise it with
the user. Never state a number, date, version, or attributed quote you have not
confirmed or been given.

### 5. Write

Write the full article to `medium_article.md`. Finished prose, publishable as-is.

- Preserve the user's own phrasings wherever they work. Do not mark them, do not
  set them apart — just keep them.
- Where they don't work, write replacement prose in the same register.
- Place the user's experience where it does a job, not where it interrupts. See
  "Placing the user's experience" in `assets/article-structures.md`.
- No placeholders, no `[insert example here]`, no editorial notes in the body.
- Follow `references/do-and-avoid.md` and `references/voice-and-antislop.md`.

The single most common failure is prose that is fluent, correct, and obviously
machine-written. Fluency is not the goal; sounding like a specific engineer who
did a specific thing is the goal. Read `references/voice-and-antislop.md` before
you write the first line, not after.

### 6. Close and CTA

A separate pass, because the ending is written on momentum and rarely revised.
Read `references/closing-and-cta.md`.

The article must not end on a summary, and it must not simply stop. It lands, it
gives the reader a takeaway they can act on, and it closes deliberately rather
than trailing off.

**Default CTA: a genuine question** — specific, arising from the argument, one the
user does not already know the answer to. No promotional line, no follow prompt,
no link, unless the user has asked for one and supplied the destination. Never
invent a newsletter or write a placeholder link. Dropping the CTA entirely is a
legitimate choice when the takeaway is the strongest line in the piece — but it is
a choice, recorded as one, not an omission.

Record which CTA was used, and why, in `medium_publish.md`.

### 7. Self-audit

Before presenting, run the article against the checklist in
`references/do-and-avoid.md`. Fix what fails. Fix it in the file — do not report
a list of issues to the user and do not annotate the draft.

Four checks worth doing explicitly, because they are the ones that get skipped:

- Read the opening 150 words as if you were scrolling a feed. Does it earn the
  next paragraph, or is it throat-clearing?
- Scan for the tells in `references/voice-and-antislop.md`. If you find three or
  more, the voice pass failed; rewrite the affected sections rather than
  swapping individual words.
- **Substitution test.** Could this have been written by a hundred other people in
  this field? If yes, the voice got sanded off.
- **Reverse test.** Would the user recognize this as theirs? Then run the
  remaining calibration checks in `references/voice-inference.md` — the
  sustained-register one catches the drift toward neutral prose that sets in
  around the last quarter of a long piece.

Last, re-read the coverage ledger against the finished article. Every row should
be findable in the file. Anything that isn't is an omission that happened during
drafting — see the standing rule below.

### 8. Package

Write `medium_publish.md` from `assets/publish-template.md`: five title options, a
subtitle, five tags, the CTA used, cover image direction, alt text for every image
referenced, and the editor formatting steps. See `references/medium-mechanics.md`.

## Standing rules

**Never invent experience.** No fabricated anecdotes, benchmarks, client stories,
error messages, or "I once had a colleague who." If the piece needs a concrete
example and the user hasn't supplied one, ask for it.

**Never drop the user's experience silently.** The mirror of the rule above, and
the one more likely to be broken. A personal experience, opinion, or judgment in
`source.md` is the reason the piece is publishable rather than derivative. If one
does not fit:

- Before drafting, it goes in "Proposed to omit" in the brief and the user
  decides.
- During drafting, stop and ask. Do not cut it and mention it afterward, and do
  not quietly compress it into a clause until it carries nothing.
- The default is to find it a home. Try the three integration moves in
  `assets/article-structures.md` first — split it, compress it to its specific
  detail, or move the claim to the story. Omission is what happens after those
  fail, with the user's agreement.
- When you do raise it, say what breaks: which section, why the flow suffers, and
  what the alternative placement would cost.

**Financial and health topics.** The user occasionally writes about money and is
not a financial advisor. Frame these strictly as personal experience — what they
did, what it cost, what happened — never as advice or recommendation. Strip
prescriptive second-person framing ("you should open a…"). Medium treats
unverified financial claims as a rules violation, not just a distribution issue.

**Length follows purpose.** A technical deep dive for a practitioner audience
typically runs 1,500–2,500 words. A sharp argument can run 800. Do not pad to hit
a number, and do not cut a piece short that needs the room.

**One article per invocation.** Do not batch.

## Reference files

Read these when the step calls for them; they are not needed all at once.

- `references/voice-inference.md` — extracting the user's register from
  `source.md` and holding it for 2,000 words. Read at step 1, checks at step 7.
- `references/voice-and-antislop.md` — voice, rhythm, and the specific phrasings
  and structures that read as machine-generated. Read before writing.
- `references/closing-and-cta.md` — how the article ends, and the CTA options.
  Read at step 6.
- `references/do-and-avoid.md` — the review checklist: what earns distribution on
  Medium and what disqualifies a story. Read before the self-audit.
- `references/medium-mechanics.md` — titles, subtitles, kickers, tags,
  distribution tiers, publications, images. Read before packaging.
- `assets/article-structures.md` — section skeletons per piece type, placing the
  user's experience, and the adjustments for writing-about-writing and
  personal-finance pieces.
- `assets/brief-template.md`, `assets/publish-template.md` — output templates.
