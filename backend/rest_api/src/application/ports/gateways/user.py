from abc import abstractmethod
from typing import Protocol

from src.domain.value_objects import (
    EntityId,
    Email
)

from src.domain.entities import User


class UserGateway(Protocol):
    @abstractmethod
    def add(self, user: User) -> User:
        ...

    @abstractmethod
    async def update(self, user: User) -> User:
        ...

    @abstractmethod
    async def read_by_id(self, user_id: EntityId) -> User | None:
        ...

    @abstractmethod
    async def read_by_email(self, email: Email) -> User | None:
        ...
