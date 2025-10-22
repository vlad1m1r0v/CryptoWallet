from typing import Optional

from src.domain.entities.base import Entity

from src.domain.value_objects.shared.entity_id import EntityId

from src.domain.value_objects.wallet.address import Address

from src.domain.value_objects.asset.asset_name import AssetName
from src.domain.value_objects.asset.asset_symbol import AssetSymbol
from src.domain.value_objects.asset.asset_network_type import AssetNetworkType
from src.domain.value_objects.asset.asset_type import AssetType
from src.domain.value_objects.asset.decimals import Decimals


class Asset(Entity[EntityId]):
    def __init__(
            self,
            *,
            id_: EntityId,
            asset_name: AssetName,
            asset_symbol: AssetSymbol,
            asset_network_type: AssetNetworkType,
            asset_type: AssetType,
            decimals: Decimals,
            contract_address: Optional[Address] = None,

    ) -> None:
        super().__init__(id_=id_)
        self.asset_name = asset_name
        self.asset_symbol = asset_symbol
        self.asset_network_type = asset_network_type
        self.asset_type = asset_type
        self.decimals = decimals
        self.contract_address = contract_address
