from typing import AsyncIterator

from dishka import (
    Provider,
    provide,
    Scope,
    from_context
)
from faststream.rabbit import RabbitBroker

from web3 import Web3

from redis.asyncio import Redis

from src.configs import (
    Config,
    InfuraConfig,
    EtherscanConfig,
    RabbitMQConfig,
    RedisConfig,
    FaucetConfig
)
from src.ports import (
    StoragePort,
    EthereumServicePort,
    BlockListenerPort
)

from src.adapters import (
    RedisStorageAdapter,
    EthereumServiceAdapter,
    BlockListenerAdapter
)


class ConfigProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def provide_infura_config(self, config: Config) -> InfuraConfig:
        return config.infura

    @provide(scope=Scope.APP)
    def provide_etherscan_config(self, config: Config) -> EtherscanConfig:
        return config.etherscan

    @provide(scope=Scope.APP)
    def provide_rabbit_mq_config(self, config: Config) -> RabbitMQConfig:
        return config.rabbit_mq

    @provide(scope=Scope.APP)
    def provide_redis_config(self, config: Config) -> RedisConfig:
        return config.redis

    @provide(scope=Scope.APP)
    def provide_faucet_config(self, config: Config) -> FaucetConfig:
        return config.faucet


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    ethereum_service = provide(
        source=EthereumServiceAdapter,
        provides=EthereumServicePort
    )


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_redis(
            self, redis_config: RedisConfig
    ) -> AsyncIterator[Redis]:
        redis = Redis.from_url(redis_config.url)
        yield redis
        await redis.close()


class StorageProvider(Provider):
    scope = Scope.APP

    storage = provide(
        source=RedisStorageAdapter,
        provides=StoragePort
    )


class RabbitMQProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_rabbitmq_broker(self, rabbit_mq_config: RabbitMQConfig) -> RabbitBroker:
        broker = RabbitBroker(url=rabbit_mq_config.url)
        await broker.start()
        return broker


class BlockListenerProvider(Provider):
    scope = Scope.APP

    storage = provide(
        source=BlockListenerAdapter,
        provides=BlockListenerPort
    )


class Web3Provider(Provider):
    @provide(scope=Scope.APP)
    def provide_web3_client(self, config: InfuraConfig) -> Web3:
        INFURA_URL = f"https://sepolia.infura.io/v3/{config.api_key}"
        return Web3(Web3.HTTPProvider(INFURA_URL))
