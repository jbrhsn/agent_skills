# medium-article-writer

An Agent Skill that turns a rough draft in `source.md` into a finished,
publishable Medium article plus a titles/tags/alt-text package.

Portable across Claude Code, OpenCode, and Google Antigravity. No scripts, no
dependencies, no agent-specific tooling — plain markdown and relative paths only.

## Layout

```
medium-article-writer/
├── SKILL.md
├── references/
│   ├── voice-inference.md       # extract the author's register, read at step 1
│   ├── voice-and-antislop.md    # voice + machine-writing tells, read before drafting
│   ├── closing-and-cta.md       # how the piece ends + CTA options, read at step 6
│   ├── do-and-avoid.md          # distribution checklist, read at audit
│   └── medium-mechanics.md      # titles, tags, images, paste flow
└── assets/
    ├── article-structures.md    # skeletons per piece type, placing experience, modes
    ├── brief-template.md        # angle, voice card, coverage ledger, omissions
    └── publish-template.md      # titles, tags, CTA record, alt text, paste steps
```

## Install

From this repo, the sync script handles every platform:

```bash
uv run scripts/sync_all.py            # every skill, all five platforms
```

To install this one skill by hand, skill discovery paths differ per platform:

| Platform | Reads |
|---|---|
| Claude Code | `~/.claude/skills/` (per-repo: `.claude/skills/`) |
| OpenCode | `~/.config/opencode/skills/` (per-repo: `.opencode/skills/`) |
| Codex / ChatGPT | `~/.agents/skills/` |
| Antigravity | `~/.gemini/config/skills/` |
| IBM Bob | `~/.bob/skills/` |

Keep one canonical copy and symlink it, so edits propagate everywhere:

```bash
mkdir -p ~/skills && cp -r medium-article-writer ~/skills/

for d in ~/.claude/skills ~/.config/opencode/skills ~/.agents/skills \
         ~/.gemini/config/skills ~/.bob/skills; do
  mkdir -p "$d" && ln -s ~/skills/medium-article-writer "$d/medium-article-writer"
done
```

**Windows** — symlinks need admin or developer mode; copying is simpler:

```powershell
Copy-Item -Recurse medium-article-writer "$env:USERPROFILE\.claude\skills\"
```

Restart the agent session afterward. Skills are discovered at startup.

### Verify

Ask the agent what skills it has available. `medium-article-writer` should appear with
its description. If it doesn't:

- Confirm the file is named `SKILL.md`, all caps.
- Confirm the frontmatter has both `name` and `description` — a skill without a
  description is not advertised to the model.
- Confirm the directory name matches the `name` field exactly.
- Confirm skill names are unique across all search locations.

## Use

```
articles/iceberg-compaction/
└── source.md
```

Write your draft, notes, or dictated thoughts into `source.md`, then tell the
agent to turn it into a Medium article. It produces `medium_brief.md` (which it
pauses on for approval — that gate is also where it tells you what it proposes to
leave out), then `medium_article.md` and `medium_publish.md`.

## Design notes

- **Facts are verify-only.** The agent may check claims already in `source.md`
  against the web. It may not search for new material to pad the piece. Anything
  it cannot confirm is surfaced in `medium_brief.md` rather than written around.
- **No fabricated experience.** Anecdotes, benchmarks, and error messages come
  from you or they don't appear.
- **No silently dropped experience.** The mirror rule. Everything load-bearing in
  `source.md` is mapped to a section in `medium_brief.md`; anything that does not
  fit is listed for your approval before it is cut, and anything that stops fitting
  mid-draft is raised rather than removed.
- **Every piece gets a real ending.** A takeaway plus a call to action, which
  defaults to a genuine question. Follow prompts, subscribe lines, and links are
  only used if you ask and supply the destination — the skill never invents one.
- **Finance pieces are framed as experience,** never advice — Medium treats
  unverified financial claims as a rules violation.
- **Zero dependencies** is deliberate. A linter for paragraph length and banned
  phrasings would break portability while catching less than the model does
  reading `voice-and-antislop.md`.

## Portability constraints

If you edit the skill, keep these or it stops working somewhere:

- Frontmatter limited to `name` and `description`. Other fields are legal in the
  spec but not interpreted everywhere.
- `name`: lowercase, digits and hyphens only, ≤64 chars, matching the directory.
- No absolute paths, no shell commands in the required path, no agent-specific
  tool names.
- Keep `SKILL.md` under 500 lines; push detail into `references/`.
- Reference files stay one level deep.
