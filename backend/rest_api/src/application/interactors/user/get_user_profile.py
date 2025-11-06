from uuid import UUID

from src.domain.exceptions import (
    UserNotFoundException
)
from src.domain.value_objects import EntityId

from src.application.ports.gateways import UserGateway
from src.application.dtos.response import GetUserProfileResponseDTO


class GetUserProfileInteractor:
    def __init__(
            self,
            user_gateway: UserGateway,
    ):
        self._user_gateway = user_gateway

    async def __call__(self, user_id: UUID) -> GetUserProfileResponseDTO:
        profile = await self._user_gateway.get_user_profile(user_id=EntityId(user_id))

        if not profile:
            raise UserNotFoundException()

        return profile
