from typing import Protocol, List, Optional
from abc import abstractmethod

from src.domain.value_objects import (
    EntityId,
    Timestamp,
    TransactionHash,
    TransactionStatus
)

from src.domain.entities import Transaction

from src.application.enums import (
    SortOrderEnum,
    TransactionSortFieldEnum
)

from src.application.dtos.response import (
    PaginatedResponseDTO,
    TransactionsListItemResponseDTO
)


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

    @abstractmethod
    async def get_transactions(
            self,
            wallet_id: EntityId,
            sort_by: Optional[TransactionSortFieldEnum] = TransactionSortFieldEnum.CREATED_AT,
            order: Optional[SortOrderEnum] = SortOrderEnum.ASC,
            page: Optional[int] = 1
    ) -> PaginatedResponseDTO[TransactionsListItemResponseDTO]:
        ...
