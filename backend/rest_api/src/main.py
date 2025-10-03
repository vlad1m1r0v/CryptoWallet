from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.configs import Config
from src.ioc.provider_registry import get_providers
from src.presentation.http.root import router as root_router

config = Config()
container = make_async_container(*get_providers(), context={Config: config})

app = FastAPI()

setup_dishka(container, app)

app.include_router(root_router)
