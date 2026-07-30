---
name: repo-docs-publisher
description: Reads an existing repository and prepares the standard docs to publish it as a public GitHub repo — README.md, HOW_TO_USE.md, CONTRIBUTING.md, LICENSE, and optionally CODE_OF_CONDUCT.md, SECURITY.md, CHANGELOG.md, and GitHub issue/PR templates. Use whenever the user wants to prepare, write, or polish docs for open-sourcing/publishing a repo, asks for a README or related docs, or mentions making a repo "ready for GitHub" or "public." Always scans the actual repo first (code, structure, dependencies, existing docs) and checks for secrets — an explicit stop gate — before recommending it be made public. Do NOT use to plan a new project (project-planner) or write/refactor code (lean-coder).
metadata:
  category: documentation
  audience: maintainers
  outputs: README.md,HOW_TO_USE.md,CONTRIBUTING.md,LICENSE
---

# Repo Docs Publisher

Reads an existing repository and prepares the documentation needed to publish it as a public GitHub repo: `README.md`, `HOW_TO_USE.md`, `CONTRIBUTING.md`, `LICENSE`, and — based on user confirmation — `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`, and GitHub issue/PR templates.

## When to use

- The user wants to prepare, write, or polish docs to open-source/publish a repo, asks for a README or related docs, or wants a repo "ready for GitHub"/"public."
- This is a documentation skill for **existing** repos, not project planning — see **Related skills**.

## Input

An existing repository to document. If the user actually wants to plan a *new* project, hand off to `project-planner`; if they want source code written or refactored, hand off to `lean-coder`.

## Output

The confirmed documentation files, written as **actual files** (not chat text) — this is a file-creation task. Always considered: `README.md`, `HOW_TO_USE.md`, `CONTRIBUTING.md`, `LICENSE`. Generated only if confirmed: `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`, and `.github/` issue/PR templates.

---

## Shared conventions (defined once, referenced by every unit)

These apply to every doc-producing unit below — do not restate them per unit.

### Reference material

Each generation unit is driven by a reference file in `references/`. Use it rather than improvising structure:

| Unit produces | Reference file |
|---|---|
| Secret scan | `references/secrets-scan-checklist.md` |
| Repo scan | `references/repo-scan-checklist.md` |
| LICENSE | `references/license-summaries.md` |
| README.md | `references/readme-template.md` |
| HOW_TO_USE.md | `references/how-to-use-template.md` |
| CONTRIBUTING.md | `references/contributing-template.md` |

### Doc standards (all generated docs)

- **Never fabricate specifics** — install/build/run commands, badge data, license choice, test/lint commands must come from the scan or from explicit user confirmation. If not found, ask; do not invent.
- **Ground every doc in the actual scanned repo**, never placeholders. A doc that still contains template tokens or generic filler has not met its Self-verify.
- **Public-audience tone**: clear, welcoming to outside contributors, no internal jargon or references to private infrastructure.
- **License legal text is always the complete, canonical standard text** for the chosen license — never paraphrased, shortened, or reproduced from memory.
- **Existing docs are an update/polish pass, not a from-scratch rewrite** — preserve accurate content the scan surfaced.

### Delegation & context hygiene

The scan units (U1 secret scan, U2 repo scan) are read-heavy passes over the whole tree — push them into subagents so full repo contents never fill the primary context. They inspect the same tree and don't depend on each other, so **dispatch them in parallel in a single message**. If subagents aren't available, run both scans inline against the reference checklists, keeping the U1 gate intact. All other units (interview, license, generation) stay in the primary session.

### Overwrite / gating policy

- Do not generate any public-facing doc until **U1's secret result has been reviewed** and any finding acknowledged (see U1 STOP GATE).
- Confirm the **full file list** with the user before generating (U3 STOP GATE) — the user may not want every optional doc.

---

## Workflow units

### Unit U1 — Secret / sensitive-info scan (ALWAYS FIRST)

