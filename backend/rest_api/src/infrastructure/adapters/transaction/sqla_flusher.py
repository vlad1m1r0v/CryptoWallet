from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.transaction import Flusher


class SqlaFlusher(Flusher):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def flush(self) -> None:
        await self._session.flush()
