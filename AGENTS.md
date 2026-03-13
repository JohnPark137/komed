# Repository Guidelines

## Project Structure & Module Organization
This repository is currently unstructured: there are no source files, test suites, or build configuration in the root yet. Keep the top level minimal and add directories intentionally as the project grows.

Recommended layout for new work:
- `src/` for application or library code
- `tests/` for automated tests that mirror `src/`
- `assets/` for static files such as images or fixtures
- `docs/` for design notes, architecture decisions, or usage guides

Example: place a feature module at `src/<feature>/` and its tests at `tests/<feature>/`.

## Build, Test, and Development Commands
No build, run, lint, or test commands are configured at the moment. When adding a toolchain, document the primary commands in this file and in the project README.

Until then, contributors should keep setup explicit and reproducible. Prefer adding scripts through the project’s package manager or task runner rather than relying on ad hoc local commands.

Examples to add once tooling exists:
- `npm run dev` for local development
- `npm test` or `pytest` for automated tests
- `npm run lint` or `ruff check .` for static analysis

## Coding Style & Naming Conventions
Use consistent, readable defaults:
- Indent with 2 spaces for JSON, YAML, and frontend code; use 4 spaces for Python if it is introduced.
- Use lowercase, hyphenated names for directories and files unless the language ecosystem prefers otherwise.
- Name tests after the unit under test, for example `tests/auth/test_login.py` or `tests/login.spec.ts`.

Adopt a formatter and linter with the first production code added, and commit their config with the same change.

## Testing Guidelines
There is no test framework configured yet. Any non-trivial feature should add automated tests alongside the implementation and document how to run them.

Prefer fast, deterministic tests. Keep test data local to the repository and avoid hidden external dependencies.

## Commit & Pull Request Guidelines
There is no existing Git history in this directory, so no repository-specific commit convention can be inferred yet. Use short, imperative commit messages such as `Add API client scaffold` or `Create login form tests`.

Pull requests should include:
- A brief description of the change and its purpose
- Linked issue or task reference when available
- Test evidence, or a clear note when tests are not yet applicable
- Screenshots or sample output for UI or CLI changes
