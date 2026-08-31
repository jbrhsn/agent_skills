# Calibration

Two pairs, one technical and one not. Read the pair closest to your domain if you are unsure whether the writing is hitting the bar — and read the other one too if you are tempted to import an engineering shape into a field that has its own.

Note what the strong versions do **not** do: they do not print the six obligations as labels. The obligations are answered in prose, in whatever order reads best. A unit that reads as a form with fields filled in has failed even if every field is correct.

---

# Pair 1 — technical

## Weak

> ### Indexes
>
> Indexes are a powerful database feature that dramatically improve query performance. An index is a data structure, typically a B-tree, that allows the database to locate rows efficiently without performing a full table scan.
>
> Key benefits:
> - Faster SELECT queries
> - Efficient sorting and range queries
> - Enforcement of uniqueness constraints
>
> However, indexes also have downsides, as they consume storage and slow down writes. It is recommended to index columns that appear frequently in WHERE clauses.

**What's wrong:** no takeaway — the reader doesn't know what they're about to gain. Opens with a definition instead of a problem, so there's no reason to care yet. "B-tree", "full table scan", "SELECT", "WHERE clause" all appear undefined; a beginner is now four terms behind. "Dramatically" and "powerful" are adjectives standing in for numbers. The benefits are bullets — parallel facts with no reasoning between them. No example, nothing concrete to follow. No trap, so the reader leaves believing "more indexes = faster", which is exactly what this unit should have killed. "It is recommended" by whom? And nothing here is top-rung: no failure mode, no scale, no alternative.

## Strong

> ### Why an index makes a query ten thousand times faster · ~5 min
>
> **An index is a second, sorted copy of one column, kept alongside the table — which is why it makes reads fast and writes slow.**
>
> You have a table of ten million users and you want the one whose email is `sam@example.com`. The database has no idea where that row is, so it does the only thing it can: reads row one, checks the email, reads row two, checks the email, and keeps going until it finds a match or runs out of table. That's a *full table scan*, and on ten million rows it takes seconds. Your page is slow, and it gets slower every time someone signs up.
>
> So you keep a smaller structure on the side: a sorted list of every email, each paired with the location of its row. Finding an email becomes a search through a sorted list rather than a walk through the whole table. That side structure is an **index**.
>
> It's the index at the back of a textbook — sorted terms, each pointing at a page number. You don't read the book to find "photosynthesis", you look it up and jump. The analogy breaks in one place, and it's the important place: a book's index is printed once and never changes, while a database index has to be updated on every single insert. That cost is the whole reason you don't index everything.
>
> Databases don't actually use a flat sorted list, because the list lives on disk and disk reads happen in fixed-size blocks called *pages*, commonly 8 KB. They use a **B-tree**: a shallow, wide tree where each node fills one page and holds many keys. Searching reads one page per level. Because the tree is wide it is also shallow — even a billion rows is usually four levels deep. Four page reads instead of a million.
>
> Work it through with ten million users, 8 KB pages, and each index entry — email plus row pointer — about 40 bytes:
>
> - Entries per page: 8192 / 40 ≈ 200
> - Leaves: 10,000,000 / 200 = 50,000 pages
> - Next level up: 50,000 / 200 = 250 pages
> - Then: 250 / 200 = 2 pages
> - Then: 1 page — the root
>
> Four levels, so a lookup is four page reads. The full scan would have read on the order of a hundred thousand pages. That's the factor of ten thousand you keep hearing quoted, and you can now derive it instead of repeating it.
>
> Which leads people somewhere reasonable and wrong: *indexes make queries fast, so I should index every column.* Each index really does speed up reads on its column — the inference is sound as far as it goes. But every index is a separate B-tree that must be updated on every insert, update, and delete. Ten indexes means one row insert triggers eleven writes. A table with heavy write traffic and generous indexing can end up slower overall than the unindexed version, and the symptom appears in write latency, not in the query you were trying to optimise. That mismatch is why it takes teams so long to diagnose.
>
> What you bought was read speed; what you sold was write speed and disk. That trade is worth it when reads outnumber writes, which covers most application workloads but not all — a high-volume event log written constantly and queried nightly may be better with almost no indexes. Two alternatives are worth knowing: hash indexes give faster exact-match lookups but cannot serve ranges or sorting, because hashing destroys ordering; log-structured merge trees invert the trade entirely, making writes cheap and reads dearer, which is why write-heavy stores like Cassandra use them.
>
> At scale the cost shows up in bulk loads. Inserting ten million rows into a table with six indexes can take an order of magnitude longer than into a bare table. The standard move is to drop the indexes, load, and rebuild. The standard incident is the team that didn't, watched the load run for nine hours, and never worked out why.
>
> **Check yourself.** Your table has one index on `email`. You add five more on other columns. Lookups by email — the ones you actually cared about — get slower. Why?
>
> <details><summary>Answer</summary>
> The email index is unchanged, so searching it costs exactly what it did before.
> What changed is around it: five more B-trees now compete for the same memory
> cache, so pages of the email index get evicted and re-read from disk. The lookup
> didn't get algorithmically worse — it stopped being served from memory.
> </details>

