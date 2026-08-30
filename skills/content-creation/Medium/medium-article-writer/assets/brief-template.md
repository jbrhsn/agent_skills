# Brief: <working title>

Keep this to one screen. It is a decision aid, not a document.

## Angle

One sentence. The specific claim or story this piece makes — not the topic.

Topic: "Iceberg compaction." Angle: "Our compaction job was the cost problem, not the query engine, and the fix was three config lines."

## Reader

Who this is for and what they already know. One or two lines. Be narrow — "data engineers running Iceberg at scale who've noticed their storage bill climbing" beats "developers."

## Promise

What the reader can do or decide after finishing. If this cannot be stated concretely, the piece isn't ready to write.

## Piece type

Tutorial / case study / opinion / explainer / experience report. Determines the structure from `article-structures.md`.

## Voice card

Six lines, from `references/voice-inference.md`. Copy the finished card here so the register is decided before drafting and checkable after.

- **Formality:**
- **Stance:**
- **Rhythm:**
- **Humor:**
- **Posture:**
- **Keep verbatim:**

## Outline

Section headers with one line each on what the section does and which piece of the user's material carries it.

1. **<header>** — <what it does> — <source material it uses>
2. ...

## Coverage ledger

Every load-bearing specific in `source.md` — numbers, versions, failures, decisions, opinions, and above all the user's own experience — mapped to the section that carries it. This is the table that keeps the piece non-derivative. If a row has no section, it belongs in "Proposed to omit" below, not nowhere.

| From `source.md` | Type | Section that carries it |
|---|---|---|
| <the specific, quoted or summarized> | number / version / failure / decision / opinion / experience | §<section> |

If this table is thin, the piece will read as generic no matter how well written.

## Proposed to omit

Anything from `source.md` that is **not** in the ledger above, with the reason. Nothing here is dropped until the user says so. An experience, opinion, or anecdote appearing in this list is a question for the user, not a decision already made — see the omission rule in `SKILL.md`.

| Item | Why it doesn't fit | Alternative |
|---|---|---|
| <the material> | <flow, scope, length, or it undercuts the angle> | <cut / move to a later piece / could fit §X if the angle widened> |

If this list is empty, say so explicitly. "Nothing proposed for omission" is a useful thing for the user to read.

## Unverified

Every claim that could not be confirmed, and every gap where the user's input is still needed. Nothing here gets written into the article until it is resolved.

- **<claim>** — <what was checked, what came back, what's needed>

## Close

The planned ending: the takeaway or decision rule the piece lands on, and the question that follows it. See `references/closing-and-cta.md`.

## Estimated length

Word count and rough read time.
