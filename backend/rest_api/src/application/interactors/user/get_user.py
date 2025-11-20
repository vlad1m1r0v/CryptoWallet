from uuid import UUID
import logging

from src.domain.exceptions import UserNotFoundException

from src.application.ports.gateways import UserGateway
from src.application.dtos.response import UserResponseDTO

logging = logging.getLogger(__name__)


class GetUserInteractor:
    def __init__(
            self,
            user_gateway: UserGateway,
    ):
        self._user_gateway = user_gateway

    async def __call__(self, user_id: UUID) -> UserResponseDTO:
        logging.info("Getting user from database...")

        user = await self._user_gateway.read(user_id=user_id)

        logging.info("Checking if user is not found...")

        if not user:
            raise UserNotFoundException()

        return user
