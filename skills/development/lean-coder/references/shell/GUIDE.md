# Shell automation

Save newly authored shell automation under the target project's `.temp/` and execute the saved file with the matching interpreter: `bash PROJECT/.temp/task.sh` for Bash syntax or `sh PROJECT/.temp/task.sh` for POSIX shell. Do not submit generated shell programs with heredocs, `bash -c`, `sh -c`, or an assembled command string. Reuse existing project scripts first and promote maintained tooling into the target project's `scripts/` directory.

Begin a Bash script with `#!/usr/bin/env bash` and use `set -euo pipefail` when its failure behavior suits the workflow. `set -e` has exceptions, so explicitly check expected failures and cleanup boundaries. Use `bash -n` before execution and ShellCheck when it is available and relevant. For POSIX shell, avoid Bash-only syntax and validate with `sh -n`.

Quote paths and variables, pass data as arguments or files, and keep the working directory explicit. Avoid `eval`, unvalidated glob expansion, and interpolating untrusted values into commands. Use an existing project environment or tool wrapper for subprocesses; Python commands use the target `.venv` through `uv run`, while Node commands use the project's package-manager scripts or local binaries.
