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
    RequestETHDict,
    SaveProductDict,
    PayOrderDict,
    UpdateOrderDict,
    GiveChatAccessDict,
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
        name="sockets.ethereum.request",
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


@amqp_router.subscriber("rest_api.save_product")
@inject
async def save_product_handler(
        data: SaveProductDict
) -> None:
    payload = {
        "id": str(data["product_id"]),
        "name": data["name"],
        "price": float(data["price"]),
        "photo_url": data["photo_url"],
        "asset_symbol": data["asset_symbol"],
        "wallet_address": data["wallet_address"],
        "created_at": str(data["created_at"])
    }

    await sio.emit("save_product", payload)


@amqp_router.subscriber(
    queue=RabbitQueue(
        name="sockets.order.pay",
        routing_key="rest_api.pay_order",
    ),
    exchange=exchange
)
@inject
async def pay_order_handler(
        data: PayOrderDict,
) -> None:
    user_room = f"user:{data['user_id']}"

    payload = {
        "id": str(data["order_id"]),
        "transaction_hash": data["transaction_hash"]
    }

    await sio.emit("pay_order", payload, user_room)


@amqp_router.subscriber(
    queue=RabbitQueue(
        name="sockets.order.update",
        routing_key="rest_api.update_order",
    ),
    exchange=exchange
)
@inject
async def update_order_handler(
        data: UpdateOrderDict,
) -> None:
    user_room = f"user:{data['user_id']}"

    payload = {
        "id": str(data["order_id"])
    }

    if status := data.get("status", None):
        payload["status"] = status

    if payment_transaction_hash := data.get("payment_transaction_hash", None):
        payload["payment_transaction_hash"] = payment_transaction_hash

    if return_transaction_hash := data.get("return_transaction_hash", None):
        payload["return_transaction_hash"] = return_transaction_hash

    await sio.emit("update_order", payload, user_room)


@amqp_router.subscriber("rest_api.give_chat_access")
@inject
async def give_chat_access_handler(
        data: GiveChatAccessDict,
) -> None:
    user_room = f"user:{data['user_id']}"
    await sio.emit("give_chat_access", {}, user_room)
