from uuid import UUID

from faststream.rabbit import RabbitBroker

from src.application.ports.events.event_publisher import EventPublisher


class RabbitMQEventPublisher(EventPublisher):
    def __init__(self, broker: RabbitBroker):
        self._broker = broker

    async def create_eth_wallet(self, user_id: UUID) -> None:
        message = {"user_id": str(user_id)}
        await self._broker.publish(
            routing_key="rest_api.create_eth_wallet",
            message=message
        )
