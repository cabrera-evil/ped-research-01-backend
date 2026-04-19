# Development

## Tooling

- Python 3.11 via `mise`
- Ruff for lint/format
- mypy for type checking
- pytest for testing
- pre-commit hooks
- Commitizen for conventional commits

## Common commands

```bash
mise install
mise run install-dev
mise run dev
mise run lint
mise run format
mise run test
```

Equivalent `make` targets are available.

## Testing focus for new features

- Add happy-path tests and validation/error tests
- Keep endpoint auth behavior explicit in tests
- Keep coverage healthy for touched modules

## Git hooks

```bash
make pre-commit-install
make pre-commit
```
