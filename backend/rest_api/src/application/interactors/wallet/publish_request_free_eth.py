from uuid import UUID
import logging

from src.domain.exceptions import (
    UserIsNotOwnerOfWalletException,
    WalletNotFoundException
)
from src.domain.value_objects import (
    EntityId,
    Address
)

from src.application.ports.gateways import WalletGateway
from src.application.ports.events import EventPublisher
from src.application.dtos.events import RequestFreeETHEventDTO

logger = logging.getLogger(__name__)


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

        logger.info("Reading wallet record from database...")

        wallet = await self._wallet_gateway.read(wallet_id=wallet_id.value)

        logger.info("Checking if wallet exists...")

        if not wallet:
            raise WalletNotFoundException()

        logger.info("Checking if user is the owner of wallet")

        if wallet["user_id"] != user_id.value:
            raise UserIsNotOwnerOfWalletException(user_id, Address(wallet["address"]))

        logger.info("Emitting event rest_api.request_free_eth...")

        return await self._event_publisher.request_free_eth(
            RequestFreeETHEventDTO(user_id=user_id.value, to_address=wallet["address"])
        )
