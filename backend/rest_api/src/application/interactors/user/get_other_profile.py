from uuid import UUID
import logging

from src.domain.exceptions import UserNotFoundException

from src.application.ports.gateways import UserGateway
from src.application.dtos.response import OtherProfileResponseDTO

logging = logging.getLogger(__name__)


class GetOtherProfileInteractor:
    def __init__(
            self,
            user_gateway: UserGateway,
    ):
        self._user_gateway = user_gateway

    async def __call__(self, user_id: UUID) -> OtherProfileResponseDTO:
        logging.info("Getting user from database...")

        user = await self._user_gateway.read_other_profile(user_id=user_id)

        logging.info("Checking if user is not found...")

        if not user:
            raise UserNotFoundException()

        return user
