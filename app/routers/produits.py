from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Produit
from app.schemas.produit import ProduitCreate, ProduitRead, ProduitUpdate

router = APIRouter(prefix="/produits", tags=["produits"])


@router.get("", response_model=list[ProduitRead])
def lister_produits(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[Produit]:
    """Liste les produits (paginée)."""
    return list(db.scalars(select(Produit).offset(skip).limit(limit)).all())


@router.get("/{produit_id}", response_model=ProduitRead)
def recuperer_produit(produit_id: int, db: Session = Depends(get_db)) -> Produit:
    """Récupère un produit par son id."""
    produit = db.get(Produit, produit_id)
    if produit is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Produit introuvable")
    return produit


@router.post("", response_model=ProduitRead, status_code=status.HTTP_201_CREATED)
def creer_produit(data: ProduitCreate, db: Session = Depends(get_db)) -> Produit:
    """Crée un nouveau produit."""
    produit = Produit(**data.model_dump())
    db.add(produit)
    db.commit()
    db.refresh(produit)
    return produit


@router.patch("/{produit_id}", response_model=ProduitRead)
def modifier_produit(
    produit_id: int, data: ProduitUpdate, db: Session = Depends(get_db)
) -> Produit:
    """Met à jour partiellement un produit."""
    produit = db.get(Produit, produit_id)
    if produit is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Produit introuvable")

    for champ, valeur in data.model_dump(exclude_unset=True).items():
        setattr(produit, champ, valeur)

    db.commit()
    db.refresh(produit)
    return produit


@router.delete("/{produit_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_produit(produit_id: int, db: Session = Depends(get_db)) -> None:
    """Supprime un produit."""
    produit = db.get(Produit, produit_id)
    if produit is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Produit introuvable")
    db.delete(produit)
    db.commit()