**Why it works:** the claim is stated before it's earned, so the reader has a frame. It opens with a problem they can feel, defines every term at the moment it's needed, derives its numbers rather than asserting them, names the misconception in the reader's own voice and explains why it's tempting, and ends somewhere a practitioner couldn't reach alone. The closing question can't be answered by scanning back up the page. And nothing is labelled — the obligations are all met, invisibly.

---

# Pair 2 — craft

Same standards, different evidence. Watch what replaces the code and the numbers.

## Weak

> ### Writing strong openings
>
> The opening line of an essay is crucial. It must hook the reader and make them want to continue. Great writers know how to craft compelling first sentences that draw readers in.
>
> Techniques include:
> - Starting with a surprising fact
> - Asking a provocative question
> - Opening with vivid imagery
> - Using a bold declarative statement
>
> Avoid clichéd openings and overly long sentences. Practice writing multiple openings for each piece and choose the strongest one.

**What's wrong:** it is the technical weak version with the nouns swapped, and it fails identically. No takeaway. "Crucial", "compelling", "draw readers in" — grading by adjective, which teaches nothing about what to actually do. A bulleted list of techniques with no reasoning connecting them and no way to choose between them. Not one line of real writing appears anywhere, so there is nothing to study. No trap, no cost, nothing a reader couldn't have guessed. "Choose the strongest one" — by what test?

## Strong

> ### What an opening line is actually for · ~5 min
>
> **An opening line's job is not to be interesting. It is to make the second line unavoidable — which is why "hooks" so often fail.**
>
> Here is a first line that is genuinely interesting and still doesn't work: *"There are more possible chess positions than atoms in the observable universe."* It's true, it's startling, and most readers stop after it. They got the fact. It's a complete unit of information, and nothing about it obliges them to keep going.
>
> Now Joan Didion, opening *The White Album*: *"We tell ourselves stories in order to live."* Less startling, harder to leave. It makes a claim that isn't finished — you don't yet know what "in order to live" is doing there, and the sentence has quietly promised that the next one explains. That gap is the mechanism. An opening works by leaving something structurally incomplete, not by being impressive.
>
> A line of dialogue works the same way: someone says something, and you cannot let the room stay silent. The analogy breaks where writing has an advantage — a reader who puts your essay down loses nothing socially, so your gap has to do all the work that awkwardness does in a conversation.
>
> Watch a revision. First attempt: *"Remote work has fundamentally changed how companies operate, and many are still adapting to this new reality."*
>
> Nothing is incomplete here. "Fundamentally changed" is an adjective doing the work a specific should be doing; "many are still adapting" could precede any of ten thousand articles, so it promises nothing in particular. A reader who stops loses nothing.
>
> Second attempt: *"Three years in, my company still hasn't worked out who owns the calendar."*
>
> Four things changed. It's specific — one company, one artefact. It admits a failure, which buys credibility, because a writer who opens by conceding is not selling. "Three years in" sets a clock without explaining it. And "who owns the calendar" is a phrase nobody uses, so the reader has to keep reading to find out what it means. The gap is now doing the work.
>
> Which is where the standard advice sends people wrong: *make the first line as striking as possible.* It's a reasonable reading of every list of hook techniques ever published. But a maximally striking line is usually a complete one — the surprising statistic, the grand declaration — and completeness is what lets a reader leave. Strikingness and incompleteness are different properties, and only the second one is load-bearing. This is why so many essays open with a bang and lose the reader by paragraph two: the opening spent the tension instead of creating it.
>
> An opening built on a gap buys attention and pays in obligation. You now have to close it, soon, and honestly — a gap you don't pay off within a paragraph or two reads as a bait-and-switch, and the reader trusts nothing after it. That's the real cost, and it's why the strongest opening for a piece you can't deliver on is a plainer one. The alternative is worth knowing: reference and technical writing legitimately opens flat, stating the conclusion first, because that reader arrived already committed and wants the answer, not a reason to continue.
>
> At the top of the craft this inverts. A writer with an established readership can open flat — *"I want to talk about my father"* — because the relationship supplies the obligation that the sentence doesn't. Which is precisely why imitating an established writer's openings is such reliably bad advice for someone without their readership.
>
> **Check yourself.** Two openings for the same essay. (a) *"Every year, four million people quit jobs they say they love."* (b) *"I gave notice on a Tuesday, and by Thursday I had run out of ways to explain it."* Both are specific and both are true. Which is likelier to get the second paragraph read, and why?
>
> <details><summary>Answer</summary>
> (b). (a) is a complete fact — surprising, but it closes. A reader can take the
> statistic and go. (b) leaves two things open: what the explanation was, and why
> it ran out. Neither can be resolved without reading on. Specificity is not the
> variable that separates them; completeness is.
> </details>

**Why it works:** it meets exactly the same six obligations. The problem is a real opening that fails, quoted. The evidence is a published line by a named writer, plus a before/after where every edit is named. The trap is standard advice, taken seriously before it is dismantled. The cost is real and the alternative is named. The top-rung note explains a real thing beginners get wrong by imitation. There is no code and no number in it anywhere, and it is not one step less rigorous for that.
