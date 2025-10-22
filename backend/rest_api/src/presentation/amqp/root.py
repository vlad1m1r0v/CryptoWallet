from dishka import FromDishka
from dishka.integrations.faststream import inject

from faststream.rabbit import RabbitRouter

from src.application.interactors.wallet.save_create_wallet import (
    SaveCreateWalletRequest,
    SaveCreateWalletInteractor
)

amqp_router = RabbitRouter()


@amqp_router.subscriber("ethereum.create_eth_wallet")
@inject
async def create_wallet_handler(
        data: SaveCreateWalletRequest,
        interactor: FromDishka[SaveCreateWalletInteractor]
) -> None:
    return await interactor(data)
