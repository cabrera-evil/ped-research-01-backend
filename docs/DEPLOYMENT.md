# Deployment

## Docker Build

```bash
make docker-build
```

Manual equivalent:

```bash
docker build -t cabreraevil/python-template:latest .
```

## Docker Compose Up/Down

```bash
make docker-up
make docker-logs
make docker-down
```

The service exposes `8000` and includes a healthcheck to `/api/v1/health`.

## Single Container Run

```bash
docker run -d \
  --name python-template \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  cabreraevil/python-template:latest
```

## Required Environment Variables

- `APP_NAME`
- `APP_VERSION`
- `ENVIRONMENT`
- `API_HOST`
- `API_PORT`
- `API_PREFIX`
- `API_KEY`
- `LOG_LEVEL`
- `LOG_FORMAT`
- `WORKERS`
- `WORKER_TIMEOUT`

Use `.env.example` as baseline values.

## Operational Notes

- Inventory data is in-memory; container/app restart resets data.
- Startup seeds sample products to show hash collisions immediately.
- Keep `API_KEY` private and rotate it for shared environments.
