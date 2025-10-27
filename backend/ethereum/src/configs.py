from os import environ as env

import pathlib

from pydantic import Field, BaseModel
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = pathlib.Path(__file__).parents[1]


class InfuraConfig(BaseModel):
    api_key: str = Field(alias="INFURA_API_KEY")


class EtherscanConfig(BaseModel):
    api_key: str = Field(alias="ETHERSCAN_API_KEY")
    api_base_url: str = Field(alias="ETHERSCAN_API_BASE_URL")


class RabbitMQConfig(BaseModel):
    host: str = Field(alias="RABBITMQ_HOST")
    port: int = Field(alias="RABBITMQ_PORT")
    user: str = Field(alias="RABBITMQ_USER")
    password: str = Field(alias="RABBITMQ_PASSWORD")
    vhost: str = Field(alias="RABBITMQ_VHOST")

    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.vhost}"


class RedisConfig(BaseModel):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")
    db: int = Field(alias="REDIS_DB", default=0)
    password: str | None = Field(alias="REDIS_PASSWORD", default=None)

    @property
    def url(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"


class Config(BaseModel):
    infura: InfuraConfig = Field(default_factory=lambda: InfuraConfig(**env))
    etherscan: EtherscanConfig = Field(default_factory=lambda: EtherscanConfig(**env))
    rabbit_mq: RabbitMQConfig = Field(default_factory=lambda: RabbitMQConfig(**env))
    redis: RedisConfig = Field(default_factory=lambda: RedisConfig(**env))


config = Config()
