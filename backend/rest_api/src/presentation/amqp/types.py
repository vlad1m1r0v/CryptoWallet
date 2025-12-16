from datetime import datetime
from decimal import Decimal
from typing import TypedDict, Optional
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
    payment_order_id: Optional[UUID]
    return_order_id: Optional[UUID]
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


class OrderRequestDict(TypedDict):
    order_id: UUID


class IncrementTotalMessagesRequestDict(TypedDict):
    user_id: UUID
