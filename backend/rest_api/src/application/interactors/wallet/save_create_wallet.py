from src.domain.enums import AssetNetworkTypeEnum
from src.domain.value_objects import (
    EntityId,
    Timestamp,
    RawPrivateKey,
    Address,
    Balance
)
from src.domain.services import WalletService

from src.application.ports.transaction import TransactionManager
from src.application.ports.gateways import (
    AssetGateway,
    WalletGateway
)
from src.application.dtos.request import SaveCreateWalletRequestDTO


class SaveCreateWalletInteractor:
    def __init__(
            self,
            wallet_service: WalletService,
            asset_gateway: AssetGateway,
            wallet_gateway: WalletGateway,
            transaction_manager: TransactionManager,
    ) -> None:
        self._wallet_service = wallet_service
        self._asset_gateway = asset_gateway
        self._wallet_gateway = wallet_gateway
        self._transaction_manager = transaction_manager

    async def __call__(self, data: SaveCreateWalletRequestDTO) -> None:
        sepolia_asset = await self._asset_gateway.read_by_network_type(AssetNetworkTypeEnum.SEPOLIA)

        entity = self._wallet_service.create_wallet(
            user_id=EntityId(data.user_id),
            asset_id=sepolia_asset.id_,
            address=Address(data.address),
            raw_private_key=RawPrivateKey(data.private_key),
            balance=Balance(data.balance),
            created_at=Timestamp(data.created_at)
        )

        self._wallet_gateway.add(entity)

        await self._transaction_manager.commit()
