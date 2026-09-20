# Content Creation Skills

Nine complementary skills support idea research, strategy, discovery, factual refinement, writing, and visual production. Use the skills needed for the request; they are not a mandatory pipeline.

| Skill | Use for | Default artifact |
|---|---|---|
| [idea-research](Common/idea-research/README.md) | Research and prioritize angles for an audience/niche | Evidence-backed ideas; optional source scaffolds |
| [content-strategy](Common/content-strategy/README.md) | Integrated idea research and weekly/monthly planning for one or multiple platforms | content_strategy.md; optional content_research.md |
| [keyword-research](Common/keyword-research/README.md) | Search intent, query phrasing, and discovery metadata | kresearch.md |
| [content-fact-checker](Common/content-fact-checker/README.md) | Claim-level validation and evidence-preserving refinement of an initial draft | Refined source or draft with attribution and a change summary |
| [remotion-infographics](Common/remotion-infographics/README.md) | A 10–30 second Remotion infographic from an article or post idea | MP4, final-frame hero PNG, and editable `remotion-infographic/` project |
| [linkedin-post-writer](Linkedin/linkedin-post-writer/README.md) | LinkedIn drafting or substantial revision | linkedin_post.md and linkedin_publish.md |
| [x-post-writer](X/x-post-writer/README.md) | Short, medium-length, and long X posts, plus connected threads | x_post.md and x_publish.md |
| [medium-article-writer](Medium/medium-article-writer/README.md) | Long-form drafting, substantial revision, and packaging | medium_article.md and medium_publish.md |
| [medium-image-prompts](Medium/medium-image-prompts/README.md) | Article visual directions and prompt text | medium_image_prompts.md |

## Shared conventions

A folder per piece with raw notes in `source.md` makes handoffs convenient, but supplied text, other filenames, topic briefs, and explicit output paths are supported. A source filename alone does not choose a platform or trigger every skill. Preserve original notes and unrelated user edits.

The LinkedIn, X, and Medium writers first present five hook-and-structure proposals for new drafts and substantial rewrites, research comparable performance patterns, recommend a faithful direction, and wait for author confirmation before writing the full artifact. Narrow edits and already confirmed directions proceed directly. Clarify material ambiguity or changes to the author's meaning; distinguish evidence, personal experience, illustrative examples, and editorial choices. Never fabricate anecdotes, metrics, quotes, sources, or test results.

References provide adaptable guidance rather than universal word counts, visual styles, or algorithm formulas. Platform claims need current evidence. Research scores describe heuristic ordering/provenance; they do not predict reach or measure search volume.

The writing, refinement, and prompt workflows prepare artifacts. They do not publish, schedule, submit, or send messages automatically. After an approved creative direction, remotion-infographics completes its requested local render; actual publication or upload remains separate.

The common content-strategy skill includes idea discovery and prioritization directly; idea-research remains available for focused discovery and optional fetchers. Plans work without writer skills, and individual writer briefs work without a full strategy document. Planning does not automatically launch drafting or publishing.

The X writer combines single posts and threads in one independent skill. An optional strategy brief such as `content_strategy.md` or `x_strategy.md`, research output, or an existing LinkedIn/Medium draft can inform its work; none is required. Short, medium-length, and long describe editorial depth rather than platform character bands. Its [handoff conventions](X/x-post-writer/references/handoffs.md) explain how optional context and writing notes support collaboration without triggering additional workflows.

Content-fact-checker improves reliability without changing the author’s core message, opinions, voice, or tone. It distinguishes verified, partially supported, unsupported, contradicted, unverified, and personal/editorial claims, and reports unresolved central conflicts for author review. Remotion-infographics requires a confirmed theme, palette, and creative direction unless the user has already supplied or delegated those choices; its final hero PNG is the actual last frame of the MP4.

## Helpers and validation

Idea research has standard-library Python helpers, run with `uv run`; missing uv requires confirmation before installation. Keyword research has a Bash helper requiring curl and jq. Browser research remains a fallback when helpers or endpoints are unavailable.

Preview helper writes with supported `--dry-run` options and keep research runs isolated. Run `uv run scripts/test_content_research.py` from the distribution repository for offline regression checks using local fixtures.

Preview repository distribution with `uv run scripts/sync_all.py --dry-run`; synchronize via the repository scripts when requested.
