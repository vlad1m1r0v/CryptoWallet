import asyncio

import logging

from dishka.integrations.faststream import setup_dishka
from dishka import make_async_container

from faststream import FastStream, ContextRepo
from faststream.rabbit import RabbitBroker

from src.broker import amqp_router

from src.configs import Config, config

from src.ports import BlockListenerPort

from src.ioc import (
    ConfigProvider,
    RedisProvider,
    StorageProvider,
    ServiceProvider,
    RabbitMQProvider,
    BlockListenerProvider,
    Web3Provider
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

container = make_async_container(
    ConfigProvider(),
    RedisProvider(),
    StorageProvider(),
    ServiceProvider(),
    RabbitMQProvider(),
    BlockListenerProvider(),
    Web3Provider(),
    context={Config: config}
)

broker = RabbitBroker(url=config.rabbit_mq.url)
broker.include_router(amqp_router)
setup_dishka(container, broker=broker)

app = FastStream(broker)


@app.on_startup
async def setup_block_listener_on_start(context: ContextRepo):
    block_listener: BlockListenerPort = await container.get(BlockListenerPort)
    task = block_listener.run()
    context.set_global("task", task)


@app.on_shutdown
async def shutdown_block_listener_on_shutdown(context: ContextRepo):
    task: asyncio.Task = context.get("task")
    task.cancel()
