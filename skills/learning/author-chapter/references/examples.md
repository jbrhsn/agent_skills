# Calibration example

The same concept — a database index — written twice. Read both if unsure whether the writing is hitting the bar.

---

## Weak version

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

**What's wrong with it:**

- Opens with a definition, not a problem. The reader has no reason to care yet.
- "B-tree", "full table scan", "SELECT", "WHERE clause" all appear undefined. A beginner is now four terms behind.
- "Dramatically improve" and "powerful" are adjectives standing in for numbers.
- The benefits are a bulleted list — parallel facts with no reasoning connecting them.
- No example at all. Nothing concrete, no values, nothing to follow.
- No trap. The reader will walk away believing "more indexes = faster", which is the exact misconception this section should have killed.
- "It is recommended" — by whom? The tradeoff is asserted, never explained.
- Nothing here is architect-level. No failure mode, no scale, no alternative.

---

## Strong version

> ### Indexes
>
> **The problem.** You have a table of ten million users and you want the one whose email is `sam@example.com`. The database has no idea where that row is, so it does the only thing it can: it reads row one, checks the email, reads row two, checks the email, and keeps going until it finds a match or runs out of table. That's called a *full table scan*, and on ten million rows it takes seconds. Your page is now slow, and it gets slower every time someone signs up.
>
> **The idea.** So you keep a second, smaller structure on the side: a sorted list of every email, each one paired with the location of its row. Now finding an email is a search through a sorted list rather than a walk through the whole table. That side structure is an **index**.
>
> **An analogy.** It's the index at the back of a textbook: sorted terms, each pointing at a page number. You don't read the book to find "photosynthesis" — you look it up, then jump. Where the analogy breaks: a book's index is printed once and never changes, while a database index has to be updated on every single insert, and that cost is the whole reason you don't index everything.
>
> **How it actually works.** Databases don't use a flat sorted list, because the list lives on disk and disk reads happen in fixed-size blocks called *pages* (commonly 8 KB). They use a **B-tree**: a shallow, wide tree where each node fills one page and holds many keys. Searching means reading one page per level of the tree. Because the tree is wide, it's also shallow — even a billion rows is usually four levels deep. Four page reads instead of a million.
>
> **Worked example.** Ten million users, 8 KB pages, and each index entry (email plus row pointer) about 40 bytes.
>
> - Entries per page: 8192 / 40 ≈ 200
> - Level 1 (leaves): 10,000,000 / 200 = 50,000 pages
> - Level 2: 50,000 / 200 = 250 pages
> - Level 3: 250 / 200 = 2 pages
> - Level 4: 1 page — the root
>
> So the tree is four levels deep, and a lookup is four page reads. The full table scan would have read on the order of a hundred thousand pages. That's the factor of ten thousand you keep hearing about, and now you can derive it instead of quoting it.
>
> **The trap.** "Indexes make queries fast, so I should index every column." It's a reasonable inference — each index really does speed up reads on its column. But every index is a separate B-tree that must be updated on every insert, update, and delete. Ten indexes means one row insert triggers eleven writes. Tables with heavy write traffic and generous indexing can end up slower overall than the unindexed version, and the symptom shows up in write latency, not in the query you were trying to optimise — which is why it takes people so long to diagnose.
>
> **Why it's built this way.** An index trades write speed and disk space for read speed. That trade is worth it when reads outnumber writes, which is most application workloads — but not all. A high-volume event log that is written constantly and queried nightly may be better off with almost no indexes at all. The alternatives worth knowing: hash indexes give faster exact-match lookups but cannot serve range queries or sorting, because a hash destroys ordering; log-structured merge trees invert the tradeoff entirely, making writes cheap and reads more expensive, which is why write-heavy stores like Cassandra use them.
>
> *Failure mode at scale:* index maintenance is the hidden cost of bulk loads. Inserting ten million rows into a table with six indexes can take an order of magnitude longer than inserting into a bare table. The standard move is to drop the indexes, load, and rebuild — and the standard incident is the team that didn't, watched the load run for nine hours, and never understood why.
>
> **Check yourself.** Your table has one index on `email`. You add five more indexes on other columns. Lookups by email — the ones you actually cared about — get slower. Why?
>
> <details><summary>Answer</summary>
> The email index itself is unchanged, so the search through it costs exactly
> what it did before. What changed is everything around it: five more B-trees
> now compete for the same memory cache, so pages of the email index get
> evicted more often and have to be re-read from disk. The lookup didn't get
> algorithmically worse — it just stopped being served from memory.
> </details>

**Why this version works:** it opens with a problem the reader can feel, defines every term at the moment it's needed, derives the numbers instead of asserting them, names the misconception in the reader's own voice, and ends somewhere a practitioner couldn't have gotten to on their own. The checkpoint question can't be answered by scanning back up the page.
