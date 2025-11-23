import logging

from src.domain.value_objects import (
    AssetName,
    AssetSymbol,
    AssetNetworkType,
    AssetType,
    Decimals,
    Address
)
from src.domain.services import AssetService

from src.application.ports.gateways import AssetGateway
from src.application.ports.transaction import TransactionManager
from src.application.dtos.request import CreateAssetRequestDTO

logger = logging.getLogger(__name__)


class CreateAssetInteractor:
    def __init__(
            self,
            transaction_manager: TransactionManager,
            asset_gateway: AssetGateway,
            asset_service: AssetService
    ):
        self._transaction_manager = transaction_manager
        self._asset_gateway = asset_gateway
        self._asset_service = asset_service

    async def __call__(self, dto: CreateAssetRequestDTO) -> None:
        logger.info("Inserting new asset record into database...")

        entity = self._asset_service.create_asset(
            asset_name=AssetName(dto.name),
            asset_symbol=AssetSymbol(dto.symbol),
            asset_network_type=AssetNetworkType(dto.network),
            asset_type=AssetType(dto.asset_type),
            decimals=Decimals(dto.decimals),
            contract_address=Address(dto.contract_address) if dto.contract_address else None
        )

        self._asset_gateway.add(asset=entity)
        await self._transaction_manager.commit()
