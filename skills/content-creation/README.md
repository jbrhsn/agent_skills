# Content Creation Skills

Five skills that take a topic from "what should I write about" to a posting-ready piece with matching visuals, for LinkedIn and Medium.

```
Common/      idea-research/          -> what to write        → ranked ideas + a source.md per idea
             keyword-research/       -> how it gets found    → kresearch.md
Linkedin/    linkedin-post-writer/   -> source.md            → linkedin_post.md
Medium/      medium-article-writer/  -> source.md            → medium_article.md
             medium-image-prompts/   -> finished article     → medium_image_prompts.md
```

## The `source.md` convention

Every skill here operates on **one folder per piece**, with raw notes in `source.md` at its root. That is the handoff format between them — `idea-research` scaffolds it, the writers consume it, and everything else lands beside it:

```
my-piece/
├── source.md                  # raw notes, dictation, rough draft
├── kresearch.md               # keyword-research
├── linkedin_post.md           # linkedin-post-writer
├── linkedin_post_notes.md     # linkedin-post-writer
├── medium_brief.md            # medium-article-writer (the approval gate)
├── medium_article.md          # medium-article-writer
├── medium_publish.md          # medium-article-writer
└── medium_image_prompts.md    # medium-image-prompts
```

Because of this, each skill also fires simply from you being *inside* such a folder and saying what you want next — you rarely have to name the skill.

## The skills

| Skill | Fires when | Produces |
|---|---|---|
| [**idea-research**](./Common/idea-research/README.md) | "what should I write about", "give me post ideas", "what's trending", "refill my pipeline" | Ranked, evidence-backed ideas from free public sources (Hacker News, Reddit, Google Trends, Medium tags), clustered by beat and scored on recency + velocity + fit + gap, plus a scaffolded `source.md` per approved idea |
| [**keyword-research**](./Common/keyword-research/README.md) | "SEO keywords", "what should I title this", "how do I make this rank", or a `source.md` exists and you ask what's next | `kresearch.md`: search intent, long-tail keywords, Medium tags, LinkedIn hashtags, optimization tips. No API key, no login |
| [**linkedin-post-writer**](./Linkedin/linkedin-post-writer/README.md) | "turn this into a post", "make this publishable", or you mention LinkedIn | `linkedin_post.md` + `linkedin_post_notes.md` — hook engineering, scroll-first structure, no-link-in-body discipline, behind an angle gate you approve before it drafts |
| [**medium-article-writer**](./Medium/medium-article-writer/README.md) | "write this up as an article", "restructure/retitle/tag this draft", or you mention Medium | `medium_article.md` plus title options, subtitle, tags, cover and alt-text notes — grounded in Medium's distribution guidelines, AI-content policy, and earnings mechanics, behind a `medium_brief.md` you approve before it drafts |
| [**medium-image-prompts**](./Medium/medium-image-prompts/README.md) | "cover art", "article visuals", "this is done, it needs images" | `medium_image_prompts.md`: one hero prompt plus three to five in-article prompts, each with placement, aspect ratio, negative prompt, alt text, and a caption carrying credit and the mandatory AI-disclosure line. **Prompt text only — nothing is rendered** |

## Review gates are not optional

Both writers stop before drafting and make you approve the angle — Medium writes a `medium_brief.md`, LinkedIn shows the claim, the surviving hooks, and what it proposes to leave out. The gate exists because both skills compress hard, and neither should get to decide on its own which of your experiences does not survive the compression. Whatever is dropped is named before it is dropped, and both writers carry a standing rule against cutting something you lived through without asking.

Neither writer scores a finished piece. The audit passes are rewrite triggers inside the workflow, not a grade — a number on a draft you just wrote is self-marking.

What is platform-specific is the advice itself: LinkedIn's dwell time, saves, and substantive comments behave nothing like Medium's read ratio and distribution rules. That is the point of splitting them rather than shipping one "write a post" skill.

None of these skills post anything anywhere. They write Markdown files next to your notes; publishing stays a deliberate manual step.

## Install

```bash
uv run scripts/sync_all.py            # every skill in the repo, all five platforms
```

Or copy individual folders into whichever skills directory your harness reads:

```bash
cp -r Common/idea-research Medium/medium-article-writer ~/.claude/skills/
```

`idea-research` and `keyword-research` ship stdlib-only Python under `scripts/` — no third-party packages, no keys.
