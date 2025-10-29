from abc import abstractmethod
from typing import Protocol, List

from src.domain.value_objects.shared.timestamp import Timestamp
from src.domain.value_objects.transaction.hash import TransactionHash
from src.domain.value_objects.transaction.status import TransactionStatus

from src.domain.entities.transaction import Transaction


class TransactionGateway(Protocol):
    @abstractmethod
    def add_many(self, transactions: List[Transaction]) -> List[Transaction]:
        ...

    @abstractmethod
    async def update_many(
            self,
            created_at: Timestamp,
            tx_hash: TransactionHash,
            status: TransactionStatus,
    ) -> List[Transaction]:
        ...
