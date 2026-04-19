from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        protected_namespaces=(),
        extra="ignore",
    )

    app_name: str = "Python Template API"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: Literal["development", "staging", "production"] = "development"

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"
    api_key: str = "apikey"

    log_level: str = "INFO"
    log_format: str = "json"

    workers: int = 1
    worker_timeout: int = 120


@lru_cache
def get_settings() -> Settings:
    return Settings()
