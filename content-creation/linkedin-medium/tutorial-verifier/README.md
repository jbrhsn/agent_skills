# tutorial-verifier

Turns a tutorial draft that contains code into a Medium-ready article whose code blocks have actually been **run and verified**, or, when execution is impossible, **statically validated** and clearly labeled as such. Extracts Python, JS/Node, and shell blocks, runs them in an isolated working directory, falls back to static syntax checks when no runtime exists, and never claims code ran when it did not.

---

## Trigger phrases

| Input | Example |
|---|---|
| Verify tutorial code | "verify the code in this tutorial", "run these code blocks", "make sure the snippets work" |
| Format for Medium | "format this tutorial for Medium", "turn this draft into a Medium article with verified code" |
| Point at a draft | a draft under `drafts/` containing Python, JS/Node, or shell code |

Do **not** use it for pure prose articles with no executable code, for editing/formatting that does not involve running code (use `editorial-reviewer`), or for rendering carousel images (use `carousel-builder`). Upstream drafting is `seed-expander` → `draft-builder` → {`linkedin-writer`, `medium-writer`}.

---

## What it does

- **Extracts every fenced code block** from the draft, recording its language tag (```python / ```js / ```bash), inferring and noting the language when untagged.
- **Handles incremental multi-block tutorials.** When block 2 depends on block 1's variables/files/installed packages, it concatenates the dependent blocks in order into one snippet and verifies them as a unit, instead of producing false failures from fresh isolated envs, then maps captured output back to each block. Genuinely independent blocks are verified separately.
- **Builds a verification plan** per block (execute or static? which env? which deps? any dangerous shell flagged for refusal).
- **Runs each block in a throwaway temp directory** via `scripts/verify.py`, capturing stdout/stderr/exit code and whether it executed or was statically validated.
- **Falls back to static validation** (`compile()`, `node --check`, `bash -n`) when a runtime or setup is unavailable, or when a shell snippet is refused, never guessing that code works.
- **Formats a Medium article** with numbered steps and language-tagged blocks, each labeled `verified ✓`, `statically validated ⚠`, or `not verified, no runtime ⏭`, including captured output for executed blocks. Before writing the article, it runs a voice-compliance gate on the PROSE only (never code blocks): scans against the voice-tone profile's avoided words/phrases and punctuation, auto-fixes mechanical violations, and flags judgment calls.

---

## Review-first flow

Never auto-runs end-to-end. There are two mandatory stop points:

1. **Before executing anything.** Show the extracted code blocks with detected language, and the verification plan (env per block, deps to install, any shell snippets flagged dangerous). Wait for approval.
2. **Before writing the final article.** Show the verification RESULTS (pass/fail/unknown, executed vs. statically validated, captured output) and wait for approval to write into `medium/`.

---

## Security

**This is NOT a sandbox.** The isolated temp directory only isolates the **working directory and `HOME`**. It does **not** restrict network access, environment variables, or the rest of the filesystem.

- The dangerous-command scan is a best-effort **denylist** and is trivially bypassable (aliases, variable indirection, `eval`, encoding, base64, encoded args). It is **not** a security boundary.
- **Never run untrusted third-party code** through this skill. It is meant for verifying the user's **own** tutorial snippets only.
- If a snippet looks untrusted or obfuscated, the skill **refuses** to execute and validates statically instead.
- All execution happens in a throwaway temp directory: no global installs, no touching the user's system, no writes outside the temp sandbox.

The shell denylist refuses (and does `bash -n` instead) on: recursive/forced `rm`, `dd`/`mkfs`/`fdisk`/`mkswap`, `sudo`/`su`/recursive `chmod -R`/`chown -R`, `curl ... | sh` / `wget ... | sh` remote-exec pipes, `eval`, fork bombs, `shutdown`/`reboot`/`halt`, writes to raw devices (`> /dev/sd*`) or into system dirs (`/etc`, `/bin`, `/usr`, `/boot`, etc.), absolute-path writes outside `/tmp`, and `iptables`/`crontab` modifications.

---

## scripts/verify.py

Handles env setup, execution, safety scanning, and static fallback. Standard-library Python only.

```bash
python3 scripts/verify.py --help

# execute a python snippet in an isolated uv/venv (with deps)
python3 scripts/verify.py --lang python --file block1.py --requirement requests

# node snippet in a temp project
python3 scripts/verify.py --lang js --file block2.js --requirement left-pad

# shell snippet (auto-refuses dangerous commands, does bash -n instead)
python3 scripts/verify.py --lang shell --file block3.sh

# force static-only, or get machine-readable output
python3 scripts/verify.py --lang python --file block1.py --static-only
python3 scripts/verify.py --lang shell --file block3.sh --json
```

### Per-language behavior

| Language | Execution | Static fallback |
|---|---|---|
| **python** | Isolated venv: `uv venv` preferred, else `python3 -m venv`; deps installed only inside the venv (`uv pip install --python …` or the venv's `pip`) | `compile()` syntax check when no venv toolchain works or a dependency install fails |
| **js** | Temp node project: `npm init -y`, optional `npm install <pkg>`, then `node snippet.js` | `node --check`; if `node` itself is missing, static validation is not possible (reported as unknown) |
| **shell** | Sandboxed temp cwd with `HOME` pointed at the sandbox; runs only after the dangerous-command scan passes | `bash -n`; a snippet matching the denylist is REFUSED and only `bash -n` is run |

The `--requirement` flag is repeatable and is ignored for shell. Output streams are capped at 256 KB each; each execution is bounded by `--timeout` (default 120s).

### Status, mode labels, and exit codes

`verify.py` prints `STATUS: PASS|FAIL|UNKNOWN` plus a **mode** that maps to the final article label:

| Mode (internal) | Reported label | Meaning |
|---|---|---|
| `executed` | `verified` | The snippet actually ran and passed |
| `static` | `statically validated` | Syntax-checked only (`compile()` / `node --check` / `bash -n`), not executed |
| `refused` | `REFUSED` | Matched the dangerous-command denylist; not executed |
| `skipped` | `SKIPPED (no runtime)` | No runtime available to execute or statically check |

| Exit code | Status | Meaning |
|---|---|---|
| `0` | pass | Executed OR statically validated cleanly |
| `1` | fail | Runtime error, syntax error, refused, etc. |
| `2` | usage | Usage / internal error (e.g. snippet file not found) |
| `3` | unknown | Could not verify: no runtime/setup available; neither executed nor statically checkable |

**`UNKNOWN` is not a failure.** It means "could not verify here." Surface it honestly (label the block `not verified, no runtime ⏭`) rather than claiming the code works.

---

## Final Medium formatting

Each step is numbered and in original tutorial order, keeps its language tag, and is labeled by verification mode:

```
### Step N: <what this does>

<short prose, in the project's voice/tone if voice-tone/ exists>

​```python
# verified ✓
<code>
​```

<expected output, from the captured run>
```

Never label a block `verified` unless it actually ran. Include captured output for executed blocks so readers see real results. Before writing, the voice-compliance gate runs on the PROSE only (never code blocks): it scans against the voice-tone profile's avoided words/phrases and punctuation, auto-fixes mechanical violations, and flags judgment calls.

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Tutorial draft | Yes | A draft (usually under `drafts/`) containing Python, JS/Node, or shell code blocks |
| `drafts/` folder | Yes | Must already exist (cwd-relative); the skill asks rather than creating it |
| `medium/` folder | For output | Destination for the finished article; asked about before creation |
| `voice-tone/` folder | Optional | Used only for the prose around code; asked about if expected but missing |
| Dependencies (`--requirement`) | Optional | Packages to install inside the isolated env per block (ignored for shell) |
| Runtimes (`uv`/`python3`, `node`/`npm`, `bash`) | Optional | Used for execution when present; absence triggers static validation or unknown |

---

## Outputs

- **Extracted blocks + verification plan** shown at the first stop point.
- **Verification results** (pass/fail/unknown, executed vs. statically validated, captured output) shown at the second stop point.
- **A Medium-ready article** under `medium/`: numbered steps, language-tagged code blocks each labeled `verified ✓`, `statically validated ⚠`, or `not verified, no runtime ⏭`, with captured output for executed blocks.

---

## Limitations

- **Not a security sandbox.** Only the working directory and `HOME` are isolated, not network, environment, or the wider filesystem. Never run untrusted code through it.
- **The dangerous-command scan is a bypassable denylist**, not a boundary; obfuscated snippets should be refused and validated statically.
- **Static validation is syntax-only.** It confirms the code parses, not that it behaves correctly. `UNKNOWN`/`statically validated` blocks are labeled honestly and never presented as `verified`.
- **Depends on available runtimes.** Missing `uv`/`python3`, `node`/`npm`, or `bash` downgrades a block to static validation or unknown.
- **Not fully automatic.** Stops for approval before executing anything and again before writing the final article.
- **Never auto-creates folders or overwrites files.** Asks when `drafts/`/`medium/`/`voice-tone/` are missing, and offers overwrite / `-v2` variant / new name when a target exists.
- **Tracker updates are prompted, not automatic.** If a `content-log.md`/`content-log.json` tracker exists, the skill asks in one line whether to update it after writing; a missing tracker never blocks the skill.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global: available in all projects (Linux/macOS)
cp -r content-creation/linkedin-medium/tutorial-verifier ~/.config/opencode/skills/

# Per-project only
cp -r content-creation/linkedin-medium/tutorial-verifier .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse content-creation\linkedin-medium\tutorial-verifier "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/tutorial-verifier.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before the verification task |

---

## Companion skills

Part of the LinkedIn/Medium content suite. Pipeline order: `seed-expander` → `draft-builder` → {`linkedin-writer`, `medium-writer`} → {`carousel-builder`, `medium-imager`, `tutorial-verifier`} → `editorial-reviewer`, with `voice-profiler` and `content-tracker` as cross-cutting support.

- **`seed-expander`**: expands a raw idea into an outline/angle
- **`draft-builder`**: turns the outline into the full tutorial draft this skill verifies
- **`linkedin-writer`** / **`medium-writer`**: turn the draft into platform-specific posts/articles upstream
- **`carousel-builder`**: sibling downstream step; renders carousel slide images
- **`editorial-reviewer`**: final editorial pass on the surrounding prose
- **`voice-profiler`**: builds the `voice-tone/` guidance used for prose around code
- **`content-tracker`**: maintains the `content-log` status (`idea` → `drafted` → `reviewed` → `posted` → `archived`)
