from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration de l'application, chargée depuis les variables d'environnement / .env."""

    # URL de connexion PostgreSQL, ex: postgresql+psycopg://user:password@host:5432/db
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/congel"

    app_name: str = "Congel API"
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("database_url")
    @classmethod
    def force_driver_psycopg(cls, v: str) -> str:
        """Accepte une URL 'postgresql://' (ex: Clever Cloud) et impose le driver psycopg."""
        if v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+psycopg://", 1)
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+psycopg://", 1)
        return v


settings = Settings()
