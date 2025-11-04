from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.transaction import TransactionManager


class SqlaTransactionManager(TransactionManager):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()
