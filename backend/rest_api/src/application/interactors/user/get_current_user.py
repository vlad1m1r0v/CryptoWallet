from src.domain.exceptions import (
    UserNotActivatedException,
    UserNotFoundException
)
from src.domain.value_objects import EntityId
from src.application.ports.gateways import UserGateway
from src.application.ports.providers import JwtProvider
from src.application.dtos.request import GetCurrentUserRequestDTO
from src.application.dtos.response import GetCurrentUserResponseDTO


class GetCurrentUserInteractor:
    def __init__(
            self,
            user_gateway: UserGateway,
            jwt_provider: JwtProvider,
    ):
        self._user_gateway = user_gateway
        self._jwt_provider = jwt_provider

    async def __call__(self, data: GetCurrentUserRequestDTO) -> GetCurrentUserResponseDTO:
        decoded = self._jwt_provider.decode(data.access_token)

        user = await self._user_gateway.read_by_id(user_id=EntityId(value=decoded['user_id']))

        if not user:
            raise UserNotFoundException()

        if not user.is_active:
            raise UserNotActivatedException()

        return GetCurrentUserResponseDTO(
            id=user.id_.value,
            username=user.username.value,
            email=user.email.value,
            avatar_filename=user.avatar_filename.value if user.avatar_filename else None,
        )
