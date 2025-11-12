import logging

from dishka.integrations.faststream import setup_dishka

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.configs import config
from src.ioc.container import container
from src.amqp_router import amqp_router


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

broker = RabbitBroker(url=config.rabbit_mq.url)
broker.include_router(amqp_router)
setup_dishka(container, broker=broker)

app = FastStream(broker)