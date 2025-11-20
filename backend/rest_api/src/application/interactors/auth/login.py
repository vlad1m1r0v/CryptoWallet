import logging

from src.domain.exceptions import (
    EmailNotFoundException,
    WrongPasswordException,
    UserNotActivatedException
)
from src.domain.ports import PasswordHasher
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

logger = logging.getLogger(__name__)


class LoginInteractor:
    def __init__(
            self,
            user_service: UserService,
            user_gateway: UserGateway,
            jwt_provider: JwtProvider,
            transaction_manager: TransactionManager,
            password_hasher: PasswordHasher
    ):
        self._user_service = user_service
        self._user_gateway = user_gateway
        self._jwt_provider = jwt_provider
        self._transaction_manager = transaction_manager
        self._password_hasher = password_hasher

    async def __call__(self, data: LoginUserRequestDTO) -> LoginUserResponseDTO:
        email = Email(data.email)
        password = RawPassword(data.password)

        logging.info("Checking if user exists...")

        if not (user := await self._user_gateway.read(email=email.value)):
            raise EmailNotFoundException(email=email)

        logging.info("Checking password...")

        if not self._password_hasher.verify(
                raw_password=password.value,
                hashed_password=user["password_hash"]
        ):
            raise WrongPasswordException(password=password)

        logging.info("Checking if user is active...")

        if not user["is_active"]:
            raise UserNotActivatedException()

        logging.info("Generating access token...")

        access_token = self._jwt_provider.encode({"user_id": str(user["id"])})
        return LoginUserResponseDTO(access_token=access_token)
