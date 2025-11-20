from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.domain.entities import Permissions


class PermissionsGateway(Protocol):
    @abstractmethod
    def add(self, entity: Permissions) -> None:
        ...

    @abstractmethod
    async def update(self, user_id: UUID, has_chat_access: bool = True) -> None:
        ...
