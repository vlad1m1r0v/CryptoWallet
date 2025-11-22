from typing import TypedDict
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from src.domain.enums import TransactionStatusEnum


class TransactionResponseAssetDTO(TypedDict):
    symbol: str
    decimals: int


class TransactionResponseWalletDTO(TypedDict):
    user_id: UUID
    asset: TransactionResponseAssetDTO
    address: str


class TransactionResponseDTO(TypedDict):
    id: UUID
    transaction_hash: str
    from_address: str
    to_address: str
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum
    created_at: datetime
    wallet: TransactionResponseWalletDTO
