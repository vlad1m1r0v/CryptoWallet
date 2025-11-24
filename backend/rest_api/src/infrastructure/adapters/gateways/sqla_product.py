from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload

from src.domain.entities import Product

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

    def add(self, product: Product) -> None:
        product_m = ProductMapper.to_model(product)
        self._session.add(product_m)

    async def read(self, product_id: UUID) -> ProductResponseDTO | None:
        stmt = (
            select(ProductM)
            .options(
                joinedload(ProductM.wallet)
                .joinedload(WalletM.asset))
            .where(ProductM.id == product_id)
        )

        result = await self._session.execute(stmt)
        model: ProductM = result.scalar_one_or_none()

        if not model:
            return None

        return ProductMapper.to_dto(model=model)

    async def list(self) -> list[ProductResponseDTO]:
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
        return ProductMapper.to_dto(models=models)


