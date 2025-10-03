from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.configs import Config
from src.ioc.provider_registry import get_providers
from src.presentation.http.root import router as root_router

config = Config()
container = make_async_container(*get_providers(), context={Config: config})

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_dishka(container, app)

app.include_router(root_router)
