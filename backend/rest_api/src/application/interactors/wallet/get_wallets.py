from uuid import UUID

from src.domain.value_objects import EntityId

from src.application.ports.gateways import WalletGateway
from src.application.dtos.response import WalletsListItemResponseDTO


class GetWalletsInteractor:
    def __init__(
            self,
            wallet_gateway: WalletGateway,
    ) -> None:
        self._wallet_gateway = wallet_gateway

    async def __call__(self, user_id: UUID) -> list[WalletsListItemResponseDTO]:
        user_id = EntityId(user_id)
        return await self._wallet_gateway.get_user_wallets(user_id)
