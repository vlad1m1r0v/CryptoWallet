import logging

from taskiq_aio_pika import AioPikaBroker
from taskiq.schedule_sources import LabelScheduleSource
from taskiq import TaskiqScheduler

from dishka.integrations.taskiq import setup_dishka

from src.configs import config
from src.ioc.container import container

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)

broker = AioPikaBroker(config.rabbit_mq.url)

setup_dishka(container=container, broker=broker)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


@broker.task(
    schedule=[{"cron": "* * * * *", "args": []}]
)
async def process_latest_delivering_order() -> None:
    message = "Getting the newest order that is being delivered..."
    logger.info(message)
    return None
