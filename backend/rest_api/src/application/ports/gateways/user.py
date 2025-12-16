from abc import abstractmethod
from typing import Protocol, Optional, Union
from uuid import UUID

from src.domain.entities import User

from src.application.dtos.response import UserResponseDTO


class UserGateway(Protocol):
    @abstractmethod
    def add(self, user: User) -> None:
        ...

    @abstractmethod
    async def delete_avatar(self, user_id: UUID) -> None:
        ...

    @abstractmethod
    async def increment_total_messages(self, user_id: UUID) -> None:
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

    @abstractmethod
    async def read(
            self,
            *,
            user_id: Optional[UUID] = None,
            email: Optional[str] = None
    ) -> UserResponseDTO | None:
        ...