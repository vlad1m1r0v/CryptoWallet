from uuid import UUID
import logging

from src.application.dtos.events import DeleteAvatarEventDTO
from src.application.ports.gateways import UserGateway
from src.application.ports.events import EventPublisher
from src.application.ports.transaction import TransactionManager

from src.application.dtos.response import UserResponseDTO

logger = logging.getLogger(__name__)


class DeleteAvatarInteractor:
    def __init__(
            self,
            user_gateway: UserGateway,
            transaction_manager: TransactionManager,
            event_publisher: EventPublisher
    ):
        self._user_gateway = user_gateway
        self._transaction_manager = transaction_manager
        self._event_publisher = event_publisher

    async def __call__(self, user_id: UUID) -> UserResponseDTO:
        logger.info("Deleting user avatar...")

        await self._user_gateway.delete_avatar(user_id=user_id)
        await self._transaction_manager.commit()

        user = await self._user_gateway.read(user_id=user_id)

        logger.info("Emitting event rest_api.update_user...")

        await self._event_publisher.delete_avatar(dto=DeleteAvatarEventDTO(user_id=user_id))

        logger.info("Returning updated user...")

        return user
