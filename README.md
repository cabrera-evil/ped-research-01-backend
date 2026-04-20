# HashStock Backend

Backend for the PED Research 01 inventory app.  
Built with FastAPI and a custom hash-table storage layer to demonstrate the selected structure from the assignment (`c) Programa base ejemplo`).

## What this app does

- Lets users create/update/delete inventory products.
- Stores products in a custom hash table keyed by product code.
- Exposes hash table stats for visualization and analysis.
- Seeds initial records with deliberate collisions to evidence collision handling.

## Selected Structure

- **Hash Table with separate chaining**
- Implementation: `app/core/hash_table.py`
- Hash function: `sum(ord(c) for c in str(key)) % table_size`
- Collision handling: each bucket stores a list of `(key, value)` pairs

## Tech Stack

- Python 3.11
- FastAPI + Uvicorn
- Pydantic v2
- Ruff (lint/format)
- mypy
- pytest
- Docker + Docker Compose

## Requirements

- Python `>=3.11`
- `make`
- Recommended: virtual environment (`make setup`)

## Quick Start

```bash
# 1) setup environment
cp .env.example .env
make setup
source .venv/bin/activate

# 2) install dependencies
make install-dev

# 3) run API
make run
```

App runs at `http://localhost:8000`.

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI: `http://localhost:8000/api/v1/openapi.json`
- Health: `http://localhost:8000/api/v1/health`

## Environment Variables

Configured via `.env`.

| Variable         | Required                   | Default                   | Description                                                   |
| ---------------- | -------------------------- | ------------------------- | ------------------------------------------------------------- |
| `APP_NAME`       | No                         | `ped-research-01-backend` | Application name shown in OpenAPI and logs.                   |
| `APP_VERSION`    | No                         | `0.1.0`                   | API version metadata.                                         |
| `DEBUG`          | No                         | `false`                   | Enables debug/reload behavior locally.                        |
| `ENVIRONMENT`    | No                         | `development`             | Runtime environment (`development`, `staging`, `production`). |
| `API_HOST`       | No                         | `0.0.0.0`                 | Bind host for server startup.                                 |
| `API_PORT`       | No                         | `8000`                    | Bind port for server startup.                                 |
| `API_PREFIX`     | No                         | `/api/v1`                 | Prefix for API routes and OpenAPI endpoint.                   |
| `API_KEY`        | Yes (for protected routes) | `apikey`                  | Required header value for `GET /ping` as `X-API-Key`.         |
| `LOG_LEVEL`      | No                         | `INFO`                    | Logging level.                                                |
| `LOG_FORMAT`     | No                         | `json`                    | `json` or console-style logs.                                 |
| `WORKERS`        | No                         | `1`                       | Worker count for production-style startup.                    |
| `WORKER_TIMEOUT` | No                         | `120`                     | Keep-alive timeout used by startup commands.                  |

Best practices:

- Use a strong `API_KEY` outside local development.
- Keep `.env` out of version control.
- Keep `LOG_FORMAT=json` in shared/prod environments.

## Available Commands

```bash
# development
make run

# production-style local run
make start
make start-multi

# quality gates
make test
make lint
make format
make pre-commit

# docker
make docker-build
make docker-up
make docker-logs
make docker-down
```

## How It Works

### App flow

1. `app/main.py` creates the FastAPI app, middlewares, and exception handlers.
2. App startup seeds sample products with known collisions.
3. `app/api/v1/router.py` mounts system and inventory modules under `/api/v1`.
4. Inventory requests flow through routes -> controller -> service -> hash table.

### Data layer

- Storage is an in-memory singleton hash table in `app/modules/inventory/service.py`.
- `POST /inventory/` is upsert behavior (insert-or-update by key).
- `GET /inventory/stats/hash` returns:
  - `table_size`
  - `total_elements`
  - `used_cells`
  - `cells_with_collision`
  - `load_factor`
  - `distribution`

### Hashing behavior

```python
sum(ord(c) for c in str(key)) % table_size
```

Collisions are resolved via separate chaining in bucket lists.

## Backend API Contract

Base path: `/api/v1`

- `GET /health` -> health status
- `GET /ping` -> protected ping (`X-API-Key` required)
- `POST /inventory/` -> upsert `Product`
- `GET /inventory/` -> list `Product[]`
- `GET /inventory/{code}` -> product by code
- `DELETE /inventory/{code}` -> delete by code
- `GET /inventory/stats/hash` -> `HashStats`

Core models live in `app/modules/inventory/schemas.py`.

## Data Rules

- `code`: required string (hash key)
- `name`: required string
- `price`: required float
- `quantity`: required integer
- `category`: required string

## Docker

```bash
make docker-build
make docker-up
```

Stop:

```bash
make docker-down
```

Operational notes:

- Container exposes port `8000`.
- Inventory storage is in-memory and resets on restart.
- Startup seeding runs each app start.

## Project Structure

```text
app/
  api/v1/                  # route composition
  core/                    # config, security, hash table core
  modules/system/          # health + protected ping
  modules/inventory/       # inventory feature (routes, controller, service, schemas)
  shared/                  # shared response schemas
  utils/                   # logger setup
tests/
  test_api.py              # API integration tests
```
