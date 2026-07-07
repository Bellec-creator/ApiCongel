from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

# Moteur de connexion à PostgreSQL.
engine = create_engine(settings.database_url, echo=settings.debug)

# Fabrique de sessions.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    """Classe de base pour tous les modèles ORM."""


def get_db() -> Generator[Session, None, None]:
    """Dépendance FastAPI : fournit une session DB et la ferme en fin de requête."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
