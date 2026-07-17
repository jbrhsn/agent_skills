---
name: tutorial-verifier
description: Use when the user asks to verify a Medium/LinkedIn tutorial's code, run code blocks, check that a tutorial draft's snippets work, or format verified code into Medium-ready blocks. Extracts code blocks (Python, JS/Node, shell) from a draft, runs them in an isolated environment, falls back to static/virtual validation when no runtime exists, and produces numbered, language-tagged Medium code blocks labeled verified or statically-validated.
---

# Tutorial Verifier

Turn a tutorial draft that contains code into a Medium-ready article whose
code blocks have actually been **run and verified**, or, when execution is
impossible, **statically validated** and clearly labeled as such.

## When to use

- The user points at a tutorial draft (usually under `drafts/`) that contains
  Python, JS/Node, or shell code and wants it checked before publishing.
- The user says things like "verify the code in this tutorial", "run these
  code blocks", "make sure the snippets work", "format this for Medium".

## When NOT to use

- Pure prose articles with no executable code.
- Editing/formatting that does not involve running or validating code.

## Folder rules (all paths are CURRENT-WORKING-DIRECTORY relative)

- Drafts live under `drafts/`.
- Finished Medium versions go under `medium/`.
- Voice/tone guidance lives under `voice-tone/` (used only for the prose
  around code).
- **If a needed folder is missing, STOP and ASK the user how to proceed.**
  Never silently create folders. If a `voice-tone/` folder is expected but
  absent, ask whether one should exist before proceeding.

## Core principle: REVIEW-FIRST, never auto-run end-to-end

There are two mandatory stop points:

1. **Before executing anything.** Show the user (a) the extracted code
   blocks with detected language, and (b) the verification plan (which env
   each will run in, any deps to install, any shell snippets flagged
   dangerous). Wait for approval.
2. **Before writing the final article.** Show the verification RESULTS
   (pass/fail/unknown, executed vs. statically validated, captured output) and
   wait for approval to write into `medium/`.

## SECURITY: this is NOT a sandbox

The isolated temp directory only isolates the working directory and `HOME`.
It does **not** restrict network access, environment variables, or the rest of
the filesystem. The dangerous-command scan is a best-effort **denylist** and is
bypassable (aliases, variable indirection, `eval`, encoding). **Never run
untrusted third-party code through this skill.** It is for verifying the
user's OWN tutorial snippets. If a snippet looks untrusted or obfuscated, refuse
and validate statically instead.

## Workflow

