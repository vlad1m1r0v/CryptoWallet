from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload

from src.domain.entities import Product
from src.domain.value_objects import EntityId

from src.application.dtos.response import ProductResponseDTO
from src.application.ports.gateways import ProductGateway

from src.infrastructure.persistence.database.models import (
    Product as ProductM,
    Wallet as WalletM
)
from src.infrastructure.persistence.database.mappers import ProductMapper


class SqlaProductGateway(ProductGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, product: Product) -> Product:
        product_m = ProductMapper.to_model(product)
        self._session.add(product_m)
        return product

    async def get_product(self, product_id: EntityId) -> ProductResponseDTO:
        stmt = (
            select(ProductM)
            .options(
                joinedload(ProductM.wallet)
                .joinedload(WalletM.asset))
            .where(ProductM.id == product_id.value)
        )

        result = await self._session.execute(stmt)
        model: ProductM = result.scalar_one()
        return ProductMapper.to_dto(model)

    async def read_by_id(self, product_id: EntityId) -> Product | None:
        stmt = select(ProductM).where(ProductM.id == product_id.value)
        result = await self._session.execute(stmt)
        model: ProductM | None = result.scalar_one_or_none()
        if not model:
            return None
        return ProductMapper.to_entity(model)

    async def get_products(self) -> list[ProductResponseDTO]:
        stmt = (
            select(ProductM)
            .options(
                joinedload(ProductM.wallet)
                .joinedload(WalletM.asset)
            )
            .order_by(desc(ProductM.created_at))
        )

        result = await self._session.execute(stmt)
        models: Sequence[ProductM] = result.scalars().all()
        return ProductMapper.to_dto_m2m(models)
