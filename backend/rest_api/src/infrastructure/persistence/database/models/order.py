from typing import TYPE_CHECKING

from sqlalchemy import Column, TIMESTAMP, ForeignKey, UUID, Enum
from sqlalchemy.orm import relationship, Mapped

from src.domain.enums import OrderStatusEnum

from src.infrastructure.persistence.database.models.base import Base

if TYPE_CHECKING:
    from src.infrastructure.persistence.database.models.wallet import Wallet
    from src.infrastructure.persistence.database.models.product import Product
    from src.infrastructure.persistence.database.models.transaction import Transaction


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"))
    wallet_id = Column(UUID(as_uuid=True), ForeignKey("wallets.id", ondelete="CASCADE"))
    payment_transaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("transactions.id", ondelete="CASCADE"),
        nullable=True
    )
    return_transaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("transactions.id", ondelete="CASCADE"),
        nullable=True
    )
    status = Column(
        Enum(OrderStatusEnum, native_enum=False),
        server_default=OrderStatusEnum.NEW,
        nullable=False
    )
    created_at = Column(TIMESTAMP(timezone=True))

    wallet: Mapped["Wallet"] = relationship(back_populates="orders")
    product: Mapped["Product"] = relationship(back_populates="orders")
    payment_transaction: Mapped["Transaction"] = relationship(
        back_populates="payment_order",
        foreign_keys=[payment_transaction_id]
    )
    return_transaction: Mapped["Transaction"] = relationship(
        back_populates="return_order",
        foreign_keys=[return_transaction_id]
    )