1. **Locate the draft.** Confirm `drafts/` exists (ask if not). Read the draft.
2. **Extract code blocks.** Pull every fenced code block. Record its language
   tag (```python / ```js / ```bash etc.). Infer language if untagged and note
   the inference.
   - **Multi-block tutorials that build state incrementally** (block 2 depends
     on block 1's variables/files/installed packages): do NOT verify each block
     in a fresh isolated env, which produces false failures. Instead concatenate
     the dependent blocks in order into ONE snippet, verify that as a unit, and
     map the captured output back to the individual blocks for display. Only
           verify blocks separately when they are genuinely independent.
   - **HTTP API tutorial snippets:** blocks that call external APIs with placeholder credentials (e.g. `YOUR_TOKEN`, `https://your-instance.azuredatabricks.net`) will return non-200 responses or non-JSON bodies at execution time. Before verification, check that: (1) the snippet handles non-200 status codes explicitly (not just `response.json()`), and (2) the snippet handles `JSONDecodeError` / non-JSON responses. If these paths are missing, add them before running `verify.py` — otherwise an authentication redirect will surface as a `FAIL` rather than the expected graceful degradation.
3. **Build the verification plan.** For each block decide: execute or static?
   which isolated env? which dependencies? Flag any shell snippet containing
   dangerous operations for refusal. **STOP. Show blocks + plan, get approval.**
4. **Verify each block** using `$SKILL_DIR/scripts/verify.py` (see below). Capture
    stdout/stderr/exit code and whether it was executed or statically validated.
5. **Review results. STOP. Show results, get approval.**
6. **Format the Medium article.** Write numbered steps with fenced,
    language-tagged code blocks, each labeled `verified ✓` or
    `statically validated ⚠`. Use `voice-tone/` guidance for the surrounding
    prose if present. Write to `medium/` (ask before creating the folder).
    **Voice compliance gate (before write).** If `voice-tone/profile.md` (or raw `voice-tone/` samples) is present, scan the prose (not code blocks) against its "Avoided Words & Phrases" and "Punctuation & Formatting Quirks". Auto-fix mechanical violations (em-dashes to periods or commas, banned punctuation) and report what changed. Flag judgment calls (hype words, AI-voice markers) for the user. Never emit a banned pattern in prose. Leave code blocks untouched. If no voice-tone exists, skip silently.

## Isolated execution procedure per language

All execution happens in a throwaway temp directory. **Never install globally,
never touch the user's system, never write outside the temp sandbox.**

### Python: isolated venv via `uv`
1. `uv venv <tmp>/.venv` (preferred). If `uv` is missing, fall back to
   `python3 -m venv <tmp>/.venv`.
2. Install any required deps ONLY inside that venv:
   `uv pip install --python <venv>/bin/python <pkg>...` (or the venv's
   `pip install` on the fallback path).
3. Run the snippet with the venv's Python; capture stdout/stderr/exit code.
4. If neither `uv` nor `python3 -m venv` works, **static validation only**
   via `compile()`.

### JS / Node: isolated temp project
1. Create a temp dir, `npm init -y`.
2. `npm install <pkg>...` for any deps, ONLY in that temp project.
3. `node snippet.js`; capture output.
4. If `node` is unavailable, **static validation only** via `node --check`
   (and if `node` itself is missing, report that static validation is not
   possible).

### Shell: sandboxed temp cwd + dangerous-command refusal
1. Run in a temp working directory with `HOME` pointed at the sandbox.
2. **Before running, scan for dangerous operations. REFUSE to execute and do
   static validation (`bash -n`) instead, warning the user, if the snippet
   contains any of:**
   - `rm -rf` / recursive-forced `rm`
   - `dd`, `mkfs`, `fdisk`, `mkswap`
   - `sudo`, `su`, recursive `chmod -R` / `chown -R`
   - `curl ... | sh` / `wget ... | sh` (remote-exec pipes)
   - fork bombs
   - `shutdown`, `reboot`, `halt`
   - writes to raw devices (`> /dev/sd*`), `/etc`, or any absolute path
     outside `/tmp` (moving into `/bin`, `/usr`, `/boot`, etc.)
   - `iptables`, `crontab` modifications
3. If safe, execute in the sandbox and capture output.

## Static / virtual validation fallback

When a runtime or setup is unavailable (or a shell snippet is refused), do NOT
guess that code works. Validate what you can:

- **Python:** `compile()` the source (syntax check) plus a manual logic review.
- **JS:** `node --check` (syntax check) plus logic review.
- **Shell:** `bash -n` (syntax check) plus logic review.

Label all such output **`statically validated ⚠ (not executed)`** in the final
article. Never claim code ran if it did not.

## Using `$SKILL_DIR/scripts/verify.py`

`$SKILL_DIR/scripts/verify.py` handles env setup, execution, safety scanning, and static
fallback. It is standard-library Python. Resolve `$SKILL_DIR` to the skill's directory
(project-local `.opencode/skills/tutorial-verifier` or global
`~/.config/opencode/skills/tutorial-verifier`).

```bash
python3 $SKILL_DIR/scripts/verify.py --help

# execute a python snippet in an isolated uv/venv (with deps)
python3 $SKILL_DIR/scripts/verify.py --lang python --file block1.py --requirement requests

# node snippet in a temp project
python3 $SKILL_DIR/scripts/verify.py --lang js --file block2.js --requirement left-pad

# shell snippet (auto-refuses dangerous commands, does bash -n instead)
python3 $SKILL_DIR/scripts/verify.py --lang shell --file block3.sh

# force static-only, or get machine-readable output
python3 $SKILL_DIR/scripts/verify.py --lang python --file block1.py --static-only
python3 $SKILL_DIR/scripts/verify.py --lang shell --file block3.sh --json
```

It prints `STATUS: PASS|FAIL|UNKNOWN` and a mode of `verified` (executed),
`statically validated`, `REFUSED`, or `SKIPPED (no runtime)`, plus captured
output. Exit codes: `0` = pass, `1` = fail/refused, `2` = usage error, `3` =
unknown (no runtime available, neither executed nor statically checkable).
Output streams are capped at 256 KB each; each execution is bounded by
`--timeout` (default 120s). Use the mode to choose the block label in the
final article. **`UNKNOWN` is not a failure.** It means "could not verify
here"; surface it honestly rather than claiming the code works.

## Final Medium formatting

For each step:

```
### Step N: <what this does>

<short prose, in the project's voice/tone if voice-tone/ exists>

​```python
# verified ✓
<code>
​```

<expected output, from the captured run>
```

- Every block keeps its language tag (` ```python `, ` ```js `, ` ```bash `).
- Label each block `verified ✓` (executed), `statically validated ⚠` (not
  executed), or `not verified, no runtime ⏭` (UNKNOWN). Never label a block
  `verified` unless it actually ran.
- Include captured output for executed blocks so readers see real results.
- Keep steps numbered and in the original tutorial order.

## Conventions

These are shared assumptions so the content skills interoperate. Each skill
still works standalone. None of these require another skill to be present.

- **Folders** (all cwd-relative): `drafts/`, `linkedin/`, `medium/`,
  `archive/`, `voice-tone/`. Never auto-create, ask the user if missing.
- **Slug**: lowercase, hyphenated, derived from the working title. Reused as
  the filename stem across skills so a piece is traceable.
- **Filenames**: `drafts/<slug>.md`, `linkedin/<slug>-<type>.md`,
  `medium/<slug>-<type>.md`, carousels at `linkedin/carousels/<slug>/`.
- **Overwrite policy**: never silently overwrite an existing file. If the
  target exists, ask the user: overwrite, write a `-v2` (then `-v3`...)
  variant, or pick a new name.
- **Status values** (if a tracker file like `content-log.md` or `content-log.json` exists at cwd): `idea` -> `drafted` -> `reviewed` -> `posted` -> `archived`. If such a tracker exists, after writing or moving a file ASK the user in one line whether to update it to the new status. Absence of a tracker must never block the skill.
