from datetime import datetime
from decimal import Decimal
from typing import TypedDict
from uuid import UUID

from src.domain.enums.asset import AssetNetworkTypeEnum

from src.domain.value_objects.shared.entity_id import EntityId
from src.domain.value_objects.shared.timestamp import Timestamp

from src.domain.value_objects.wallet.raw_private_key import RawPrivateKey
from src.domain.value_objects.wallet.address import Address
from src.domain.value_objects.wallet.balance import Balance

from src.domain.services.wallet import WalletService

from src.application.ports.transaction.transaction_manager import TransactionManager
from src.application.ports.gateways.asset import AssetGateway
from src.application.ports.gateways.wallet import WalletGateway


class SaveCreateWalletRequest(TypedDict):
    user_id: UUID
    address: str
    private_key: str
    balance: Decimal
    created_at: datetime


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

    async def __call__(self, data: SaveCreateWalletRequest) -> None:
        sepolia_asset = await self._asset_gateway.read_by_network_type(AssetNetworkTypeEnum.SEPOLIA)

        entity = self._wallet_service.create_wallet(
            user_id=EntityId(data["user_id"]),
            asset_id=sepolia_asset.id_,
            address=Address(data["address"]),
            raw_private_key=RawPrivateKey(data["private_key"]),
            balance=Balance(data["balance"]),
            created_at=Timestamp(data["created_at"]),
        )

        self._wallet_gateway.add(entity)

        await self._transaction_manager.commit()
