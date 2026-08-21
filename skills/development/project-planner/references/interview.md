# Interview

## Budget

- **20 questions total**, hard ceiling.
- **4–6 per turn**, grouped by theme so the user answers in one pass.
- Typically 3–4 turns. If you are at 20 and still missing something, put it in the PRD's
  Open Questions rather than asking a 21st.

Spend the budget where the answer changes the plan. A question whose answer you could get
by reading `package.json`, `README.md`, or the directory tree is a wasted question — read
first, ask second.

## Turn format

Number questions continuously across turns (Q1…Q20) so the user can see the budget being
spent. Where a sensible default exists, offer it — `Q7: Auth — email/password, OAuth, or
none for v1? (default: none for v1)`. A user who says "default is fine" has still given
you an answer you can confirm; a user who says nothing has not.

Keep each question to one line. No preamble paragraphs between questions.

## Turn 1 — Shape (always ask)

Establish what the thing is before anything else.

- What is being built, in one or two sentences?
- Who uses it, and what is the single job they hire it for?
- What does "done" look like for v1 — the smallest version worth shipping?
- What is explicitly out of scope for v1?
- Is this greenfield, or extending an existing codebase?
- Any hard deadline or time budget?

## Turn 2 — Stack and constraints

In **standard mode**, ask what they have decided and what is open:

- Language, framework, runtime — decided or open?
- Data: what is stored, and in what (relational, document, files, none)?
- Deployment target — local only, VPS, container, serverless, app store?
- External services or APIs it must talk to?
- Anything they are required to use (team standard, existing infra)?
- Anything they refuse to use?

In **learn-by-building mode**, replace the first item with:

- Which language/framework do you want to learn through this project?
- What is your current level with it — never touched it, read the docs, built a toy?
- What do you already know well that transfers (another language, general web, DBs)?
- Do you want depth (understand why) or velocity (enough to ship, revisit later)?
- Roughly how much time per week for learning + building?
- Is production-readiness a goal, or is this a learning artifact?

The level answer drives the granularity of `learnings/topics.md`. Ask it plainly and do
not soften it — a beginner told "you probably know X" gets a curriculum with holes in it.

## Turn 3 — Behaviour and edges

- Walk me through the main flow, start to finish.
- What are the states or entities in the system, and how do they relate?
- What must never happen (the failure you would actually care about)?
- Who can see or do what — any roles or permissions?
- Expected scale: rough number of users, records, requests?
- How will you know it works — manual check, tests, both?

## Turn 4 — Gaps only

Do not ask a fixed set here. Ask only about contradictions in earlier answers, or areas
where you cannot write a testable requirement. Two to four questions. If there are none,
skip this turn entirely and go to confirmation.

## State file

After every batch, write `docs/.planner-state.md`. It survives PRD approval because the
surface interview (Stage 5) appends to it — delete it only after the UIUX doc is approved
at Stage 7.

```markdown
# Planner state (delete after PRD approval)
Mode: standard | learn-by-building
Questions used: 11 / 20

## Answered
- Q1 What: ...
- Q2 Users: ...

## Open
- Deployment target — not yet asked
```

## Confirmation (Stage 2)

Play back as a numbered list, in the user's vocabulary, not yours:

```
Functional
  FR-01  A user can upload a CSV and see a preview before import.
  FR-02  ...
Non-functional
  NFR-01 Import of a 10k-row file completes in under 5 seconds.
Out of scope for v1
  - Multi-user accounts
  - Scheduled imports
Open questions
  - Max file size — you said "reasonable", need a number
```

Ask: "Correct anything that is wrong or missing. I will write the PRD from exactly this
list." Wait for a reply. A requirement that is vague at this stage produces a unit that
cannot be tested at Stage 5 — push for a number, a threshold, or an observable outcome
now rather than discovering it later.
