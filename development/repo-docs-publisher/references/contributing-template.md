# CONTRIBUTING.md template

```markdown
# Contributing to <Project Name>

Thanks for considering contributing! Here's how to get set up.

## Development Setup

1. Fork and clone the repo
2. Install dependencies:
   \`\`\`bash
   <actual install command>
   \`\`\`
3. <any other setup steps detected — env vars needed, services to run locally, etc.>

## Running Tests

\`\`\`bash
<actual test command detected, e.g. npm test / pytest / go test ./...>
\`\`\`

## Code Style

<Actual linter/formatter detected, e.g. "This project uses ESLint and Prettier — run `npm run lint` before submitting.">

## Making a Pull Request

1. Create a branch: `git checkout -b <type>/<short-description>` <!-- match actual branch naming convention if evident from git history, else suggest a sensible default like feature/, fix/ -->
2. Make your changes with clear, focused commits <!-- mention conventional commits format only if evident from git log -->
3. Ensure tests pass and linting is clean
4. Open a PR describing what changed and why

## Reporting Bugs / Requesting Features

Please open a GitHub issue <!-- reference issue templates here if Phase 7 generated them --> with as much detail as possible: steps to reproduce, expected vs actual behavior, environment details.

## Questions

<Where to ask — GitHub Discussions, an issue, etc.>

<!-- Include only if CODE_OF_CONDUCT.md was generated (Phase 7) -->
## Code of Conduct

This project follows a [Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you're expected to uphold it.
```

## Guidance

- Every command in this file must be one actually found in the repo (manifest scripts, Makefile targets, etc.) — never invent a plausible-sounding command that wasn't verified.
- If branch/commit conventions aren't evident from git history, propose a simple sensible default rather than fabricating a convention that doesn't exist, and note it's a suggestion.
- Keep tone welcoming — this is often a new contributor's first interaction with the project.