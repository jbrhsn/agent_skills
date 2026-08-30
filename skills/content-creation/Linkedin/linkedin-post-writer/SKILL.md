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

**1. Read and mine `source.md`.** Identify the single most interesting claim in it — the one thing a peer would argue with, not the summary of everything present. A post carries one idea. Everything else in `source.md` is either supporting evidence or gets cut. If two genuinely separate ideas exist, say so and ask which one to build, rather than merging them into a mushy post.

While reading, inventory separately everything that is **already the author's**: a personal experience, an opinion, a judgment call, a number they measured, a decision they regret. That material cannot be regenerated from general knowledge, and the gate in step 4 depends on the list being complete.

**2. Infer voice.** Read `references/voice-inference.md`, extract the author's register from `source.md` itself, and write the five-line voice card it describes before drafting anything. Never impose a generic LinkedIn-influencer voice — the whole point is that the post sounds like the person who wrote the notes.

**3. Build the hook.** Read `references/hook-frameworks.md`. Draft five candidate hooks, apply the predictability test, and keep the two or three that survive. The hook must work inside the mobile fold (~140 characters) and must not be predictable from its own first line. Do not pick a single winner yet — the survivors go to the author in step 4.

**4. Show the angle. Stop.** Before drafting, show four things and nothing else:

- **The claim** the post will make, in one sentence.
- **The surviving hooks** from step 3, numbered, so the author can pick or redirect.
- **What carries it** — the evidence, number, or moment from `source.md` doing the actual work.
- **What gets left out** — everything from the step 1 inventory this angle has no room for, one line each.

Keep it under a screen. A rejected angle costs thirty seconds; a rejected post costs the whole draft. The last bullet is the reason the gate exists: compressing `source.md` into 1,400 characters is severe, and what does not survive that compression is the author's call, not yours.

If the author says to skip ahead, skip the gate — but still say in one line what you are leaving out, because that decision is theirs whether or not the gate gets shown.

**5. Draft the body.** Read `references/structure-and-format.md`. Build hook → re-hook → value → close. Land inside the 1,200–1,600 character band. Cut anything that reads as filler; dwell time comes from substance, not length.

**6. Audit before writing files.** Read `references/algorithm-mechanics.md` and check the draft against the hard rules below. The audit is where most drafts actually improve — treat it as a rewrite pass, not a checkbox.

**7. Write both files.** Write `linkedin_post.md` (clean post body only) and `linkedin_post_notes.md` (from the template in `assets/`). Report the final character count, and make sure the notes file's "Cut, and why" section matches what was actually agreed at the gate.

## Hard rules

These come from how the 2026 LinkedIn ranking system actually distributes content. `references/algorithm-mechanics.md` explains the reasoning; the rules themselves are short enough to keep here.

- **No external links in the post body.** Links in the body cut reach by roughly 50–70%. Move every URL to the suggested first comment in the notes file.
- **No engagement bait.** "Comment YES if you agree", "Repost if this resonates", "Tag someone who needs this", reaction polling — all actively suppressed. A real question is the alternative, and ending on a strong takeaway with no question is equally valid. See "The close" in `references/structure-and-format.md`.
- **1,200–1,600 characters** unless the idea genuinely needs less. Never pad to reach the band.
- **Default to zero bold.** LinkedIn has no real bold — the only mechanism is pasted Unicode mathematical characters, which screen readers read as gibberish and search indexing skips. One phrase is the ceiling, only when the author has asked for emphasis, and never on a term that matters for discoverability.
- **Two emojis maximum**, used as visual separators, never as decoration or bullet substitutes on every line.
- **No hashtag stuffing.** Zero to three specific tags. Natural keyword use in the prose does more than tags now.
- **Never invent facts, numbers, quotes, or anecdotes** that are not in `source.md`. If the post needs a statistic to land and none exists, flag the gap in the notes file rather than fabricating one.

## Never drop the author's own material silently

The mirror of "never invent facts", and the rule more likely to be broken. A personal experience, opinion, or judgment in `source.md` is the reason the post is worth reading rather than something anyone could have generated. A post is 1,400 characters, so most of `source.md` genuinely will not fit — that is not the problem. Deciding what does not fit without saying so is.

- **Before drafting**, everything being left out is named at the gate in step 4, and the author decides.
- **During drafting**, if something the author lived through turns out not to fit the angle, stop and ask. Do not cut it and mention it afterward, and do not compress it into a clause until it carries nothing.
- **The default is to find it a home.** An experience that will not fit the body often works as the opening — the mid-scene story open and the named-cost admission in `references/hook-frameworks.md` exist for exactly this. Try that before proposing to cut it.
- **When you do raise it**, say what breaks: which zone it would land in, and what it would push out.

## Reference map

Load these as needed rather than all at once:

| File | Read it when |
| --- | --- |
| `references/voice-inference.md` | Step 2 — determining register and writing the voice card |
| `references/hook-frameworks.md` | Step 3 — writing and stress-testing the opening |
| `references/structure-and-format.md` | Step 5 — building the body, formatting, and killing AI tells |
| `references/algorithm-mechanics.md` | Step 6 — auditing distribution risk and filling the notes file |
| `assets/post_notes_template.md` | Step 7 — writing `linkedin_post_notes.md` |
