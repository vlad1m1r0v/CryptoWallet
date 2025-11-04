from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.gateways import AssetGateway

from src.domain.entities import Asset as AssetE
from src.domain.enums import AssetNetworkTypeEnum

from src.infrastructure.persistence.database.mappers import AssetMapper
from src.infrastructure.persistence.database.models import Asset as AssetM


class SqlaAssetGateway(AssetGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def read_by_network_type(self, network_type: AssetNetworkTypeEnum) -> AssetE:
        stmt = select(AssetM).where(AssetM.network == network_type)
        result = await self._session.execute(stmt)
        asset_m: AssetM = result.scalar_one()

        return AssetMapper.to_entity(asset_m)