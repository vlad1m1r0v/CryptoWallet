from datetime import datetime
from decimal import Decimal
from typing import TypedDict, List
from uuid import UUID

from src.domain.enums.asset import AssetNetworkTypeEnum
from src.domain.enums.transaction import TransactionStatusEnum

from src.domain.value_objects.shared.entity_id import EntityId
from src.domain.value_objects.shared.timestamp import Timestamp

from src.domain.value_objects.wallet.raw_private_key import RawPrivateKey
from src.domain.value_objects.wallet.address import Address
from src.domain.value_objects.wallet.balance import Balance

from src.domain.value_objects.transaction.value import TransactionValue
from src.domain.value_objects.transaction.hash import TransactionHash
from src.domain.value_objects.transaction.status import TransactionStatus
from src.domain.value_objects.transaction.fee import TransactionFee

from src.domain.exceptions.wallet import WalletAlreadyExistsException

from src.domain.entities.wallet import Wallet
from src.domain.entities.transaction import Transaction

from src.domain.services.wallet import WalletService
from src.domain.services.transaction import TransactionService

from src.application.ports.gateways.asset import AssetGateway
from src.application.ports.gateways.wallet import WalletGateway
from src.application.ports.gateways.transaction import TransactionGateway

from src.application.ports.transaction.transaction_manager import TransactionManager
from src.application.ports.transaction.flusher import Flusher


class TransactionDTO(TypedDict):
    hash: str
    from_address: str
    to_address: str
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum
    created_at: datetime


class WalletWithTransactionsDTO(TypedDict):
    user_id: UUID
    address: str
    private_key: str
    balance: Decimal
    created_at: datetime
    transactions: List[TransactionDTO]


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

    async def __call__(self, data: WalletWithTransactionsDTO) -> None:
        address = Address(data["address"])

        if await self._wallet_gateway.read_by_address(address=address):
            raise WalletAlreadyExistsException(address=address)

        sepolia_asset = await self._asset_gateway.read_by_network_type(AssetNetworkTypeEnum.SEPOLIA)

        wallet: Wallet = self._wallet_service.create_wallet(
            user_id=EntityId(data["user_id"]),
            asset_id=sepolia_asset.id_,
            address=Address(data["address"]),
            raw_private_key=RawPrivateKey(data["private_key"]),
            balance=Balance(data["balance"]),
            created_at=Timestamp(data["created_at"]),
        )

        self._wallet_gateway.add(wallet)

        await self._flusher.flush()

        transactions: list[Transaction] = [
            self._transaction_service.create_transaction(
                wallet_id=wallet.id_,
                from_address=Address(t["from_address"]),
                to_address=Address(t["to_address"]),
                value=TransactionValue(t["value"]),
                transaction_hash=TransactionHash(t["hash"]),
                transaction_fee=TransactionFee(t["transaction_fee"]),
                transaction_status=TransactionStatus(t["transaction_status"]),
                created_at=Timestamp(t["created_at"]),
            ) for t in data["transactions"]
        ]

        self._transaction_gateway.add_many(transactions)

        await self._transaction_manager.commit()