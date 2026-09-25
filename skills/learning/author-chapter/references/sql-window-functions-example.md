# From a SQL note to a practical chapter

Use this calibration example for technical modules with runnable examples and subtle boundary cases. Choose it instead of the shorter [ratios example](chapter-example.md) when those features matter. The data is invented; no learner performance or production benchmark is claimed. The chapter's length and headings are not a template.

Verification: the setup and all ten subsequent SQL queries were executed in SQLite 3.51.0 and compared with complete expected results, including ties, frame boundaries, missing previous rows, and the practice answer. The filtered-total example was also checked. Other database engines were not tested.

## Input stub

```markdown
# SQL window functions

Teach window functions so I can keep individual activity records while calculating totals, rankings, changes, and moving averages. Include practice. Assume basic SELECT, WHERE, and arithmetic; explain grouping and any other SQL needed. Use SQLite for runnable examples.
```

## Author's coverage choices

The learning goal requires the difference between grouping and preserving rows, followed by partitions, ordering, and frames. Tied scores and repeated dates expose mistakes that unique values would hide. Common table expressions support filtering calculated results. Explicit frames, NULL boundaries, and row-based versus calendar-based averages are necessary for correct application. Distribution functions such as `NTILE`, advanced frame exclusions, and production query tuning are optional extensions beyond this first module.

## Finished chapter

---

# SQL window functions: keep each row and see the bigger picture

Imagine you are tracking a reading challenge. Each row records one person's reading session. You want to show the session's page count alongside that person's total, compare it with their previous session, and find their strongest sessions. A plain total answers only part of the question: you still need the individual records.

A **window function** adds a calculation using related rows while keeping the current row visible. Think of a spreadsheet where each session keeps its own line, with extra columns showing its place in the wider story. This analogy describes the result; it does not mean the database stores rows in spreadsheet order or runs the calculation cell by cell.

We will build those extra columns using a small dataset. You should already recognize `SELECT` as choosing output columns and `WHERE` as filtering rows. The remaining SQL is introduced as we need it.

## Seven sessions you can inspect by hand

Use an empty scratch database in a SQLite environment that supports window functions. Run this setup once, then run each later query against the same database. The chapter uses SQLite syntax; check your own database's documentation before assuming every detail transfers unchanged.

```sql
CREATE TABLE reading_sessions (
    session_id INTEGER PRIMARY KEY,
    reader TEXT NOT NULL,
    read_on TEXT NOT NULL,
    pages INTEGER NOT NULL CHECK (pages > 0)
);

INSERT INTO reading_sessions (session_id, reader, read_on, pages) VALUES
    (1, 'Ava', '2026-01-01', 10),
    (2, 'Ava', '2026-01-02', 20),
    (3, 'Ava', '2026-01-02', 20),
    (4, 'Ava', '2026-01-04',  5),
    (5, 'Ben', '2026-01-01',  8),
    (6, 'Ben', '2026-01-03', 12),
    (7, 'Ben', '2026-01-04',  7);
```

`PRIMARY KEY` gives each session a unique identifier. `NOT NULL` requires a value; the `CHECK` requires a positive page count. Dates are consistently formatted text in year-month-day order, so sorting these strings sorts these dates. Within the same date, we will use `session_id` to define a stable order. It is a chosen tie-breaker, not evidence of an exact time of day.

| session_id | reader | read_on | pages |
|---|---|---|---:|
| 1 | Ava | 2026-01-01 | 10 |
| 2 | Ava | 2026-01-02 | 20 |
| 3 | Ava | 2026-01-02 | 20 |
| 4 | Ava | 2026-01-04 | 5 |
| 5 | Ben | 2026-01-01 | 8 |
| 6 | Ben | 2026-01-03 | 12 |
| 7 | Ben | 2026-01-04 | 7 |

Ava has two sessions on the same date with the same page count. Keep an eye on them: ties are where several window queries become surprising.

## A total without losing the sessions

First, a grouped query produces one summary row per reader. `SUM` adds values, and `GROUP BY` identifies which rows belong to each summary. `AS` names an output column.

```sql
SELECT reader, SUM(pages) AS total_pages
FROM reading_sessions
GROUP BY reader
ORDER BY reader;
```

The result is just two rows: Ava with 55 pages and Ben with 27. That is useful for a scoreboard, but the session dates and individual page counts are no longer represented as separate rows.

