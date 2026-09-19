# Content Creation Skills

Five complementary skills support idea research, discovery, writing, and visual planning. Use the skills needed for the request; they are not a mandatory pipeline.

| Skill | Use for | Default artifact |
|---|---|---|
| [idea-research](Common/idea-research/README.md) | Research and prioritize angles for an audience/niche | Evidence-backed ideas; optional source scaffolds |
| [keyword-research](Common/keyword-research/README.md) | Search intent, query phrasing, and discovery metadata | kresearch.md |
| [linkedin-post-writer](Linkedin/linkedin-post-writer/README.md) | LinkedIn drafting or revision | linkedin_post.md and useful posting notes |
| [medium-article-writer](Medium/medium-article-writer/README.md) | Long-form drafting, revision, and packaging | medium_article.md, optional brief/publishing notes |
| [medium-image-prompts](Medium/medium-image-prompts/README.md) | Article visual directions and prompt text | medium_image_prompts.md |

## Shared conventions

A folder per piece with raw notes in `source.md` makes handoffs convenient, but supplied text, other filenames, topic briefs, and explicit output paths are supported. A source filename alone does not choose a platform or trigger every skill. Preserve original notes and unrelated user edits.

Ordinary drafting and revision proceed without repeated approval gates. Clarify material ambiguity or changes to the author's meaning; distinguish evidence, personal experience, illustrative examples, and editorial choices. Never fabricate anecdotes, metrics, quotes, sources, or test results.

References provide adaptable guidance rather than universal word counts, visual styles, or algorithm formulas. Platform claims need current evidence. Research scores describe heuristic ordering/provenance; they do not predict reach or measure search volume.

The writing and prompt workflows prepare artifacts. They do not publish, schedule, submit, or send messages automatically. Actual rendering can continue when requested using the appropriate available tools.

## Helpers and validation

Idea research has standard-library Python helpers, run with `uv run`; missing uv requires confirmation before installation. Keyword research has a Bash helper requiring curl and jq. Browser research remains a fallback when helpers or endpoints are unavailable.

Preview helper writes with supported `--dry-run` options and keep research runs isolated. Run `uv run scripts/test_content_research.py` from the distribution repository for offline regression checks using local fixtures.

Preview repository distribution with `uv run scripts/sync_all.py --dry-run`; synchronize via the repository scripts when requested.
