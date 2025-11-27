from collections.abc import Iterable

from dishka import Provider

from ioc.config import ConfigProvider
from ioc.mongo import MongoProvider
from ioc.jwt import JwtProvider


def get_providers() -> Iterable[Provider]:
    return (
        ConfigProvider(),
        MongoProvider(),
        JwtProvider()
    )
