from datetime import datetime
from typing import TypedDict, Optional
from decimal import Decimal
from uuid import UUID

from src.domain.enums import OrderStatusEnum


class OrderResponseProductWalletAssetDTO(TypedDict):
    symbol: str
    decimals: int


class OrderResponseProductWalletDTO(TypedDict):
    asset: OrderResponseProductWalletAssetDTO
    address: str


class OrderResponseProductDTO(TypedDict):
    name: str
    price: Decimal
    photo_filename: str
    wallet: OrderResponseProductWalletDTO


class OrderResponseTransactionDTO(TypedDict):
    transaction_hash: str


class OrderResponseDTO(TypedDict):
    id: UUID
    product: OrderResponseProductDTO
    payment_transaction: Optional[OrderResponseTransactionDTO]
    return_transaction: Optional[OrderResponseTransactionDTO]
    status: OrderStatusEnum
    created_at: datetime
