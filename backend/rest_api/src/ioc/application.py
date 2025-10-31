from dishka import Provider, Scope, provide, provide_all

from src.application.ports.transaction.transaction_manager import TransactionManager
from src.application.ports.transaction.flusher import Flusher
from src.application.ports.providers.jwt import JwtProvider
from src.application.ports.providers.mail import MailProvider
from src.application.ports.providers.file_uploader import FileUploader
from src.application.ports.events.event_publisher import EventPublisher
from src.application.ports.gateways.user import UserGateway
from src.application.ports.gateways.wallet import WalletGateway
from src.application.ports.gateways.asset import AssetGateway
from src.application.ports.gateways.transaction import TransactionGateway

from src.application.interactors.auth.register import RegisterInteractor
from src.application.interactors.auth.login import LoginInteractor
from src.application.interactors.user.get_current_user import GetCurrentUserInteractor
from src.application.interactors.user.update_user import UpdateUserInteractor
from src.application.interactors.wallet.publish_create_wallet import PublishCreateWalletInteractor
from src.application.interactors.wallet.publish_import_wallet import PublishImportWalletInteractor
from src.application.interactors.wallet.save_create_wallet import SaveCreateWalletInteractor
from src.application.interactors.wallet.save_import_wallet import SaveImportWalletInteractor
from src.application.interactors.transaction.publish_create_transaction import PublishCreateTransactionInteractor
from src.application.interactors.transaction.create_pending_transaction import CreatePendingTransactionInteractor
from src.application.interactors.transaction.complete_transaction import CompleteTransactionInteractor
from src.application.interactors.transaction.get_transactions import GetTransactionsInteractor

from src.infrastructure.adapters.transaction.sqla_transaction_manager import SqlaTransactionManager
from src.infrastructure.adapters.transaction.sqla_flusher import SqlaFlusher

from src.infrastructure.adapters.providers.pyjwt import PyJwtProvider
from src.infrastructure.adapters.providers.mailjet.provider import MailjetProvider
from src.infrastructure.adapters.providers.s3_file_uploader import S3FileUploader

from src.infrastructure.adapters.event_publishers.rabbitmq_event_publisher import RabbitMQEventPublisher

from src.infrastructure.adapters.gateways.sqla_user import SqlaUserGateway
from src.infrastructure.adapters.gateways.sqla_asset import SqlaAssetGateway
from src.infrastructure.adapters.gateways.sqla_wallet import SqlaWalletGateway
from src.infrastructure.adapters.gateways.sqla_transaction import SqlaTransactionGateway


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

    interactors = provide_all(
        RegisterInteractor,
        LoginInteractor,
        GetCurrentUserInteractor,
        UpdateUserInteractor,
        PublishCreateWalletInteractor,
        PublishImportWalletInteractor,
        SaveCreateWalletInteractor,
        SaveImportWalletInteractor,
        PublishCreateTransactionInteractor,
        CreatePendingTransactionInteractor,
        CompleteTransactionInteractor,
        GetTransactionsInteractor
    )
