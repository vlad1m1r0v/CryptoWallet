from dishka import Provider, Scope, provide, provide_all

from src.application.ports.transaction.transaction_manager import TransactionManager
from src.application.ports.transaction.flusher import Flusher
from src.application.ports.providers.jwt import JwtProvider
from src.application.ports.providers.mail import MailProvider
from src.application.ports.gateways.user import UserGateway

from src.application.interactors.user.register import RegisterInteractor
from src.application.interactors.user.login import LoginInteractor
from src.application.interactors.user.get_current_user import GetCurrentUserInteractor
from src.application.interactors.user.update_user import UpdateUserInteractor

from src.infrastructure.adapters.transaction.sqla_transaction_manager import SqlaTransactionManager
from src.infrastructure.adapters.transaction.sqla_flusher import SqlaFlusher
from src.infrastructure.adapters.providers.pyjwt import PyJwtProvider
from src.infrastructure.adapters.providers.mailjet.provider import MailjetProvider
from src.infrastructure.adapters.gateways.sqla_user import SqlaUserGateway


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

    user_gateway = provide(
        source=SqlaUserGateway,
        provides=UserGateway
    )

    interactors = provide_all(
        RegisterInteractor,
        LoginInteractor,
        GetCurrentUserInteractor,
        UpdateUserInteractor,
    )
