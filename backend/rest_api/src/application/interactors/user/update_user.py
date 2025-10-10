from dataclasses import dataclass
from typing import TypedDict, Optional
from uuid import UUID

from src.application.ports.gateways.user import UserGateway
from src.application.ports.transaction.transaction_manager import TransactionManager
from src.domain.exceptions.user import (
    PasswordsNotMatchError,
    RepeatPasswordIsNotSetError,
    UserNotFoundError
)
from src.domain.services.user import UserService
from src.domain.value_objects.entity_id import EntityId
from src.domain.value_objects.raw_password import RawPassword
from src.domain.value_objects.username import Username


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateUserRequest:
    username: str
    password: Optional[str] = None
    repeat_password: Optional[str] = None


class UpdateUserResponse(TypedDict):
    username: str
    email: str
    avatar_url: Optional[str]


class UpdateUserInteractor:
    def __init__(
            self,
            user_gateway: UserGateway,
            user_service: UserService,
            transaction_manager: TransactionManager,
    ):
        self._user_gateway = user_gateway
        self._user_service = user_service
        self.transaction_manager = transaction_manager

    async def __call__(self, user_id: UUID, data: UpdateUserRequest) -> UpdateUserResponse:
        user = await self._user_gateway.read_by_id(user_id=EntityId(value=user_id))

        if not user:
            raise UserNotFoundError()

        user.username = Username(data.username)

        if data.password:
            if not data.repeat_password:
                raise RepeatPasswordIsNotSetError()

            password = RawPassword(data.password)
            repeat_password = RawPassword(data.repeat_password)

            if password != repeat_password:
                raise PasswordsNotMatchError()

            self._user_service.change_password(user, password)

        updated = await self._user_gateway.update(user)
        await self.transaction_manager.commit()

        return UpdateUserResponse(
            username=updated.username.value,
            email=updated.email.value,
            avatar_url=updated.avatar_url.value if updated.avatar_url else None,
        )
