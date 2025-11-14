from datetime import datetime
from typing import TypedDict

from uuid import UUID

import logging

from dishka import FromDishka
from dishka.integrations.faststream import inject

from faststream.rabbit import RabbitRouter, RabbitBroker

from src.db.dtos import OrderDTO
from src.db.repositories import OrderRepositoryPort
from src.faststream.services import RequestServicePort
from src.enums import OrderStatusEnum

logger = logging.getLogger(__name__)

amqp_router = RabbitRouter()


class CreateOrderDict(TypedDict):
    id: UUID
    status: OrderStatusEnum
    created_at: datetime


@amqp_router.subscriber("rest_api.create_order")
@inject
async def create_order_handler(
        data: CreateOrderDict,
        repository: FromDishka[OrderRepositoryPort]
) -> None:
    await repository.add_order(OrderDTO(**data))


class UpdateOrderDict(TypedDict):
    id: UUID
    status: OrderStatusEnum


@amqp_router.subscriber("rest_api.update_order")
@inject
async def update_order_handler(
        data: UpdateOrderDict,
        repository: FromDishka[OrderRepositoryPort]
) -> None:
    await repository.update_order(order_id=data["id"], status=data["status"])


class PayOrderDict(TypedDict):
    id: UUID


@amqp_router.subscriber("rest_api.pay_order")
@inject
async def pay_order_handler(
        data: PayOrderDict,
        request_service: FromDishka[RequestServicePort],
        broker: FromDishka[RabbitBroker]
) -> None:
    is_successful = await request_service.run_10_000_google_requests()

    if is_successful:
        await broker.publish(
            queue="ibay.deliver_order",
            message={"order_id": data["id"]}
        )
    else:
        await broker.publish(
            queue="ibay.fail_order",
            message={"order_id": data["id"]}
        )
