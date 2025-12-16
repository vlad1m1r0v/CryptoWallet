from dishka import (
    Provider,
    from_context,
    provide,
    Scope
)

from faststream.rabbit import RabbitBroker

from configs import Config


class BrokerProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def provide_rabbitmq_client(self, config: Config) -> RabbitBroker:
        broker = RabbitBroker(url=config.rabbit.url)
        await broker.start()
        return broker