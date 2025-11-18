from abc import abstractmethod
from typing import (
    Protocol,
    Optional,
    overload,
    Union
)
from uuid import UUID

from src.domain.enums import OrderStatusEnum
from src.domain.entities import Order

from src.application.dtos.response import OrderResponseDTO


class OrderGateway(Protocol):
    @abstractmethod
    def add(self, order: Order) -> None:
        ...

    @overload
    @abstractmethod
    async def read(self, order_id: UUID) -> OrderResponseDTO | None:
        ...

    @overload
    @abstractmethod
    async def read(self, tx_hash: str) -> OrderResponseDTO | None:
        ...

    @abstractmethod
    async def read(self, arg: Union[str, UUID]) -> OrderResponseDTO | None:
        ...

    @abstractmethod
    async def list(self, user_id: UUID) -> list[OrderResponseDTO]:
        ...

    @abstractmethod
    async def update(
            self,
            order_id: UUID,
            status: Optional[OrderStatusEnum] = None,
            payment_transaction_id: Optional[UUID] = None,
            return_transaction_id: Optional[UUID] = None
    ) -> None:
        ...
