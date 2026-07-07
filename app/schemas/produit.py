from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class ProduitBase(BaseModel):
    nom: str
    categorie: str | None = None
    quantite: int = 1
    date_congelation: date | None = None
    date_peremption: date | None = None


class ProduitCreate(ProduitBase):
    """Données attendues pour créer un produit."""


class ProduitUpdate(BaseModel):
    """Tous les champs optionnels pour une mise à jour partielle."""

    nom: str | None = None
    categorie: str | None = None
    quantite: int | None = None
    date_congelation: date | None = None
    date_peremption: date | None = None


class ProduitRead(ProduitBase):
    """Données renvoyées par l'API."""

    id: int
    cree_le: datetime

    model_config = ConfigDict(from_attributes=True)
