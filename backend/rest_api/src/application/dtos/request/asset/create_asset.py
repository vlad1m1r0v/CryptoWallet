from dataclasses import dataclass
from typing import Optional

from src.domain.enums import AssetNetworkTypeEnum, AssetTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateAssetRequestDTO:
    name: str
    symbol: str
    decimals: int
    network: AssetNetworkTypeEnum
    asset_type: AssetTypeEnum
    contract_address: Optional[str] = None
