from uuid import UUID

from src.application.ports.events import EventPublisher


class PublishCreateWalletInteractor:
    def __init__(self, event_publisher: EventPublisher) -> None:
        self._event_publisher = event_publisher

    async def __call__(self, user_id: UUID) -> None:
        return await self._event_publisher.create_eth_wallet(user_id)
