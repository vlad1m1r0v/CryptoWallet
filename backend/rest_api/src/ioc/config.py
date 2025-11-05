from dishka import Provider, provide, Scope, from_context

from src.configs import (
    Config,
    FrontendConfig,
    SecurityConfig,
    PostgresConfig,
    MailingConfig,
    S3Config,
    RedisConfig
)


class ConfigProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def provide_frontend_config(self, config: Config) -> FrontendConfig:
        return config.frontend

    @provide(scope=Scope.APP)
    def provide_security_config(self, config: Config) -> SecurityConfig:
        return config.security

    @provide(scope=Scope.APP)
    def provide_postgres_config(self, config: Config) -> PostgresConfig:
        return config.postgres

    @provide(scope=Scope.APP)
    def provide_mailing_config(self, config: Config) -> MailingConfig:
        return config.mailing

    @provide(scope=Scope.APP)
    def provide_s3_config(self, config: Config) -> S3Config:
        return config.s3

    @provide(scope=Scope.APP)
    def provide_redis_config(self, config: Config) -> RedisConfig:
        return config.redis
