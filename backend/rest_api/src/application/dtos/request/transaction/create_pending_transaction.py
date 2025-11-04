from dataclasses import dataclass
from decimal import Decimal

from src.domain.enums import TransactionStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePendingTransactionRequestDTO:
    hash: str
    from_address: str
    to_address: str
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum