import asyncio

from taskiq_redis import ListQueueBroker

from dishka import make_async_container
from dishka.integrations.taskiq import (
    setup_dishka,
    TaskiqProvider,
)

from src.ioc import get_providers

from src.infrastructure.adapters.tasks import broker

container = make_async_container(*get_providers(), TaskiqProvider())

setup_dishka(container, broker)


async def run_broker(list_queue_broker: ListQueueBroker):
    await list_queue_broker.startup()


if __name__ == "__main__":
    asyncio.run(run_broker(broker))
