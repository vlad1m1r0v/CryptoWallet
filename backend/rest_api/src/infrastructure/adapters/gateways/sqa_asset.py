from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.gateways.asset import AssetGateway
from src.domain.entities.asset import Asset as AssetE
from src.domain.enums.asset import AssetNetworkTypeEnum
from src.domain.value_objects.shared.entity_id import EntityId
from src.domain.value_objects.asset.asset_name import AssetName
from src.domain.value_objects.asset.asset_symbol import AssetSymbol
from src.domain.value_objects.asset.asset_network_type import AssetNetworkType
from src.domain.value_objects.asset.asset_type import AssetType
from src.domain.value_objects.asset.decimals import Decimals
from src.domain.value_objects.wallet.address import Address

from src.infrastructure.persistence.database.models.asset import Asset as AssetM


class SqlaAssetGateway(AssetGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_asset_by_network_type(self, network_type: AssetNetworkTypeEnum) -> AssetE:
        stmt = select(AssetM).where(AssetM.network == network_type)
        result = await self._session.execute(stmt)
        orm_asset: AssetM = result.scalar_one()

        return AssetE(
            id_=EntityId(orm_asset.id),
            asset_name=AssetName(orm_asset.name),
            asset_symbol=AssetSymbol(orm_asset.symbol),
            asset_network_type=AssetNetworkType(orm_asset.network),
            asset_type=AssetType(orm_asset.asset_type),
            decimals=Decimals(orm_asset.decimals),
            contract_address=Address(orm_asset.contract_address) if orm_asset.contract_address else None
        )