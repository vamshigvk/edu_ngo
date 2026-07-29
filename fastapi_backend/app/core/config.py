"""Application configuration loaded from environment / .env file."""
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central, typed application settings.

    Values are read from environment variables and an optional `.env` file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "FFG Mentorship API"
    app_env: str = "development"
    debug: bool = True
    api_prefix: str = "/api"

    # Database — SQLite for dev, swap DATABASE_URL to postgresql+asyncpg://... for prod.
    database_url: str = "sqlite+aiosqlite:///./ffg.db"

    # Security / JWT
    jwt_secret: str = "change-me-to-a-long-random-secret"
    jwt_algorithm: str = "HS256"
    # Sessions expire after one hour; the SPA auto-logs-out on the resulting 401.
    access_token_expire_minutes: int = 60

    # CORS
    cors_origins: str = "*"

    # Email / SMTP
    smtp_host: str = ""
    smtp_port: int = 25
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    smtp_use_tls: bool = False
    smtp_use_ssl: bool = False
    smtp_timeout_seconds: int = 10

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


settings = get_settings()
