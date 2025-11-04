from decimal import Decimal
from uuid import UUID

from faststream.rabbit import RabbitBroker

from src.application.ports.events import EventPublisher


class RabbitMQEventPublisher(EventPublisher):

    def __init__(self, broker: RabbitBroker):
        self._broker = broker

    async def create_eth_wallet(self, user_id: UUID) -> None:
        message = {"user_id": str(user_id)}
        await self._broker.publish(
            routing_key="rest_api.create_eth_wallet",
            message=message
        )

    async def import_eth_wallet(self, user_id: UUID, private_key: str) -> None:
        message = {"user_id": str(user_id), "private_key": private_key}
        await self._broker.publish(
            routing_key="rest_api.import_eth_wallet",
            message=message
        )

    async def create_transaction(self, private_key: str, to_address, amount: Decimal) -> None:
        message = {"private_key": private_key, "to_address": to_address, "amount": amount}
        await self._broker.publish(
            routing_key="rest_api.create_transaction",
            message=message
        )
