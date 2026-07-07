import os

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _force_driver_psycopg(url: str) -> str:
    """Accepte une URL 'postgresql://' / 'postgres://' et impose le driver psycopg."""
    for prefix in ("postgresql://", "postgres://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    return url


class Settings(BaseSettings):
    """Configuration de l'application, chargée depuis les variables d'environnement / .env."""

    # URL de connexion PostgreSQL, ex: postgresql+psycopg://user:password@host:5432/db
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/congel"

    # Clever Cloud fournit automatiquement cette variable quand l'add-on PostgreSQL est lié.
    postgresql_addon_uri: str | None = None

    app_name: str = "Congel API"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @model_validator(mode="after")
    def resolve_database_url(self) -> "Settings":
        # Si l'add-on Clever Cloud est lié et que DATABASE_URL n'est pas fixé explicitement,
        # on utilise l'URI de l'add-on.
        if self.postgresql_addon_uri and not os.getenv("DATABASE_URL"):
            self.database_url = self.postgresql_addon_uri
        self.database_url = _force_driver_psycopg(self.database_url)
        return self


settings = Settings()