- **Goal/scope**: since the target is a **public** repo, find any material that must not be published, before any doc is drafted.
- **Inputs**: the repo tree; `references/secrets-scan-checklist.md`.
- **Do**: delegate to a subagent (dispatched in parallel with U2) briefed with the checklist. Search for `.env` files, hardcoded API keys/tokens/passwords, private keys/certs, private URLs or internal hostnames, credentials in config files, and `.gitignore` gaps (no `.gitignore`, or one not covering common secret patterns). Distinguish material present only in the **working tree** (a `.gitignore` fix + removal suffices) from material **already committed to git history** (recommend history-rewriting via `git filter-repo` or BFG **plus credential rotation**, since deleting in a new commit leaves it recoverable). Report exactly what was found and where (`file:line`), or confirm the scan was clean.
- **Self-verify**: confirm the scan actually ran against the checklist and produced either a clean confirmation or a concrete `file:line` finding list — not an assumption.
- **STOP GATE (hand back)**: **if anything is found, stop.** Surface the findings (`file:line`) clearly, recommend removal/rotation and history-scrubbing for anything already committed, and **do not proceed to draft any public-facing docs or call the repo "ready for public" until the user acknowledges.** → Hand control back to the user/orchestrator. If clean, note it briefly and proceed.
- **Report contract**: `secret scan: <CLEAN | N findings> | findings: <file:line list or none> | committed-to-history: <yes/no/n-a> | gate: <passed | BLOCKED awaiting acknowledgement>`.

### Unit U2 — Scan the repo

- **Goal/scope**: build an accurate picture of the repo so no doc contains fabricated specifics.
- **Inputs**: the repo tree; `references/repo-scan-checklist.md`.
- **Do**: delegate to a subagent (dispatched in parallel with U1) briefed with the checklist. Report back:
  - Language(s), framework(s), package manager, and dependencies from manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.).
  - Test runner, linter/formatter, CI config (`.github/workflows/`) if present — these inform badges and CONTRIBUTING.
  - Existing docs (`README.md`, `LICENSE`, etc.) with their current content surfaced, so an update/polish pass preserves accurate parts.
  - Inferred project purpose, entry points, install/build/run commands, directory layout.
  - Whether a `LICENSE` file exists (reused in U4 if so).
  - **Monorepo vs single package**: detect multiple manifests under `packages/`/`apps/`, workspaces, `go.work`, Cargo workspace, etc. If a monorepo, flag it so U3 can ask about root-level vs per-package docs and the primary package.
- **Self-verify**: confirm each checklist area is answered (or explicitly marked "none found"), and that reported commands/badges trace to real files — no invented specifics.
- **Report contract**: `repo scan: complete | stack: <langs/frameworks/pm> | tests/lint/CI: <found or none> | existing docs: <list> | LICENSE present: <yes/no> | monorepo: <yes/no>`.

### Unit U3 — Interview & confirm file list

- **Goal/scope**: resolve only what scanning couldn't determine, and lock the exact set of files to generate.
- **Inputs**: U1 result (must be passed/acknowledged), U2 scan results.
- **Do**: ask the user **only** for gaps scanning left open — don't re-ask anything evident from the repo. Typical gaps: project name/tagline (if not obvious from manifest/repo name), target audience/use case (tone), whether issue/PR templates are wanted, and any scan ambiguity (multiple entry points, unclear install). If U2 flagged a monorepo, ask whether the user wants **root-level** docs, **per-package** docs, or both, and which package is primary/published — default to root-level docs plus a short "Packages" section unless they ask otherwise. Keep it to a single batch of questions.
- **Self-verify**: confirm the U1 gate is cleared and every open ambiguity has an answer or a stated default.
- **STOP GATE (hand back)**: present the **full file list to generate** (README, HOW_TO_USE, CONTRIBUTING, LICENSE, plus any of CODE_OF_CONDUCT/SECURITY/CHANGELOG/templates) and **confirm it before generating anything.** → Hand control back for the file-list decision.
- **Report contract**: `gaps resolved: <list> | monorepo scope: <root/per-package/both/n-a> | confirmed file list: <files> | awaiting: file-list confirmation`.

### Unit U4 — Generate LICENSE

- **Goal/scope**: ensure a correct, canonical license is in place.
- **Inputs**: U2's LICENSE-present flag + manifest `license` field; `references/license-summaries.md`.
- **Do**: if `LICENSE` already exists, reuse it as-is — **unless** the scan shows inconsistency (manifest `license` names a different license, stale copyright year/holder). In that case flag the mismatch and ask which is correct before proceeding, rather than silently trusting either. If no `LICENSE` exists, summarize the common options (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause) and their practical implications using `references/license-summaries.md`, let the user pick, then generate the **full, complete standard text** for the chosen license — never paraphrase or shorten.
- **Self-verify**: confirm `LICENSE` exists with complete canonical text (not a summary/excerpt) and no manifest/file mismatch remains unresolved.
- **Report contract**: `LICENSE: <reused as-is | generated <SPDX-id>> | mismatch: <none | resolved: <which>>`.

### Unit U5 — Generate README.md

