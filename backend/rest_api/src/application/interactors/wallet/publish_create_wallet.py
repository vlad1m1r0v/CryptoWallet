from uuid import UUID
import logging

from src.application.ports.events import EventPublisher
from src.application.dtos.events import CreateWalletEventDTO

logger = logging.getLogger(__name__)

class PublishCreateWalletInteractor:
    def __init__(self, event_publisher: EventPublisher) -> None:
        self._event_publisher = event_publisher

    async def __call__(self, user_id: UUID) -> None:
        logging.info("Emitting event rest_api.create_eth_wallet...")

        return await self._event_publisher.create_eth_wallet(CreateWalletEventDTO(user_id=user_id))
