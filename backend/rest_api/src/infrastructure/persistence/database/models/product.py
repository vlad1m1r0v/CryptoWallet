from typing import TYPE_CHECKING

from sqlalchemy import Column, String, DECIMAL, TIMESTAMP, ForeignKey, UUID
from sqlalchemy.orm import relationship, Mapped


from src.infrastructure.persistence.database.models.base import Base


if TYPE_CHECKING:
    from src.infrastructure.persistence.database.models.wallet import Wallet

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)
    price = Column(DECIMAL(precision=100, scale=0), nullable=False)
    photo_filename = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)

    wallet: Mapped["Wallet"] = relationship(back_populates="products")