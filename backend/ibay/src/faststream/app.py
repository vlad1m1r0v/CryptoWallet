import logging
import asyncio

from dishka.integrations.faststream import setup_dishka

from faststream import FastStream, ContextRepo
from faststream.rabbit import RabbitBroker

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.configs import config
from src.ioc.container import container
from src.faststream.tasks import TaskRunner
from src.faststream.amqp_router import amqp_router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

broker = RabbitBroker(url=config.rabbit_mq.url)
broker.include_router(amqp_router)
setup_dishka(container, broker=broker)

app = FastStream(broker)


@app.on_startup
async def setup_task_on_start(context: ContextRepo):
    rabbit_broker = await container.get(RabbitBroker)
    session_maker = await container.get(async_sessionmaker[AsyncSession])

    task_runner = TaskRunner(broker=rabbit_broker, session_maker=session_maker)
    task = await task_runner.run()
    context.set_global("task", task)


@app.on_shutdown
async def shutdown_task_on_shutdown(context: ContextRepo):
    task: asyncio.Task = context.get("task")
    task.cancel()
