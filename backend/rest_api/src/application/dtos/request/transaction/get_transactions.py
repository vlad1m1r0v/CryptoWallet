from dataclasses import dataclass
from typing import Optional, Literal
from uuid import UUID

from src.application.enums import SortOrderEnum

TransactionSortField = Literal["created_at", "transaction_status", "transaction_fee"]

@dataclass(frozen=True, slots=True, kw_only=True)
class GetTransactionsRequestDTO:
    page: Optional[int] = 1
    per_page: Optional[int] = 20
    user_id: UUID
    wallet_id: UUID
    sort: Optional[TransactionSortField] = "created_at"
    order: Optional[SortOrderEnum] = SortOrderEnum.DESC
