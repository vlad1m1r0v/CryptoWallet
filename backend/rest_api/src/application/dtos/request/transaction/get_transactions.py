from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.application.enums import (
    TransactionSortFieldEnum,
    SortOrderEnum
)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetTransactionsRequestDTO:
    page: Optional[int] = 1
    wallet_id: UUID
    sort_by: TransactionSortFieldEnum
    order: SortOrderEnum
