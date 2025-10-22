from abc import abstractmethod
from typing import Protocol

from src.domain.enums.asset import AssetNetworkTypeEnum

from src.domain.entities.asset import Asset


class AssetGateway(Protocol):
    @abstractmethod
    async def get_asset_by_network_type(self, network_type: AssetNetworkTypeEnum) -> Asset:
        ...