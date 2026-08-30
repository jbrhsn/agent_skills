# Surface interview

Runs at Stage 5, after the PRD is approved — never before. The questions are about how the PRD's already-confirmed requirements surface to the user, so writing the PRD first is what makes the questions answerable instead of speculative.

## Budget

- **10 questions maximum**, separate from the Stage 1 budget.
- **4–6 per turn.** Usually one turn, sometimes two.
- Skip a question if the answer is already implied by the PRD (e.g. the PRD already named specific pages, or said "single form, no navigation") — read `docs/prd.md` before drafting questions, same discipline as Stage 1.

## By surface type

### web / mobile / desktop

- Walk me through the primary flow screen by screen — what does the user see at each step? (This is the backbone of the Flows section.)
- How many distinct pages/screens does v1 need? Name them.
- For the 2–3 most important components (the ones the whole flow depends on), what should happen when: it's loading, it's empty, it errors, the action succeeds?
- Any navigation model preference — tabs, sidebar, single page, modal-heavy — or open?
- (web only) Does layout need to work on mobile browsers, or desktop-only for v1?
- (mobile only) iOS, Android, or both? Any platform convention that matters to you (e.g. must feel native, cross-platform look is fine)?

### conversational (CLI / chatbot)

- Walk me through a typical session start to finish — what does the user type or say, and what comes back, at each turn?
- What commands, intents, or inputs does v1 need to handle? List them.
- When the input is invalid or the system can't help, what should the response look like — an error message, a suggestion, a fallback to a human/default path?
- Is there a persistent state across turns (session memory, context), or is each turn independent?
- What does a successful end-of-session look like — how does the user know they're done?

### headless (only if the PRD leaves it unclear)

- For each external-facing interface named in the PRD's constraints or data model: what does a caller send, and what do they get back, in plain terms (not a schema)?
- What does a caller see when something goes wrong — an error code, a message, silent failure?
- Is this interface versioned, or is v1 the only version that will ever need to exist?

Ask only what Stage 0's surface type plus the PRD leave genuinely open. A headless project with a fully-specified data model in the PRD may need zero questions here — say so and move straight to Stage 6 rather than padding the interview.

## Turn format

Same discipline as the main interview: number continuously, one line per question, offer a default where a sensible one exists. Do not re-ask anything the PRD already answers — cite the PRD line back to the user instead if they seem to be repeating themselves.

## State file

If this stage spans more than one turn, append to `docs/.planner-state.md` under a `## UIUX interview` heading using the same answered/open format as Stage 1. Delete `docs/.planner-state.md` entirely once the UIUX doc is approved at Stage 7.

## Confirmation

Play back what you're about to write — screens/states or turns/responses, whichever applies — as a short numbered list before drafting `docs/uiux.md`. Same rule as the PRD: do not proceed on silence.
