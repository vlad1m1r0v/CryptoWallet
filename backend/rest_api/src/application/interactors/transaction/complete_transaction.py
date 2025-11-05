from src.domain.value_objects import (
    Timestamp,
    TransactionStatus,
    TransactionHash,
    Balance
)

from src.application.ports.transaction import TransactionManager
from src.application.ports.gateways import (
    TransactionGateway,
    WalletGateway
)
from src.application.dtos.request import UpdateTransactionRequestDTO


class CompleteTransactionInteractor:
    def __init__(
            self,
            transaction_gateway: TransactionGateway,
            wallet_gateway: WalletGateway,
            transaction_manager: TransactionManager,
    ) -> None:
        self._transaction_gateway = transaction_gateway
        self._wallet_gateway = wallet_gateway
        self._transaction_manager = transaction_manager

    async def __call__(self, data: UpdateTransactionRequestDTO) -> None:
        await self._transaction_gateway.update_many(
            created_at=Timestamp(data.created_at),
            status=TransactionStatus(data.transaction_status),
            tx_hash=TransactionHash(data.hash),
        )

        tx = await self._transaction_gateway.get_one_by_hash(TransactionHash(data.hash))

        from_wallet = await self._wallet_gateway.read_by_address(tx.from_address)

        if from_wallet:
            await self._wallet_gateway.decrement_balance(
                wallet_id=from_wallet.id_,
                amount=Balance(tx.transaction_fee.value + tx.value.value)
            )

        to_wallet = await self._wallet_gateway.read_by_address(tx.to_address)

        if to_wallet:
            await self._wallet_gateway.increment_balance(
                wallet_id=to_wallet.id_,
                amount=Balance(tx.transaction_fee.value + tx.value.value)
            )

        await self._transaction_manager.commit()
