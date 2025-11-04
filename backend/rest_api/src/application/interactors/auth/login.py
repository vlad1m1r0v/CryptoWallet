from src.domain.exceptions import (
    EmailNotFoundException,
    WrongPasswordException,
    UserNotActivatedException
)
from src.domain.services import UserService
from src.domain.value_objects import (
    Email,
    RawPassword
)
from src.application.ports.gateways import UserGateway
from src.application.ports.providers import JwtProvider
from src.application.ports.transaction import TransactionManager
from src.application.dtos.request import LoginUserRequestDTO
from src.application.dtos.response import LoginUserResponseDTO



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

    async def __call__(self, data: LoginUserRequestDTO) -> LoginUserResponseDTO:
        email = Email(data.email)
        password = RawPassword(data.password)

        if not (user := await self._user_gateway.read_by_email(email)):
            raise EmailNotFoundException(email=email)

        if not self._user_service.is_password_valid(user=user, raw_password=password):
            raise WrongPasswordException(password=password)

        if not user.is_active:
            raise UserNotActivatedException()

        access_token = self._jwt_provider.encode({"user_id": str(user.id_.value)})
        return LoginUserResponseDTO(access_token=access_token)
