from src.domain.value_objects.shared.entity_id import EntityId

from src.domain.value_objects.wallet.address import Address

from src.domain.value_objects.asset.asset_name import AssetName
from src.domain.value_objects.asset.asset_symbol import AssetSymbol
from src.domain.value_objects.asset.asset_network_type import AssetNetworkType
from src.domain.value_objects.asset.asset_type import AssetType
from src.domain.value_objects.asset.decimals import Decimals

from src.domain.entities.asset import Asset as AssetE

from src.infrastructure.persistence.database.mappers.base import BaseMapper

from src.infrastructure.persistence.database.models.asset import Asset as AssetM


class AssetMapper(BaseMapper[AssetE, AssetM]):
    @staticmethod
    def to_entity(model: AssetM) -> AssetE:
        return AssetE(
            id_=EntityId(model.id),
            asset_name=AssetName(model.name),
            asset_symbol=AssetSymbol(model.symbol),
            asset_network_type=AssetNetworkType(model.network),
            asset_type=AssetType(model.asset_type),
            decimals=Decimals(model.decimals),
            contract_address=Address(model.contract_address) if model.contract_address else None

        )

    @staticmethod
    def to_model(asset: AssetE) -> AssetM:
        return AssetM(
            id=asset.id_.value,
            name=asset.asset_name.value,
            symbol=asset.asset_symbol.value,
            network=asset.asset_network_type.value,
            asset_type=asset.asset_type.value,
            decimals=asset.decimals.value,
            contract_address=asset.contract_address.value if asset.contract_address else None
        )
