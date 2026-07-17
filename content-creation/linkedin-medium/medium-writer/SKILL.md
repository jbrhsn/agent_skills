---
name: medium-writer
description: Use when the user wants to write, format, or sharpen a Medium article from a source draft or raw idea. Applies deep Medium-specific craft — title and subtitle engineering, hook types, read-ratio pacing, emotional arc, and formatting for completion — for Short Articles, Long Articles, Tutorials, and Listicles. Produces posting-ready output with mandatory review gates before writing. Trigger on "write a Medium article", "turn this into a Medium post", "Medium version", "make this go viral on Medium".
---

# Medium Writer

Take a source draft, a rough idea, or raw notes and produce a posting-ready Medium article, applying deep platform craft: title and subtitle engineering, hook selection, read-ratio-aware pacing, emotional arc writing, and visual formatting for a narrow reading column. Output is shaped specifically for Medium's distribution system, which rewards completion (read ratio) over clicks.

This skill handles four Medium content types: **Short Article**, **Long Article**, **Tutorial**, and **Listicle**. For Tutorial output, code blocks are written and labeled as unverified — running and verifying code is outside this skill's scope.

## When to use

- User has a `drafts/<slug>.md` source draft and wants a Medium-ready version.
- User pastes raw notes, bullets, or a rough idea and says "make this a Medium article".
- User wants to sharpen or rewrite an existing Medium article with better craft.
- This skill is LinkedIn only for LinkedIn content — use a LinkedIn-specific skill for that.
- Tutorial code blocks produced by this skill are labeled unverified; if verified execution is needed, run the code blocks separately after this skill completes.

## Folder conventions (cwd-relative)

- `drafts/`: source drafts read from here.
- `medium/`: finished Medium files written here.
- `voice-tone/`: voice samples + style instructions.

If `medium/` is needed but missing, STOP and ask the user how to proceed. Never silently create folders.

## Content types

| Type | Word count | Reading time | Primary use |
|---|---|---|---|
| Short Article | 700–1,000 words | 3–5 min | Single insight, personal story, opinion |
| Long Article | 1,300–1,800 words | 6–8 min | Deep dive, layered argument, narrative |
| Tutorial | 800–2,000 words | varies | Step-by-step, code blocks, practical guide |
| Listicle | 800–1,500 words | 4–7 min | Numbered/structured list with depth per item |

If the user has not specified a type, detect the best fit from the input substance, state your reasoning in one line, then ASK for confirmation before writing. Never silently default.

## Voice handling

Before writing anything:
- If `voice-tone/profile.md` exists, read it. Use the `### Medium` subsection of `## Per-Platform Notes` if present — this is the most specific voice signal.
- If only raw samples exist in `voice-tone/`, read them and infer rhythm, vocabulary, and structural habits.
- If `voice-tone/` does NOT exist, note this to the user in one line ("No voice-tone/ found — proceeding with neutral professional voice") and continue. Do not block the skill.

Voice adapts to the content type: Short Articles are more personal and punchy; Long Articles allow a more essayistic, considered tone; Tutorials are instructional but still human; Listicles are direct with real depth per item.

---

## Medium craft rules (apply to all content types)

These are the non-negotiable mechanics of writing well for Medium. Apply every rule on every piece.

### 1. Title engineering

Medium shows the title to browsers and search before anything else. A reader spends about 5 seconds deciding whether to click — this is the single biggest lever.

**Title mechanics:**
- **Lead with "I" and a stake (first-person) or a named role and a stake (third-person).** First-person titles with a specific, lived outcome consistently outperform generic advice titles: "I Deleted Every App on My Phone for 30 Days — Here's What Actually Changed" earns a click while "How to Be More Productive" is forgettable. For third-person voice profiles, the equivalent is leading with a named role, team, or organization plus a concrete outcome: "How Engineers Cut Databricks Costs by 60% Without Sacrificing Performance" applies the same specificity lever without first-person framing. Either way: specific outcome > vague promise.
- **One promise, not three.** Pick the single strongest idea and put only that in the title. If you're tempted to use "and," you have two titles fighting each other — cut to the better one.
- **Specific numbers, timeframes, and outcomes build trust.** "3 Habits That Fixed My Sleep in 2 Weeks" beats "The Secret to Sweet Dreams." Specificity is a credibility signal.
- **Write 10 title variants before choosing.** Your first instinct is the most generic one everyone else already wrote. Force past the obvious options — the interesting angle is usually title #7 or #8.
- **Read it aloud as a stranger.** If you'd have to explain what it means, it's not ready.
- **Format correctly:** use Title Case (capitalize every word except small prepositions and articles), no ending period. Medium curation can disqualify improperly formatted titles.

