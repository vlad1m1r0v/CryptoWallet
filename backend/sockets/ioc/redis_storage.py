from typing import AsyncIterator

from dishka import Provider, provide, Scope

from redis.asyncio import Redis

from redis_storage import (
    ChatUsersStorage,
    RedisChatUsersStorage
)

from configs import RedisConfig


class RedisStorageProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def provide_redis(
            self, redis_config: RedisConfig
    ) -> AsyncIterator[Redis]:
        redis = Redis.from_url(redis_config.url)
        yield redis
        await redis.close()

    chat_users_storage = provide(
        source=RedisChatUsersStorage,
        provides=ChatUsersStorage
    )
