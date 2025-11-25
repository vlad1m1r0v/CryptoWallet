from dishka import Provider, provide, Scope, from_context

from configs import (
    Config,
    JwtConfig,
    MongoConfig,
    RabbitMQConfig,
    RedisConfig,
    S3Config,
)


class ConfigProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def provide_jwt_config(self, config: Config) -> JwtConfig:
        return config.jwt

    @provide(scope=Scope.APP)
    def provide_mongo_config(self, config: Config) -> MongoConfig:
        return config.mongo

    @provide(scope=Scope.APP)
    def provide_rabbit_config(self, config: Config) -> RabbitMQConfig:
        return config.rabbit

    @provide(scope=Scope.APP)
    def provide_redis_config(self, config: Config) -> RedisConfig:
        return config.redis

    @provide(scope=Scope.APP)
    def provide_s3_config(self, config: Config) -> S3Config:
        return config.s3