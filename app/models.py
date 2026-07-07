from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Produit(Base):
    """Un produit stocké au congélateur."""

    __tablename__ = "produits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(120), nullable=False)
    categorie: Mapped[str | None] = mapped_column(String(60), nullable=True)
    quantite: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    date_congelation: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_peremption: Mapped[date | None] = mapped_column(Date, nullable=True)
    cree_le: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
