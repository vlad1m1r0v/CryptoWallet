from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from src.application.dtos.response import WalletsListItemResponseDTO
from src.domain.entities import Wallet
from src.domain.value_objects import (
    EntityId,
    Address, Balance
)
from src.domain.entities.wallet import Wallet as WalletE

from src.application.ports.gateways import WalletGateway

from src.infrastructure.persistence.database.models import Wallet as WalletM
from src.infrastructure.persistence.database.mappers import (
    WalletMapper,
    WalletsListMapper
)


class SqlaWalletGateway(WalletGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, wallet: WalletE) -> WalletE:
        wallet_m = WalletMapper.to_model(wallet)
        self._session.add(wallet_m)
        return wallet

    async def read_by_address(self, address: Address) -> WalletE | None:
        stmt = select(WalletM).where(WalletM.address == address.value)
        result = await self._session.execute(stmt)
        model: WalletM | None = result.scalar_one_or_none()
        if not model:
            return None
        return WalletMapper.to_entity(model)

    async def read_by_id(self, wallet_id: EntityId) -> WalletE | None:
        stmt = select(WalletM).where(WalletM.id == wallet_id.value)
        result = await self._session.execute(stmt)
        model: WalletM | None = result.scalar_one_or_none()
        if not model:
            return None
        return WalletMapper.to_entity(model)

    async def decrement_balance(self, wallet_id: EntityId, amount: Balance) -> Wallet:
        stmt = update(WalletM).where(
            WalletM.id == wallet_id.value
        ).values(
            balance=WalletM.balance - amount.value,
        ).returning(WalletM)

        result = await self._session.execute(stmt)
        model: WalletM = result.scalar_one()
        return WalletMapper.to_entity(model)

    async def increment_balance(self, wallet_id: EntityId, amount: Balance) -> Wallet:
        stmt = update(WalletM).where(
            WalletM.id == wallet_id.value
        ).values(
            balance=WalletM.balance + amount.value,
        ).returning(WalletM)

        result = await self._session.execute(stmt)
        model: WalletM = result.scalar_one()
        return WalletMapper.to_entity(model)

    async def get_user_wallets(self, user_id: EntityId) -> list[WalletsListItemResponseDTO]:
        stmt = select(WalletM).options(joinedload(WalletM.asset)).where(WalletM.user_id == user_id.value)
        result = await self._session.execute(stmt)
        models: Sequence[WalletM] = result.scalars().all()
        return WalletsListMapper.to_dto_m2m(models)
