from uuid import UUID

from src.application.ports.events import EventPublisher


class PublishImportWalletInteractor:
    def __init__(self, event_publisher: EventPublisher) -> None:
        self._event_publisher = event_publisher

    async def __call__(self, user_id: UUID, private_key: str) -> None:
        return await self._event_publisher.import_eth_wallet(
            user_id=user_id,
            private_key=private_key
        )
