from src.domain.value_objects import (
    Timestamp,
    TransactionStatus,
    TransactionHash
)

from src.application.ports.transaction import TransactionManager
from src.application.ports.gateways import TransactionGateway
from src.application.dtos.request import UpdateTransactionRequestDTO

class CompleteTransactionInteractor:
    def __init__(
            self,
            transaction_gateway: TransactionGateway,
            transaction_manager: TransactionManager,
    ) -> None:
        self._transaction_gateway = transaction_gateway
        self._transaction_manager = transaction_manager

    async def __call__(self, data: UpdateTransactionRequestDTO) -> None:
        await self._transaction_gateway.update_many(
            created_at=Timestamp(data.created_at),
            status=TransactionStatus(data.transaction_status),
            tx_hash=TransactionHash(data.hash),
        )

        await self._transaction_manager.commit()
