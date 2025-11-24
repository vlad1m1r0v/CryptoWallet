import logging

from src.domain.exceptions import (
    EmailAlreadyExistsException,
    FieldsDoNotMatchException
)
from src.domain.value_objects import (
    Email,
    RawPassword,
    Username
)
from src.domain.services import (
    UserService,
    PermissionsService
)

from src.application.ports.gateways import (
    UserGateway,
    PermissionsGateway
)
from src.application.ports.providers import (
    JwtProvider,
    MailProvider
)
from src.application.ports.tasks import TaskRunner
from src.application.ports.events import EventPublisher
from src.application.ports.transaction import (
    TransactionManager,
    Flusher
)
from src.application.dtos.request import RegisterUserRequestDTO
from src.application.dtos.response import RegisterUserResponseDTO
from src.application.dtos.events import SaveUserEventDTO

logger = logging.getLogger(__name__)


class RegisterInteractor:
    def __init__(
            self,
            user_service: UserService,
            permissions_service: PermissionsService,
            user_gateway: UserGateway,
            permissions_gateway: PermissionsGateway,
            jwt_provider: JwtProvider,
            mail_provider: MailProvider,
            task_runner: TaskRunner,
            flusher: Flusher,
            transaction_manager: TransactionManager,
            event_publisher: EventPublisher
    ):
        self._user_service = user_service
        self._permissions_service = permissions_service
        self._user_gateway = user_gateway
        self._permissions_gateway = permissions_gateway
        self._jwt_provider = jwt_provider
        self._mail_provider = mail_provider
        self._task_runner = task_runner
        self._flusher = flusher
        self._transaction_manager = transaction_manager
        self._event_publisher = event_publisher

    async def __call__(self, data: RegisterUserRequestDTO) -> RegisterUserResponseDTO:
        username = Username(data.username)
        email = Email(data.email)
        password = RawPassword(data.password)
        repeat_password = RawPassword(data.repeat_password)

        logging.info("Checking if 'password' and 'repeat_password' match...")

        if password != repeat_password:
            raise FieldsDoNotMatchException(field_1="password", field_2="repeat_password")

        logging.info("Checking if user with given email already exists...")

        if await self._user_gateway.read(email=email.value):
            raise EmailAlreadyExistsException(email=email)

        logging.info("Creating new user...")

        user = self._user_service.create_user(
            username=username,
            email=email,
            raw_password=password
        )

        self._user_gateway.add(user)
        await self._flusher.flush()

        logging.info("Creating permission record for user...")

        permissions = self._permissions_service.create_permissions(user_id=user.id_)
        self._permissions_gateway.add(permissions)

        await self._transaction_manager.commit()

        logging.info("Emitting event rest_api.save_user...")

        await self._event_publisher.save_user(dto=SaveUserEventDTO(
            user_id=user.id_.value,
            username=username.value
        ))

        logging.info("Sending welcome email...")

        self._mail_provider.send_welcome_email(
            to=email.value,
            username=username.value
        )

        logging.info("Giving access to chat for user after 60s...")

        await self._task_runner.give_chat_access(user_id=user.id_.value)

        logging.info("Generating access token...")

        access_token = self._jwt_provider.encode({"user_id": str(user.id_.value)})
        return RegisterUserResponseDTO(access_token=access_token)
