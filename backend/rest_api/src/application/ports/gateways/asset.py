from abc import abstractmethod
from typing import Protocol

from src.domain.enums import AssetNetworkTypeEnum

from src.domain.entities import Asset


class AssetGateway(Protocol):
    @abstractmethod
    async def read_by_network_type(self, network_type: AssetNetworkTypeEnum) -> Asset:
        ...