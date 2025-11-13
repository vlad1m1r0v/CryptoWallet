from src.configs import PostgresConfig


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

def new_session_maker(postgres_config: PostgresConfig) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        postgres_config.async_url,
        pool_size=15,
        max_overflow=15,
    )

    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False
    )