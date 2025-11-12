from datetime import datetime
from typing import TypedDict

from uuid import UUID

import logging

from dishka import FromDishka
from dishka.integrations.faststream import inject

from faststream.rabbit import RabbitRouter

from src.db.dtos import OrderDTO
from src.db.repositories import OrderRepositoryPort
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
