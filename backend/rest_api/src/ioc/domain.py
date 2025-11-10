from dishka import Provider, Scope, provide

from src.domain.ports import (
    PasswordHasher,
    IdGenerator,
    SecretEncryptor,
    TimestampGenerator
)
from src.domain.services import (
    UserService,
    WalletService,
    TransactionService,
    ProductService,
    OrderService
)

from src.infrastructure.adapters.utils import (
    BcryptPasswordHasher,
    UuidGenerator,
    AESSecretEncryptor,
    DatetimeGenerator
)


class DomainProvider(Provider):
    scope = Scope.REQUEST

    user_service = provide(source=UserService)

    wallet_service = provide(source=WalletService)

    transaction_service = provide(source=TransactionService)

    product_service = provide(source=ProductService)

    order_service = provide(source=OrderService)

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

    datetime_generator = provide(
        source=DatetimeGenerator,
        provides=TimestampGenerator
    )
