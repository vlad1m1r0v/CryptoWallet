from contextlib import asynccontextmanager
from typing import AsyncIterator

from dishka import make_async_container
from dishka.integrations import fastapi as fastapi_integration
from dishka.integrations import faststream as faststream_integration

import uvicorn

from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from faststream.rabbit import RabbitBroker

from slowapi.errors import RateLimitExceeded

from src.presentation.http.handlers import root_router
from src.presentation.http.exceptions import (
    error_handler,
    validation_error_handler,
    rate_limit_error_handler
)
from src.presentation.http.limiter import limiter
from src.presentation.amqp.router import amqp_router

from src.ioc import get_providers

from src.configs import Config, config

from pydantic import ValidationError


def create_app() -> FastAPI:
    container = make_async_container(*get_providers(), context={Config: config})

    broker = RabbitBroker(url=config.rabbit_mq.url)
    broker.include_router(amqp_router)
    faststream_integration.setup_dishka(container, broker=broker)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        async with broker:
            await broker.start()
            yield

    app = FastAPI(lifespan=lifespan)

    app.state.limiter = limiter

    origins = [config.frontend.url]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(root_router)

    app.add_exception_handler(RateLimitExceeded, rate_limit_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(Exception, error_handler)

    fastapi_integration.setup_dishka(container, app)

    return app


if __name__ == "__main__":
    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
