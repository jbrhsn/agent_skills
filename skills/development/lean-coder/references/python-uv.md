# Python tooling: use `uv`

For Python work, **`uv` is the default package/environment manager** — use it instead of `pip`, `pip-tools`, `virtualenv`/`venv`, `pipenv`, or `poetry` unless the project is already committed to a different tool (see below). `uv` is faster, resolves and locks deterministically, and keeps environments reproducible. Common commands:

- **Project init / deps:** `uv init` (new project), `uv add <pkg>` / `uv remove <pkg>` to manage dependencies in `pyproject.toml` (edit `pyproject.toml` + lockfile, don't hand-edit a `requirements.txt`).
- **Environment:** `uv venv` to create `.venv`; `uv sync` to install from the lock. Don't manually `python -m venv` + `pip install`.
- **Running:** `uv run <cmd>` (e.g. `uv run pytest`, `uv run python -m app`) so it executes in the project environment without manual activation.
- **Ad-hoc tools:** `uvx <tool>` (e.g. `uvx ruff check`) instead of globally installing.
- **Python versions:** `uv python install <version>` / pin via `uv python pin`.

Match the existing project, though — this is a default, not a mandate to convert:

- If a repo already uses Poetry, Pipenv, plain pip+`requirements.txt`, or Conda, **stay consistent with it** rather than introducing `uv` unasked; migrating build tooling is a scope change, so if `uv` would genuinely help, raise it as a minimal-vs-robust tradeoff and ask before switching.
- Adding a dependency is still governed by the "Writing the code" judgment in SKILL.md — reach for stdlib first; `uv` is how you add a dependency once you've decided one is warranted, not a reason to add more.
- If `uv` isn't installed in the environment and can't be used, fall back to the project's existing tool and note it, rather than blocking.
