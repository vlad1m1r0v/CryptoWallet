from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from src.enums import OrderStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderDTO:
    id: UUID
    status: OrderStatusEnum
    created_at: datetime