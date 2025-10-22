from sqlalchemy import Column, String, TIMESTAMP, DECIMAL, ForeignKey, func, LargeBinary, UUID

from src.infrastructure.persistence.database.models.base import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    asset_id = Column(UUID, ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    address = Column(String(255), nullable=False, unique=True)
    private_key = Column(LargeBinary, nullable=False)
    balance = Column(DECIMAL(precision=100, scale=0), nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
