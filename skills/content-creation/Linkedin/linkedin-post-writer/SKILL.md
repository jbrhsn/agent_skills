---
name: linkedin-post-writer
description: Turns a folder containing a source.md of raw notes into a publication-ready LinkedIn post plus a posting-notes file. Use this skill whenever the user mentions source.md, a LinkedIn post, LinkedIn content, or asks to polish, write up, or publish raw thoughts as a post — even when they never say the words "LinkedIn post" explicitly. Also use it when the user points at a folder and says something like "make this publishable", "turn this into a post", or "clean this up for posting".
---
# LinkedIn Post

Convert raw thinking in `source.md` into a post that survives the feed: strong hook, real substance, author's own voice, no AI tells.

## Inputs and outputs

**Input:** `source.md` in a working folder — raw notes, half-formed thoughts, bullet dumps, links, data, anecdotes. Assume it is unstructured and that the user has not decided the angle yet.

**Outputs, written to the same folder as `source.md`:**

- `linkedin_post.md` — the post body only, ready to copy-paste into the LinkedIn composer. No title, no frontmatter, no commentary, no markdown headings.
- `linkedin_post_notes.md` — posting metadata, built from `assets/post_notes_template.md`.

If `source.md` is missing, ask for the folder path rather than guessing. If the folder already contains a `linkedin_post.md`, ask whether to overwrite or write a `-v2` variant.

## Workflow

**1. Read and mine `source.md`.**
Identify the single most interesting claim in it — the one thing a peer would argue with, not the summary of everything present. A post carries one idea. Everything else in `source.md` is either supporting evidence or gets cut. If two genuinely separate ideas exist, say so and ask which one to build, rather than merging them into a mushy post.

**2. Infer voice.**
Read `references/voice-inference.md` and extract the author's register from `source.md` itself. Never impose a generic LinkedIn-influencer voice — the whole point is that the post sounds like the person who wrote the notes.

**3. Build the hook.**
Read `references/hook-frameworks.md`. Write several candidate hooks internally, apply the predictability test, and keep the strongest one. The hook must work inside the mobile fold (~140 characters) and must not be predictable from its own first line.

**4. Draft the body.**
Read `references/structure-and-format.md`. Build hook → re-hook → value → close. Land inside the 1,200–1,600 character band. Cut anything that reads as filler; dwell time comes from substance, not length.

**5. Audit before writing files.**
Read `references/algorithm-mechanics.md` and check the draft against the hard rules below. The audit is where most drafts actually improve — treat it as a rewrite pass, not a checkbox.

**6. Write both files.**
Write `linkedin_post.md` (clean post body only) and `linkedin_post_notes.md` (from the template in `assets/`). Report the final character count to the user and name the one tradeoff made while drafting, so they can push back.

## Hard rules

These come from how the 2026 LinkedIn ranking system actually distributes content. `references/algorithm-mechanics.md` explains the reasoning; the rules themselves are short enough to keep here.

- **No external links in the post body.** Links in the body cut reach by roughly 50–70%. Move every URL to the suggested first comment in the notes file.
- **No engagement bait.** "Comment YES if you agree", "Repost if this resonates", "Tag someone who needs this", reaction polling — all actively suppressed. Ask a real question instead.
- **1,200–1,600 characters** unless the idea genuinely needs less. Never pad to reach the band.
- **One bolded phrase at most**, and never on a term that matters for search — Unicode styling breaks screen readers and keyword parsing.
- **Two emojis maximum**, used as visual separators, never as decoration or bullet substitutes on every line.
- **No hashtag stuffing.** Zero to three specific tags. Natural keyword use in the prose does more than tags now.
- **Never invent facts, numbers, quotes, or anecdotes** that are not in `source.md`. If the post needs a statistic to land and none exists, flag the gap in the notes file rather than fabricating one.

## Reference map

Load these as needed rather than all at once:

| File                                   | Read it when                                                    |
| -------------------------------------- | --------------------------------------------------------------- |
| `references/voice-inference.md`      | Step 2 — determining tone and register                         |
| `references/hook-frameworks.md`      | Step 3 — writing and stress-testing the opening                |
| `references/structure-and-format.md` | Step 4 — building the body, formatting, and killing AI tells   |
| `references/algorithm-mechanics.md`  | Step 5 — auditing distribution risk and filling the notes file |
| `assets/post_notes_template.md`      | Step 6 — writing`linkedin_post_notes.md`                     |
