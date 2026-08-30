# Medium mechanics

Platform specifics needed when packaging `medium_publish.md`. Behaviour changes over time; treat anything here that contradicts what the user sees in the editor as out of date.

---

## The header block

Three elements, in order, above the body:

**Kicker** — optional. A word or short phrase above the title, used for a series name or category. Created by placing text above the title line and applying the small "T" format. Only works above the title.

**Title** — the first line of the story. Applied with the large "T". Only the first line is treated as the title.

**Subtitle** — the line directly below the title, applied with the small "T". A subheader in that position converts into the story's subtitle.

Formatting matters mechanically, not just visually: an unformatted title or subtitle can leave the story's metadata wrong and weakens it in curation. Always include the formatting steps in `medium_publish.md` — the user is pasting markdown into a WYSIWYG editor and the header block will not survive the paste intact.

The title, subtitle, and cover image together are what a reader sees in the feed. Medium will not Boost a story if those three don't convey enough about the piece to let a reader decide.

## Titles

Supply five options, spanning different strategies rather than five rewordings of one:

1. **Position** — states a claim the reader can dispute. *Airflow Was the Wrong Abstraction for Our Team*
2. **Outcome with a number** — *We Cut Our Warehouse Bill 40% by Deleting Three dbt Models*
3. **Problem-first** — *The Silent Failure Mode in Every Incremental Model I've Shipped*
4. **Contrarian** — *Stop Reaching for a Vector Database*
5. **Plain and descriptive** — *How Iceberg Compaction Actually Works*

Avoid: "N Things", "The Ultimate Guide to", "Everything You Need to Know About", "You Won't Believe", question titles answerable with yes or no.

Rough length target: under about 60 characters so it doesn't truncate in feeds and search.

## Subtitles

One sentence. It should add information, not restate the title. Its job is to answer "what specifically am I getting?"

Weak: *A deep dive into data pipeline optimization.* Strong: *What broke at 400M rows a day, what we tried first, and the config that actually fixed it.*

## Tags

Five per story. The first three matter most for where the story enters reader feeds.

- First three: narrow and specific. *Apache Iceberg*, *dbt*, *LLM Evaluation*.
- Remaining two: broader reach. *Data Engineering*, *Artificial Intelligence*.
- At least one should be an Explore-page topic — this matters most for writers with a small follower count.
- Tags must genuinely describe the piece. Off-topic tagging forfeits General Distribution.

## Distribution tiers

Worth understanding because it explains reach:

- **Network** — baseline. Goes to the writer's own followers, and the publication's if the piece is in one. Everything that doesn't break the rules gets at least this.
- **General** — matched to readers by interest and related follows. Forfeited by the disqualifiers in `do-and-avoid.md`.
- **Boost** — curated amplification, layered on top of the other two. Reviewed by humans against the Boost guidelines.

These tiers only govern discovery inside Medium's own surfaces — feed, digests, app. Direct links, search, and social sharing work regardless of tier.

## Publications

For an account under roughly 5,000 followers, the publication is the distribution. Editor nominations drive about half of all Boosted stories, and a piece on a small personal profile reaches almost no one by comparison.

In `medium_publish.md`, name one or two plausible target publications for the piece's topic and note that submission guidelines should be checked before submitting — each publication sets its own requirements, and several mandate a kicker and subtitle.

## Images

- Every image needs alt text. Supply it in `medium_publish.md` for each image the article references — Medium's guidelines call out alt text and credits explicitly.
- Images should carry information: diagrams, screenshots, real output, architecture sketches. Decorative stock adds nothing and can hurt.
- Captions carry credits. AI-generated images must be captioned as such.
- No cover image is better than a poorly chosen one.

## Paste workflow

The article is written as markdown but Medium's editor is not a markdown editor. Include these steps in `medium_publish.md`:

1. Paste the body first, leaving the title area alone.
2. Move the title to the first line, select it, apply the large "T".
3. Select the subtitle line below it, apply the small "T".
4. Re-apply subheads — pasted `##` may arrive as body text. Large "T" for section headers, small "T" for sub-sections.
5. Re-create code blocks. Medium supports embedded Gists for anything longer than a few lines, which render better and stay copyable.
6. Insert images, then add captions and alt text.
7. Add the five tags in the publish dialog, ordered deliberately.
8. Check the preview title and subtitle in the three-dot menu before publishing.

## After publishing

Note in `medium_publish.md`: if click-through sits below about 3% after 48 hours, the title is the problem, not the topic. Rewriting the title on a live story is cheaper than writing a new piece.
