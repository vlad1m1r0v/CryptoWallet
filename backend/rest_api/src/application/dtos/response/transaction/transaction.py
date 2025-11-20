from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from src.domain.enums import TransactionStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class TransactionResponseAssetDTO:
    symbol: str
    decimals: int


@dataclass(frozen=True, slots=True, kw_only=True)
class TransactionResponseWalletDTO:
    user_id: UUID
    asset: TransactionResponseAssetDTO
    address: str

@dataclass(frozen=True, slots=True, kw_only=True)
class TransactionResponseDTO:
    id: UUID
    transaction_hash: str
    from_address: str
    to_address: str
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum
    created_at: datetime
    wallet: TransactionResponseWalletDTO