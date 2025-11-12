from dishka import Provider, provide, Scope, from_context

from src.configs import (
    Config,
    PostgresConfig,
    RabbitMQConfig
)


class ConfigProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def provide_postgres_config(self, config: Config) -> PostgresConfig:
        return config.postgres

    @provide(scope=Scope.APP)
    def provide_rabbitmq_config(self, config: Config) -> RabbitMQConfig:
        return config.rabbit_mq