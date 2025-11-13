from os import environ as env

from pydantic import Field, BaseModel
from dotenv import load_dotenv

load_dotenv()


class PostgresConfig(BaseModel):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    login: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DB")

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.login}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def sync_url(self) -> str:
        return f"postgresql+psycopg2://{self.login}:{self.password}@{self.host}:{self.port}/{self.database}"


class RabbitMQConfig(BaseModel):
    host: str = Field(alias="RABBITMQ_HOST")
    port: int = Field(alias="RABBITMQ_PORT")
    user: str = Field(alias="RABBITMQ_USER")
    password: str = Field(alias="RABBITMQ_PASSWORD")
    vhost: str = Field(alias="RABBITMQ_VHOST")

    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.vhost}"


class Config(BaseModel):
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
    rabbit_mq: RabbitMQConfig = Field(default_factory=lambda: RabbitMQConfig(**env))


config = Config()

__all__ = [
    config,
    Config
]
