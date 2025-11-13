import asyncio
import abc
import random
import logging

from faststream.rabbit import RabbitBroker

from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from src.db.repositories import OrderRepositoryAdapter

logger = logging.getLogger(__name__)


class TaskRunnerInterface(abc.ABC):
    @abc.abstractmethod
    async def run(self) -> asyncio.Task:
        ...


class TaskRunner(TaskRunnerInterface):
    def __init__(
            self,
            broker: RabbitBroker,
            session_maker: async_sessionmaker[AsyncSession]
    ):
        self._broker = broker
        self._session_maker = session_maker

    async def run(self) -> asyncio.Task:
        return asyncio.create_task(self._loop())

    async def _loop(self):
        while True:
            logging.info("Running loop...")

            async with self._session_maker() as session:
                repository = OrderRepositoryAdapter(session)

                order = await repository.get_latest_delivering_order()

                if order:
                    is_successful = random.random() > 0.5

                    if is_successful:
                        await self._broker.publish(
                            queue="ibay.complete_order",
                            message={"order_id": order.id}
                        )
                    else:
                        await self._broker.publish(
                            queue="ibay.return_order",
                            message={"order_id": order.id}
                        )

                await asyncio.sleep(5)
