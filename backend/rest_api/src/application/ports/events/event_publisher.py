from abc import abstractmethod
from decimal import Decimal
from typing import Protocol
from uuid import UUID
from datetime import datetime

from src.domain.enums import OrderStatusEnum


class EventPublisher(Protocol):
    @abstractmethod
    async def create_eth_wallet(self, user_id: UUID) -> None:
        ...

    @abstractmethod
    async def import_eth_wallet(self, user_id: UUID, private_key: str) -> None:
        ...

    @abstractmethod
    async def create_transaction(
            self,
            private_key: str,
            to_address: str,
            amount: Decimal,
            payment_order_id: UUID | None = None,
            return_order_id: UUID | None = None
    ) -> None:
        ...

    @abstractmethod
    async def request_free_eth(self, to_address: str) -> None:
        ...

    @abstractmethod
    async def create_order(self, order_id: UUID, status: OrderStatusEnum, created_at: datetime) -> None:
        ...

    @abstractmethod
    async def pay_order(self, order_id: UUID) -> None:
        ...

    @abstractmethod
    async def update_order(self, order_id: UUID, status: OrderStatusEnum) -> None:
        ...
