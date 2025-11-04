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
from src.application.dtos.request import (
    SaveImportWalletRequestDTO
)


class SaveImportWalletInteractor:
    def __init__(
            self,
            wallet_service: WalletService,
            transaction_service: TransactionService,
            asset_gateway: AssetGateway,
            wallet_gateway: WalletGateway,
            transaction_gateway: TransactionGateway,
            transaction_manager: TransactionManager,
            flusher: Flusher
    ) -> None:
        self._wallet_service = wallet_service
        self._transaction_service = transaction_service

        self._asset_gateway = asset_gateway
        self._wallet_gateway = wallet_gateway
        self._transaction_gateway = transaction_gateway

        self._transaction_manager = transaction_manager
        self._flusher = flusher

    async def __call__(self, data: SaveImportWalletRequestDTO) -> None:
        address = Address(data.address)

        if await self._wallet_gateway.read_by_address(address=address):
            raise WalletAlreadyExistsException(address=address)

        sepolia_asset = await self._asset_gateway.read_by_network_type(AssetNetworkTypeEnum.SEPOLIA)

        wallet: Wallet = self._wallet_service.create_wallet(
            user_id=EntityId(data.user_id),
            asset_id=sepolia_asset.id_,
            address=Address(data.address),
            raw_private_key=RawPrivateKey(data.private_key),
            balance=Balance(data.balance),
            created_at=Timestamp(data.created_at),
        )

        self._wallet_gateway.add(wallet)

        await self._flusher.flush()

        transactions: list[Transaction] = [
            self._transaction_service.create_transaction(
                wallet_id=wallet.id_,
                from_address=Address(t.from_address),
                to_address=Address(t.to_address),
                value=TransactionValue(t.value),
                transaction_hash=TransactionHash(t.hash),
                transaction_fee=TransactionFee(t.transaction_fee),
                transaction_status=TransactionStatus(t.transaction_status),
                created_at=Timestamp(t.created_at),
            ) for t in data.transactions
        ]

        self._transaction_gateway.add_many(transactions)

        await self._transaction_manager.commit()
