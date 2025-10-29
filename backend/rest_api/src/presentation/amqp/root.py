from dishka import FromDishka
from dishka.integrations.faststream import inject

from faststream.rabbit import RabbitRouter

from src.application.interactors.wallet.save_create_wallet import (
    SaveCreateWalletRequest,
    SaveCreateWalletInteractor
)

from src.application.interactors.wallet.save_import_wallet import (
    WalletWithTransactionsDTO,
    SaveImportWalletInteractor
)

from src.application.interactors.transaction.create_pending_transaction import (
    TransactionDTO,
    CreatePendingTransactionInteractor
)

from src.application.interactors.transaction.complete_transaction import (
    UpdateTransactionDTO,
    CompleteTransactionInteractor
)

amqp_router = RabbitRouter()


@amqp_router.subscriber("ethereum.create_eth_wallet")
@inject
async def create_wallet_handler(
        data: SaveCreateWalletRequest,
        interactor: FromDishka[SaveCreateWalletInteractor]
) -> None:
    return await interactor(data)


@amqp_router.subscriber("ethereum.import_eth_wallet")
@inject
async def import_wallet_handler(
        data: WalletWithTransactionsDTO,
        interactor: FromDishka[SaveImportWalletInteractor]
) -> None:
    return await interactor(data)

@amqp_router.subscriber("ethereum.create_pending_transaction")
@inject
async def create_pending_transaction_handler(
        data: TransactionDTO,
        interactor: FromDishka[CreatePendingTransactionInteractor]
) -> None:
    return await interactor(data)


@amqp_router.subscriber("ethereum.complete_transaction")
@inject
async def complete_transaction_handler(
        data: UpdateTransactionDTO,
        interactor: FromDishka[CompleteTransactionInteractor]
) -> None:
    return await interactor(data)