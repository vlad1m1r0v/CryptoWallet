from src.configs import Config, config

from src.ioc.config import ConfigProvider
from src.ioc.broker import RabbitMQProvider
from src.ioc.db import DatabaseProvider
from src.ioc.service import ServiceProvider

from dishka import make_async_container

container = make_async_container(
    ConfigProvider(),
    RabbitMQProvider(),
    DatabaseProvider(),
    ServiceProvider(),
    context={Config: config}
)
