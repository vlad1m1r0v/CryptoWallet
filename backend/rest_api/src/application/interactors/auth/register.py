from src.domain.exceptions import (
    EmailAlreadyExistsException,
    FieldsDoNotMatchException
)
from src.domain.value_objects import (
    Email,
    RawPassword,
    Username
)
from src.domain.services import UserService

from src.application.ports.gateways import UserGateway
from src.application.ports.providers import (
    JwtProvider,
    MailProvider
)
from src.application.ports.transaction import TransactionManager
from src.application.dtos.request import RegisterUserRequestDTO
from src.application.dtos.response import RegisterUserResponseDTO


class RegisterInteractor:
    def __init__(
            self,
            user_service: UserService,
            user_gateway: UserGateway,
            jwt_provider: JwtProvider,
            mail_provider: MailProvider,

            transaction_manager: TransactionManager
    ):
        self._user_service = user_service
        self._user_gateway = user_gateway
        self._jwt_provider = jwt_provider
        self._mail_provider = mail_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, data: RegisterUserRequestDTO) -> RegisterUserResponseDTO:
        username = Username(data.username)
        email = Email(data.email)
        password = RawPassword(data.password)
        repeat_password = RawPassword(data.repeat_password)

        if password != repeat_password:
            raise FieldsDoNotMatchException(field_1="password", field_2="repeat_password")

        if await self._user_gateway.read_by_email(email):
            raise EmailAlreadyExistsException(email=email)

        user = self._user_service.create_user(
            username=username,
            email=email,
            raw_password=password
        )

        self._user_gateway.add(user)
        await self._transaction_manager.commit()

        self._mail_provider.send_welcome_email(
            to=email.value,
            username=username.value
        )

        access_token = self._jwt_provider.encode({"user_id": str(user.id_.value)})
        return RegisterUserResponseDTO(access_token=access_token)
