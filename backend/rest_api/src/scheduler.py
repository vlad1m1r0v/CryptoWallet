import asyncio

from taskiq_redis import RedisScheduleSource

from src.infrastructure.adapters.tasks import redis_source


async def run_scheduler(source: RedisScheduleSource) -> None:
    await source.startup()


if __name__ == "__main__":
    asyncio.run(run_scheduler(redis_source))
