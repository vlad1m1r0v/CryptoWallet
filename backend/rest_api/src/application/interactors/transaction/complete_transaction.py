from datetime import datetime
from typing import TypedDict

from src.domain.enums.transaction import TransactionStatusEnum

from src.domain.value_objects.shared.timestamp import Timestamp
from src.domain.value_objects.transaction.status import TransactionStatus
from src.domain.value_objects.transaction.hash import TransactionHash

from src.application.ports.transaction.transaction_manager import TransactionManager

from src.application.ports.gateways.transaction import TransactionGateway


class UpdateTransactionDTO(TypedDict):
    hash: str
    transaction_status: TransactionStatusEnum
    created_at: datetime


class CompleteTransactionInteractor:
    def __init__(
            self,
            transaction_gateway: TransactionGateway,
            transaction_manager: TransactionManager,
    ) -> None:
        self._transaction_gateway = transaction_gateway
        self._transaction_manager = transaction_manager

    async def __call__(self, data: UpdateTransactionDTO) -> None:
        await self._transaction_gateway.update_many(
            created_at=Timestamp(data['created_at']),
            status=TransactionStatus(data['transaction_status']),
            tx_hash=TransactionHash(data['hash']),
        )

        await self._transaction_manager.commit()
