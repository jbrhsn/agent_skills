# Algorithm Mechanics

Why the hard rules exist. Read this when auditing a draft (workflow step 5) and when filling the posting-notes file.

## Contents
- [How distribution actually works](#how-distribution-actually-works)
- [What the ranker rewards](#what-the-ranker-rewards)
- [What the ranker punishes](#what-the-ranker-punishes)
- [The audit pass](#the-audit-pass)
- [Timing and the first hour](#timing-and-the-first-hour)

---

## How distribution actually works

LinkedIn's feed runs on an LLM-based ranking stack rather than a like-counting heuristic. Two layers matter:

1. **Retrieval.** An encoder reads the semantic meaning of the post and matches it against each member's inferred interests. This is why a post can reach people who don't follow the author — if the topic fits their "topic DNA", they become candidates.
2. **Ranking.** A transformer orders candidates by *predicted relevance and engagement quality*, not by predicted like count.

The practical consequence: **the post's subject matter is a distribution lever, not just a content choice.** A clearly-about-one-thing post gets matched confidently. A post that wanders across three topics gets matched weakly to all of them and distributed to nobody in particular.

This also means consistency compounds. An author who posts on two or three recurring topics accumulates topical authority in the retrieval layer, and their posts get shown to interested non-followers. The niche tag in the posting notes exists to make that consistency visible over time.

## What the ranker rewards

**Dwell time — the dominant signal.** The system measures how long someone reads before scrolling away, not whether they tapped a reaction. Posts holding attention for a minute or more materially outperform posts scanned in three seconds. This is the mechanical reason the value section has to actually deliver something: padding buys length but loses dwell time, because readers bail.

**Saves.** The strongest long-tail signal. A save tells the ranker the content has reference value beyond the moment, which extends distribution well past the first day. Content shaped as a framework, a checklist, a decision rule, or a numbered process gets saved. A pure anecdote rarely does. When `source.md` contains something generalizable, shaping it as a reusable rule is worth more than shaping it as a story.

**Substantive comments.** Comments carry roughly an order of magnitude more weight than likes, and multi-reply threads carry more than single comments. Crucially the ranker distinguishes *substantive* replies from "Great post!" — generic comments no longer help. This is why the closing question has to be answerable with a real opinion. A question anyone can answer with one word generates the kind of comment that no longer counts.

**Author replies.** Replying to comments in the first couple of hours meaningfully lifts a post's lifetime engagement. This belongs in the notes file as a reminder, since it's the author's job, not the draft's.

## What the ranker punishes

**External links in the body.** Roughly 50–70% reach reduction. The platform is suppressing exits. The workaround is stable and widely used: post the full value as text, put the URL in the first comment, and optionally reference it in the post as "link in the comments". Every URL found in `source.md` goes to the notes file, never into `linkedin_post.md`.

**Engagement bait.** The platform has publicly acknowledged that a majority of high-engagement 2025 posts used tactics that didn't produce genuine satisfaction, and shipped ranking changes to deprioritize them. Detection covers explicit bait ("comment YES", "repost if you agree", "tag someone"), reaction polling, and manufactured curiosity gaps that the post never pays off. The last one is subtle and worth checking: a hook that promises a revelation the body doesn't deliver is bait even without a bait phrase in it.

**Reciprocal engagement patterns.** Pods are detected with high accuracy and draw silent reach penalties. Not a drafting concern, but worth never recommending in the notes.

**Hashtag stuffing.** Hashtag influence has weakened to near-noise. Natural use of the domain's actual vocabulary in the prose feeds the retrieval encoder far better than appended tags. Zero to three specific tags is the ceiling, and zero is a fine answer.

## The audit pass

Run every draft through this before writing files. Treat failures as rewrite triggers, not as notes to mention.

1. **One idea?** Can the post be summarized in a single sentence? If it takes two, cut one.
2. **Hook fold-safe?** Does the first ~140 characters stand alone and create tension?
3. **Promise paid?** Does the body deliver exactly what the hook implied? Unpaid promises are bait.
4. **Dwell-worthy?** Is there a sentence a knowledgeable reader would stop on? If every line is generic, the post has no reason to hold attention.
5. **Save-worthy?** Is there a reusable rule, framework, or number? If not, is that acceptable for this post's goal?
6. **Comment-worthy close?** Could a smart person disagree with the closing question in a paragraph? One-word-answerable questions fail.
7. **Zero URLs in the body?**
8. **Zero bait phrases?**
9. **Character count in the 1,200–1,600 band?**
10. **Facts traceable to `source.md`?** Every number, quote, and anecdote must be in the source. No exceptions.

## Timing and the first hour

The post is tested on a small slice of the network first — a few percent — and how that slice behaves in the first 60 to 90 minutes largely determines whether distribution expands. Posts that underperform in that window rarely recover.

Practical guidance for the notes file:
- **Best days:** Tuesday through Thursday.
- **Best windows:** roughly 8–10am and 12–1pm in the *audience's* timezone. Infer the audience's geography from `source.md` where it's evident; otherwise default to the author's local working hours and say so.
- **Author availability matters more than the exact slot.** Posting when the author can reply for the next 90 minutes beats posting at a theoretically optimal time and disappearing.
- **Scheduling tools do not incur a penalty.** Don't warn against them.
