from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.enums import AssetNetworkTypeEnum

from src.application.dtos.response import AssetResponseDTO
from src.application.ports.gateways import AssetGateway

from src.infrastructure.persistence.database.models import Asset as AssetM
from src.infrastructure.persistence.database.mappers import AssetMapper


class SqlaAssetGateway(AssetGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def read(self, network_type: AssetNetworkTypeEnum) -> AssetResponseDTO | None:
        stmt = select(AssetM).where(AssetM.network == network_type)
        result = await self._session.execute(stmt)
        asset_m: AssetM = result.scalar_one_or_none()

        if not asset_m:
            return None

        return AssetMapper.to_dto(asset_m)
