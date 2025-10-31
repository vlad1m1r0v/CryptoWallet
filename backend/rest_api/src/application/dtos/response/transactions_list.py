from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from src.domain.enums.transaction import TransactionStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class AssetDTO:
    symbol: str
    decimals: int


@dataclass(frozen=True, slots=True, kw_only=True)
class WalletDTO:
    asset: AssetDTO

@dataclass(frozen=True, slots=True, kw_only=True)
class TransactionListItemDTO:
    id: UUID
    transaction_hash: str
    from_address: str
    to_address: str
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum
    created_at: datetime
    wallet: WalletDTO