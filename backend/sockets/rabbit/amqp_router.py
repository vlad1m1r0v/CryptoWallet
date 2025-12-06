import logging

from dishka import FromDishka
from dishka.integrations.faststream import inject

from faststream.rabbit import (
    RabbitRouter,
    RabbitQueue,
    RabbitExchange,
    ExchangeType
)

from mongo.dtos import (
    CreateUserDTO,
    UpdateUserDTO
)

from mongo.repositories import UserRepository

from ws.app import sio

from rabbit.dicts import (
    SaveUserDict,
    UpdateUserDict,
    DeleteAvatarDict,
    SaveWalletDict,
    UpdateWalletDict,
    SavePendingTransactionDict,
    CompleteTransactionDict,
    RequestETHDict
)

logger = logging.getLogger(__name__)

amqp_router = RabbitRouter()

exchange = RabbitExchange("exchange", auto_delete=True, type=ExchangeType.DIRECT)


@amqp_router.subscriber("rest_api.save_user")
@inject
async def save_user_handler(
        data: SaveUserDict,
        repository: FromDishka[UserRepository]
) -> None:
    await repository.create(CreateUserDTO(**data))


@amqp_router.subscriber("rest_api.update_user")
@inject
async def update_user_handler(
        data: UpdateUserDict,
        repository: FromDishka[UserRepository]
) -> None:
    await repository.update(UpdateUserDTO(**data))


@amqp_router.subscriber("rest_api.delete_avatar")
@inject
async def delete_avatar_handler(
        data: DeleteAvatarDict,
        repository: FromDishka[UserRepository]
) -> None:
    await repository.delete_avatar(user_id=data["user_id"])


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


@amqp_router.subscriber("rest_api.update_wallet")
@inject
async def update_wallet_handler(
        data: UpdateWalletDict,
) -> None:
    user_room = f"user:{data['user_id']}"

    payload = {
        "id": str(data["wallet_id"]),
        "balance": float(data["balance"])
    }

    await sio.emit("update_wallet", payload, user_room)


@amqp_router.subscriber("rest_api.save_pending_transaction")
@inject
async def save_pending_transaction_handler(
        data: SavePendingTransactionDict,
) -> None:
    user_room = f"user:{data['user_id']}"

    payload = {
        "id": str(data["transaction_id"]),
        "wallet_id": str(data["wallet_id"]),
        "wallet_address": data["wallet_address"],
        "transaction_hash": data["transaction_hash"],
        "from_address": data["from_address"],
        "to_address": data["to_address"],
        "value": float(data["value"]),
        "transaction_fee": float(data["transaction_fee"]),
        "transaction_status": data["transaction_status"],
        "asset_symbol": data["asset_symbol"],
    }

    await sio.emit("save_pending_transaction", payload, user_room)


@amqp_router.subscriber("rest_api.complete_transaction")
@inject
async def complete_transaction_handler(
        data: CompleteTransactionDict,
) -> None:
    user_room = f"user:{data['user_id']}"

    payload = {
        "id": str(data["transaction_id"]),
        "wallet_id": str(data["wallet_id"]),
        "wallet_address": data["wallet_address"],
        "transaction_hash": data["transaction_hash"],
        "from_address": data["from_address"],
        "to_address": data["to_address"],
        "value": float(data["value"]),
        "transaction_fee": float(data["transaction_fee"]),
        "transaction_status": data["transaction_status"],
        "asset_symbol": data["asset_symbol"],
        "transaction_type": data["transaction_type"],
        "created_at": data["created_at"].isoformat(),
    }

    await sio.emit("complete_transaction", payload, user_room)


@amqp_router.subscriber(
    queue=RabbitQueue(
        name="sockets",
        routing_key="rest_api.request_free_eth",
    ),
    exchange=exchange
)
@inject
async def request_free_eth_handler(
        data: RequestETHDict,
) -> None:
    user_room = f"user:{data['user_id']}"
    await sio.emit("request_free_eth", {}, user_room)
