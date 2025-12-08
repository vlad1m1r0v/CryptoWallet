from typing import TypedDict, NotRequired
from decimal import Decimal
from datetime import datetime
from enum import StrEnum, auto
from uuid import UUID


class SaveUserDict(TypedDict):
    user_id: UUID
    username: str


class UpdateUserDict(TypedDict):
    user_id: UUID
    username: NotRequired[str]
    avatar_filename: NotRequired[str]


class DeleteAvatarDict(TypedDict):
    user_id: UUID


class SaveWalletDict(TypedDict):
    user_id: UUID
    wallet_id: UUID
    address: str
    balance: Decimal
    asset_symbol: str


class UpdateWalletDict(TypedDict):
    user_id: UUID
    wallet_id: UUID
    balance: Decimal


class TransactionStatusEnum(StrEnum):
    SUCCESSFUL = auto()
    PENDING = auto()
    FAILED = auto()


class SavePendingTransactionDict(TypedDict):
    user_id: UUID
    transaction_id: UUID
    transaction_hash: str
    from_address: str
    to_address: str
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum
    wallet_id: UUID
    wallet_address: str
    asset_symbol: str


class TransactionTypeEnum(StrEnum):
    INCOME = auto()
    EXPENSE = auto()


class CompleteTransactionDict(TypedDict):
    user_id: UUID
    wallet_address: str
    transaction_id: UUID
    transaction_hash: str
    from_address: str
    to_address: str
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum
    wallet_id: UUID
    wallet_address: str
    asset_symbol: str
    transaction_type: TransactionTypeEnum
    created_at: datetime


class RequestETHDict(TypedDict):
    user_id: UUID
    to_address: str


class SaveProductDict(TypedDict):
    product_id: UUID
    name: str
    price: Decimal
    photo_url: str
    asset_symbol: str
    wallet_address: str
    created_at: datetime

__all__ = [
    "SaveUserDict",
    "UpdateUserDict",
    "DeleteAvatarDict",
    "SaveWalletDict",
    "UpdateWalletDict",
    "SavePendingTransactionDict",
    "CompleteTransactionDict",
    "RequestETHDict"
]
