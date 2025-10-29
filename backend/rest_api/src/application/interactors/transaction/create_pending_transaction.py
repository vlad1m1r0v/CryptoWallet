from typing import TypedDict
from decimal import Decimal

from src.domain.enums.transaction import TransactionStatusEnum

from src.domain.value_objects.transaction.hash import TransactionHash
from src.domain.value_objects.transaction.status import TransactionStatus
from src.domain.value_objects.transaction.fee import TransactionFee
from src.domain.value_objects.transaction.value import TransactionValue
from src.domain.value_objects.wallet.address import Address

from src.domain.entities.transaction import Transaction

from src.domain.services.transaction import TransactionService

from src.application.ports.transaction.transaction_manager import TransactionManager

from src.application.ports.gateways.wallet import WalletGateway
from src.application.ports.gateways.transaction import TransactionGateway


class TransactionDTO(TypedDict):
    hash: str
    from_address: str
    to_address: str
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum


class CreatePendingTransactionInteractor:
    def __init__(
            self,
            wallet_gateway: WalletGateway,
            transaction_gateway: TransactionGateway,
            transaction_service: TransactionService,
            transaction_manager: TransactionManager,
    ) -> None:
        self._wallet_gateway = wallet_gateway
        self._transaction_gateway = transaction_gateway
        self._transaction_service = transaction_service
        self._transaction_manager = transaction_manager

    async def __call__(self, data: TransactionDTO) -> None:
        transactions: list[Transaction] = []

        from_wallet = await self._wallet_gateway.read_by_address(Address(data["from_address"]))

        if from_wallet:
            transaction = self._transaction_service.create_transaction(
                wallet_id=from_wallet.id_,
                transaction_hash=TransactionHash(data["hash"]),
                from_address=Address(data["from_address"]),
                to_address=Address(data["to_address"]),
                value=TransactionValue(data["value"]),
                transaction_status=TransactionStatus(data["transaction_status"]),
                transaction_fee=TransactionFee(data["transaction_fee"]),
            )

            transactions.append(transaction)

        to_wallet = await self._wallet_gateway.read_by_address(Address(data["to_address"]))

        if to_wallet:
            transaction = self._transaction_service.create_transaction(
                wallet_id=to_wallet.id_,
                transaction_hash=TransactionHash(data["hash"]),
                from_address=Address(data["from_address"]),
                to_address=Address(data["to_address"]),
                value=TransactionValue(data["value"]),
                transaction_status=TransactionStatus(data["transaction_status"]),
                transaction_fee=TransactionFee(data["transaction_fee"]),
            )

            transactions.append(transaction)

        self._transaction_gateway.add_many(transactions)

        await self._transaction_manager.commit()
