
from dishka import Provider, Scope, provide, provide_all

from src.application.interactors.wallet.save_create_wallet import SaveCreateWalletInteractor
from src.application.ports.transaction.transaction_manager import TransactionManager
from src.application.ports.transaction.flusher import Flusher
from src.application.ports.providers.jwt import JwtProvider
from src.application.ports.providers.mail import MailProvider
from src.application.ports.providers.file_uploader import FileUploader
from src.application.ports.events.event_publisher import EventPublisher
from src.application.ports.gateways.user import UserGateway
from src.application.ports.gateways.wallet import WalletGateway
from src.application.ports.gateways.asset import AssetGateway

from src.application.interactors.auth.register import RegisterInteractor
from src.application.interactors.auth.login import LoginInteractor
from src.application.interactors.user.get_current_user import GetCurrentUserInteractor
from src.application.interactors.user.update_user import UpdateUserInteractor
from src.application.interactors.wallet.publish_create_wallet import PublishCreateWalletInteractor

from src.infrastructure.adapters.transaction.sqla_transaction_manager import SqlaTransactionManager
from src.infrastructure.adapters.transaction.sqla_flusher import SqlaFlusher
from src.infrastructure.adapters.providers.pyjwt import PyJwtProvider
from src.infrastructure.adapters.providers.mailjet.provider import MailjetProvider
from src.infrastructure.adapters.providers.s3_file_uploader import S3FileUploader
from src.infrastructure.adapters.event_publishers.rabbitmq_event_publisher import RabbitMQEventPublisher
from src.infrastructure.adapters.gateways.sqla_user import SqlaUserGateway
from src.infrastructure.adapters.gateways.sqa_asset import SqlaAssetGateway
from src.infrastructure.adapters.gateways.sqa_wallet import SqlaWalletGateway


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

    interactors = provide_all(
        RegisterInteractor,
        LoginInteractor,
        GetCurrentUserInteractor,
        UpdateUserInteractor,
        PublishCreateWalletInteractor,
        SaveCreateWalletInteractor
    )
