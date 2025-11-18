from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.domain.entities import Product

from src.application.dtos.response import ProductResponseDTO


class ProductGateway(Protocol):
    @abstractmethod
    def add(self, product: Product) -> None:
        ...

    @abstractmethod
    async def read(self, product_id: UUID) -> ProductResponseDTO | None:
        ...

    @abstractmethod
    async def list(self) -> list[ProductResponseDTO]:
        ...
