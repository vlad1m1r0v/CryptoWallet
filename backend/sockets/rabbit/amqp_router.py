from typing import TypedDict, NotRequired
from decimal import Decimal

from uuid import UUID

import logging

from dishka import FromDishka
from dishka.integrations.faststream import inject

from faststream.rabbit import RabbitRouter

from mongo.dtos import (
    CreateUserDTO,
    UpdateUserDTO
)

from mongo.repositories import UserRepository

from ws.app import sio

logger = logging.getLogger(__name__)

amqp_router = RabbitRouter()


class SaveUserDict(TypedDict):
    user_id: UUID
    username: str


@amqp_router.subscriber("rest_api.save_user")
@inject
async def save_user_handler(
        data: SaveUserDict,
        repository: FromDishka[UserRepository]
) -> None:
    await repository.create(CreateUserDTO(**data))


class UpdateUserDict(TypedDict):
    user_id: UUID
    username: NotRequired[str]
    avatar_filename: NotRequired[str]


@amqp_router.subscriber("rest_api.update_user")
@inject
async def update_user_handler(
        data: UpdateUserDict,
        repository: FromDishka[UserRepository]
) -> None:
    await repository.update(UpdateUserDTO(**data))


class DeleteAvatarDict(TypedDict):
    user_id: UUID


@amqp_router.subscriber("rest_api.delete_avatar")
@inject
async def delete_avatar_handler(
        data: DeleteAvatarDict,
        repository: FromDishka[UserRepository]
) -> None:
    await repository.delete_avatar(user_id=data["user_id"])


class SaveWalletDict(TypedDict):
    user_id: UUID
    wallet_id: UUID
    address: str
    balance: Decimal
    asset_symbol: str


@amqp_router.subscriber("rest_api.save_wallet")
@inject
async def save_wallet_handler(
        data: SaveWalletDict,
) -> None:
    user_room = f"user:{data['user_id']}"

    payload = {
        "id": str(data["wallet_id"]),
        "address": data["address"],
        "balance": float(data["balance"]),
        "asset_symbol": data["asset_symbol"]
    }

    await sio.emit("save_wallet", payload, user_room)