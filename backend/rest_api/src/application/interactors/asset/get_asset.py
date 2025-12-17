import logging

from src.domain.enums import AssetNetworkTypeEnum

from src.application.ports.gateways import AssetGateway
from src.application.dtos.response import AssetResponseDTO

logger = logging.getLogger(__name__)


class GetAssetInteractor:
    def __init__(
            self,
            asset_gateway: AssetGateway
    ):
        self._asset_gateway = asset_gateway

    async def __call__(self) -> AssetResponseDTO | None:
        return await self._asset_gateway.read(network_type=AssetNetworkTypeEnum.SEPOLIA)
