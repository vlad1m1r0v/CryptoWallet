from typing import AsyncIterable

from dishka import Provider, provide, Scope, from_context
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.configs import Config
from src.db.session import new_session_maker
from src.db.repositories import (
    OrderRepositoryPort,
    OrderRepositoryAdapter
)


class DatabaseProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    order_gateway = provide(
        source=OrderRepositoryAdapter,
        provides=OrderRepositoryPort
    )
