from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class WalletResponseAssetDTO:
    symbol: str
    decimals: int


@dataclass(frozen=True, slots=True, kw_only=True)
class WalletResponseDTO:
    id: UUID
    address: str
    balance: Decimal
    asset: WalletResponseAssetDTO