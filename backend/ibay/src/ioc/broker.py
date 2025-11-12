from dishka import Provider, provide, Scope
from faststream.rabbit import RabbitBroker

from src.configs import RabbitMQConfig


class RabbitMQProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_rabbitmq_broker(self, rabbit_mq_config: RabbitMQConfig) -> RabbitBroker:
        broker = RabbitBroker(url=rabbit_mq_config.url)
        await broker.start()
        return broker