Add `OVER` to use `SUM` as a window calculation instead:

```sql
SELECT session_id, reader, pages,
       SUM(pages) OVER (PARTITION BY reader) AS reader_total,
       SUM(pages) OVER () AS everyone_total
FROM reading_sessions
ORDER BY reader, session_id;
```

| session_id | reader | pages | reader_total | everyone_total |
|---|---|---:|---:|---:|
| 1 | Ava | 10 | 55 | 82 |
| 2 | Ava | 20 | 55 | 82 |
| 3 | Ava | 20 | 55 | 82 |
| 4 | Ava | 5 | 55 | 82 |
| 5 | Ben | 8 | 27 | 82 |
| 6 | Ben | 12 | 27 | 82 |
| 7 | Ben | 7 | 27 | 82 |

`PARTITION BY reader` creates a separate calculation group for each reader. Ava's rows use Ava's total; Ben's use Ben's. Empty `OVER ()` uses all seven rows together. Adding these calculations preserves the seven session rows. [SQLite's window-function introduction](https://www.sqlite.org/windowfunctions.html#introduction_to_window_functions) describes this distinction.

The repeated 55 is context attached to each Ava session, not four separate totals to add again. Decide what one output row should represent before writing a query: a reader summary suggests grouping; a session with extra context suggests a window.

## How far had each reader got at this point?

The whole-reader total is constant, but a running total grows as sessions accumulate. To calculate one, SQL needs an order and a rule for which rows to include at each position.

```sql
SELECT session_id, reader, read_on, pages,
       SUM(pages) OVER (
           PARTITION BY reader
           ORDER BY read_on, session_id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_pages
FROM reading_sessions
ORDER BY reader, read_on, session_id;
```

Read the expression from the inside outward: stay within one reader, arrange their sessions by date and ID, take all rows from the beginning through this row, then add their pages. That moving selection is the **frame**.

For Ava, the results are 10, 30, 50, and 55. At session 3, the frame contains sessions 1, 2, and 3, so the sum is 10 + 20 + 20 = 50. Ben starts a new partition, producing 8, 20, and 27.

The `ORDER BY` inside `OVER` determines calculation order. The final `ORDER BY` determines display order. They have separate jobs; keeping both explicit makes the example readable and repeatable. [SQLite's ordering example](https://www.sqlite.org/windowfunctions.html#introduction_to_window_functions) demonstrates this separation.

What if you ordered only by date and left out the frame?

```sql
SELECT session_id, read_on, pages,
       SUM(pages) OVER (ORDER BY read_on) AS default_running_pages
FROM reading_sessions
WHERE reader = 'Ava'
ORDER BY read_on, session_id;
```

Now the results are **10, 50, 50, 55**. Both January 2 sessions receive 50. In SQLite, the default ordered aggregate frame includes rows tied with the current row on the window's ordering expressions. Those tied rows are called **peers**. [SQLite's frame documentation](https://www.sqlite.org/windowfunctions.html#frame_specifications) specifies this behavior.

That may be useful when you want a total through the current date. For a session-by-session total, the earlier explicit `ROWS` frame and unique tie-breaker express the intended result. Adding only an outer display order would not fix the calculation.

## Who gets first place when two sessions tie?

A ranking question needs a different order: most pages first. `DESC` means descending, so larger counts come earlier.

```sql
SELECT session_id, reader, pages,
       ROW_NUMBER() OVER (
           PARTITION BY reader ORDER BY pages DESC, session_id
       ) AS position,
       RANK() OVER (
           PARTITION BY reader ORDER BY pages DESC
       ) AS shared_rank,
       DENSE_RANK() OVER (
           PARTITION BY reader ORDER BY pages DESC
       ) AS distinct_rank
FROM reading_sessions
ORDER BY reader, pages DESC, session_id;
```

Ava's rows illustrate the difference:

| session_id | pages | position | shared_rank | distinct_rank |
|---|---:|---:|---:|---:|
| 2 | 20 | 1 | 1 | 1 |
| 3 | 20 | 2 | 1 | 1 |
| 1 | 10 | 3 | 3 | 2 |
| 4 | 5 | 4 | 4 | 3 |

`ROW_NUMBER` gives each row a separate position. `RANK` shares a place for ties and leaves gaps afterward. `DENSE_RANK` shares a place but counts the next distinct score without a gap. These are different answers to different questions, not interchangeable spellings. [SQLite's built-in functions](https://www.sqlite.org/windowfunctions.html#built_in_window_functions) define their tie behavior.

Notice that only `ROW_NUMBER` includes `session_id` in its window order. It needs a predictable way to choose between equal scores. Adding that unique ID to `RANK` or `DENSE_RANK` would make the ordering combinations distinct and destroy the score ties we meant to preserve.

“Two sessions per reader” calls for row numbers up to two. “Every session in the two highest distinct page counts” calls for dense ranks up to two and can return more than two rows. Clarify what “top two” means before choosing a function.

## Comparing a session with the one before it

A ranking compares positions; a change calculation needs a value from another row. `LAG(pages)` retrieves the previous row's page count in the specified order. `LEAD(pages)` looks forward instead.

```sql
SELECT session_id, reader, pages,
       LAG(pages) OVER (
           PARTITION BY reader ORDER BY read_on, session_id
       ) AS previous_pages,
       pages - LAG(pages) OVER (
           PARTITION BY reader ORDER BY read_on, session_id
       ) AS page_change
FROM reading_sessions
ORDER BY reader, read_on, session_id;
```

For Ava, `previous_pages` is NULL, 10, 20, 20, and `page_change` is NULL, 10, 0, -15. A negative result means this session had fewer pages than the previous one. The first comparison is `NULL`, SQL's marker for a missing or unknown value, because no earlier session exists. Subtracting a missing value does not establish a numeric difference.

Here “previous” means the previous recorded session, not yesterday. January 4 follows the second January 2 session even though January 3 is absent. Also, `LAG(pages, 1, 0)` would supply zero when no preceding row exists, changing the meaning to a zero baseline. It would not replace a NULL stored in an existing preceding row. [SQLite's `LAG` and `LEAD` reference](https://www.sqlite.org/windowfunctions.html#built_in_window_functions) explains these boundaries.

## A moving average needs a smaller frame

Individual sessions can vary. To average the current session and up to two previous sessions, change the function and frame:

```sql
SELECT session_id, reader, pages,
       AVG(pages) OVER (
           PARTITION BY reader
           ORDER BY read_on, session_id
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS recent_average
FROM reading_sessions
ORDER BY reader, read_on, session_id;
```

`AVG` adds the included values and divides by their count. Ava's first average is 10 because only one session is available. Her second is (10 + 20) / 2 = 15. Her third is (10 + 20 + 20) / 3, approximately 16.67. At session 4, the oldest session drops out: (20 + 20 + 5) / 3 = 15.

This is a **three-session** moving average, not a three-day average. Two sessions can share a date, and some dates have none. A calendar-based report needs a decision about whether missing days count as zero or remain absent; it may need daily grouping and a calendar table before the window calculation. Do not label a row-based calculation as time-based just because it is ordered by a date.

Frames matter for functions such as `SUM`, `AVG`, and `LAST_VALUE`; SQLite's ranking functions and `LAG`/`LEAD` do not use the frame to restrict their calculation. [SQLite's function reference](https://www.sqlite.org/windowfunctions.html#built_in_window_functions) distinguishes these cases.

For example, asking for the last session's pages requires reaching the end of the partition:

```sql
SELECT session_id, reader, pages,
       LAST_VALUE(pages) OVER (
           PARTITION BY reader
           ORDER BY read_on, session_id
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS final_session_pages
FROM reading_sessions
ORDER BY reader, read_on, session_id;
```

Every Ava row receives 5; every Ben row receives 7. Without the explicit full-partition frame, the default frame with this unique ordering ends at the current row, and `LAST_VALUE` would return that row's page count. Its name means last value in the frame, not automatically last value in all the reader's sessions.

## Keeping only the rows you calculated

We can now identify each reader's strongest session, but how do we keep only that row? SQLite does not allow window functions directly in `WHERE`. Calculate the result in an inner query, then filter it outside. [SQLite's window-function placement rules](https://www.sqlite.org/windowfunctions.html#introduction_to_window_functions) establish this restriction.

```sql
WITH ranked AS (
    SELECT session_id, reader, pages,
           ROW_NUMBER() OVER (
               PARTITION BY reader ORDER BY pages DESC, session_id
           ) AS position
    FROM reading_sessions
)
SELECT session_id, reader, pages
FROM ranked
WHERE position = 1
ORDER BY reader;
```

`WITH ranked AS (...)` defines a **common table expression**, or CTE: a named query result available to the following query. You can think of `ranked` as a temporary result for this statement, without assuming the database physically creates a separate stored table.

The result is Ava's session 2 with 20 pages and Ben's session 6 with 12. Session 3 ties with session 2, but the ID tie-breaker deliberately selects just one. Use `RANK` ordered only by pages and filter rank 1 if the task should keep every tied winner.

Filter placement also affects totals. A `WHERE pages >= 10` inside a query restricts the sessions available to its window calculations. Ava's total would become 50 and Ben's 12. To display those same qualifying sessions alongside totals over their entire history, calculate the totals inside a CTE without that filter, then apply it in the outer query. The order of written clauses is not the order in which their results become available; SQLite's [SELECT processing description](https://www.sqlite.org/lang_select.html) explains the input filtering stage.

## Build a report that answers a new question

Using the existing table, produce each reader's **two most recent sessions**. Include their ID, date, page count, and the percentage of that reader's **entire recorded page total** contributed by each selected session. For sessions on the same date, treat the larger ID as more recent for this exercise.

This combines two different views of the data: recency chooses the rows, but the percentage must still use the full history. Try writing the query before reading the answer. Check that each reader has two rows, that the dates are the latest available, and that the percentages use 55 for Ava and 27 for Ben as denominators.

A hint if needed: compute the total and a recency row number inside the same CTE, then filter outside it. A percentage is a part divided by the whole, multiplied by 100. Use `100.0` in the expression to keep fractional results with these integer inputs.

### A solution and how to check it

```sql
WITH annotated AS (
    SELECT session_id, reader, read_on, pages,
           SUM(pages) OVER (PARTITION BY reader) AS reader_total,
           ROW_NUMBER() OVER (
               PARTITION BY reader ORDER BY read_on DESC, session_id DESC
           ) AS recency
    FROM reading_sessions
)
SELECT session_id, reader, read_on, pages,
       ROUND(100.0 * pages / reader_total, 2) AS percent_of_history
FROM annotated
WHERE recency <= 2
ORDER BY reader, read_on DESC, session_id DESC;
```

`ROUND(..., 2)` rounds the displayed percentage to two decimal places. This data's positive page counts ensure the denominator is nonzero. In data allowing a zero total, decide what a percentage should mean before dividing; an undefined percentage should not silently become zero.

| session_id | reader | read_on | pages | percent_of_history |
|---|---|---|---:|---:|
| 4 | Ava | 2026-01-04 | 5 | 9.09 |
| 3 | Ava | 2026-01-02 | 20 | 36.36 |
| 7 | Ben | 2026-01-04 | 7 | 25.93 |
| 6 | Ben | 2026-01-03 | 12 | 44.44 |

For session 4, 100 × 5 / 55 is approximately 9.09. If you got 20%, you probably calculated the total after keeping only Ava's last two sessions, whose pages add to 25. If you returned both January 2 rows as well as January 4, you likely ranked dates with ties instead of selecting exactly two sessions. If fractions vanished, inspect whether your expression used integer arithmetic.

These percentages do not need to add to 100 for each reader: we are displaying only part of their history. That observation is a useful check on whether the query answers the intended question.

When writing your own window query, first decide what one row represents. Then choose which rows belong together, what order the calculation needs, and whether a frame should cover all rows, earlier rows, or nearby rows. Finally, place filters where they preserve the history your calculation is meant to see. Those decisions explain the result more reliably than memorizing function names.

---

## Why these choices serve the goal

- One small dataset connects totals, chronology, ranking, and comparisons. Repeated dates and scores expose peer groups and tie-breaking with concrete results.
- The chapter teaches grouping, frames, CTEs, and NULL only where the reader needs them. Each SQL block is complete given the shared setup.
- Predictions and arithmetic make the results inspectable without trusting the query blindly. The practical changes the ordering goal and combines it with a full-history denominator.
- The spreadsheet analogy explains preserved detail without claiming a physical execution model. Dialect boundaries and source links qualify behavior that should not be generalized carelessly.
- The chapter intentionally leaves advanced distribution functions, frame exclusions, and performance tuning for further study rather than claiming to cover every window feature.
