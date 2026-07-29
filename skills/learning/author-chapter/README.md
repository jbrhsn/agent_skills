# author-chapter

Turns a blank stub (or thin file) into a fully template-compliant learning chapter. Researches live official sources, writes every section to the repo's own standard, runs an automated quality gate, and writes the final file only after every check passes.

---

## Trigger phrases

| Input | Example |
|---|---|
| Populate a stub | "populate this chapter", "fill in this stub" |
| Author by name | "author the notes for [topic]" |
| By file path | "write `01-networking/01-vpc/01-concepts.md`" |
| Template-aware | "write the [chapter name] chapter following the template" |

Do **not** trigger this skill to create a new repo (use `create-learning-repo`) or to generate a quiz/exam (use `generate-practice-exam`).

---

## What it does

Runs **five confirmed phases**. Every phase except the final write ends with an explicit "proceed" gate:

| Phase | What happens |
|---|---|
| **Phase 0 — Locate contract** | Identifies the target file; walks up the tree to find `AGENTS.md` + `templates/`; confirms the file is a stub (will not silently overwrite authored content) |
| **Phase 1 — Research** | Fetches the official documentation, exam objective wording, and changelog in parallel; presents a compact research brief with planned concepts and worked example scenario for approval |
| **Phase 2 — Draft** | Writes every section in the template's order to the required depth; presents the full draft for review |
| **Phase 3 — Quality gate** | Self-audits the draft against a pass/fail checklist; any failure blocks completion; fixes failures and re-runs until all rows are ✓ |
| **Phase 4 — Write** | Writes the file with the `Write` tool; reports a structured completion summary |

---

## Contract-first design

The section order and depth rules are **read from the target repo's own files at runtime** — not hardcoded into this skill:

| Situation | Contract used |
|---|---|
| `AGENTS.md` + `templates/` both found | Reads and follows them — they win |
| Neither found (loose Markdown folder) | Asks confirmation, then falls back to built-in `reference/quality-gate.md` |
| Only one found | Uses what is present, falls back for the missing piece; tells you which contract applies |

This makes the skill portable across repos with different templates and standards.

---

## Quality gate checks (Phase 3)

These checks are the enforcement layer for the repo's 9 content-depth rules (defined in the repo's `AGENTS.md`, written by `create-learning-repo`) — one rule maps to one or more concrete checks. Every chapter is validated against them before writing. Any ✗ blocks completion:

| Check | Type |
|---|---|
| TL;DR ends with bolded "one thing to remember" | Deterministic |
| ELI5 has structural analogy + corrects a misconception | Qualitative |
| Every Key Concept sub-section has How + Where | Qualitative |
| Key Parameters table present (or explicit "none" note) | Deterministic |
| Worked Example follows 5-step format | Structural |
| ≥2 implementation snippets, different angles | Count |
| ≥1 anti-pattern snippet with corrected version | Deterministic |
| Every snippet opens with a scenario/anti-pattern comment | Deterministic |
| Pitfalls have all 3 parts (label + why + correct model) | Structural |
| 5 questions spanning 3 cognitive levels | Count + qualitative |
| ≥1 multi-select question | Deterministic |
| `<details>` count == question count (+1 if a sample question section exists) | Count |
| Every answer explains correct + why distractors fail | Qualitative |
| Further Reading: official docs only, all links verified | Deterministic |
| Zero TODO/STUB markers remain | Deterministic |

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Target file path (or chapter name) | Yes | The stub or thin file to populate |
| `AGENTS.md` + `templates/` | Preferred | Authoritative authoring contract; skill falls back to built-in if absent |
| Live web access | Yes | Phase 1 fetches official docs; requires network access |

---

## Outputs

A single fully-authored Markdown chapter at the target path. Completion report:

```
Authored:      path/to/file.md
Contract:      repo templates/AGENTS.md  (or built-in fallback)
Sections:      N (all template sections present)
Snippets:      N (incl. N anti-pattern)
Questions:     5 (N multi-select)
Links verified:N/N
Quality gate:  PASS (all checks ✓)
```

---

## Limitations

- **One file per invocation.** The skill authors only the file you explicitly name. It does not batch-populate a module unless you ask for each file separately.
- **Stubs only, freely.** For files with existing authored content, the skill stops and asks before proceeding.
- **Official sources only.** The Further Reading section uses only official documentation — no third-party blogs, Medium, or YouTube.
- **Live research required.** Phase 1 makes real web requests. Avoid running in offline environments. If official sources are unreachable, the skill stops rather than authoring from training data — paste doc excerpts directly, or use `create-learning-repo`'s Phase 1 fallback prompts and share the results.
- **No exam/quiz generation.** Use `generate-practice-exam` for that.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global — available in all projects (Linux/macOS)
cp -r learning/author-chapter ~/.config/opencode/skills/

# Per-project only
cp -r learning/author-chapter .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse learning\author-chapter "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/author-chapter.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before naming the chapter to author |

---

## Companion skills

- **`create-learning-repo`** — scaffolds the repo and stubs that this skill populates
- **`generate-practice-exam`** — builds mock exams from chapters authored by this skill
