# ui-ux-designer

Designs user flows, screen layouts, and a design system for an app, and writes them to `docs/ux-design.md`. There is no image generation — flows are Mermaid diagrams and screens are structured text descriptions, never wireframe images or Figma files. Can also propose revisions to an existing `docs/01-spec.md` / `docs/02-design.md` when UX decisions surface changes.

---

## Trigger phrases

| Input | Example |
|---|---|
| Design the interface | "design the UI/UX for this app" |
| Design specific artifacts | "design the screens / user flows / wireframes / layouts" |
| Visual direction | "figure out the look and feel" |
| Slash command | `/design-ux` |
| Revise from UX decisions | "update `docs/01-spec.md` / `docs/02-design.md` based on these UX choices" |

Do **not** trigger this skill for general project planning (use `project-planner`) or for writing code (use `lean-coder`).

---

## What it does

Runs **nine confirmed phases**. Interview and write phases end with an explicit gate; the skill never runs two phases blindly in one pass:

| Phase | What happens |
|---|---|
| **Phase 0 — Assess applicability** | Determines whether the project has a user-facing interface at all. If it is CLI-only, an API/backend service, or a library, it says so and stops rather than fabricating screens — or offers the lighter CLI-ergonomics treatment. A **TUI** counts as a genuine user-facing surface and takes the normal path |
| **Phase 1 — Gather context** | If `docs/01-spec.md` / `docs/02-design.md` exist, delegates reading them to an `explore` subagent (via Task) for a design-relevant briefing; reads directly when docs are short, only one exists, or subagents are unavailable |
| **Phase 2 — Interview** | Asks in batches of 5 questions (`question` tool where available), covering users, core flows, platform, visual tone, and screen scope; skips anything already answered |
| **Phase 3 — User flows** | Produces a Mermaid flowchart per core flow, including decision points and error/edge paths, using `references/flow-diagram-guide.md` |
| **Phase 4 — Screens** | Writes a structured text layout per screen (not ASCII art, not images) using `references/screen-template.md` |
| **Phase 5 — Design system** | Always required: color palette, typography, spacing, and core components with states, using `references/design-system-template.md` |
| **Phase 6 — Accessibility** | Off by default; added only if requested — or forced when the spec makes accessibility a requirement — using `references/accessibility-checklist.md` |
| **Phase 7 — Write `docs/ux-design.md`** | Assembles the phases into the output file and gets approval/revisions before considering the design done |
| **Phase 8 — Propagate changes** | If UX work surfaced scope/architecture changes, proposes edits back to `docs/01-spec.md` / `docs/02-design.md` — summarized and confirmed first, never silently rewritten |

**Non-interactive fallback:** when the `question` tool is unavailable or the user is not present, it falls back to plain numbered questions; in a fully automated run it proceeds with best-reasoned assumptions and records each one as an open question in the output.

---

## Output file

`docs/ux-design.md` at the repo root — a single file containing user flows, screen-by-screen layout descriptions, and the design system. For plain command-line tools, it uses the CLI-ergonomics template instead (see below).

---

## The CLI fork

For a plain command-line tool (flags in, text out, no full-screen interface), Phase 0 offers the lighter command-ergonomics treatment. If accepted, the skill uses `references/cli-ergonomics-template.md` — command structure, flags and arguments, output design, errors and exit codes, help and discoverability, and interaction/safety — and skips the screen and flow phases (3-5). A **TUI** does not take this path; it is a genuine user-facing surface and gets the normal screen/flow treatment.

---

## Inputs

| Input | Required | Description |
|---|---|---|
| `docs/01-spec.md` | Optional | Read as source of truth for scope/users/requirements if present (owned by `project-planner`) |
| `docs/02-design.md` | Optional | Read as source of truth for architecture/stack if present (owned by `project-planner`) |
| Interactive user | Preferred | Answers the batched interview and approves the output; non-interactive fallback proceeds with recorded assumptions |
| `explore` subagent | Optional | Reads spec/design docs in Phase 1; skill reads inline when subagents are unavailable |

---

## Outputs

`docs/ux-design.md` — flows, screen layouts, and design system. Optionally, proposed edits to `docs/01-spec.md` / `docs/02-design.md` when UX work implies scope or architecture changes (always confirmed, never silent). No images, Figma files, or wireframe files are produced.

---

## Limitations

- **No image generation.** All output is Mermaid diagrams (flows) and structured text (screens) — never wireframe images, mockups, or Figma files.
- **Stops for non-UI projects.** For CLI-only tools, APIs, or libraries it says so and stops rather than fabricating screens (the CLI-ergonomics fork is offered instead).
- **Spec/design docs are read-only.** `docs/01-spec.md` and `docs/02-design.md` are owned by `project-planner`; this skill only *proposes* edits and confirms before writing.
- **Accessibility off by default.** The accessibility section is added only when requested, or when the spec makes accessibility a requirement.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global — available in all projects (Linux/macOS)
cp -r development/ui-ux-designer ~/.config/opencode/skills/

# Per-project only
cp -r development/ui-ux-designer .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse development\ui-ux-designer "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/ui-ux-designer.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before asking for the UI/UX design |

---

## Companion skills

- **`project-planner`** — owns `docs/01-spec.md` and `docs/02-design.md`; runs before this skill
- **`lean-coder`** — implements the screens and flows this skill designs
- **`repo-docs-publisher`** — publishes an existing repo's docs (not part of the design pass)
