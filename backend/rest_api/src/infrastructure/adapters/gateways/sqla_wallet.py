from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.value_objects import (
    EntityId,
    Address
)
from src.domain.entities.wallet import Wallet as WalletE

from src.application.ports.gateways import WalletGateway

from src.infrastructure.persistence.database.models import Wallet as WalletM
from src.infrastructure.persistence.database.mappers import WalletMapper


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
