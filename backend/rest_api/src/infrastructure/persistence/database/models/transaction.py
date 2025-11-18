from typing import TYPE_CHECKING

from sqlalchemy import Column, String, DECIMAL, TIMESTAMP, ForeignKey, UUID, Enum
from sqlalchemy.orm import relationship, Mapped

from src.domain.enums import TransactionStatusEnum

from src.infrastructure.persistence.database.models.base import Base

if TYPE_CHECKING:
    from src.infrastructure.persistence.database.models.wallet import Wallet
    from src.infrastructure.persistence.database.models.order import Order


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    from_address = Column(String(255), nullable=False)
    to_address = Column(String(255), nullable=False)
    value = Column(DECIMAL(precision=100, scale=0), nullable=False)
    transaction_status = Column(Enum(TransactionStatusEnum, native_enum=False), nullable=False)
    transaction_fee = Column(DECIMAL(precision=100, scale=0), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True)

    wallet: Mapped["Wallet"] = relationship(back_populates="transactions")
    payment_order: Mapped["Order"] = relationship(
        back_populates="payment_transaction",
        primaryjoin="Order.payment_transaction_id == Transaction.id",
        uselist=False
    )
    return_order: Mapped["Order"] = relationship(
        back_populates="return_transaction",
        primaryjoin="Order.return_transaction_id == Transaction.id",
        uselist=False
    )
