# Project Handoff

<!-- Managed by the end-session / init-session skills. Section order is fixed; the file is compacted on every write, not appended to. -->

## Project Snapshot

agent_skills: curated 11-skill distribution repo for OpenCode, IBM Bob, Google Antigravity, Claude Code, and Codex/ChatGPT, plus 3 base agent definitions (orchestrator, executor, ask) and 1 opt-in OpenCode plugin (search-internet).
Skill organization: agent_session_management (2), learning (2), development (2), content-creation (5).
Sync model: scripts/common.py + per-platform scripts, dynamic discovery, PEP 723 + `uv run`. Agents/plugins sync fully to OpenCode (composition engine in scripts/plugins.py handles overlays); executor.md also translates to a Claude Code subagent at ~/.claude/agents/; Antigravity gets one global instructions file at ~/.gemini/config/AGENTS.md. IBM Bob and Codex/ChatGPT get skills only (at ~/.bob/skills and ~/.agents/skills respectively). Full SHA-256 checksum and parity verification integrated via `sync_all.py --verify`.

## Cumulative Learnings

- author-chapter redesign (2026-08-31): the fixed 'Part 1 Foundations -> Part 4 Architect' skeleton and 8-part labelled concept block were replaced with obligations, not headings - a spine (one-minute takeaway, mental model, Core path, Going deeper, closing sections) plus six questions every unit answers in prose (why it exists, what it is, show me one, where people go wrong, what it cost, can I do it). Only 'show me one' varies by domain, via references/domains.md - this is the same 'fixed spine + thin domain data' pattern used in create-learning-repo's PROFILES dict, applied to a prompt-only skill with no code.
- author-chapter now reads a create-learning-repo scaffolded file's frontmatter/brief as its assignment instead of re-planning (Phase 1) - tier ladder names are used verbatim from frontmatter `tiers`, never relabelled to Junior/Architect. This closes the contract gap between the two skills flagged at the end of the create-learning-repo session. Verified empirically: scaffolded a `craft` chapter with `tier_count: 3` and confirmed the drafted spine correctly carries a 3-rung Beginner/Practitioner/Voice ladder rather than defaulting to 4 or relabelling.
- Resolved stub-vs-spine layout conflict: a scaffolded learning.md arrives organised as one heading per tier rung (stub scaffolding); the authored spine organises by Core path / Going deeper instead. Rule now explicit in structure.md, SKILL.md and checklist.md: frontmatter + `## Brief` block survive untouched, everything below is replaced, rungs move down onto individual units, and the stub's HTML-comment prompts must never survive into the delivered file.
- author-chapter completeness is now graded against the plan's brief (topic coverage, per-topic depth, every ladder rung reached, stated purpose delivered), not against word count or a Tier-3-must-be-populated rule. The ~5-minute unit is a shaping/cutting guide only - never a reason to cut real coverage, never a reason to pad. A scope-halt was added: past ~18 implied units, the skill stops before writing and tells the user to split the chapter in PLAN.md rather than writing an oversized or thinned file.
- author-chapter now makes web search mandatory (not optional) when WebSearch/WebFetch tools exist: minimum one 'current state' query per chapter plus one per volatile topic, with version numbers/prices/benchmarks/dates/best-practice claims required to be sourced or explicitly flagged unverified. Findings land in `## Sources` with retrieval dates. This is a new phase (Phase 3) inserted between planning and writing.
- Verified sync integrity for a second time with a different check: after syncing an author-chapter change that grew references/ from 5 to 7 files, ran an independent SHA-256 tree hash (paths normalised, whole-tree hash) comparing the repo against all 5 destinations rather than just trusting sync_all.py --verify's own per-file report - all 5 matched the repo hash exactly, and a targeted grep for old-skill-version text markers found zero hits anywhere. Confirms the rmtree-before-copytree cleanup from the previous session generalises to a references/ file-count change too, not just top-level file renames.

## Last Session

- Redesigned create-learning-repo end to end: six fixed files per chapter (learning/examples/practice/interview/thought_leadership/quizzies), profile-as-data tier ladders (technical/craft/practice/exam/custom), plan-driven briefs with purpose required and depth/style/serves as thin-brief warnings.
- Synced and verified create-learning-repo across all 5 platforms with SHA-256 parity; confirmed no stale files survive a shape-changing sync.
- Flagged author-chapter as not yet updated to consume the new brief format - named as the explicit next target.

