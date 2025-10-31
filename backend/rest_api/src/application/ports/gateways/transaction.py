from typing import Protocol, List, Optional
from abc import abstractmethod
from enum import StrEnum

from src.domain.value_objects.shared.entity_id import EntityId
from src.domain.value_objects.shared.timestamp import Timestamp
from src.domain.value_objects.transaction.hash import TransactionHash
from src.domain.value_objects.transaction.status import TransactionStatus

from src.domain.entities.transaction import Transaction

from src.application.enums.sort_order import SortOrderEnum

from src.application.dtos.response.paginated_response import PaginatedResult
from src.application.dtos.response.transactions_list import TransactionListItemDTO


class SortFieldEnum(StrEnum):
    CREATED_AT = "created_at"
    STATUS = "status"
    TRANSACTION_FEE = "transaction_fee"


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
            sort_by: Optional[SortFieldEnum] = SortFieldEnum.CREATED_AT,
            order: Optional[SortOrderEnum] = SortOrderEnum.ASC,
            page: Optional[int] = 1
    ) -> PaginatedResult[TransactionListItemDTO]:
        ...
