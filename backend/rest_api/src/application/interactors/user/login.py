from dataclasses import dataclass
from typing import TypedDict, Optional

from src.application.ports.gateways.user import UserGateway
from src.application.ports.providers.jwt import JwtProvider
from src.application.ports.transaction.transaction_manager import TransactionManager
from src.domain.exceptions.user import (
    PasswordsNotMatchError,
    EmailNotFoundError,
    UserNotActivatedError
)
from src.domain.services.user import UserService
from src.domain.value_objects.email import Email
from src.domain.value_objects.raw_password import RawPassword


@dataclass(frozen=True, slots=True, kw_only=True)
class LoginUserRequest:
    email: str
    password: str
    remember_me: Optional[bool] = False


class LoginUserResponse(TypedDict):
    access_token: str


class LoginInteractor:
    def __init__(
            self,
            user_service: UserService,
            user_gateway: UserGateway,
            jwt_provider: JwtProvider,
            transaction_manager: TransactionManager
    ):
        self._user_service = user_service
        self._user_gateway = user_gateway
        self._jwt_provider = jwt_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, data: LoginUserRequest) -> LoginUserResponse:
        email = Email(data.email)
        password = RawPassword(data.password)

        if not (user := await self._user_gateway.read_by_email(email)):
            raise EmailNotFoundError(email=email)

        if not self._user_service.is_password_valid(user=user, raw_password=password):
            raise PasswordsNotMatchError()

        if not user.is_active:
            raise UserNotActivatedError()

        access_token = self._jwt_provider.encode({"user_id": str(user.id_.value)})
        return LoginUserResponse(access_token=access_token)
