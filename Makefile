.PHONY: help install install-dev setup run start start-multi test lint format pre-commit-install pre-commit commit docker-build docker-up docker-down docker-logs clean

help:
	@echo "Available commands:"
	@echo "  make setup              - Setup development environment"
	@echo "  make install            - Install dependencies"
	@echo "  make install-dev        - Install development dependencies"
	@echo "  make run                - Run development server (auto-reload)"
	@echo "  make start              - Run production server (single worker)"
	@echo "  make start-multi        - Run production server (multi-worker)"
	@echo "  make test               - Run tests"
	@echo "  make lint               - Run linting"
	@echo "  make format             - Format code"
	@echo "  make pre-commit-install - Install pre-commit hooks"
	@echo "  make pre-commit         - Run pre-commit on all files"
	@echo "  make commit             - Create a semantic commit"
	@echo "  make docker-build       - Build Docker image"
	@echo "  make docker-up          - Start Docker containers"
	@echo "  make docker-down        - Stop Docker containers"
	@echo "  make docker-logs        - View Docker container logs"
	@echo "  make clean              - Clean cache and temporary files"

setup:
	@echo "Setting up development environment..."
	python -m venv .venv
	@echo "Activate with: source .venv/bin/activate (Linux/Mac) or .venv\\Scripts\\activate (Windows)"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

start:
	uvicorn app.main:app --host $${API_HOST:-0.0.0.0} --port $${API_PORT:-8000} --timeout-keep-alive $${WORKER_TIMEOUT:-120}

start-multi:
	uvicorn app.main:app --host $${API_HOST:-0.0.0.0} --port $${API_PORT:-8000} --workers $${WORKERS:-4} --timeout-keep-alive $${WORKER_TIMEOUT:-120}

test:
	pytest tests/ -v

lint:
	ruff check app/ tests/ scripts/

format:
	ruff format app/ tests/ scripts/

pre-commit-install:
	pre-commit install
	pre-commit install --hook-type commit-msg

pre-commit:
	pre-commit run --all-files

commit:
	cz commit

docker-build:
	docker build -t cabreraevil/python-template:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf build/ dist/ htmlcov/ .coverage
