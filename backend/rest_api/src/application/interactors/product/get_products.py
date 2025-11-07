from src.application.dtos.response import ProductResponseDTO
from src.application.ports.gateways import ProductGateway


class GetProductsInteractor:
    def __init__(self, product_gateway: ProductGateway):
        self._product_gateway = product_gateway

    async def __call__(self) -> list[ProductResponseDTO]:
        return await self._product_gateway.get_products()
