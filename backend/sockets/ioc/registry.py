from collections.abc import Iterable

from dishka import Provider

from ioc.config import ConfigProvider
from ioc.mongo import MongoProvider


def get_providers() -> Iterable[Provider]:
    return (
        ConfigProvider(),
        MongoProvider()
    )
