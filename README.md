# python-template

Reusable Python boilerplate for API and script projects.

## What this template includes

- FastAPI starter with modular routing
- Public health endpoint and protected sample endpoint (`X-API-Key`)
- Generic CLI script scaffold in `scripts/template_cli.py`
- Docker + Docker Compose setup
- `mise` tasks and `Makefile` commands
- Ruff, mypy, pytest, pre-commit, Commitizen
- Minimal docs for quickstart, development, and deployment

## Project structure

```text
python-template/
├── app/
│   ├── main.py
│   ├── api/v1/router.py
│   ├── core/                 # config + security
│   ├── modules/system/       # starter endpoints
│   ├── shared/               # shared schemas
│   └── utils/                # logging
├── scripts/template_cli.py
├── tests/test_api.py
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── mise.toml
└── docs/
```

## Quick start

```bash
cp .env.example .env
make install-dev
make run
```

Then open:

- Swagger UI: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health

Protected endpoint example:

```bash
curl -H "X-API-Key: apikey" http://localhost:8000/api/v1/ping
```

## Useful commands

```bash
make format
make lint
make test
make docker-build
make docker-up
```

## Notes

- Default Docker image/tag: `cabreraevil/python-template:latest`
- Existing publish workflow under `.github/workflows/publish-dockerhub.yaml` is intentionally kept as-is.
