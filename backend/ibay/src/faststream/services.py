import abc
import asyncio
import logging
import time

import aiohttp

logger = logging.getLogger(__name__)


class RequestServicePort(abc.ABC):
    async def run_10_000_google_requests(self) -> bool:
        ...


class RequestServiceAdapter(RequestServicePort):
    @staticmethod
    async def _fetch_url(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> bool:
        async with semaphore:
            async with session.get(url, timeout=10) as response:
                return response.status == 200

    async def run_10_000_google_requests(self) -> bool:
        is_successful = True
        CONCURRENCY_LIMIT = 200
        REQUESTS_AMOUNT = 10000
        HTTP_URL = "https://www.google.com"

        semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
        tasks: list[asyncio.Task] = []

        async with aiohttp.ClientSession() as session:
            for i in range(REQUESTS_AMOUNT):
                task = asyncio.create_task(self._fetch_url(session, HTTP_URL, semaphore))
                tasks.append(task)

            start_time = time.time()
            logger.info(f"Execution of {REQUESTS_AMOUNT} requests started with concurrency limit {CONCURRENCY_LIMIT}.")

            try:
                await asyncio.gather(*tasks)

            except Exception as exc:
                logger.error(f"Execution stopped. Exception message:\n {exc}")
                is_successful = False

            end_time = time.time()
            duration = end_time - start_time

            message = f"Execution ended successfully." if is_successful else f"Execution failed."
            logger.info(f"{message}.\nDuration: {duration} seconds.")

        return is_successful
