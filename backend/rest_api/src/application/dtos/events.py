from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from typing import Optional
from enum import StrEnum, auto

from src.domain.enums import (
    OrderStatusEnum,
    TransactionStatusEnum
)


@dataclass(frozen=True, slots=True, kw_only=True)
class SaveUserEventDTO:
    user_id: UUID
    username: str


@dataclass(frozen=True, slots=True, kw_only=True)
class GiveChatAccessEventDTO:
    user_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateUserEventDTO:
    user_id: UUID
    username: Optional[str] = None
    avatar_filename: Optional[str] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteAvatarEventDTO:
    user_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateWalletEventDTO:
    user_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class ImportWalletEventDTO:
    user_id: UUID
    private_key: str


@dataclass(frozen=True, slots=True, kw_only=True)
class SaveWalletEventDTO:
    user_id: UUID
    wallet_id: UUID
    address: str
    balance: Decimal
    asset_symbol: str


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateWalletEventDTO:
    user_id: UUID
    wallet_id: UUID
    balance: Decimal


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateTransactionEventDTO:
    private_key: str
    to_address: str
    amount: Decimal
    payment_order_id: Optional[UUID] = None
    return_order_id: Optional[UUID] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class SavePendingTransactionEventDTO:
    user_id: UUID
    transaction_id: UUID
    transaction_hash: str
    from_address: str
    to_address: str
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum
    asset_symbol: str


class TransactionTypeEnum(StrEnum):
    INCOME = auto()
    EXPENSE = auto()


@dataclass(frozen=True, slots=True, kw_only=True)
class CompleteTransactionEventDTO:
    user_id: UUID
    transaction_id: UUID
    transaction_hash: str
    from_address: str
    to_address: str
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum
    wallet_address: str
    transaction_type: TransactionTypeEnum = field(init=False)
    asset_symbol: str
    created_at: datetime

    def __post_init__(self):
        object.__setattr__(
            self,
            "transaction_type",
            TransactionTypeEnum.INCOME
            if self.to_address == self.wallet_address
            else TransactionTypeEnum.EXPENSE
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class RequestFreeETHEventDTO:
    user_id: UUID
    to_address: str


@dataclass(frozen=True, slots=True, kw_only=True)
class SaveProductEventDTO:
    product_id: UUID
    name: str
    price: Decimal
    photo_filename: str
    asset_symbol: str
    wallet_address: str
    created_at: datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateOrderEventDTO:
    order_id: UUID
    status: OrderStatusEnum
    created_at: datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class PayOrderEventDTO:
    user_id: UUID
    order_id: UUID
    transaction_hash: str


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateOrderEventDTO:
    user_id: UUID
    order_id: UUID
    status: Optional[OrderStatusEnum] = None
    payment_transaction_hash: Optional[str] = None
    return_transaction_hash: Optional[str] = None