**Weak → strong example:**
- Weak: *"Lessons From My First Startup"*
- Strong: *"My Startup Failed in 11 Months. Here's the One Decision That Killed It."*
- Strong (third-person): *"Startups That Failed in Year One Share This One Decision. Here's What It Was."*

The second version has a timeframe, a stake (failure), and a single specific promise — not a grab-bag of lessons.

### 2. Subtitle engineering

The subtitle appears everywhere your title does — feeds, profile listings, digest emails. It's your second and last chance to convert a browser into a reader.

**Subtitle mechanics:**
- **Subtitle = the title's unanswered question.** If the title raises curiosity, the subtitle should deepen it, not resolve it. Never summarize the ending.
- **Do a different job than the title.** Title = hook. Subtitle = context or stakes. Together they read like a two-line pitch, not two versions of the same sentence.
- **Keep it under ~15 words.** Longer gets truncated in previews and loses its punch.
- **Format it correctly.** Type the subtitle on the line immediately below the title, highlight it, and click the small "T" icon. Without this, Medium treats it as a regular paragraph and it won't display in previews or curation.

**Example:**
- Title: *"My Startup Failed in 11 Months. Here's the One Decision That Killed It."*
- Subtitle: *"It wasn't the funding, the market, or my co-founder. It was something I did in week one."*

The subtitle rules out the obvious answers (new tension) without revealing the resolution. It adds information the title didn't — that's its only job.

### 3. Opening hook (first 2–3 sentences)

Medium does not count a "read" unless someone stays past roughly 3 seconds. The opening affects your read ratio more than any other single paragraph.

**Four hook types, each writeable cold and alone:**

1. **Observational hook** — state a plain, specific fact or scene with no editorializing. Forces curiosity through concreteness.
   > *"I quit my job on a Tuesday, told no one, and didn't apply for a new one for six months."*

2. **Narrative hook** — drop the reader into a moment mid-action, before explaining anything.
   > *"The email said 'final decision' in the subject line. I read it twice before I understood what it meant for my rent."*

3. **Rhetorical hook** — ask a question the reader silently answers "yes" to, which pulls them into agreeing to keep reading.
   > *"Ever made a decision in five minutes that took five years to undo?"*

4. **Authority hook** — open with a claim or number that positions you as worth listening to, then immediately back it with a specific detail (not a vague credential).
   > *"I've read over 200 rejection emails. Only one of them changed how I write."*

These four types are the core opening hooks for Medium articles.

