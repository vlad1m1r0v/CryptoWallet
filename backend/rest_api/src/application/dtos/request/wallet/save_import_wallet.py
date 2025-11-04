from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from src.domain.enums import TransactionStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class SaveImportWalletRequestTransactionDTO:
    hash: str
    from_address: str
    to_address: str
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum
    created_at: datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class SaveImportWalletRequestDTO:
    user_id: UUID
    address: str
    private_key: str
    balance: Decimal
    created_at: datetime
    transactions: list[SaveImportWalletRequestTransactionDTO]
