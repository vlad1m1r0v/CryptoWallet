from abc import abstractmethod
from decimal import Decimal
from typing import Protocol
from uuid import UUID


class EventPublisher(Protocol):
    @abstractmethod
    async def create_eth_wallet(self, user_id: UUID) -> None:
        ...

    @abstractmethod
    async def import_eth_wallet(self, user_id: UUID, private_key: str) -> None:
        ...

    @abstractmethod
    async def create_transaction(self, private_key: str, to_address: str, amount: Decimal) -> None:
        ...

    @abstractmethod
    async def request_free_eth(self, to_address: str) -> None:
        ...