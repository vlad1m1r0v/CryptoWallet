from datetime import datetime
from typing import TypedDict, NotRequired

from uuid import UUID

import logging

from dishka import FromDishka
from dishka.integrations.faststream import inject

from faststream.rabbit import (
    RabbitRouter,
    RabbitBroker,
    RabbitQueue,
    RabbitExchange,
    ExchangeType
)

from src.db.dtos import OrderDTO
from src.db.repositories import OrderRepositoryPort
from src.faststream.services import RequestServicePort
from src.enums import OrderStatusEnum

logger = logging.getLogger(__name__)

amqp_router = RabbitRouter()

exchange = RabbitExchange("exchange", auto_delete=True, type=ExchangeType.DIRECT)


class CreateOrderDict(TypedDict):
    order_id: UUID
    status: OrderStatusEnum
    created_at: datetime


@amqp_router.subscriber("rest_api.create_order")
@inject
async def create_order_handler(
        data: CreateOrderDict,
        repository: FromDishka[OrderRepositoryPort]
) -> None:
    logger.info("Order creation...")

    await repository.add_order(OrderDTO(
        id=data["order_id"],
        status=data["status"],
        created_at=data["created_at"])
    )


class UpdateOrderDict(TypedDict):
    order_id: UUID
    status: NotRequired[OrderStatusEnum]


@amqp_router.subscriber(
    queue=RabbitQueue(
        name="ibay.order.update",
        routing_key="rest_api.update_order"
    ),
    exchange=exchange
)
@inject
async def update_order_handler(
        data: UpdateOrderDict,
        repository: FromDishka[OrderRepositoryPort]
) -> None:
    logger.info("Order update...")

    if not data.get("status"):
        return

    await repository.update_order(
        order_id=data["order_id"],
        status=data["status"]
    )


class PayOrderDict(TypedDict):
    order_id: UUID


@amqp_router.subscriber(
    queue=RabbitQueue(
        name="ibay.order.pay",
        routing_key="rest_api.pay_order"
    ),
    exchange=exchange
)
@inject
async def pay_order_handler(
        data: PayOrderDict,
        request_service: FromDishka[RequestServicePort],
        broker: FromDishka[RabbitBroker]
) -> None:
    logger.info("Order payment...")

    is_successful = await request_service.run_10_000_google_requests()

    if is_successful:
        await broker.publish(
            routing_key="ibay.deliver_order",
            message={"order_id": data["order_id"]}
        )
    else:
        await broker.publish(
            routing_key="ibay.fail_order",
            message={"order_id": data["order_id"]}
        )
