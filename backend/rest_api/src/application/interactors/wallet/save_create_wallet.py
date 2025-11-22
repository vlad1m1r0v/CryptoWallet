import logging

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
from src.application.ports.events import EventPublisher
from src.application.dtos.request import SaveCreateWalletRequestDTO
from src.application.dtos.events import SaveWalletEventDTO

logger = logging.getLogger(__name__)


class SaveCreateWalletInteractor:
    def __init__(
            self,
            wallet_service: WalletService,
            asset_gateway: AssetGateway,
            wallet_gateway: WalletGateway,
            transaction_manager: TransactionManager,
            event_publisher: EventPublisher
    ) -> None:
        self._wallet_service = wallet_service
        self._asset_gateway = asset_gateway
        self._wallet_gateway = wallet_gateway
        self._transaction_manager = transaction_manager
        self._event_publisher = event_publisher

    async def __call__(self, data: SaveCreateWalletRequestDTO) -> None:
        logger.info("Getting sepolia asset record from database...")

        sepolia_asset = await self._asset_gateway.read(network_type=AssetNetworkTypeEnum.SEPOLIA)

        logger.info("Inserting new wallet record into database...")

        entity = self._wallet_service.create_wallet(
            user_id=EntityId(data.user_id),
            asset_id=EntityId(sepolia_asset["id"]),
            address=Address(data.address),
            raw_private_key=RawPrivateKey(data.private_key),
            balance=Balance(data.balance),
            created_at=Timestamp(data.created_at)
        )

        self._wallet_gateway.add(entity)

        await self._transaction_manager.commit()

        wallet = await self._wallet_gateway.read(wallet_id=entity.id_.value)

        logger.info("Emitting event rest_api.save_wallet...")

        await self._event_publisher.save_wallet(
            SaveWalletEventDTO(
                user_id=wallet["user_id"],
                wallet_id=wallet["id"],
                address=wallet["address"],
                balance=wallet["balance"] / ( 10 ** wallet["asset"]["decimals"]),
                asset_symbol=wallet["asset"]["symbol"],
            )
        )
