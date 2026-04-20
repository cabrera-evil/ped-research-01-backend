# Development

## Architecture

- `app/core/hash_table.py`: hash table (selected structure)
- `app/modules/inventory/`: assignment demo business module
- `app/modules/system/`: health + protected ping endpoints
- `app/api/v1/router.py`: API router composition
- `app/main.py`: app bootstrap and seed data with intentional collisions

## Hash Table Rules in This Project

- Storage is in-memory only (module-level singleton in `inventory/service.py`)
- Product `code` is the hash key
- `POST /api/v1/inventory/` performs upsert behavior
- Collision handling is separate chaining (bucket lists)

## Tooling

- Python 3.11
- Ruff (format + lint)
- mypy
- pytest
- pre-commit
- Commitizen

## Common Commands

```bash
make install-dev
make run
make format
make lint
make test
make pre-commit
```

## Development Notes

- Seed data is loaded at startup in `lifespan` to evidence collisions.
- Hash stats endpoint is the main observability tool for table behavior.
- Because storage is in memory, data resets when the process restarts.
