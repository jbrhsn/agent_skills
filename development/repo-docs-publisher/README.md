# repo-docs-publisher

Reads an existing repository and prepares the standard documentation needed to publish it as a public GitHub repo — `README.md`, `HOW_TO_USE.md`, `CONTRIBUTING.md`, and `LICENSE`, plus optional community files. Scans the actual repo (code, structure, dependencies, existing docs) so nothing is fabricated, and runs a secrets/sensitive-info scan first so private material never ships to a public repo.

---

## Trigger phrases

| Input | Example |
|---|---|
| Prepare for open-sourcing | "prepare this repo for GitHub", "get this ready for open-sourcing" |
| Write a README | "write a README for this repo" |
| Make it public/ready | "make this repo public", "is this repo ready to publish?" |
| Polish existing docs | "polish the docs", "clean up the README and CONTRIBUTING" |

Do **not** trigger this skill to plan a *new* project (use `project-planner`) or to write/refactor source code (use `lean-coder`).

---

## What it does

Runs **nine confirmed phases**. The two scans (Phases 0 and 1) launch as **parallel subagents in a single message** so the full repo contents never land in the main context; the Phase 0 gate still applies to the secrets result regardless of concurrency. Doc generation does not begin until any secrets finding is acknowledged:

| Phase | What happens |
|---|---|
| **Phase 0 — Secrets scan** | **Always first.** A subagent briefed with `secrets-scan-checklist.md` searches for `.env` files, keys/tokens/passwords, private URLs/hostnames, and `.gitignore` gaps. **Hard gate:** if anything is found, stop and flag it (`file:line`) and do not draft any public-facing docs until the user acknowledges |
| **Phase 1 — Repo scan** | A second subagent (parallel with Phase 0) briefed with `repo-scan-checklist.md` detects language/framework/package manager, dependencies, test runner, linter, CI config, existing docs, entry points, install/build/run commands, and monorepo vs single package |
| **Phase 2 — Ask + confirm** | Asks the user only for what scanning could not infer (name/tagline, audience, wanted extras), then confirms the full file list to generate before writing anything |
| **Phase 3 — License** | Reuses an existing `LICENSE` as-is (flagging any mismatch with the manifest); otherwise summarizes MIT / Apache-2.0 / GPL-3.0 / BSD-3-Clause and generates the full canonical text for the chosen one |
| **Phase 4 — README.md** | Generates `README.md` from `readme-template.md` with only badges that Phase 1 actually detected |
| **Phase 5 — HOW_TO_USE.md** | Generates the detailed usage doc from `how-to-use-template.md`; README links here rather than duplicating depth |
| **Phase 6 — CONTRIBUTING.md** | Generates `CONTRIBUTING.md` from `contributing-template.md`, tailored to the real test/lint/PR conventions found |
| **Phase 7 — Optional extras** | Generates only what was confirmed: `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`, `.github/` issue & PR templates |
| **Phase 8 — Wrap up** | Re-confirms any flagged secrets were remediated **before** generating files; writes all confirmed files to disk and summarizes, noting the Phase 0 scan only covered what was inspected |

---

## Files it can generate

| File | When |
|---|---|
| `README.md` | Always considered |
| `HOW_TO_USE.md` | Always considered |
| `CONTRIBUTING.md` | Always considered |
| `LICENSE` | Always considered (reused as-is if present, else chosen with the user) |
| `CODE_OF_CONDUCT.md` | Only if confirmed |
| `SECURITY.md` | Only if confirmed |
| `CHANGELOG.md` | Only if confirmed (seeded from git tags/releases if any) |
| `.github/` issue & PR templates | Only if confirmed |

---

## Safety: secrets scan

Phase 0 delegates a scan to a subagent briefed with `references/secrets-scan-checklist.md`. It searches for `.env` files, private keys/certs, hardcoded API keys/tokens/passwords, private URLs or internal hostnames, and `.gitignore` gaps. It distinguishes material present only in the **working tree** (a `.gitignore` fix plus removal is enough) from material **already committed to git history** — for the latter it recommends history-rewriting tools (`git filter-repo`, BFG Repo-Cleaner) plus credential rotation, since deleting a file in a new commit leaves it recoverable. Any finding **blocks doc generation** until the user acknowledges it.

License legal text is always fetched from the canonical, current source — never reproduced, paraphrased, or shortened from memory.

---

## Inputs

| Input | Required | Description |
|---|---|---|
| An existing repository | Yes | The repo to document; this skill documents existing repos, it does not plan new ones |
| Subagents (Task tool) | Optional | Used for the two scans; falls back to running both scans inline against the reference checklists if unavailable |
| Interactive user | Yes | Answers license choice and confirms the optional-file list before generation |
| Network access | Optional | Used to fetch canonical license text in Phase 3 |

---

## Outputs

The confirmed documentation files written to disk (see "Files it can generate"), followed by a summary of what was created. The summary carries a caveat: the Phase 0 scan only checked what this skill inspected — a full git-history audit is the user's responsibility if the repo has commit history predating this pass.

---

## Limitations

- **Existing repos only.** Documents a repo that already exists; it does not plan a new project (use `project-planner`).
- **Never fabricates specifics.** Install commands, badges, and license choices are only ever those found in the repo or confirmed by the user.
- **Monorepo handling asks first.** For monorepos it asks whether you want root-level docs, per-package docs, or both, and which package is primary.
- **Documentation only.** It writes docs, never source code (use `lean-coder` for code).
- **Not a full history audit.** The secrets scan is not a substitute for a complete git-history audit of the repository.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global — available in all projects (Linux/macOS)
cp -r development/repo-docs-publisher ~/.config/opencode/skills/

# Per-project only
cp -r development/repo-docs-publisher .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse development\repo-docs-publisher "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/repo-docs-publisher.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before naming the repo to document |

---

## Companion skills

- **`project-planner`** — for planning a *new* project from an idea (spec/design/roadmap/backlog)
- **`lean-coder`** — for writing or refactoring the repo's code
- **`ui-ux-designer`** — for designing an app's UI/UX
