from dishka import FromDishka
from dishka.integrations.faststream import inject

from faststream.rabbit import RabbitRouter

from src.application.interactors import (
    SaveCreateWalletInteractor,
    SaveImportWalletInteractor,
    CreatePendingTransactionInteractor,
    CompleteTransactionInteractor
)

from src.presentation.amqp.types import (
    SaveCreateWalletRequestDict,
    SaveImportWalletRequestDict,
    CreatePendingTransactionRequestDict,
    UpdateTransactionRequestDict
)

from src.presentation.amqp.mappers import (
    SaveCreateWalletRequestMapper,
    SaveImportWalletRequestMapper,
    CreatePendingTransactionRequestMapper,
    UpdateTransactionRequestMapper
)

amqp_router = RabbitRouter()


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
