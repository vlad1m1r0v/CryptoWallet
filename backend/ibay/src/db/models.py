
from sqlalchemy import Column, TIMESTAMP, UUID, Enum

from src.enums import OrderStatusEnum

from src.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True)
    status = Column(Enum(OrderStatusEnum), server_default=OrderStatusEnum.NEW, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True))