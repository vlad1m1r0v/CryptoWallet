from dataclasses import dataclass
from datetime import datetime

from src.domain.enums import TransactionStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateTransactionRequestDTO:
    hash: str
    transaction_status: TransactionStatusEnum
    created_at: datetime
