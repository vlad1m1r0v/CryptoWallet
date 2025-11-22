import logging

from src.application.dtos.response import ProductResponseDTO
from src.application.ports.gateways import ProductGateway

logger = logging.getLogger(__name__)

class GetProductsInteractor:
    def __init__(self, product_gateway: ProductGateway):
        self._product_gateway = product_gateway

    async def __call__(self) -> list[ProductResponseDTO]:
        logger.info("Getting list of products from database...")

        return await self._product_gateway.list()
