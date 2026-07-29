---
name: repo-docs-publisher
description: Reads an existing repository and prepares the standard docs to publish it as a public GitHub repo — README.md, HOW_TO_USE.md, CONTRIBUTING.md, LICENSE, and optionally CODE_OF_CONDUCT.md, SECURITY.md, CHANGELOG.md, and GitHub issue/PR templates. Use whenever the user wants to prepare, write, or polish docs for open-sourcing/publishing a repo, asks for a README or related docs, or mentions making a repo "ready for GitHub" or "public." Always scans the actual repo first (code, structure, dependencies, existing docs) and checks for secrets before recommending it be made public. Do NOT use to plan a new project (project-planner) or write/refactor code (lean-coder).
metadata:
  category: documentation
  audience: maintainers
  outputs: README.md,HOW_TO_USE.md,CONTRIBUTING.md,LICENSE
---

# Repo Docs Publisher

Reads an existing repository and prepares the documentation needed to publish it as a public GitHub repo: `README.md`, `HOW_TO_USE.md`, `CONTRIBUTING.md`, `LICENSE`, and — based on user confirmation — `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`, and GitHub issue/PR templates.

## Workflow

**Use subagents for the two scans.** Phases 0 and 1 are both read-heavy passes over the entire repo — exactly the work to push into subagents (via the Task tool) so the full repo contents never land in your main context. Launch them **in parallel in a single message**: one subagent for the secrets/sensitive-info scan (Phase 0) and one for the repo/tech scan (Phase 1). They inspect the same tree and don't depend on each other, so running them together is strictly faster. The Phase 0 **gate still applies to the results**: even though the scans run concurrently, do not draft any public-facing docs until you've reviewed the secrets subagent's report and, if it found anything, gotten the user's acknowledgement. The interview (Phase 2), license choice, approvals, and file generation stay in the primary session. (If subagents aren't available in the environment, run both scans inline using the reference checklists, keeping the Phase 0 gate intact.)

### Phase 0: Secret / sensitive-info scan (always first)

Before publishing anything, since the goal is a **public** repo, scan for material that must not be published. Delegate this to a subagent (an `explore` or `general` subagent) briefed with `references/secrets-scan-checklist.md`:

- Have it search for `.env` files, hardcoded API keys/tokens/passwords, private URLs or internal hostnames, credentials in config files, and `.gitignore` gaps (e.g. no `.gitignore` at all, or one that doesn't cover common secret file patterns).
- Tell it to report exactly what was found and where (`file:line`), or to confirm the scan was clean.
- If anything is found: **stop and flag it clearly to the user** before proceeding with documentation. List what was found and where, and recommend removal/rotation and history-scrubbing (e.g. via `git filter-repo` or BFG) if secrets are already committed — do not proceed to draft public-facing docs until the user acknowledges this.
- If nothing is found, briefly note the scan was clean and proceed.

### Phase 1: Scan the repo

Delegate this to a second subagent (launched in parallel with the Phase 0 one), briefed with `references/repo-scan-checklist.md` for a systematic list of what to inspect and where. Ask it to report back:

- Language(s), framework(s), package manager, and dependencies from manifest files (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.).
- Test runner, linter/formatter, and CI config (e.g. `.github/workflows/`) if present — these inform badges and CONTRIBUTING.md.
- Existing docs (`README.md`, `LICENSE`, etc.) — if present, treat this as an **update/polish** pass, not a from-scratch write; the subagent should surface their current content so accurate parts are preserved.
- Inferred project purpose (from code structure, existing docstrings/comments, package description fields), entry points, install/build/run commands, and directory layout.
- Whether an existing `LICENSE` file is present. If one exists, use it as-is (don't re-ask about licensing). If none exists, this is handled in Phase 3.
- **Monorepo vs single package:** detect whether the repo is a monorepo (multiple package manifests under `packages/`, `apps/`, workspaces in `package.json`/`pyproject.toml`, `go.work`, Cargo workspace, etc.). If so, ask in Phase 2 whether the user wants **root-level** docs describing the whole repo, **per-package** docs, or both — and confirm which package is the primary/published one so the README quick-start points at the right entry point. Default to root-level docs plus a short "Packages" section listing each package with a one-line purpose, unless the user asks for per-package docs.

### Phase 2: Ask only what can't be inferred

Ask the user only for what scanning couldn't determine — don't re-ask things already evident from the repo. Typical gaps:

- Project name/tagline if not obvious from manifest or repo name
- Target audience / intended use case (helps tone of README)
- Whether GitHub issue/PR templates are wanted (see Phase 7)
- Anything scan results were ambiguous about (e.g. multiple possible entry points, unclear install method)

Keep this brief — a single batch of questions is usually enough since Phase 1 should have resolved most of it. Confirm the full file list to generate (README, HOW_TO_USE, CONTRIBUTING, LICENSE, plus any of CODE_OF_CONDUCT/SECURITY/CHANGELOG/templates) before generating, since the user may not want all of them for this repo.

### Phase 3: License

- If `LICENSE` already exists, reuse it as-is — **unless** the scan shows it's inconsistent with the repo (e.g. manifest `license` field names a different license than the `LICENSE` file, or a stale copyright year/holder). In that case flag the mismatch to the user and ask which is correct before proceeding, rather than silently trusting either.
- If not, help the user pick one. Briefly summarize the common options (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause) and their practical implications, then generate the full, correct license text for the one chosen. Use `references/license-summaries.md` for the summaries — never paraphrase or shorten actual license legal text, always use the complete standard text for whichever license is chosen.

### Phase 4: Generate README.md

Use `references/readme-template.md`. Standard sections: title/tagline, badges, description, table of contents (for longer READMEs), installation, quick usage example, link to `HOW_TO_USE.md` for detailed usage, contributing link (to `CONTRIBUTING.md`), license section (referencing `LICENSE`).

Always propose badges relevant to what Phase 1 detected (build status if CI config found, license badge, package-registry version badge if published, language/version badges) — don't fabricate a badge for something that doesn't exist (e.g. no build badge if there's no CI config).

### Phase 5: Generate HOW_TO_USE.md

Keep this separate from README.md per project convention. Use `references/how-to-use-template.md`. This is the detailed usage doc: full setup, configuration options, common workflows/examples, troubleshooting tips. README.md should link here rather than duplicating this content — keep the split clean (README = quick start + overview, HOW_TO_USE = depth).

### Phase 6: Generate CONTRIBUTING.md

Use `references/contributing-template.md`, always tailored to what Phase 1 detected — reference the actual test command, linter, and branch/PR conventions found in the repo (e.g. `npm test`, `pytest`, `make lint`) rather than generic placeholders. Cover: how to set up a dev environment, how to run tests/lint, branch naming or commit conventions if any are evident from git history, and the PR process.

### Phase 7: Optional extras

Ask (if not already answered in Phase 2) whether the user wants:
- `CODE_OF_CONDUCT.md` (standard Contributor Covenant text if yes)
- `SECURITY.md` (how to report vulnerabilities)
- `CHANGELOG.md` (seed from git tags/releases if any exist, else a starter template)
- GitHub issue templates and a PR template under `.github/`

Generate only what's confirmed.

### Phase 8: Wrap up

If Phase 0 flagged any secrets, **before generating files re-confirm they were remediated** (removed/rotated, history scrubbed if already committed). If the user chose to proceed without remediating, note explicitly in your summary that the repo still contains the flagged material and should not be made public until it's resolved — don't let a flagged finding silently pass through to a "ready to publish" state.

Generate all confirmed files as actual files (not just chat text) — this is a file-creation task. Let the user review afterward rather than gating each file individually. Summarize what was created and remind them the secrets scan (Phase 0) only checked what this skill inspected — a full history audit is their responsibility if the repo has existing commit history predating this pass.

## Related skills

- **`project-planner`** — for planning a *new* project from an idea (spec/design/roadmap/backlog). This skill is for documenting an *existing* repo, not planning; hand off if the user actually wants to plan.
- **`lean-coder`** — for writing or refactoring the repo's code. This skill only writes documentation, never source code.
- **`ui-ux-designer`** — for designing an app's UI/UX. Unrelated to publishing docs.

## Notes

- This is a documentation skill for **existing** repos, not project planning (see Related skills above).
- Never fabricate specifics (install commands, badge data, license choice) that weren't found in the repo or confirmed by the user.
- Keep tone appropriate for a public open-source audience: clear, welcoming to outside contributors, no internal jargon or references to private infrastructure.