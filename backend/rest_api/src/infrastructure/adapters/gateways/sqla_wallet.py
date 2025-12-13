from typing import Optional, Sequence
from uuid import UUID
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, Select
from sqlalchemy.orm import joinedload

from src.domain.entities import Wallet

from src.application.dtos.response import WalletResponseDTO
from src.application.ports.gateways import WalletGateway

from src.infrastructure.persistence.database.models import Wallet as WalletM
from src.infrastructure.persistence.database.mappers import WalletMapper


class SqlaWalletGateway(WalletGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, wallet: Wallet) -> None:
        wallet_m = WalletMapper.to_model(wallet)
        self._session.add(wallet_m)

    async def read(
            self,
            address: Optional[str] = None,
            wallet_id: Optional[UUID] = None
    ) -> WalletResponseDTO | None:
        stmt: Select = select(WalletM).options(joinedload(WalletM.asset))

        if wallet_id:
            stmt = stmt.where(WalletM.id == wallet_id)

        elif address:
            stmt = stmt.where(WalletM.address == address)

        else:
            return None

        result = await self._session.execute(stmt)
        model: WalletM = result.scalar_one_or_none()

        if not model:
            return None

        return WalletMapper.to_dto(model=model)

    async def decrement_balance(self, wallet_id: UUID, amount: Decimal) -> None:
        stmt = (
            update(WalletM)
            .where(WalletM.id == wallet_id)
            .values(balance=WalletM.balance - amount)
        )

        await self._session.execute(stmt)

    async def increment_balance(self, wallet_id: UUID, amount: Decimal) -> None:
        stmt = (
            update(WalletM)
            .where(WalletM.id == wallet_id)
            .values(balance=WalletM.balance + amount)
        )

        await self._session.execute(stmt)

    async def list(self, user_id: UUID) -> list[WalletResponseDTO]:
        stmt = (
            select(WalletM)
            .options(joinedload(WalletM.asset))
            .where(WalletM.user_id == user_id)
            .order_by(WalletM.created_at.desc())
        )
        result = await self._session.execute(stmt)
        models: Sequence[WalletM] = result.scalars().all()
        return WalletMapper.to_dto(models=models)
