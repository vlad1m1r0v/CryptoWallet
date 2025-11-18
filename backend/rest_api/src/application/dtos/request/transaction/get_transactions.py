from dataclasses import dataclass
from typing import Optional, Literal
from uuid import UUID

from src.application.enums import SortOrderEnum

TransactionSortField = Literal["created_at", "status", "transaction_fee"]

@dataclass(frozen=True, slots=True, kw_only=True)
class GetTransactionsRequestDTO:
    page: Optional[int] = 1
    wallet_id: UUID
    sort: Optional[TransactionSortField] = "created_at"
    order: Optional[SortOrderEnum] = SortOrderEnum.DESC