## Current Session

**Date:** 2026-08-31
**Focus:** Redesigned skills/learning/author-chapter to stop forcing one engineering-shaped format onto every domain, to consume create-learning-repo's new brief as its assignment, and to write in takeaway-first, bite-sized (~5 min) units instead of a single undifferentiated long document

### Done
- Rewrote SKILL.md: 6-phase workflow (read assignment / scope-check halt / mandatory research / write unit-by-unit / audit / deliver), 28-year-old-who-knows-nothing reader model, non-negotiables updated for takeaway-first and obligations-not-headings
- Rewrote references/structure.md: replaced the fixed Part0-4/Tier0-3 skeleton with a universal spine (In one minute / mental model / Core path / Going deeper / closing sections) and the per-concept 8-part block with 6 prose obligations; added the stub-vs-spine replacement rule and sizing guidance (unit is a shaping guide, never a length gate)
- Added references/domains.md (new): 4 packs - technical, craft, practice, exam - each defining what counts as evidence, what a worked example is, what the top rung means, and what never to do, keyed to create-learning-repo's existing profile names
- Added references/file-types.md (new): what each of the 6 scaffolded files is for, and the 3 refusals - quizzies.md ships with blank answers, practice.md ships with no solutions, thought_leadership.md never gets invented evidence
- Rewrote references/checklist.md: completeness-against-brief section runs first and is fully mechanical (topic-by-topic, rung-by-rung); universal/domain/file-type sections replace the old one-size checklist; added sourcing and stub-replacement checks
- Rewrote references/examples.md: added a second calibration pair (craft/essay-openings) alongside the technical one, both rewritten to demonstrate takeaway-first units and prose obligations with no visible labels
- Edited references/voice.md and references/pedagogy.md: reader model changed to the 28-year-old, 'bias long' replaced with 'bias complete per unit, then end the unit', added BLUF/vital-few/let-the-reader-stop sections, generalised Tier-3 language to 'the top rung'
- Updated the skill's README.md, skills/learning/README.md, and root README.md to describe the new shape
- Verified end-to-end: scaffolded a real craft-profile, tier_count:3 chapter via create-learning-repo and confirmed the emitted brief/frontmatter matches everything author-chapter's Phase 1 claims to read
- Synced all 11 skills to all 5 platforms and verified with both sync_all.py --verify and an independent full-tree SHA-256 hash comparison plus a stale-marker grep across every destination - all clean

### Decisions
- Kept the 'fixed universal spine + thin per-domain data' pattern from create-learning-repo's PROFILES dict, applied here as domains.md rather than per-domain document templates - avoids reintroducing format-per-domain complexity
- Chose obligations-not-headings (6 questions answered in prose) over the old printed 8-label block, specifically because the labelled block itself was steering models toward one register regardless of topic - verified against the rewritten calibration examples
- Completeness against the plan's brief replaces length/word-count as the audit gate; the ~5-minute unit size is advisory only and must never be used to cut real coverage or to pad
- Added a hard scope-halt (~18 units) that stops the skill before writing rather than letting it silently produce an oversized or under-scoped chapter - user must resplit in PLAN.md and re-scaffold
- Web search made mandatory (not just permitted) whenever the host has WebSearch/WebFetch, given the skill's own training-cutoff risk on version-sensitive claims
- Resolved the stub-layout-vs-spine-layout conflict discovered during verification by making the rule explicit in three files rather than leaving it implicit: frontmatter/Brief block preserved, tier headings replaced by Core path/Going deeper, rung names moved onto individual units

### Open Items
- [ ] All author-chapter and create-learning-repo changes are synced to all 5 platforms but still uncommitted in git (9 modified files + 2 new references files in author-chapter, plus the prior session's create-learning-repo changes) - user has not yet asked to commit
- [ ] User raised whether tier headings should survive as subheadings inside each unit/section rather than disappearing entirely when the spine replaces the stub's per-rung layout - flagged, not decided; current behavior drops the tier heading and tags the rung onto each unit instead
- [ ] No live end-to-end author-chapter authoring run has been done yet (only the scaffold-side brief was verified) - the actual writing workflow (Phases 3-6: research, unit-by-unit writing, audit, delivery) has not been exercised on a real topic
