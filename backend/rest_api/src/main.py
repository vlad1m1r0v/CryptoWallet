from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.presentation.http.handlers.root import router as root_router
from src.presentation.http.exceptions.exception_handler import error_handler

from src.configs import Config, config
from src.ioc.provider_registry import get_providers

container = make_async_container(*get_providers(), context={Config: config})

app = FastAPI()

origins = [config.frontend.url]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)

app.add_exception_handler(Exception, error_handler)

setup_dishka(container, app)
