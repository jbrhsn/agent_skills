# Repo scan checklist

Systematic list of what to inspect before asking the user anything, and where to look.

> Run the secrets/sensitive-info scan (`secrets-scan-checklist.md`) **before** this scan — it is the Phase 0 gate and must clear before any docs work begins.

## Language & stack detection

| Signal file | Indicates |
|---|---|
| `package.json` | Node.js/JS/TS; check `scripts`, `dependencies`, `engines` |
| `pyproject.toml` / `setup.py` / `requirements.txt` | Python; check build backend, deps |
| `go.mod` | Go; check module path, Go version |
| `Cargo.toml` | Rust; check crate deps |
| `pom.xml` / `build.gradle` | Java/Kotlin |
| `Gemfile` | Ruby |
| `composer.json` | PHP |
| `CMakeLists.txt` / `Makefile` (as primary build) | C / C++ |
| `*.csproj` / `*.sln` | .NET (C#) |
| `pubspec.yaml` | Dart / Flutter |
| `mix.exs` | Elixir |

## What to extract from each

- **Project name & description**: from manifest `name`/`description` fields, or repo directory name and top-level README/docstring if no manifest field.
- **Install command**: infer from package manager (`npm install`, `pip install -e .`, `go build`, `cargo build`, `bundle install`).
- **Run/build/test commands**: check manifest `scripts`/`Makefile`/`tox.ini`/`justfile` for existing named commands rather than guessing.
- **Entry point**: `main.py`, `main.go`, `index.js`, `src/main.rs`, or whatever `scripts.start`/`main` field points to.
- **Dependencies**: list direct dependencies only for README purposes; full list isn't needed in docs.

## CI / tooling detection

- `.github/workflows/*.yml` → CI exists, note what it runs (tests, lint, build) for both the build-status badge and for tailoring CONTRIBUTING.md.
- Linter/formatter config: `.eslintrc*`, `.prettierrc*`, `ruff.toml`/`.flake8`, `rustfmt.toml`, etc.
- Test framework: inferred from dependencies (`jest`, `pytest`, `vitest`, `go test` needs no dep, `cargo test` needs no dep) or config files.

## Existing docs check

- `README.md`, `LICENSE`/`LICENSE.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`, `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md` — note which already exist. Treat any that exist as a starting point to read and refine, not overwrite blind.

## Directory structure

Get a top-2-levels view of the repo to understand overall layout (monorepo vs single package, `src/`/`lib`/`test` conventions) — this informs both the README's structure section and CONTRIBUTING's dev-setup instructions.

## Git history signals (lightweight, optional)

- Recent commit message style can hint at conventions worth mentioning in CONTRIBUTING.md (e.g. conventional commits format) — don't over-invest here, a quick `git log --oneline -20` is enough.
- Existing tags can seed a CHANGELOG.md if one is requested.