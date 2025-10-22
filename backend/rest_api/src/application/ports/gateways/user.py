from abc import abstractmethod
from typing import Protocol

from src.domain.value_objects.shared.entity_id import EntityId

from src.domain.value_objects.user.email import Email

from src.domain.entities.user import User


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