**For deeper hook engineering**, read `$SKILL_DIR/reference/hook-writing-guide.md` (resolve `$SKILL_DIR` to this skill's directory — the guide lives alongside this SKILL.md under `reference/`). It contains the full framework: curiosity gap theory, four psychological levers, five hook types, a 7-dimension scoring rubric, and naturalness check. Apply those tools to score and select variants when hook quality is the focus of the session. This skill works without the guide — the four types above are sufficient for most sessions.

**How to pick:** write one variant per type, read all four aloud, cut the three you didn't reach for instinctively.

**Trap to avoid:** if your first sentence could open any article on this topic, delete it and start one sentence later — the real hook is usually already in sentence two or three.

### 4. Length and pacing

Medium's algorithm weighs read ratio — the percentage of people who finish, not just click. A good read ratio is 20–50%. Shorter pieces score higher because they're easier to complete; longer pieces only win if every section earns its place.

**Pacing mechanics:**
- **Decide length before drafting, not after.** Personal story or opinion: 3–5 min (700–1,000 words). How-to or deep dive: 6–8 min (1,300–1,800 words). Roughly 7 minutes (~1,400–1,600 words) is often the sweet spot for meatier pieces.
- **Cut in a second pass, not the first.** Draft freely. Then remove every paragraph that restates something already said — redundancy is the #1 killer of read-through on Medium.
- **One idea per paragraph.** If a paragraph is doing two jobs, split it. Dense paragraphs are where readers silently drop off.
- **End sections on a pull, not a period.** Close each section with a line that creates a small question for the next one, so scrolling feels like following a thread rather than finishing a chapter.

**Self-check (no tools needed):** read the draft back and mark every paragraph where you'd personally stop reading if skimming. If more than 20% of paragraphs get marked, that's the cut list.

### 5. Formatting for the eye

Medium's narrow reading column makes undifferentiated text look like a wall. Use the platform's formatting tools so the page doesn't cause silent bounces.

**Formatting mechanics:**
- **Break every 3–5 sentences.** Even mid-thought is fine stylistically if it improves scannability.
- **Use one pull quote per 400–500 words** for longer pieces — pick the single sharpest sentence and format it as a pull quote so skimmers get the takeaway even if they don't read every word.
- **Use subheaders to mark real shifts** in argument or story, not arbitrary breaks. Subheads should work as a mini table-of-contents if someone only reads those.
- **Title Case for main subheads, Sentence case for sub-subheads.** Stay consistent — inconsistent header casing signals sloppiness to readers even if they can't name why.
- **Never format title/subtitle with bold or the small "T" icon as a workaround.** Medium's curation system can disqualify improperly formatted titles.

**Reference structure for a 1,500-word piece:**
```
Hook (2–3 sentences, no header)
Section 1 — setup [Header]
  3–4 short paragraphs, 1 pull quote
Section 2 — turn [Header]
  3–4 short paragraphs
Section 3 — resolution [Header]
  2–3 short paragraphs
Closing line (1–2 sentences, echoes the hook)
```

### 6. Writing toward a specific emotion

This is the deepest lever and the one most writers skip. High-arousal emotions — awe, anger, anxiety — get shared significantly more than low-arousal emotions like sadness, even when writing quality is equal. Neutral, purely informational writing is the hardest thing to make spread.

**Emotion mechanics:**
- **Before drafting, name the one feeling you want the reader to have when they finish.** Not "informed" — that is not an emotion. Try: relieved, indignant, awestruck, unsettled, validated. Write it at the top of your draft as a private note.
- **Reverse-engineer from the ending.** Draft the last paragraph first if you're struggling — knowing the emotional landing makes it much easier to build a path toward it rather than discovering the feeling by accident in revision.
- **Turn abstractions into a single moment.** "Burnout is a serious problem" produces no arousal. "I cried in a parking lot before a client call and then muted myself and finished the call anyway" produces arousal — it's concrete and specific.
- **Don't manufacture outrage or fear artificially.** Readers can tell, it damages trust, and Medium's system penalizes hollow clickbait through lower read ratios.
- **Sadness alone under-performs — pair it with a turn.** If your story is genuinely sad, give it a second beat: hope, defiance, a hard-won insight. Sadness plus resolution reads very differently than sadness alone.

**Self-check:** after finishing the draft, ask: *"If a stranger read only my last paragraph, would they feel something specific enough to want to tell someone about it?"* If the honest answer is "they'd feel informed," go back and find the one true, specific moment in the piece and build the ending around that instead.

### 7. Headline-to-content honesty

Medium's distribution system was explicitly built to reward completion, not clicks. A punchy title that oversells actively hurts your read ratio, which then throttles future distribution.

**Honesty mechanics:**
- **After drafting, reread only your title, subtitle, and final section back to back.** If the ending doesn't deliver on what the title promised, fix whichever is true: the title is overselling, or the piece needs a stronger landing.
- **Avoid "you won't believe" framing** unless the reader genuinely won't — Medium readers are experienced with the platform and clock hollow curiosity gaps fast, which shows up as high bounce, not high reads.

---

## Workflow

### Step 1 — Intake and type selection
Read the input (source draft, file, or pasted notes). If a content type has not been specified:
- Detect the best fit from the substance (single insight or personal story → Short Article; layered argument with multiple sections → Long Article; step-by-step with code or instructions → Tutorial; structured numbered list with depth per item → Listicle).
- State your recommendation in one line with brief reasoning.
- STOP and ask the user to confirm the type before proceeding.

### Step 2 — Title and subtitle engineering (mandatory first stop)
Before any other drafting work:
- Generate **10 title variants**. Number them 1–10. Avoid generic forms in the first 5; push harder on variants 6–10.
- Mark the top 2–3 titles with a brief note on why (specificity, stake, promise).
- Generate **3 subtitle variants** for the top title. Label each with its job (adds stakes / adds context / deepens tension).
- STOP and present titles and subtitles to the user. Ask them to pick one title and one subtitle (or mix elements).
- Do NOT write any body copy until a title AND subtitle are selected.

### Step 3 — Opening hook (mandatory second stop)
After title and subtitle are confirmed:
- Generate **4 hook variants**, one per type (Observational, Narrative, Rhetorical, Authority). Label each.
- Apply the aloud test mentally to each. Mark the 1–2 strongest with a brief note on why.
- STOP and present only the hooks. Ask the user to pick one or mix elements from two.
- Do NOT draft the full body until a hook is selected.

### Step 4 — Draft the full piece
Using the selected title, subtitle, hook, and the craft rules above:
- **State the target emotion** in one word before drafting (e.g. "Target emotion: unsettled"). This is a private production note shown to the user in the audit step.
- Select the section structure appropriate to the content type (use the reference structure from Rule 5 as a base). State which structure and why (one line).
- Write the body applying: one-idea-per-paragraph, 3–5 sentence paragraph cap, pull quotes at appropriate intervals, section-end pulls, specificity rules, emotion arc building toward the stated feeling.
- Write the closing paragraph last — it must deliver the stated emotion and honor the title's promise.
- Apply the human-voice checks from the voice profile as you write, not only at the end.

Do NOT present the draft yet — proceed to Step 5 first.

### Step 5 — Self-audit (run before review)
Before showing the draft to the user, run these checks internally and report the results:

| Check | Pass criteria |
|---|---|
| Title format | Title Case; no ending period; single promise; under ~70 characters |
| Subtitle format | Under ~15 words; does a different job than the title; adds new information |
| Hook check | First sentence cannot be deleted without losing something; no throat-clearing present |
| Length match | Word count within target range for the chosen content type |
| Paragraph density | No paragraph over 5 sentences; blank line between every paragraph |
| Emotion anchor | Closing paragraph delivers the named target emotion, not just information |
| Title-to-content honesty | Ending delivers what the title promised; no oversell |
| Pull quote presence (Long/Tutorial/Listicle only) | At least 1 pull quote per 400–500 words. Skip this check for Short Articles. |

Report each check as PASS or FLAGGED with a one-line note. Fix all FLAGGED items before presenting to the user. If a check still fails after one fix attempt, flag it for the user rather than looping silently.

### Step 6 — Review-first (mandatory stop)
Present:
1. The full draft.
2. The self-audit results (all checks + any fixes made).
3. The target emotion (one word) and a one-line note on the section structure used.

STOP. Ask the user to approve, request edits, or reject. Do NOT write any file yet. Iterate on the draft in place if edits are requested, re-running the self-audit after each significant change.
If running non-interactively (e.g. in a batch pipeline or scripted run), document this gate as "skipped — auto-proceeding with output as drafted" and continue; do not silently omit the gate from the output log.

### Step 7 — Persist (after approval)
**Voice compliance gate (before write).** If `voice-tone/profile.md` (or raw `voice-tone/` samples) is present, scan the approved text against its "Avoided Words & Phrases" and "Punctuation & Formatting Quirks" sections. Auto-fix mechanical violations (em-dashes, banned punctuation) and report what changed. Flag judgment-call violations (hype words, AI-voice markers) for the user. Never emit a banned pattern. If no voice-tone exists, skip silently.

Write the file:
- Short Article → `medium/<slug>-short.md`
- Long Article → `medium/<slug>-long.md`
- Tutorial → `medium/<slug>-tutorial.md`
- Listicle → `medium/<slug>-listicle.md`

**Overwrite policy**: never silently overwrite an existing file. If the target exists, ask: overwrite, write a `-v2` variant, or pick a new name.

Confirm the exact written path to the user.

If a `content-log.json` tracker exists at cwd, ask in one line whether to update the piece's status to `reviewed`.

## Handoff

Tutorial articles produced by this skill contain code blocks labeled `# unverified` — running and verifying those blocks is a separate step outside this skill's scope.

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
