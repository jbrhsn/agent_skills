# linkedin-post-writer

Turns a folder's `source.md` (raw notes) into a publication-ready LinkedIn post plus posting notes.

Built for the workflow: one folder per post → dump raw thinking into `source.md` → run the harness → get a post you can paste.

## Install

Drop the `linkedin-post-writer/` folder into your skills directory:

```
~/.config/opencode/skills/linkedin-post-writer/     # OpenCode
.opencode/skills/linkedin-post-writer/              # or project-local
```

For Claude Code, use `~/.claude/skills/` instead. The skill is plain markdown with no dependencies, so it works in any harness that reads `SKILL.md` frontmatter.

## Use

```
opencode "turn source.md in ./posts/eval-driven-dev into a LinkedIn post"
```

It also triggers on phrasings that never say "LinkedIn" — "polish this up for posting", "make source.md publishable", "write this folder up as a post".

## Inputs and outputs

**In:** `source.md` — unstructured. Bullets, half-thoughts, pasted logs, links, numbers. No format required.

**Out:** written next to `source.md`:

| File | Contents |
|---|---|
| `linkedin_post.md` | Post body only. No frontmatter, no headings, no commentary. Paste-ready. |
| `linkedin_post_notes.md` | Topic tag, character count, first-comment link, timing, gaps, angle chosen, and the full cut list. |

## What it actually does

1. Finds the single sharpest claim in `source.md` — a post carries one idea, not a summary of the notes
2. Infers the author's voice from the source rather than imposing a generic creator tone, and writes a voice card
3. Drafts five hooks, kills the predictable ones, keeps the two or three the body could pay off
4. **Stops** and shows you the claim, the surviving hooks, and what it proposes to leave out
5. Builds hook → re-hook → value → close, targeting 1,200–1,600 characters
6. Audits against distribution rules and strips AI tells
7. Writes both files and reports the character count and the full cut list

## Design decisions

**Voice is inferred, not fixed.** There's no persona baked in. The skill reads register, technical density, sentence rhythm, and hedging out of `source.md` and preserves them. The transformation is structural — reorganize the material, leave the voice alone.

**One post, not variants.** It commits to an angle and names the passed-over alternative in the notes file so you can redirect it in one message. If `source.md` contains two genuinely separate ideas, it asks rather than merging them.

**Nothing you lived through gets cut silently.** Turning notes into 1,400 characters is mostly subtraction, and the skill is explicitly told to cut. So the cutting happens in front of you: the step 4 gate lists what this angle has no room for *before* drafting, anything discovered mid-draft gets raised rather than quietly compressed away, and the notes file carries the full cut list afterward. An experience that will not fit the body is usually a hook, and it tries that first.

**Nothing gets fabricated.** Numbers, quotes, and anecdotes must trace to `source.md`. Missing evidence gets flagged in the notes file instead of invented — which matters, since a fabricated stat in a technical post is a credibility event.

**Anti-slop is a first-class pass.** The failure mode for LLM-drafted posts isn't bad structure, it's recognizable machine prose. `references/structure-and-format.md` carries an explicit ban list ("it's not just X, it's Y", "here's the thing", em-dash saturation, triadic rhythm) and positive moves that restore a human register.

## Layout

```
linkedin-post-writer/
├── SKILL.md                          # Lean orchestrator: workflow + hard rules
├── README.md
├── references/
│   ├── algorithm-mechanics.md        # Why the rules exist + the 11-point audit
│   ├── hook-frameworks.md            # Hook types, fold limits, predictability test
│   ├── structure-and-format.md       # Anatomy, length, formatting, AI-tell removal
│   └── voice-inference.md            # Reading register out of source.md
└── assets/
    └── post_notes_template.md        # Template for linkedin_post_notes.md
```

`SKILL.md` stays around 100 lines and loads references on demand, so the always-resident cost is small and the detail lives one level down.

## The rules it enforces

Derived from how LinkedIn's 2026 LLM-based ranking stack distributes content — the ranker optimizes for dwell time, saves, and substantive comments rather than likes.

- **No links in the body.** Body links cut reach ~50–70%. Every URL moves to the suggested first comment.
- **No engagement bait.** "Comment YES", "tag someone", reaction polling — actively suppressed. Includes the subtle version: a hook promising something the body never delivers.
- **1,200–1,600 characters,** never padded to reach it.
- **Default to zero bold.** The only mechanism is pasted Unicode, which screen readers read as gibberish and search skips. One phrase is the ceiling, on request, never on a keyword that matters for discovery.
- **Two emojis maximum.** Zero if the source shows an author who doesn't use them.
- **Zero to three hashtags.** Hashtag weight is close to noise now; natural domain vocabulary in the prose does more.

## Tuning it

The rules are values, not code — edit the markdown directly.

- Different length band or emoji tolerance → `SKILL.md`, "Hard rules"
- New hook type, or one that keeps producing weak openings → `references/hook-frameworks.md`
- Phrases the drafts keep reaching for that you hate → the ban list in `references/structure-and-format.md`
- Different notes fields → `assets/post_notes_template.md`

If a locked-in voice is ever wanted instead of inference, add `references/voice-profile.md` with samples and point step 2 of the workflow at it.

## Not included

No `scripts/`. The task is text transformation end to end, so a script directory would be dead weight. A validator (character-count check, URL detection, bait-phrase grep) is the one addition that would justify one — worth adding if the audit step ever gets skipped in practice.

The 1,200–1,600 band, timing windows, and format benchmarks are published aggregates, not laws. Your own analytics beat them; adjust the numbers when they disagree.
