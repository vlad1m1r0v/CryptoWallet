from dishka import Provider, provide, Scope

from src.faststream.services import (
    RequestServicePort,
    RequestServiceAdapter
)


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    request_service = provide(
        source=RequestServiceAdapter,
        provides=RequestServicePort
    )
