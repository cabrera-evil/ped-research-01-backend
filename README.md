# PED Research 01 Backend

FastAPI backend for the hash-table assignment demo (`c) Programa base ejemplo`).

## Selected Structure

- Structure: **Hash Table with separate chaining**
- Implementation: `app/core/hash_table.py`
- Hash function: `sum(ord(c) for c in key) % table_size`
- Collision strategy: each bucket stores a chain (`list[(key, value)]`)

## What This App Demonstrates

Small inventory application where product `code` is the hash key:

- Insert / update product
- Search product by code
- Delete product
- List all products
- Inspect hash internals (`load_factor`, `distribution`, `cells_with_collision`)

On startup, the app seeds products with deliberate collisions:

- `P001` and `P010` collide
- `P002` and `P020` collide

This makes collision behavior observable immediately through `/api/v1/inventory/stats/hash`.

## Run Locally

```bash
cp .env.example .env
make setup
source .venv/bin/activate
make install-dev
make run
```

Open:

- App root: <http://localhost:8000/>
- Swagger: <http://localhost:8000/docs>
- Health: <http://localhost:8000/api/v1/health>

## Run With Docker

```bash
make docker-build
make docker-up
make docker-logs
```

Stop:

```bash
make docker-down
```

## API Endpoints

- `GET /api/v1/health`
- `GET /api/v1/ping` (requires `X-API-Key`)
- `POST /api/v1/inventory/` (add/update)
- `GET /api/v1/inventory/` (list)
- `GET /api/v1/inventory/{code}` (search)
- `DELETE /api/v1/inventory/{code}` (delete)
- `GET /api/v1/inventory/stats/hash` (hash table metrics)

## Quick Demo (Evidence of Functioning)

```bash
# 1) View initial hash stats (after seeded data with collisions)
curl -s http://localhost:8000/api/v1/inventory/stats/hash

# 2) Read product by key
curl -s http://localhost:8000/api/v1/inventory/P001

# 3) Update same key (insert acts as upsert)
curl -s -X POST http://localhost:8000/api/v1/inventory/ \
  -H "Content-Type: application/json" \
  -d '{"code":"P001","name":"Laptop Stand PRO","price":49.99,"quantity":10,"category":"Electronics"}'

# 4) Delete key
curl -s -X DELETE http://localhost:8000/api/v1/inventory/P001
```

## Docs

- `docs/QUICKSTART.md`
- `docs/HASH_TABLE.md`
- `docs/DEVELOPMENT.md`
- `docs/DEPLOYMENT.md`
