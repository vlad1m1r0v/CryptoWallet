from uuid import UUID
import logging

from src.domain.value_objects import EntityId

from src.application.ports.gateways import WalletGateway
from src.application.dtos.response import WalletResponseDTO

logger = logging.getLogger(__name__)


class GetWalletsInteractor:
    def __init__(
            self,
            wallet_gateway: WalletGateway,
    ) -> None:
        self._wallet_gateway = wallet_gateway

    async def __call__(self, user_id: UUID) -> list[WalletResponseDTO]:
        logger.info("Getting list of wallets for user...")

        return await self._wallet_gateway.list(user_id=EntityId(user_id).value)
