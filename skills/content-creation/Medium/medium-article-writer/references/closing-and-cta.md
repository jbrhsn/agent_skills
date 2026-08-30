# Closing and CTA

Read this after the draft is written, before the self-audit. The ending is a
separate pass because it is the part most likely to be written on momentum and
least likely to be revised.

Two rules sit in tension elsewhere in this skill and get resolved here.
`do-and-avoid.md` bans a conclusion that summarizes. `voice-and-antislop.md` bans
the stock closers — "In conclusion", "Happy coding!", "What are your thoughts?
Let me know in the comments." Together they can read as a ban on ending the
article at all, which produces a piece that simply stops. That is a worse failure
than a weak conclusion, because the last two hundred words are what a reader
carries out and what decides the follow.

An article needs an ending. It does not need a summary.

---

## The shape of a close

Three parts, in order. The whole thing runs 80–150 words.

**1. The landing.** One or two sentences that finish the argument on its own
terms. Not a recap — the last move of the piece. Often it is the sentence the
whole article was built to earn.

**2. The takeaway.** The decision rule, the checklist, the config, the thing the
reader does differently on Monday. `do-and-avoid.md` item 7 makes this
non-optional; it is what earns the clap. It can be one sentence. In a tutorial it
is often a short list, and that is the one place a list belongs in the close.

**3. The CTA.** See below. Default is a question. It attaches to the takeaway —
same paragraph or the one immediately after — never as a separate block under its
own subhead.

A close that summarizes fails at part 1. A close that stops after part 1 fails at
part 2, which is the more common failure in technical writing.

---

## CTA options

### Question (default)

A genuine question, arising from the argument, that the writer does not already
know the answer to. It is the default because it carries zero promotional weight,
needs no external destination, and works on every piece type.

What makes it real:

- It names the specific case the article did not cover. *"The part I still don't
  have a clean answer for: what do you do when the compaction window and the read
  SLA genuinely conflict? I've only ever solved it by moving the SLA."*
- It admits a limit in the writer's own experience. A question the article
  already answered is rhetorical, and the rhetorical question is a listed tell.
- It could produce a reply the writer would actually read.

What disqualifies it:

- "What do you think?" / "Have you run into this?" / "Let me know in the
  comments." Generic, and the last one is a banned string.
- Anything phrased to farm agreement. "Agree?" is engagement bait.
- A question the piece already settled. That is a summary wearing a question mark.

One question. Two is a survey.

### Soft follow or subscribe

One line, after the takeaway, describing what the writer publishes rather than
asking for the follow. *"I write up one production failure like this a month."*
Never stacked with a question — pick one. Use when the user asks for it, or when
the piece is part of a series and continuity is the actual value to the reader.

### Owned destination

A link to the user's own newsletter, site, or mailing list. Medium's rules permit
first-party promotion; what costs reach is the volume of it, and Boost curators
weigh whether the story serves readers more than it serves the thing being linked.

Constraints if used: one link, at the end, never mid-article, never more than one
sentence of framing, and the article must stand complete without clicking it. No
affiliate links, no "buy", no gated "full version behind the signup". A piece
whose real purpose is signups is a named low-value category in the distribution
guidelines.

Only use this when the user has supplied the destination. Never invent one, and
never write a placeholder link.

### None

Correct when the takeaway is the strongest line in the article and anything after
it would blunt it. Ending on a decision rule is a complete ending. Record it as a
deliberate choice in `medium_publish.md` rather than leaving the CTA field blank.

---

## Defaults

- Default to the **question**, unless the user has said otherwise for this piece
  or in general.
- Never reach for follow, subscribe, or a link on your own initiative. Those are
  the user's call, and guessing at a newsletter that may not exist produces a
  placeholder — which this skill does not ship.
- Record the choice and the reason in `medium_publish.md`. One line. The user
  overrides it in seconds if it is wrong.

## Per piece type

- **Tutorial** — takeaway is the checklist or the decision rule for when this
  approach applies. Question is about the boundary: where the reader's setup
  might differ.
- **Case study / post-mortem** — takeaway is what transfers. Question is about
  the part that did not generalize.
- **Opinion** — takeaway is the practical consequence of the claim. Question
  targets the strongest counter-case, honestly. Do not end an argument by
  restating it louder.
- **Explainer** — takeaway is when this matters in practice. Question is a real
  edge the writer has hit.
- **Experience report** — takeaway is what the user would do differently.
  Question follows naturally from that.

## Finance and health pieces

The close is where prescriptive framing creeps back in after being stripped from
the body. No "you should", no "start by opening a…", no implied recommendation in
the question. The takeaway is what the user did and would change, stated in first
person. No link to any financial product, ever.

## Check before presenting

- [ ] The close does not restate the article.
- [ ] There is a concrete takeaway, not just a landing.
- [ ] The CTA is one of the four options and is recorded in `medium_publish.md`.
- [ ] If it is a question: specific, genuinely open, one of them, answerable by a
  practitioner.
- [ ] No banned closer, no engagement bait, no placeholder link.
- [ ] The last sentence is worth being the last sentence.
