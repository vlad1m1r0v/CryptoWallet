from dishka import Provider, Scope, provide, provide_all

from src.application.ports.transaction import (
    TransactionManager,
    Flusher
)
from src.application.ports.providers import (
    JwtProvider,
    MailProvider,
    FileUploader
)
from src.application.ports.events import EventPublisher
from src.application.ports.gateways import (
    UserGateway,
    WalletGateway,
    AssetGateway,
    TransactionGateway,
    ProductGateway,
    OrderGateway,
    PermissionsGateway
)
from src.application.ports.tasks import TaskRunner
from src.application.interactors import (
    RegisterInteractor,
    LoginInteractor,
    GetUserInteractor,
    UpdateUserInteractor,
    DeleteAvatarInteractor,
    PublishCreateWalletInteractor,
    PublishImportWalletInteractor,
    SaveCreateWalletInteractor,
    SaveImportWalletInteractor,
    GetWalletsInteractor,
    PublishRequestFreeETHInteractor,
    PublishCreateTransactionInteractor,
    CreatePendingTransactionInteractor,
    CompleteTransactionInteractor,
    GetTransactionsInteractor,
    CreateProductInteractor,
    GetProductsInteractor,
    CreateOrderInteractor,
    UpdateOrderInteractor,
    GetOrdersInteractor,
    CreateAssetInteractor
)

from src.infrastructure.adapters.transaction import (
    SqlaTransactionManager,
    SqlaFlusher
)
from src.infrastructure.adapters.providers import PyJwtProvider, MailjetProvider, S3FileUploader
from src.infrastructure.adapters.event_publishers import RabbitMQEventPublisher
from src.infrastructure.adapters.gateways import (
    SqlaUserGateway,
    SqlaAssetGateway,
    SqlaWalletGateway,
    SqlaTransactionGateway,
    SqlaProductGateway,
    SqlaOrderGateway,
    SqlaPermissionsGateway
)
from src.infrastructure.adapters.tasks import TaskIqTaskRunner


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    transaction_manager = provide(
        source=SqlaTransactionManager,
        provides=TransactionManager
    )

    flusher = provide(
        source=SqlaFlusher,
        provides=Flusher
    )

    jwt_provider = provide(
        source=PyJwtProvider,
        provides=JwtProvider
    )

    mail_provider = provide(
        source=MailjetProvider,
        provides=MailProvider
    )

    file_uploader = provide(
        source=S3FileUploader,
        provides=FileUploader
    )

    event_publisher = provide(
        source=RabbitMQEventPublisher,
        provides=EventPublisher
    )

    user_gateway = provide(
        source=SqlaUserGateway,
        provides=UserGateway
    )

    asset_gateway = provide(
        source=SqlaAssetGateway,
        provides=AssetGateway
    )

    wallet_gateway = provide(
        source=SqlaWalletGateway,
        provides=WalletGateway
    )

    transaction_gateway = provide(
        source=SqlaTransactionGateway,
        provides=TransactionGateway
    )

    product_gateway = provide(
        source=SqlaProductGateway,
        provides=ProductGateway
    )

    order_gateway = provide(
        source=SqlaOrderGateway,
        provides=OrderGateway
    )

    permissions_gateway = provide(
        source=SqlaPermissionsGateway,
        provides=PermissionsGateway
    )

    task_runner = provide(
        source=TaskIqTaskRunner,
        provides=TaskRunner
    )

    interactors = provide_all(
        RegisterInteractor,
        LoginInteractor,
        GetUserInteractor,
        UpdateUserInteractor,
        DeleteAvatarInteractor,
        PublishCreateWalletInteractor,
        PublishImportWalletInteractor,
        SaveCreateWalletInteractor,
        SaveImportWalletInteractor,
        GetWalletsInteractor,
        PublishRequestFreeETHInteractor,
        PublishCreateTransactionInteractor,
        CreatePendingTransactionInteractor,
        CompleteTransactionInteractor,
        GetTransactionsInteractor,
        CreateProductInteractor,
        GetProductsInteractor,
        CreateOrderInteractor,
        UpdateOrderInteractor,
        GetOrdersInteractor,
        CreateAssetInteractor
    )
