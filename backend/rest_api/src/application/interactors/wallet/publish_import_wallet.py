from uuid import UUID
import logging

from src.application.ports.events import EventPublisher
from src.application.dtos.events import ImportWalletEventDTO

logger = logging.getLogger(__name__)


class PublishImportWalletInteractor:
    def __init__(self, event_publisher: EventPublisher) -> None:
        self._event_publisher = event_publisher

    async def __call__(self, user_id: UUID, private_key: str) -> None:
        logger.info("Emitting event rest_api.import_eth_wallet...")

        return await self._event_publisher.import_eth_wallet(
            ImportWalletEventDTO(user_id=user_id, private_key=private_key)
        )
