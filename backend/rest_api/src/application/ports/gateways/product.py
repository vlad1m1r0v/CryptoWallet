from abc import abstractmethod
from typing import Protocol

from src.domain.value_objects import EntityId
from src.domain.entities import Product

from src.application.dtos.response import ProductResponseDTO

class ProductGateway(Protocol):
    @abstractmethod
    def add(self, product: Product) -> Product:
        ...

    @abstractmethod
    async def read_by_id(self, product_id: EntityId) -> ProductResponseDTO:
        ...

    @abstractmethod
    async def get_products(self) -> list[ProductResponseDTO]:
        ...