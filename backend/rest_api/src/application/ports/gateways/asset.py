from abc import abstractmethod
from typing import Protocol

from src.domain.enums import AssetNetworkTypeEnum
from src.domain.entities import Asset

from src.application.dtos.response import AssetResponseDTO


class AssetGateway(Protocol):
    @abstractmethod
    async def read(self, network_type: AssetNetworkTypeEnum) -> AssetResponseDTO | None:
        ...

    @abstractmethod
    def add(self, asset: Asset) -> None:
        ...