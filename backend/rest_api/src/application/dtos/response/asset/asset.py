from typing import TypedDict, Optional
from uuid import UUID

from src.domain.enums import (
    AssetNetworkTypeEnum,
    AssetTypeEnum,
)


class AssetResponseDTO(TypedDict):
    id: UUID
    name: str
    symbol: str
    decimals: int
    network: AssetNetworkTypeEnum
    asset_type: AssetTypeEnum
    contract_address: Optional[str]
