from abc import abstractmethod
from typing import Protocol

from src.domain.value_objects import (
    EntityId,
    Email
)
from src.domain.entities import User

from src.application.dtos.response import GetUserProfileResponseDTO


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

    @abstractmethod
    async def get_user_profile(self, user_id: EntityId) -> GetUserProfileResponseDTO | None:
        ...
