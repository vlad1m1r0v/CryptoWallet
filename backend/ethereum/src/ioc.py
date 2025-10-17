from dishka import (
    Provider,
    provide,
    Scope,
    from_context
)

from web3 import Web3

from src.configs import (
    Config,
    InfuraConfig,
    EtherscanConfig,
    RabbitMQConfig
)
from src.ports import EthereumServicePort

from src.adapters import EthereumServiceAdapter


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


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    ethereum_service = provide(
        source=EthereumServiceAdapter,
        provides=EthereumServicePort
    )


class Web3Provider(Provider):
    @provide(scope=Scope.APP)
    def provide_web3_client(self, config: InfuraConfig) -> Web3:
        INFURA_URL = f"https://sepolia.infura.io/v3/{config.api_key}"
        return Web3(Web3.HTTPProvider(INFURA_URL))
