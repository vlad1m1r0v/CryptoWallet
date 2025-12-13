from typing import Sequence, Optional, Any
from uuid import UUID

from sqlalchemy import select, update, and_, or_, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, aliased

from src.domain.entities import Order
from src.domain.enums import OrderStatusEnum

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

    @staticmethod
    def __base_select() -> tuple[
        Select,
        WalletM,
        TransactionM,
        TransactionM
    ]:
        wallet_alias = aliased(WalletM)
        payment_transaction_alias = aliased(TransactionM)
        return_transaction_alias = aliased(TransactionM)

        stmt: Select = (
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
                joinedload(OrderM.payment_transaction.of_type(payment_transaction_alias)),
                # Order -> Return Transaction
                joinedload(OrderM.return_transaction.of_type(return_transaction_alias)),
                # Order -> Wallet
                joinedload(OrderM.wallet)
            )
        )

        return stmt, wallet_alias, payment_transaction_alias, return_transaction_alias

    async def update(
            self,
            order_id: UUID,
            status: Optional[OrderStatusEnum] = None,
            payment_transaction_id: Optional[UUID] = None,
            return_transaction_id: Optional[UUID] = None
    ) -> None:

        values_to_update: dict[str, Any] = {}

        if status:
            values_to_update["status"] = status.value

        if payment_transaction_id:
            values_to_update["payment_transaction_id"] = payment_transaction_id

        if return_transaction_id:
            values_to_update["return_transaction_id"] = return_transaction_id

        stmt = update(OrderM).where(OrderM.id == order_id).values(**values_to_update)
        await self._session.execute(stmt)

    async def list(self, user_id: UUID) -> list[OrderResponseDTO]:
        stmt, wallet_alias, _, _ = self.__base_select()
        stmt = (stmt
                .where(and_(wallet_alias.user_id == user_id))
                .order_by(OrderM.created_at.desc())
                )
        result = await self._session.execute(stmt)
        models: Sequence[OrderM] = result.scalars().all()
        return OrderMapper.to_dto(models=models)

    async def read(
            self,
            order_id: Optional[UUID] = None,
            tx_hash: Optional[str] = None
    ) -> OrderResponseDTO | None:
        stmt, _, payment_transaction_alias, return_transaction_alias = self.__base_select()

        if tx_hash:
            stmt = stmt.where(
                or_(
                    payment_transaction_alias.transaction_hash == tx_hash,
                    return_transaction_alias.transaction_hash == tx_hash
                )
            )

        elif order_id:
            stmt = stmt.where(OrderM.id == order_id)

        else:
            return None

        result = await self._session.execute(stmt)
        model: OrderM = result.scalar_one_or_none()

        if not model:
            return None

        return OrderMapper.to_dto(model=model)

    def add(self, order: Order) -> None:
        model = OrderMapper.to_model(order)
        self._session.add(model)
