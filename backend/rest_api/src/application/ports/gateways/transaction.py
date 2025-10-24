from abc import abstractmethod
from typing import Protocol, List

from src.domain.entities.transaction import Transaction


class TransactionGateway(Protocol):
    @abstractmethod
    def add_many(self, transactions: List[Transaction]) -> List[Transaction]:
        ...