# Quickstart

## 1) Setup

```bash
cp .env.example .env
make setup
source .venv/bin/activate
make install-dev
```

## 2) Run API

```bash
make run
```

- App root: http://localhost:8000/
- Swagger docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/v1/health

## 3) Verify Assignment Demo (`c`)

Check hash table stats (includes collision evidence after startup seed):

```bash
curl -s http://localhost:8000/api/v1/inventory/stats/hash
```

Read seeded product:

```bash
curl -s http://localhost:8000/api/v1/inventory/P001
```

Create/update product:

```bash
curl -s -X POST http://localhost:8000/api/v1/inventory/ \
  -H "Content-Type: application/json" \
  -d '{"code":"P099","name":"Whiteboard Marker","price":1.99,"quantity":200,"category":"Office"}'
```

Delete product:

```bash
curl -s -X DELETE http://localhost:8000/api/v1/inventory/P099
```

## 4) Protected Endpoint Example

```bash
curl -s -H "X-API-Key: apikey" http://localhost:8000/api/v1/ping
```

## 5) Quality Checks

```bash
make format
make lint
make test
```
