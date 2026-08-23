# linkedin-post

Turns a folder's `source.md` (raw notes) into a publication-ready LinkedIn post plus posting notes.

Built for the workflow: one folder per post → dump raw thinking into `source.md` → run the harness → get a post you can paste.

## Install

Drop the `linkedin-post/` folder into your skills directory:

```
~/.config/opencode/skills/linkedin-post/     # OpenCode
.opencode/skills/linkedin-post/              # or project-local
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
| `linkedin_post_notes.md` | Topic tag, character count, first-comment link, timing, gaps, tradeoff made. |

## What it actually does

1. Finds the single sharpest claim in `source.md` — a post carries one idea, not a summary of the notes
2. Infers the author's voice from the source rather than imposing a generic creator tone
3. Drafts several hooks, kills the predictable ones, keeps the one the body can pay off
4. Builds hook → re-hook → value → close, targeting 1,200–1,600 characters
5. Audits against distribution rules and strips AI tells
6. Writes both files and reports the character count and the tradeoff it made

## Design decisions

**Voice is inferred, not fixed.** There's no persona baked in. The skill reads register, technical density, sentence rhythm, and hedging out of `source.md` and preserves them. The transformation is structural — reorganize the material, leave the voice alone.

**One post, not variants.** It commits to an angle and names the tradeoff in the notes file so you can redirect it in one message. If `source.md` contains two genuinely separate ideas, it asks rather than merging them.

**Nothing gets fabricated.** Numbers, quotes, and anecdotes must trace to `source.md`. Missing evidence gets flagged in the notes file instead of invented — which matters, since a fabricated stat in a technical post is a credibility event.

**Anti-slop is a first-class pass.** The failure mode for LLM-drafted posts isn't bad structure, it's recognizable machine prose. `references/structure-and-format.md` carries an explicit ban list ("it's not just X, it's Y", "here's the thing", em-dash saturation, triadic rhythm) and positive moves that restore a human register.

## Layout

```
linkedin-post/
├── SKILL.md                          # Lean orchestrator: workflow + hard rules
├── README.md
├── references/
│   ├── algorithm-mechanics.md        # Why the rules exist + the 10-point audit
│   ├── hook-frameworks.md            # Hook types, fold limits, predictability test
│   ├── structure-and-format.md       # Anatomy, length, formatting, AI-tell removal
│   └── voice-inference.md            # Reading register out of source.md
└── assets/
    └── post_notes_template.md        # Template for linkedin_post_notes.md
```

`SKILL.md` stays under ~90 lines and loads references on demand, so the always-resident cost is small and the detail lives one level down.

## The rules it enforces

Derived from how LinkedIn's 2026 LLM-based ranking stack distributes content — the ranker optimizes for dwell time, saves, and substantive comments rather than likes.

- **No links in the body.** Body links cut reach ~50–70%. Every URL moves to the suggested first comment.
- **No engagement bait.** "Comment YES", "tag someone", reaction polling — actively suppressed. Includes the subtle version: a hook promising something the body never delivers.
- **1,200–1,600 characters,** never padded to reach it.
- **One bolded phrase at most,** and never on a keyword that matters for search.
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
