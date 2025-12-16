from dishka import FromDishka
from dishka.integrations.faststream import inject

from faststream.rabbit import (
    RabbitRouter
)

from src.domain.enums import OrderStatusEnum

from src.application.interactors import (
    IncrementTotalMessagesInteractor,
    SaveCreateWalletInteractor,
    SaveImportWalletInteractor,
    CreatePendingTransactionInteractor,
    CompleteTransactionInteractor,
    UpdateOrderInteractor
)

from src.presentation.amqp.types import (
    SaveCreateWalletRequestDict,
    SaveImportWalletRequestDict,
    CreatePendingTransactionRequestDict,
    UpdateTransactionRequestDict,
    OrderRequestDict,
    IncrementTotalMessagesRequestDict
)

from src.presentation.amqp.mappers import (
    SaveCreateWalletRequestMapper,
    SaveImportWalletRequestMapper,
    CreatePendingTransactionRequestMapper,
    UpdateTransactionRequestMapper
)

amqp_router = RabbitRouter()


@amqp_router.subscriber("sockets.create_message")
@inject
async def create_message_handler(
        data: IncrementTotalMessagesRequestDict,
        interactor: FromDishka[IncrementTotalMessagesInteractor]
) -> None:
    return await interactor(data["user_id"])


@amqp_router.subscriber("ethereum.create_eth_wallet")
@inject
async def create_wallet_handler(
        data: SaveCreateWalletRequestDict,
        interactor: FromDishka[SaveCreateWalletInteractor]
) -> None:
    dto = SaveCreateWalletRequestMapper.to_dataclass(data)
    return await interactor(dto)


@amqp_router.subscriber("ethereum.import_eth_wallet")
@inject
async def import_wallet_handler(
        data: SaveImportWalletRequestDict,
        interactor: FromDishka[SaveImportWalletInteractor]
) -> None:
    dto = SaveImportWalletRequestMapper.to_dataclass(data)
    return await interactor(dto)


@amqp_router.subscriber("ethereum.create_pending_transaction")
@inject
async def create_pending_transaction_handler(
        data: CreatePendingTransactionRequestDict,
        interactor: FromDishka[CreatePendingTransactionInteractor]
) -> None:
    dto = CreatePendingTransactionRequestMapper.to_dataclass(data)
    return await interactor(dto)


@amqp_router.subscriber("ethereum.complete_transaction")
@inject
async def complete_transaction_handler(
        data: UpdateTransactionRequestDict,
        interactor: FromDishka[CompleteTransactionInteractor]
) -> None:
    dto = UpdateTransactionRequestMapper.to_dataclass(data)
    return await interactor(dto)


@amqp_router.subscriber("ibay.fail_order")
@inject
async def fail_order_handler(
        data: OrderRequestDict,
        interactor: FromDishka[UpdateOrderInteractor]
) -> None:
    await interactor(order_id=data["order_id"], status=OrderStatusEnum.FAILED)


@amqp_router.subscriber("ibay.deliver_order")
@inject
async def deliver_order_handler(
        data: OrderRequestDict,
        interactor: FromDishka[UpdateOrderInteractor]
) -> None:
    await interactor(order_id=data["order_id"], status=OrderStatusEnum.DELIVERING)


@amqp_router.subscriber("ibay.return_order")
@inject
async def return_order_handler(
        data: OrderRequestDict,
        interactor: FromDishka[UpdateOrderInteractor]
) -> None:
    await interactor(order_id=data["order_id"], status=OrderStatusEnum.RETURNED)


@amqp_router.subscriber("ibay.complete_order")
@inject
async def return_order_handler(
        data: OrderRequestDict,
        interactor: FromDishka[UpdateOrderInteractor]
) -> None:
    await interactor(order_id=data["order_id"], status=OrderStatusEnum.COMPLETED)
