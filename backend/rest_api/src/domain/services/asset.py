from typing import Optional

from src.domain.entities import Asset

from src.domain.ports import IdGenerator

from src.domain.value_objects import (
    AssetName,
    AssetSymbol,
    AssetNetworkType,
    AssetType,
    Decimals,
    Address
)


class AssetService:
    def __init__(
            self,
            id_generator: IdGenerator
    ) -> None:
        self._id_generator = id_generator

    def create_asset(
            self,
            asset_name: AssetName,
            asset_symbol: AssetSymbol,
            asset_network_type: AssetNetworkType,
            asset_type: AssetType,
            decimals: Decimals,
            contract_address: Optional[Address] = None,
    ) -> Asset:
        asset_id = self._id_generator()

        return Asset(
            id_=asset_id,
            asset_name=asset_name,
            asset_symbol=asset_symbol,
            asset_network_type=asset_network_type,
            asset_type=asset_type,
            decimals=decimals,
            contract_address=contract_address
        )
