from faststream.rabbit import RabbitBroker

from typing import Any
from dataclasses import asdict

from src.application.ports.events import EventPublisher
from src.application.dtos.events import (
    SaveUserEventDTO,
    GiveChatAccessEventDTO,
    UpdateUserEventDTO,
    CreateWalletEventDTO,
    SaveWalletEventDTO,
    UpdateWalletEventDTO,
    ImportWalletEventDTO,
    CreateTransactionEventDTO,
    SavePendingTransactionEventDTO,
    CompleteTransactionEventDTO,
    RequestFreeETHEventDTO,
    SaveProductEventDTO,
    CreateOrderEventDTO,
    PayOrderEventDTO,
    UpdateOrderEventDTO
)


def exclude_none_factory(data: list[tuple[str, Any]]) -> dict:
    return {k: v for k, v in data if v is not None}


class RabbitMQEventPublisher(EventPublisher):
    def __init__(self, broker: RabbitBroker):
        self._broker = broker

    async def save_user(self, dto: SaveUserEventDTO) -> None:
        await self._broker.publish(
            routing_key="rest_api.save_user",
            message=asdict(dto)
        )

    async def give_chat_access_to_user(self, dto: GiveChatAccessEventDTO) -> None:
        await self._broker.publish(
            routing_key="rest_api.give_chat_access_to_user",
            message=asdict(dto)
        )

    async def update_user(self, dto: UpdateUserEventDTO) -> None:
        await self._broker.publish(
            routing_key="rest_api.update_user",
            message=asdict(dto, dict_factory=exclude_none_factory)
        )

    async def create_eth_wallet(self, dto: CreateWalletEventDTO) -> None:
        await self._broker.publish(
            routing_key="rest_api.create_eth_wallet",
            message=asdict(dto)
        )

    async def import_eth_wallet(self, dto: ImportWalletEventDTO) -> None:
        await self._broker.publish(
            routing_key="rest_api.import_eth_wallet",
            message=asdict(dto)
        )

    async def save_wallet(self, dto: SaveWalletEventDTO) -> None:
        await self._broker.publish(
            routing_key="rest_api.save_wallet",
            message=asdict(dto)
        )

    async def update_wallet(self, dto: UpdateWalletEventDTO) -> None:
        await self._broker.publish(
            routing_key="rest_api.update_wallet",
            message=asdict(dto)
        )

    async def create_transaction(self, dto: CreateTransactionEventDTO) -> None:
        await self._broker.publish(
            routing_key="rest_api.create_transaction",
            message=asdict(dto, dict_factory=exclude_none_factory)
        )

    async def save_pending_transaction(self, dto: SavePendingTransactionEventDTO) -> None:
        await self._broker.publish(
            routing_key="rest_api.save_pending_transaction",
            message=asdict(dto)
        )

    async def complete_transaction(self, dto: CompleteTransactionEventDTO) -> None:
        await self._broker.publish(
            routing_key="rest_api.complete_transaction",
            message=asdict(dto)
        )

    async def request_free_eth(self, dto: RequestFreeETHEventDTO) -> None:
        await self._broker.publish(
            routing_key="rest_api.request_free_eth",
            message=asdict(dto)
        )

    async def save_product(self, dto: SaveProductEventDTO) -> None:
        await self._broker.publish(
            routing_key="rest_api.save_product",
            message=asdict(dto)
        )

    async def create_order(self, dto: CreateOrderEventDTO) -> None:
        await self._broker.publish(
            routing_key="rest_api.create_order",
            message=asdict(dto)
        )

    async def pay_order(self, dto: PayOrderEventDTO) -> None:
        await self._broker.publish(
            routing_key="rest_api.pay_order",
            message=asdict(dto)
        )

    async def update_order(self, dto: UpdateOrderEventDTO) -> None:
        await self._broker.publish(
            routing_key="rest_api.update_order",
            message=asdict(dto, dict_factory=exclude_none_factory)
        )