- **Goal/scope**: produce the quick-start + overview entry doc.
- **Inputs**: U2 scan results; `references/readme-template.md`.
- **Do**: generate `README.md` from the template. Standard sections: title/tagline, badges, description, table of contents (for longer READMEs), installation, quick usage example, link to `HOW_TO_USE.md` for detailed usage, contributing link (to `CONTRIBUTING.md`), license section (referencing `LICENSE`). Propose **only** badges the U2 scan supports (build status if CI found, license badge, package-registry version if published, language/version badges) — never fabricate a badge for something absent (no build badge without CI).
- **Self-verify**: confirm `README.md` exists with the required sections, reflects the actual scanned repo (real commands, real badges), contains no placeholders, and links to HOW_TO_USE/CONTRIBUTING/LICENSE rather than duplicating them.
- **Report contract**: `README.md: written | sections: <present> | badges: <only-detected list> | placeholders: none`.

### Unit U6 — Generate HOW_TO_USE.md

- **Goal/scope**: produce the detailed usage doc, kept separate from README per project convention.
- **Inputs**: U2 scan results; `references/how-to-use-template.md`.
- **Do**: generate `HOW_TO_USE.md` from the template: full setup, configuration options, common workflows/examples, troubleshooting. Keep the split clean — README = quick start + overview, HOW_TO_USE = depth; README links here rather than duplicating this content.
- **Self-verify**: confirm `HOW_TO_USE.md` exists with real setup/config/usage grounded in the scan, no placeholders, and that it holds the depth README defers to it.
- **Report contract**: `HOW_TO_USE.md: written | covers: setup/config/workflows/troubleshooting | placeholders: none`.

### Unit U7 — Generate CONTRIBUTING.md

- **Goal/scope**: produce the contributor guide tailored to this repo's real workflow.
- **Inputs**: U2 scan results (test/lint commands, CI, git history conventions); `references/contributing-template.md`.
- **Do**: generate `CONTRIBUTING.md` from the template, tailored to what U2 detected — reference the **actual** test command, linter, and branch/PR conventions (`npm test`, `pytest`, `make lint`, etc.) rather than generic placeholders. Cover: dev-environment setup, running tests/lint, branch/commit conventions if evident from git history, and the PR process.
- **Self-verify**: confirm `CONTRIBUTING.md` exists and its commands/conventions match the real repo — no generic placeholder commands.
- **Report contract**: `CONTRIBUTING.md: written | test/lint cmds: <actual> | conventions: <from history or none> | placeholders: none`.

### Unit U8 — Generate optional extras (only what was confirmed)

- **Goal/scope**: generate the community/meta files the user confirmed in U3.
- **Inputs**: U3's confirmed file list; U2 scan results (git tags/releases for CHANGELOG).
- **Do**: generate **only** the confirmed items:
  - `CODE_OF_CONDUCT.md` — standard Contributor Covenant text.
  - `SECURITY.md` — how to report vulnerabilities.
  - `CHANGELOG.md` — seed from git tags/releases if any exist, else a starter template.
  - GitHub issue templates and a PR template under `.github/`.
- **Self-verify**: confirm each confirmed file exists and nothing **unconfirmed** was generated; CHANGELOG reflects real tags if any were found.
- **Report contract**: `optional extras: <files written or none> | unconfirmed files generated: none`.

### Unit U9 — Wrap up & final gate

- **Goal/scope**: confirm the repo is safe to call publishable and summarize what was produced.
- **Inputs**: U1 result, all generated files.
- **Do**: if U1 flagged secrets, **re-confirm remediation** (removed/rotated, history scrubbed if committed) before treating the repo as ready. If the user chose to proceed without remediating, state **explicitly** in the summary that the repo still contains the flagged material and must not be made public until resolved — never let a flagged finding silently pass to a "ready to publish" state. Summarize all files created and remind the user that U1 only checked what this skill inspected — a full git-history audit is their responsibility if the repo has commit history predating this pass.
- **Self-verify**: confirm every confirmed file was written to disk and the secret-remediation status is stated honestly (ready vs. still-blocked).
- **STOP GATE (hand back, conditional)**: if U1 findings were **not** remediated, do **not** declare the repo "ready for public" — surface the outstanding blocker and hand back. → Hand control back for remediation.
- **Report contract**: `files written: <list> | secret status: <clean | remediated | STILL BLOCKED: <what>> | public-ready: <yes | no — blocked>`.

---

## Related skills

- **`project-planner`** — for planning a *new* project from an idea (spec/design/roadmap/backlog). This skill documents an *existing* repo; hand off if the user actually wants to plan.
- **`lean-coder`** — for writing or refactoring the repo's code. This skill only writes documentation, never source code.
- **`ui-ux-designer`** — for designing an app's UI/UX. Unrelated to publishing docs.
