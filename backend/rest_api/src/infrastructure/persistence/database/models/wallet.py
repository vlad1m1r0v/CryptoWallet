from typing import List, TYPE_CHECKING

from sqlalchemy import Column, String, TIMESTAMP, DECIMAL, ForeignKey, func, LargeBinary, UUID
from sqlalchemy.orm import Mapped, relationship

from src.infrastructure.persistence.database.models.base import Base

if TYPE_CHECKING:
    from src.infrastructure.persistence.database.models.asset import Asset
    from src.infrastructure.persistence.database.models.user import User
    from src.infrastructure.persistence.database.models.transaction import Transaction
    from src.infrastructure.persistence.database.models.product import Product


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    asset_id = Column(UUID, ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    address = Column(String(255), nullable=False, unique=True)
    private_key = Column(LargeBinary, nullable=False)
    balance = Column(DECIMAL(precision=100, scale=0), nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    asset: Mapped["Asset"] = relationship(back_populates="wallets")
    user: Mapped["User"] = relationship(back_populates="wallets")
    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="wallet",
        uselist=True,
        cascade="all, delete-orphan",
    )
    products: Mapped[List["Product"]] = relationship(
        back_populates="wallet",
        uselist=True,
        cascade="all, delete-orphan",
    )