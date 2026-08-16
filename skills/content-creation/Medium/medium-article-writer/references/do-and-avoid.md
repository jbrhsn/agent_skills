# What earns distribution, and what kills it

Two lists. The first is craft. The second is closer to policy — several items are
explicit disqualifiers in Medium's published Distribution Guidelines, and no
amount of good writing routes around them.

Use this as a checklist during the self-audit pass. Fix failures in the file.

---

## Do

1. **Make the writer's authority visible early.** Medium weighs a credible,
   first-hand reason for *this* writer covering *this* topic above any claimed
   credential. If the user built the thing, ran the migration, or ate the outage,
   that must surface in the first few hundred words.

2. **Put one arguable position in the title.** Something a reader can nod at or
   object to. "How We Cut Airflow DAG Runtime by 60% by Deleting the Scheduler"
   beats "Optimizing Airflow Performance."

3. **Make title, subtitle, and cover honestly preview the piece.** Medium will not
   Boost a story when these don't give a feed reader enough context to decide.
   This is a hard gate, not a preference.

4. **Write a subtitle for every piece.** It is the second line a reader sees and
   the main thing that converts a title glance into a click.

5. **Be specific.** Named tools, version numbers, dates, real figures, real
   tradeoffs. "We moved to Iceberg 1.5 in March and the compaction job went from
   40 minutes to 6" is the unit of credibility. "Modern table formats improve
   performance" is filler.

6. **Anchor to something recent when the topic allows** — a release, a CVE, a
   pricing change, a deprecation. Currency is rewarded.

7. **Give the reader something usable on exit.** A checklist, a decision rule, a
   config, a thing to try Monday. The takeaway is what earns the clap and follow.

8. **Earn the click in the first three paragraphs.** State the stakes, the
   promise, and why this writer. No warm-up.

9. **Keep paragraphs to one to three sentences.** Most reading happens on a phone.

10. **Use descriptive subheads every 200–300 words.** They should carry meaning
    when read alone — a reader who only scans the subheads should get the argument.

11. **Vary sentence rhythm deliberately.** Short. Then a longer one that carries a
    qualification or a turn. Uniform cadence is the loudest machine tell there is.

12. **Make images do work.** Diagrams, screenshots, architecture sketches, real
    output. Medium explicitly wants images that add value, with alt text and
    credits. A decorative stock photo of a laptop adds nothing.

13. **Link and source claims,** preferring primary sources: docs, the release
    notes, the paper, the incident report.

14. **Let purpose set length.** Medium states plainly that well-crafted stories can
    be short or long. Do not pad.

15. **Use all five tags, first three narrow.** Broad tags ("AI", "Technology")
    drop the piece into a pool it cannot win. Specific tags ("dbt", "Apache
    Iceberg", "LLM Evaluation") reach the readers who want it. At least one tag
    should be an Explore-page topic.

16. **Target a publication in the niche.** Editor nominations account for roughly
    half of Boosted stories, and for an account under ~5K followers the
    publication path dominates reach. Match the publication's submission rules.

17. **Optimize for completion, not clicks.** A piece at 2,000 views and 85%
    completion is worth more than 5,000 views at 40%. Structure so the reader
    finishes.

18. **Show the failure, not just the fix.** What was tried and abandoned is the
    part no one else writes and the part practitioners trust.

19. **Proofread.** "Free of errors" is named explicitly as a craftsmanship signal
    curators use.

20. **Treat the title as testable.** Medium's own guidance puts a healthy CTR at
    7–10%; 2–3% is a title problem, not a topic problem. Supply five title
    options in `publish.md` so the user can rewrite rather than abandon a piece.

---

## Avoid

1. **Fabricated facts, figures, quotes, or anecdotes.** Medium explicitly bars
   articles containing easily disprovable AI-hallucinated stories, statistics, or
   events. This is the single highest-severity item on the list.

2. **Clickbait and hyperbole.** Misleading or sensational framing disqualifies a
   story from General Distribution.

3. **The opposite failure: vague, mysterious, or formulaic titles.** Medium calls
   these out as just as damaging as sensationalism. "The One Thing Nobody Tells
   You About Data Pipelines" fails on both counts at once.

4. **Meta-Medium posts** — earnings, Boost, the Partner Program. These are capped
   at Network Distribution by policy regardless of quality.

5. **Derivative content.** Paraphrasing, recombining, or rehashing what is easily
   found elsewhere is explicitly non-Boostable. If the piece could have been
   written without the user's specific experience, it should not be published.

6. **Roundups, listicle padding, and link farming.** Named as low-value content.

7. **Pieces whose real purpose is signups, traffic, or sales.** Also named as low
   value. The guidelines warn specifically against leaving the reader feeling
   they read a sales pitch.

8. **Tag spam and mass @-mentions.** Both forfeit General Distribution.

9. **Uncredited or copyrighted images.** AI-generated images must be captioned as
   such.

10. **Unverified health, safety, or financial claims.** A rules violation, not a
    distribution issue. See the financial framing rule in `SKILL.md`.

11. **Prolific profanity and NSFW material** if wide distribution matters.

12. **Non-English drafts.** Not currently eligible for Boost or General
    Distribution.

13. **Rants, outrage bait, and private disputes.** "Unconstructive negativity" is
    a named disqualifier. A strong critical argument is fine; a grievance is not.

14. **Walls of text.** Five- and six-sentence paragraphs destroy mobile read-through.

15. **Burying the lede behind personal preamble.** Earn the digression later, or
    cut it.

16. **Bulleting what should be prose.** Medium is a reading platform. Lists are for
    genuinely enumerable things — steps, options, criteria. An argument in bullet
    form is an argument that was never made.

17. **Bolded-lead bullet stacks.** `**Thing:** explanation` repeated eight times is
    the most recognizable machine-writing layout in circulation.

18. **Keyword stuffing and headline formulas.** "X Things", "The Ultimate Guide
    to", "You Won't Believe" — all pattern-match to content farms.

19. **Hedged, sourceless generalities.** "Many engineers find that…", "It is often
    said…", "Studies show…" without a link. Either name it or cut it.

20. **A conclusion that summarizes.** Restating the article back to the reader
    wastes the last thing they read. End on the takeaway, a decision rule, or a
    genuine open question.

---

## Fast audit

Run these six before presenting. If any fails, fix the file.

- [ ] Would this piece be impossible to write without the user's specific
      experience? If not, it is derivative.
- [ ] Is every number, version, date, and quote either verified or supplied by
      the user?
- [ ] Does the title state a position, and does the article deliver exactly that?
- [ ] Can a reader who only reads the subheads reconstruct the argument?
- [ ] Is there a concrete takeaway a reader could act on tomorrow?
- [ ] Does any paragraph run past three sentences without earning it?
