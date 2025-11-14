from typing import Any
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from faststream.rabbit import RabbitBroker

from src.domain.enums import OrderStatusEnum

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

    async def create_transaction(
            self,
            private_key: str,
            to_address: str,
            amount: Decimal,
            payment_order_id: UUID | None = None,
            return_order_id: UUID | None = None
    ) -> None:
        message: dict[str, Any] = {"private_key": private_key, "to_address": to_address, "amount": amount}

        if payment_order_id:
            message.setdefault("payment_order_id", payment_order_id)

        if return_order_id:
            message.setdefault("return_order_id", return_order_id)

        await self._broker.publish(
            routing_key="rest_api.create_transaction",
            message=message
        )

    async def request_free_eth(self, to_address: str) -> None:
        message = {"to_address": to_address}

        await self._broker.publish(
            routing_key="rest_api.request_free_eth",
            message=message
        )

    async def create_order(self, order_id: UUID, status: OrderStatusEnum, created_at: datetime) -> None:
        message = {"id": order_id, "status": status, "created_at": created_at}

        await self._broker.publish(
            routing_key="rest_api.create_order",
            message=message
        )

    async def pay_order(self, order_id: UUID) -> None:
        message = {"id": order_id}

        await self._broker.publish(
            routing_key="rest_api.pay_order",
            message=message
        )

    async def update_order(self, order_id: UUID, status: OrderStatusEnum) -> None:
        message = {"id": order_id, "status": status}

        await self._broker.publish(
            routing_key="rest_api.update_order",
            message=message
        )
