from collections.abc import Iterable

from dishka import Provider

from src.ioc.application import ApplicationProvider
from src.ioc.domain import DomainProvider
from src.ioc.database import DatabaseProvider
from src.ioc.config import ConfigProvider


def get_providers() -> Iterable[Provider]:
    return (
        ApplicationProvider(),
        DomainProvider(),
        DatabaseProvider(),
        ConfigProvider(),
    )