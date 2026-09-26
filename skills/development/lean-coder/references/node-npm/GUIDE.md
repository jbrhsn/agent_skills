# Node.js, npm, and TypeScript

Use the target project's declared Node version, package manager, manifest, lockfile, and workspace configuration. Node has no `.venv` equivalent: project-local dependencies and package-manager scripts provide the execution boundary. Prefer an existing `npm run <script>` command because npm runs it from the package root with local `node_modules/.bin` available. Preserve pnpm, Yarn, Bun, or another established package manager instead of switching it to npm.

Before executing newly authored Node or TypeScript automation, save it under the target project's `.temp/` with an explicit `.mjs`, `.cjs`, `.js`, or supported TypeScript extension, then run that file through the project's established toolchain. Do not use `node -e`, `node --eval`, stdin, or a shell command string for generated program source. Use `.mjs` or `.cjs` where the package module type would otherwise be ambiguous.

Use project-local tools and pinned dependencies. Do not rely on a globally installed binary or let `npx`/`npm exec` fetch an undeclared package for routine work. `npm exec --no -- <tool>` is suitable when the tool is already installed locally. Use `npm ci` only for a deliberate clean install with a compatible lockfile; it removes `node_modules` and fails when the manifest and lockfile disagree. Use the existing install command for intentional dependency changes or first-time setup.

For scripts that call Python, launch Python with `uv run --python PROJECT/.venv/bin/python python SCRIPT.py`; do not call a configured interpreter directly as a fallback. Pass process arguments as arrays rather than composing shell strings, keep the target working directory explicit, and propagate nonzero exit status.
