from collections.abc import Sequence
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  POSTGRES_USER: str
  POSTGRES_PASSWORD: str
  POSTGRES_DB: str
  POSTGRES_DB_TEST: str
  POSTGRES_PORT: int
  POSTGRES_DOCKER_PORT: int
  DATABASE_URL: str
  DATABASE_TEST_URL: str
  DATABASE_ADMIN_URL: str
  SECRET_KEY: str
  ACCESS_TOKEN_DURATION_MINUTES: int
  REFRESH_TOKEN_DURATION_DAYS: int
  CORS_ORIGINS: Sequence[str]
  SALT_ROUNDS: int
  PRODUCTION: bool
  GOOGLE_CLIENT_ID: str
  GOOGLE_CLIENT_SECRET: str
  ADMIN_EMAILS: set[str]
  BACKEND_PORT: int
  BACKEND_DOCKER_PORT: int

  model_config = SettingsConfigDict(env_file='.env')


@lru_cache  # Para que no llame cada vez el mismo objeto, lo guarda en cache
def get_settings() -> Settings:
  return Settings()  # type: ignore
