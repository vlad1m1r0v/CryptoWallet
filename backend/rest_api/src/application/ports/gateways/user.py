from abc import abstractmethod
from typing import Protocol, Optional, overload, Union
from uuid import UUID

from src.domain.entities import User

from src.application.dtos.response import UserResponseDTO


class UserGateway(Protocol):
    @abstractmethod
    def add(self, user: User) -> None:
        ...

    @abstractmethod
    async def update(
            self,
            user_id: UUID,
            username: Optional[str] = None,
            password_hash: Optional[bytes] = None,
            avatar_filename: Optional[str] = None
    ) -> None:
        ...

    @overload
    @abstractmethod
    async def read(self, user_id: UUID) -> UserResponseDTO | None:
        ...

    @overload
    @abstractmethod
    async def read(self, email: str) -> UserResponseDTO | None:
        ...

    @abstractmethod
    async def read(self, arg: Union[UUID, str]) -> UserResponseDTO | None:
        ...