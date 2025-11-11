from typing import Optional
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.domain.enums import TransactionStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePendingTransactionRequestDTO:
    payment_order_id: Optional[UUID] = None
    return_order_id: Optional[UUID] = None
    hash: str
    from_address: str
    to_address: str
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum
