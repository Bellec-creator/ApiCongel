from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import produits


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Crée les tables au démarrage (pratique en dev ; en prod, préférer Alembic).
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

# CORS : autorise l'app Flutter à appeler l'API. À restreindre en production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(produits.router)


@app.get("/")
def racine() -> dict[str, str]:
    return {"message": f"Bienvenue sur {settings.app_name}"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
