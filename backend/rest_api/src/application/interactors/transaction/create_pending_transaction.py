from src.domain.value_objects import (
    EntityId,
    TransactionHash,
    TransactionStatus,
    TransactionFee,
    TransactionValue,
    Address
)
from src.domain.entities import Transaction
from src.domain.services import TransactionService

from src.application.ports.transaction import (
    TransactionManager,
    Flusher
)
from src.application.ports.gateways import (
    WalletGateway,
    TransactionGateway,
    OrderGateway
)
from src.application.dtos.request import CreatePendingTransactionRequestDTO

class CreatePendingTransactionInteractor:
    def __init__(
            self,
            wallet_gateway: WalletGateway,
            transaction_gateway: TransactionGateway,
            order_gateway: OrderGateway,
            transaction_service: TransactionService,
            transaction_manager: TransactionManager,
            flusher: Flusher
    ) -> None:
        self._wallet_gateway = wallet_gateway
        self._transaction_gateway = transaction_gateway
        self._order_gateway = order_gateway
        self._transaction_service = transaction_service
        self._transaction_manager = transaction_manager
        self._flusher = flusher

    async def __call__(self, data: CreatePendingTransactionRequestDTO) -> None:
        transactions: list[Transaction] = []

        from_wallet = await self._wallet_gateway.read_by_address(Address(data.from_address))

        if from_wallet:
            transaction = self._transaction_service.create_transaction(
                wallet_id=from_wallet.id_,
                transaction_hash=TransactionHash(data.hash),
                from_address=Address(data.from_address),
                to_address=Address(data.to_address),
                value=TransactionValue(data.value),
                transaction_status=TransactionStatus(data.transaction_status),
                transaction_fee=TransactionFee(data.transaction_fee),
            )

            transactions.append(transaction)

        to_wallet = await self._wallet_gateway.read_by_address(Address(data.to_address))

        if to_wallet:
            transaction = self._transaction_service.create_transaction(
                wallet_id=to_wallet.id_,
                transaction_hash=TransactionHash(data.hash),
                from_address=Address(data.from_address),
                to_address=Address(data.to_address),
                value=TransactionValue(data.value),
                transaction_status=TransactionStatus(data.transaction_status),
                transaction_fee=TransactionFee(data.transaction_fee),
            )

            transactions.append(transaction)

        self._transaction_gateway.add_many(transactions)

        await self._flusher.flush()

        if data.payment_order_id:
            await self._order_gateway.update(
                order_id=EntityId(data.payment_order_id),
                payment_transaction_id=transactions[0].id_
            )

        if data.return_order_id:
            await self._order_gateway.update(
                order_id=EntityId(data.return_order_id),
                return_transaction_id=transactions[0].id_
            )

        await self._transaction_manager.commit()
