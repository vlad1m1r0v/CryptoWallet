from dishka import Provider, Scope, provide

from src.domain.ports.password_hasher import PasswordHasher
from src.domain.ports.id_generator import IdGenerator
from src.domain.ports.secret_encryptor import SecretEncryptor

from src.domain.services.user import UserService
from src.domain.services.wallet import WalletService

from src.infrastructure.adapters.utils.bcrypt_hasher import BcryptPasswordHasher
from src.infrastructure.adapters.utils.uuid_generator import UuidGenerator
from src.infrastructure.adapters.utils.aes_secret_encryptor import AESSecretEncryptor


class DomainProvider(Provider):
    scope = Scope.REQUEST

    user_service = provide(source=UserService)

    wallet_service = provide(source=WalletService)

    password_hasher = provide(
        source=BcryptPasswordHasher,
        provides=PasswordHasher,
    )

    secret_encryptor = provide(
        source=AESSecretEncryptor,
        provides=SecretEncryptor,
    )

    user_id_generator = provide(
        source=UuidGenerator,
        provides=IdGenerator,
    )
