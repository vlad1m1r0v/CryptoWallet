from abc import abstractmethod
from typing import (
    Protocol,
    Optional
)

from src.domain.value_objects import (
    EntityId,
    OrderStatus,
    TransactionHash
)
from src.domain.entities import Order

from src.application.dtos.response import OrderResponseDTO


class OrderGateway(Protocol):
    @abstractmethod
    def add(self, order: Order) -> Order:
        ...

    @abstractmethod
    async def get_order(self, order_id: EntityId) -> OrderResponseDTO:
        ...

    @abstractmethod
    async def get_order_by_tx_hash(self, tx_hash: TransactionHash) -> OrderResponseDTO | None:
        ...

    @abstractmethod
    async def get_orders(self, user_id: EntityId) -> list[OrderResponseDTO]:
        ...

    @abstractmethod
    async def update(
            self,
            order_id: EntityId,
            status: Optional[OrderStatus] = None,
            payment_transaction_id: Optional[EntityId] = None,
            return_transaction_id: Optional[EntityId] = None
    ) -> Order:
        ...


