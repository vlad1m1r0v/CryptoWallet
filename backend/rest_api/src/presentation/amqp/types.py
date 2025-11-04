from datetime import datetime
from decimal import Decimal
from typing import TypedDict
from uuid import UUID

from src.domain.enums import TransactionStatusEnum


class SaveCreateWalletRequestDict(TypedDict):
    user_id: UUID
    address: str
    private_key: str
    balance: Decimal
    created_at: datetime


class SaveImportWalletRequestTransactionDict(TypedDict):
    hash: str
    from_address: str
    to_address: str
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum
    created_at: datetime


class SaveImportWalletRequestDict(TypedDict):
    user_id: UUID
    address: str
    private_key: str
    balance: Decimal
    created_at: datetime
    transactions: list[SaveImportWalletRequestTransactionDict]


class CreatePendingTransactionRequestDict(TypedDict):
    hash: str
    from_address: str
    to_address: str
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum


class UpdateTransactionRequestDict(TypedDict):
    hash: str
    transaction_status: TransactionStatusEnum
    created_at: datetime
