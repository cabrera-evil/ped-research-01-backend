# Quickstart

## Setup

```bash
cp .env.example .env
make setup
source .venv/bin/activate
make install-dev
```

## Run API

```bash
make run
```

- App: http://localhost:8000/
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health

## Call protected sample endpoint

```bash
curl -H "X-API-Key: apikey" http://localhost:8000/api/v1/ping
```

## Run script scaffold

```bash
python scripts/template_cli.py --name developer
python scripts/template_cli.py --name developer --json
```

## Checks

```bash
make format
make lint
make test
```
