from dishka import Provider, Scope, provide

from src.domain.ports.password_hasher import PasswordHasher
from src.domain.ports.id_generator import IdGenerator
from src.domain.services.user import UserService
from src.infrastructure.adapters.utils.bcrypt_hasher import BcryptPasswordHasher
from src.infrastructure.adapters.utils.uuid_generator import UuidGenerator


class DomainProvider(Provider):
    scope = Scope.REQUEST

    user_service = provide(source=UserService)

    password_hasher = provide(
        source=BcryptPasswordHasher,
        provides=PasswordHasher,
    )
    user_id_generator = provide(
        source=UuidGenerator,
        provides=IdGenerator,
    )
