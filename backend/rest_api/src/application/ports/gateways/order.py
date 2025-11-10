from abc import abstractmethod
from typing import Protocol

from src.domain.value_objects import EntityId
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
    async def get_orders(self, user_id: EntityId) -> list[OrderResponseDTO]:
        ...
