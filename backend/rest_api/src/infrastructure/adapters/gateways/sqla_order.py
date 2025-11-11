from typing import Sequence

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, aliased

from src.domain.entities import Order
from src.domain.value_objects import EntityId

from src.application.dtos.response import OrderResponseDTO
from src.application.ports.gateways import OrderGateway

from src.infrastructure.persistence.database.mappers import OrderMapper
from src.infrastructure.persistence.database.models import (
    Wallet as WalletM,
    Product as ProductM,
    Order as OrderM
)


class SqlaOrderGateway(OrderGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, order: Order) -> Order:
        model = OrderMapper.to_model(order)
        self._session.add(model)
        return model

    async def get_order(self, order_id: EntityId) -> OrderResponseDTO:
        stmt = (
            select(OrderM)
            .options(
                # Order -> Product -> Wallet -> Asset
                joinedload(OrderM.product)
                .joinedload(ProductM.wallet)
                .joinedload(WalletM.asset),
                # Order -> Payment Transaction
                joinedload(OrderM.payment_transaction),
                # Order -> Return Transaction
                joinedload(OrderM.return_transaction),
                # Order -> Wallet
                joinedload(OrderM.wallet)
            )
            .where(OrderM.id == order_id.value)
        )

        result = await self._session.execute(stmt)
        model: OrderM = result.scalar_one()
        return OrderMapper.to_dto(model)

    async def get_orders(self, user_id: EntityId) -> list[OrderResponseDTO]:
        wallet_alias = aliased(WalletM)

        stmt = (
            select(OrderM)
            .options(
                # Order -> Product -> Wallet -> Asset
                joinedload(OrderM.product)
                .joinedload(ProductM.wallet.of_type(wallet_alias))
                .joinedload(wallet_alias.asset),
                # Order -> Product -> Wallet -> User
                joinedload(OrderM.product)
                .joinedload(ProductM.wallet.of_type(wallet_alias))
                .joinedload(wallet_alias.user),
                # Order -> Payment Transaction
                joinedload(OrderM.payment_transaction),
                # Order -> Return Transaction
                joinedload(OrderM.return_transaction),
                # Order -> Wallet
                joinedload(OrderM.wallet)
            )
            .where(and_(wallet_alias.user_id == user_id.value))
        )
        result = await self._session.execute(stmt)
        model: Sequence[OrderM] = result.scalars().all()
        return OrderMapper.to_dto_m2m(model)
