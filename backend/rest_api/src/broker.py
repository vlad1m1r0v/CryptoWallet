from src.configs import (
    Config,
    config
)

from dishka import make_async_container
from dishka.integrations.taskiq import (
    setup_dishka,
    TaskiqProvider,
)

from src.ioc import get_providers

from src.infrastructure.adapters.tasks import broker

container = make_async_container(*get_providers(), TaskiqProvider(), context={Config: config})

setup_dishka(container, broker)
