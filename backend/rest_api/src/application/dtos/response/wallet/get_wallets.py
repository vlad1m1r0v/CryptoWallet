from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class WalletsListItemResponseAssetDTO:
    symbol: str
    decimals: int


@dataclass(frozen=True, slots=True, kw_only=True)
class WalletsListItemResponseDTO:
    id: UUID
    address: str
    balance: Decimal
    asset: WalletsListItemResponseAssetDTO