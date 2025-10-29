from sqlalchemy import Column, String, DECIMAL, TIMESTAMP, ForeignKey, func, UUID, Enum

from src.domain.enums.transaction import TransactionStatusEnum

from src.infrastructure.persistence.database.models.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)
    transaction_hash = Column(String(66), unique=True, nullable=False)
    from_address = Column(String(255), nullable=False)
    to_address = Column(String(255), nullable=False)
    value = Column(DECIMAL(precision=100, scale=0), nullable=False)
    transaction_status = Column(Enum(TransactionStatusEnum), nullable=False)
    transaction_fee = Column(DECIMAL(precision=100, scale=0), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True)