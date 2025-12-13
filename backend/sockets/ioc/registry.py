from collections.abc import Iterable

from dishka import Provider

from ioc.config import ConfigProvider
from ioc.mongo import MongoProvider
from ioc.jwt import JwtProvider
from ioc.redis_storage import RedisStorageProvider


def get_providers() -> Iterable[Provider]:
    return (
        ConfigProvider(),
        MongoProvider(),
        JwtProvider(),
        RedisStorageProvider(),
    )
