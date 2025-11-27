from dishka import Provider, Scope, provide

from jwt_decoder import (
    JwtDecoder,
    PyJwtDecoder
)


class JwtProvider(Provider):
    scope = Scope.REQUEST

    jwt_decoder = provide(
        source=PyJwtDecoder,
        provides=JwtDecoder
    )
