# medium-article

An Agent Skill that turns a rough draft in `source.md` into a finished,
publishable Medium article plus a titles/tags/alt-text package.

Portable across Claude Code, OpenCode, and Google Antigravity. No scripts, no
dependencies, no agent-specific tooling — plain markdown and relative paths only.

## Layout

```
medium-article/
├── SKILL.md
├── references/
│   ├── do-and-avoid.md          # distribution checklist, read at audit
│   ├── voice-and-antislop.md    # voice + machine-writing tells, read before drafting
│   └── medium-mechanics.md      # titles, tags, images, paste flow
└── assets/
    ├── article-structures.md    # skeletons per piece type + finance/writing modes
    ├── brief-template.md
    └── publish-template.md
```

## Install

Skill discovery paths differ per agent. Two locations cover all three:

| Agent | Reads |
|---|---|
| Claude Code | `.claude/skills/`, `~/.claude/skills/` |
| OpenCode | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` (+ `~` equivalents) |
| Antigravity | `.agents/skills/` (`.agent/skills/` still supported) |

Keep one canonical copy and symlink it, so edits propagate everywhere.

**Global, macOS/Linux:**

```bash
mkdir -p ~/skills
cp -r medium-article ~/skills/

mkdir -p ~/.claude/skills ~/.agents/skills
ln -s ~/skills/medium-article ~/.claude/skills/medium-article
ln -s ~/skills/medium-article ~/.agents/skills/medium-article
```

**Per-project:**

```bash
mkdir -p .claude/skills .agents/skills
ln -s ../../skills/medium-article .claude/skills/medium-article
ln -s ../../skills/medium-article .agents/skills/medium-article
```

**Windows** — symlinks need admin or developer mode; copying is simpler:

```powershell
Copy-Item -Recurse medium-article "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse medium-article "$env:USERPROFILE\.agents\skills\"
```

Restart the agent session afterward. Skills are discovered at startup.

### Verify

Ask the agent what skills it has available. `medium-article` should appear with
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
pauses on for approval), then `medium_article.md` and `medium_publish.md`.

## Design notes

- **Facts are verify-only.** The agent may check claims already in `source.md`
  against the web. It may not search for new material to pad the piece. Anything
  it cannot confirm is surfaced in `medium_brief.md` rather than written around.
- **No fabricated experience.** Anecdotes, benchmarks, and error messages come
  from you or they don't appear.
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
