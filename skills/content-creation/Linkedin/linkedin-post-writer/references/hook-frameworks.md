# Hook Frameworks

The hook decides whether the post exists. Read this at workflow step 3.

## Contents
- [The fold](#the-fold)
- [The predictability test](#the-predictability-test)
- [Hook types](#hook-types)
- [The re-hook](#the-re-hook)
- [Hook anti-patterns](#hook-anti-patterns)
- [Working method](#working-method)

---

## The fold

LinkedIn truncates at "see more" — around **140 characters on mobile**, ~210 on desktop. Mobile is the constraint that matters.

Two structural consequences:

**Write the hook for 140 characters.** Everything after that is read only by people who already committed. A hook whose payload lands at character 190 has no hook on mobile.

**Use white space to push the fold down.** A common move among strong creators: one sharp opening line, then a double line break. The blank line consumes fold space, so the reader sees the complete hook and a gap rather than a hook cut mid-sentence. The reader has already absorbed the full opening before "see more" appears.

## The predictability test

The single most useful filter. Read only the first line, then ask: **can I predict the rest of the post?**

If yes, the hook is dead. It has announced its own conclusion and given the reader permission to scroll.

- ❌ "Here are 5 lessons I learned from building an AI agent." — Predictable. The reader knows the shape, the genre, and roughly the content.
- ✅ "Our agent worked perfectly in eval and failed on day one in production. The gap wasn't the model." — Unpredictable. Creates a specific question the reader now wants answered.

Second filter: **the walk-away test.** If someone read the hook, got distracted for a minute, and came back — would they still want to know the answer? Curiosity that survives a distraction is real curiosity. Curiosity that only exists because a sentence trailed off is a trick.

## Hook types

Pick based on what `source.md` actually contains. Forcing a hook type onto material that doesn't support it produces the fakeness readers detect immediately.

**Counterintuitive claim.** Use when the source contains a genuinely contrarian position. States something the audience believes is wrong.
> Most RAG problems aren't retrieval problems.

**Knowledge gap.** Use when the source contains a hard-won lesson. Signals that something important went unsaid.
> Nobody warned me about this before I shipped my first model to production. It cost six weeks.

**Specific number.** Use when the source contains real data. Numbers are concrete and unignorable — but only when they're actually in the source.
> We cut inference cost by 71% without touching the model.

**Mid-scene story open.** Use when the source contains a real incident. Drops the reader into action with no preamble.
> The pager went off at 3am. The dashboard was green.

**Named-cost admission.** Use when the source contains a mistake. Vulnerability with a concrete price attached, which is what separates it from performative humility.
> I spent four months building the wrong abstraction. Here's the signal I ignored.

**Direct address.** Use when the source targets a specific audience segment. Narrows deliberately, which the retrieval layer rewards.
> If you're an engineer being asked to "add AI" to a product that doesn't need it, this is for you.

**Sharp definition.** Use when the source reframes a familiar concept. Compresses an idea into a line worth stealing.
> An eval isn't a test. It's a disagreement made measurable.

## The re-hook

Lines 3–5, immediately after the fold. Its job is to convert a "see more" click into a full read.

The re-hook makes one **specific promise** about what the reader gets — narrower than the hook, concrete enough to be checkable.

> Hook: Our agent worked perfectly in eval and failed on day one in production.
> Re-hook: The failure mode had nothing to do with the model, and it's now the first thing I check in every system I build.

The re-hook is not a summary and not a thesis restatement. If it can be deleted without the post losing anything, it was a restatement — rewrite it.

## Hook anti-patterns

**Setup throat-clearing.** "I've been thinking a lot about..." / "Recently I had an interesting conversation about..." Burns the entire mobile fold on preamble. Delete the first sentence and check whether the post starts better — it usually does.

**Announcement openers.** "Excited to share..." / "Thrilled to announce..." Reads as a press release, and the reader has correctly learned these posts contain no insight.

**Unpaid curiosity gaps.** "What happened next changed everything." If the body doesn't deliver something that actually qualifies, this is bait — and unpaid bait is the pattern the ranker now suppresses.

**Stacked rhetorical questions.** "Ever felt stuck? Wondered if there's a better way?" Reads as a template, and templates get scrolled.

**Fake specificity.** Numbers or details invented to make a hook land. If the number isn't in `source.md`, the hook can't use it. Rewrite the hook around what's true instead.

**Manufactured stakes.** "This one decision nearly ended my career." If the source says the decision was mildly annoying, the hook is lying, and the body will expose it within three lines.

## Working method

1. Extract the sharpest claim, number, or moment from `source.md`.
2. Draft five hooks across different types. Volume matters more than care at this stage — the first hook is almost always the most obvious one.
3. Kill anything over 140 characters or anything failing the predictability test.
4. Of the survivors, pick the one making the most specific promise the body can genuinely pay.
5. Write the re-hook, then re-read hook and re-hook together as a unit. They should read as one continuous thought, not two competing openings.
