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
    encrypted_private_key: bytes


class OrderResponseProductDTO(TypedDict):
    name: str
    price: Decimal
    photo_filename: str
    wallet: OrderResponseProductWalletDTO


class OrderResponseTransactionDTO(TypedDict):
    transaction_hash: str
    transaction_fee: Decimal


class OrderResponseWalletDTO(TypedDict):
    address: str


class OrderResponseDTO(TypedDict):
    id: UUID
    product: OrderResponseProductDTO
    wallet: OrderResponseWalletDTO
    payment_transaction: Optional[OrderResponseTransactionDTO]
    return_transaction: Optional[OrderResponseTransactionDTO]
    status: OrderStatusEnum
    created_at: datetime
