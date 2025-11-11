from typing import Sequence, Optional, Any

from sqlalchemy import select, update, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, aliased, InstrumentedAttribute

from src.domain.entities import Order
from src.domain.value_objects import (
    EntityId,
    OrderStatus,
    TransactionHash
)

from src.application.dtos.response import OrderResponseDTO
from src.application.ports.gateways import OrderGateway

from src.infrastructure.persistence.database.mappers import OrderMapper
from src.infrastructure.persistence.database.models import (
    Transaction as TransactionM,
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

    async def get_order_by_tx_hash(self, tx_hash: TransactionHash) -> OrderResponseDTO | None:
        payment_transaction_alias = aliased(TransactionM)
        return_transaction_alias = aliased(TransactionM)

        stmt = (
            select(OrderM)
            .options(
                # Order -> Product -> Wallet -> Asset
                joinedload(OrderM.product)
                .joinedload(ProductM.wallet)
                .joinedload(WalletM.asset),
                # Order -> Payment Transaction
                joinedload(OrderM.payment_transaction.of_type(payment_transaction_alias)),
                # Order -> Return Transaction
                joinedload(OrderM.return_transaction.of_type(return_transaction_alias)),
                # Order -> Wallet
                joinedload(OrderM.wallet)
            )
            .where(
                or_(
                    payment_transaction_alias.transaction_hash == tx_hash.value,
                    return_transaction_alias.transaction_hash == tx_hash.value
                )
            )
        )

        result = await self._session.execute(stmt)
        model: OrderM | None = result.scalar_one_or_none()

        if not model:
            return None

        return OrderMapper.to_dto(model)

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

    async def update(
            self,
            order_id: EntityId,
            status: Optional[OrderStatus] = None,
            payment_transaction_id: Optional[EntityId] = None,
            return_transaction_id: Optional[EntityId] = None
    ) -> Order:
        values_to_update: dict[str, Any] = {}

        if status:
            values_to_update["status"] = status.value

        if payment_transaction_id:
            values_to_update["payment_transaction_id"] = payment_transaction_id.value

        if return_transaction_id:
            values_to_update["OrderM.return_transaction_id"] = return_transaction_id.value

        stmt = update(OrderM).where(OrderM.id == order_id.value).values(**values_to_update).returning(OrderM)
        result = await self._session.execute(stmt)
        model: OrderM = result.scalar_one()

        return OrderMapper.to_entity(model)
