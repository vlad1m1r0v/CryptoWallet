from dataclasses import dataclass
from typing import TypedDict

from src.application.ports.gateways.user import UserGateway
from src.application.ports.providers.jwt import JwtProvider
# from src.application.ports.providers.mail import MailProvider
from src.application.ports.transaction.transaction_manager import TransactionManager
from src.domain.exceptions.user import PasswordsNotMatchError, EmailAlreadyExistsError
from src.domain.services.user import UserService
from src.domain.value_objects.email import Email
from src.domain.value_objects.raw_password import RawPassword
from src.domain.value_objects.username import Username


@dataclass(frozen=True, slots=True, kw_only=True)
class RegisterUserRequest:
    username: str
    email: str
    password: str
    repeat_password: str


class RegisterUserResponse(TypedDict):
    access_token: str


class RegisterInteractor:
    def __init__(
            self,
            user_service: UserService,
            user_gateway: UserGateway,
            jwt_provider: JwtProvider,
            # mail_provider: MailProvider,

            transaction_manager: TransactionManager
    ):
        self._user_service = user_service
        self._user_gateway = user_gateway
        self._jwt_provider = jwt_provider
        # self._mail_provider = mail_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, data: RegisterUserRequest) -> RegisterUserResponse:
        username = Username(data.username)
        email = Email(data.email)
        password = RawPassword(data.password)
        repeat_password = RawPassword(data.repeat_password)

        if password != repeat_password:
            raise PasswordsNotMatchError()

        if await self._user_gateway.read_by_email(email):
            raise EmailAlreadyExistsError(email=email)

        user = self._user_service.create_user(
            username=username,
            email=email,
            raw_password=password
        )

        self._user_gateway.add(user)
        await self._transaction_manager.commit()

        # await self._mail_provider.send_welcome_email(
        #     to=email,
        #     username=str(username)
        # )

        access_token = self._jwt_provider.encode({"user_id": str(user.id_.value)})
        return RegisterUserResponse(access_token=access_token)
