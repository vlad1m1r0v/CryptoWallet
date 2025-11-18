from src.domain.entities import Asset as AssetE

from src.application.dtos.response import AssetResponseDTO

from src.infrastructure.persistence.database.models import Asset as AssetM


class AssetMapper:
    @staticmethod
    def to_model(entity: AssetE) -> AssetM:
        return AssetM(
            id=entity.id_.value,
            name=entity.asset_name.value,
            symbol=entity.asset_symbol.value,
            network=entity.asset_network_type.value,
            asset_type=entity.asset_type.value,
            decimals=entity.decimals.value,
            contract_address=entity.contract_address.value if entity.contract_address else None
        )

    @staticmethod
    def to_dto(model: AssetM) -> AssetResponseDTO:
        return AssetResponseDTO(
            id=model.id,
            name=model.name,
            symbol=model.symbol,
            network=model.network,
            asset_type=model.asset_type,
            decimals=model.decimals,
            contract_address=model.contract_address
        )
