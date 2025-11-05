from uuid import UUID

from src.domain.exceptions import (
    UserIsNotOwnerOfWalletException,
    WalletNotFoundException
)
from src.domain.value_objects import EntityId

from src.application.ports.gateways import WalletGateway
from src.application.ports.events import EventPublisher


class PublishRequestFreeETHInteractor:
    def __init__(
            self,
            wallet_gateway: WalletGateway,
            event_publisher: EventPublisher
    ) -> None:
        self._wallet_gateway = wallet_gateway
        self._event_publisher = event_publisher

    async def __call__(self, user_id: UUID, wallet_id: UUID) -> None:
        wallet_id = EntityId(wallet_id)
        user_id = EntityId(user_id)

        wallet = await self._wallet_gateway.read_by_id(wallet_id)

        if not wallet:
            raise WalletNotFoundException()

        if wallet.user_id != user_id:
            raise UserIsNotOwnerOfWalletException(user_id, wallet.address)

        return await self._event_publisher.request_free_eth(
            to_address=wallet.address.value,
        )
