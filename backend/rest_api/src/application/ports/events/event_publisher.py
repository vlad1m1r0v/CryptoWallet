from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class EventPublisher(Protocol):
    @abstractmethod
    async def create_eth_wallet(self, user_id: UUID) -> None:
        ...

    @abstractmethod
    async def import_eth_wallet(self, user_id: UUID, private_key: str) -> None:
        ...
