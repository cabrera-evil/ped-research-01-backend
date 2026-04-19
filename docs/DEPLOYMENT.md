# Deployment

## Docker image

Build the image:

```bash
make docker-build
# or
docker build -t cabreraevil/python-template:latest .
```

Run the container:

```bash
docker run -d \
  --name python-template \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  cabreraevil/python-template:latest
```

## Docker Compose

```bash
make docker-up
make docker-logs
make docker-down
```

The compose service exposes port `8000` and includes a healthcheck against `/api/v1/health`.

## Environment variables

At minimum, set:

- `APP_NAME`
- `ENVIRONMENT`
- `API_HOST`
- `API_PORT`
- `API_PREFIX`
- `API_KEY`
- `LOG_LEVEL`
- `LOG_FORMAT`

Use `.env.example` as the baseline.

## Production notes

- Run behind a reverse proxy/load balancer for TLS termination.
- Rotate `API_KEY` and avoid committing secrets.
- Keep `LOG_FORMAT=json` for structured logs in centralized logging systems.
