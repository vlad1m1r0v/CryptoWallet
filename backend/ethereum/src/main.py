import logging

from dishka.integrations.faststream import setup_dishka
from dishka import make_async_container

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.broker import amqp_router

from src.configs import Config, config

from src.ioc import (
    ConfigProvider,
    ServiceProvider,
    Web3Provider
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

container = make_async_container(
    ConfigProvider(),
    ServiceProvider(),
    Web3Provider(),
    context={Config: config}
)

broker = RabbitBroker(url=config.rabbit_mq.url)
broker.include_router(amqp_router)
setup_dishka(container, broker=broker)

app = FastStream(broker)
