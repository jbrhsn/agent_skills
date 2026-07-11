# Secrets & sensitive-info scan checklist

Run this before generating any public-facing docs. The goal is to catch things that must not ship in a public repo.

## Files to check for

- `.env`, `.env.local`, `.env.*` (any environment files not gitignored)
- `*.pem`, `*.key`, `*.p12`, `*.pfx` (private keys/certs)
- `credentials.json`, `service-account*.json`, `secrets.yml`/`secrets.yaml`
- `.aws/credentials`, `.netrc`, `.npmrc` with auth tokens
- Database dump files, `.sql` files that might contain real data

## Patterns to grep for in tracked files

If `ripgrep` (`rg`) is available, prefer it — it's faster and its `-g` globs work as expected:

```bash
rg -niE "(api[_-]?key|secret|password|token|access[_-]?key)\s*[:=]\s*['\"][a-z0-9_-]{8,}" \
  -g '*.js' -g '*.ts' -g '*.py' -g '*.go' -g '*.rb' -g '*.java' -g '*.json' -g '*.yml' -g '*.yaml' -g '*.env' .
rg -n "AKIA[0-9A-Z]{16}" .                                  # AWS access key ID
rg -n "\-\-\-\-\-BEGIN.*PRIVATE KEY\-\-\-\-\-" .            # private key blocks
rg -n "gh[pousr]_[A-Za-z0-9]{36,}" .                        # GitHub tokens: ghp_/gho_/ghu_/ghs_/ghr_
rg -n "github_pat_[A-Za-z0-9_]{22,}" .                      # GitHub fine-grained PAT
rg -n "xox[baprs]-[A-Za-z0-9-]{10,}" .                      # Slack tokens
rg -n "sk-(proj-)?[A-Za-z0-9_-]{20,}" .                     # OpenAI-style keys (incl. sk-proj- project keys)
rg -n "AIza[0-9A-Za-z_-]{35}" .                             # Google API key
rg -n "(?i)aws_secret_access_key\s*[:=]\s*['\"][A-Za-z0-9/+=]{40}" .  # AWS secret access key
```

If only `grep` is available, note that `grep --include` does **not** perform brace expansion — `--include="*.{js,ts}"` matches nothing. Repeat `--include` per extension instead:

```bash
grep -rniE "(api[_-]?key|secret|password|token|access[_-]?key)[[:space:]]*[:=][[:space:]]*['\"][a-z0-9_-]{8,}" \
  --include=*.js --include=*.ts --include=*.py --include=*.go --include=*.rb \
  --include=*.java --include=*.json --include=*.yml --include=*.yaml --include=*.env .
grep -rnE "AKIA[0-9A-Z]{16}" .
grep -rnE "\-\-\-\-\-BEGIN.*PRIVATE KEY\-\-\-\-\-" .
grep -rnE "gh[pousr]_[A-Za-z0-9]{36,}" .
grep -rnE "github_pat_[A-Za-z0-9_]{22,}" .
grep -rnE "xox[baprs]-[A-Za-z0-9-]{10,}" .
grep -rnE "sk-(proj-)?[A-Za-z0-9_-]{20,}" .
grep -rnE "AIza[0-9A-Za-z_-]{35}" .
```

Treat matches as candidates to review, not confirmed secrets — check context (a variable named `API_KEY` reading from `process.env.API_KEY` is fine; a literal string value is the problem).

## .gitignore check

- Confirm a `.gitignore` exists.
- Confirm it covers at minimum: `.env*`, `node_modules/`, build output dirs, `*.log`, common OS files (`.DS_Store`), and any secret-file patterns relevant to the detected stack.
- If secrets matched above are **already committed** in git history (not just present in the working tree), a `.gitignore` fix alone won't remove them from history — flag this explicitly and mention history-rewriting tools (`git filter-repo`, BFG Repo-Cleaner) and credential rotation as the necessary remediation, since simply deleting the file in a new commit leaves it recoverable in history.

## Output

Report findings as a short list: file/pattern found, why it's a concern, and recommended action (add to `.gitignore` / remove and rotate / scrub history). If clean, say so briefly and move on — don't pad the response with a lengthy "no issues found" writeup.