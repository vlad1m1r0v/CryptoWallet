from dataclasses import dataclass
from typing import TypedDict, Optional

from src.application.ports.gateways.user import UserGateway
from src.application.ports.providers.jwt import JwtProvider
from src.domain.exceptions.user import (
    UserNotActivatedError,
    UserNotFoundError
)
from src.domain.value_objects.entity_id import EntityId


@dataclass(frozen=True, slots=True, kw_only=True)
class GetCurrentUserRequest:
    access_token: str


class GetCurrentUserResponse(TypedDict):
    username: str
    email: str
    avatar_url: Optional[str]


class GetCurrentUserInteractor:
    def __init__(
            self,
            user_gateway: UserGateway,
            jwt_provider: JwtProvider,
    ):
        self._user_gateway = user_gateway
        self._jwt_provider = jwt_provider

    async def __call__(self, data: GetCurrentUserRequest) -> GetCurrentUserResponse:
        decoded = self._jwt_provider.decode(data.access_token)

        user = await self._user_gateway.read_by_id(user_id=EntityId(value=decoded['user_id']))

        if not user:
            raise UserNotFoundError()

        if not user.is_active:
            raise UserNotActivatedError()

        return GetCurrentUserResponse(
            username=user.username.value,
            email=user.email.value,
            avatar_url=user.avatar_url.value if user.avatar_url else None,
        )
