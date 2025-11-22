import logging

from src.domain.enums import AssetNetworkTypeEnum
from src.domain.value_objects import (
    EntityId,
    Timestamp,
    RawPrivateKey,
    Address,
    Balance,
    TransactionValue,
    TransactionHash,
    TransactionStatus,
    TransactionFee
)
from src.domain.exceptions import WalletAlreadyExistsException
from src.domain.entities import (
    Wallet,
    Transaction
)
from src.domain.services import WalletService, TransactionService

from src.application.ports.gateways import (
    AssetGateway,
    WalletGateway,
    TransactionGateway
)
from src.application.ports.transaction import (
    TransactionManager,
    Flusher
)
from src.application.ports.events import EventPublisher
from src.application.dtos.request import (
    SaveImportWalletRequestDTO
)
from src.application.dtos.events import (
    SaveWalletEventDTO
)

logger = logging.getLogger(__name__)


class SaveImportWalletInteractor:
    def __init__(
            self,
            wallet_service: WalletService,
            transaction_service: TransactionService,
            asset_gateway: AssetGateway,
            wallet_gateway: WalletGateway,
            transaction_gateway: TransactionGateway,
            transaction_manager: TransactionManager,
            flusher: Flusher,
            event_publisher: EventPublisher
    ) -> None:
        self._wallet_service = wallet_service
        self._transaction_service = transaction_service

        self._asset_gateway = asset_gateway
        self._wallet_gateway = wallet_gateway
        self._transaction_gateway = transaction_gateway

        self._transaction_manager = transaction_manager
        self._flusher = flusher
        self._event_publisher = event_publisher

    async def __call__(self, data: SaveImportWalletRequestDTO) -> None:
        address = Address(data.address)

        logger.info("Checking if wallet with given address already exists...")

        if await self._wallet_gateway.read(address=address.value):
            raise WalletAlreadyExistsException(address=address)

        logger.info("Getting sepolia asset record from database...")

        sepolia_asset = await self._asset_gateway.read(network_type=AssetNetworkTypeEnum.SEPOLIA)

        logger.info("Importing wallet...")

        entity: Wallet = self._wallet_service.create_wallet(
            user_id=EntityId(data.user_id),
            asset_id=EntityId(sepolia_asset["id"]),
            address=Address(data.address),
            raw_private_key=RawPrivateKey(data.private_key),
            balance=Balance(data.balance),
            created_at=Timestamp(data.created_at),
        )

        self._wallet_gateway.add(entity)

        await self._flusher.flush()

        logger.info("Importing transaction history for imported wallet...")

        transactions: list[Transaction] = [
            self._transaction_service.create_transaction(
                wallet_id=entity.id_,
                from_address=Address(t.from_address),
                to_address=Address(t.to_address),
                value=TransactionValue(t.value),
                transaction_hash=TransactionHash(t.hash),
                transaction_fee=TransactionFee(t.transaction_fee),
                transaction_status=TransactionStatus(t.transaction_status),
                created_at=Timestamp(t.created_at),
            ) for t in data.transactions
        ]

        self._transaction_gateway.add(transactions=transactions)

        await self._transaction_manager.commit()

        wallet = await self._wallet_gateway.read(wallet_id=entity.id_.value)

        logger.info("Emitting event rest_api.save_wallet...")

        await self._event_publisher.save_wallet(
            SaveWalletEventDTO(
                user_id=wallet["user_id"],
                wallet_id=wallet["id"],
                address=wallet["address"],
                balance=wallet["balance"] / (10 ** wallet["asset"]["decimals"]),
                asset_symbol=wallet["asset"]["symbol"],
            )
        )
