import logging

from dishka import make_async_container
from dishka.integrations.faststream import setup_dishka

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from rabbit.amqp_router import amqp_router

from ioc.registry import get_providers

from configs import (
    config,
    Config
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

broker = RabbitBroker(url=config.rabbit.url)
broker.include_router(amqp_router)

container = make_async_container(*get_providers(), context={Config: config})
setup_dishka(container, broker=broker)

app = FastStream(broker)
