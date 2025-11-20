from uuid import UUID
from typing import Union
import logging

from src.domain.exceptions import (
    FieldRequiredException,
    FieldsDoNotMatchException
)
from src.domain.value_objects import (
    UploadedFile,
    Filename,
    RawPassword,
    PasswordHash,
    Username
)
from src.domain.ports import PasswordHasher

from src.application.ports.providers import FileUploader
from src.application.ports.gateways import UserGateway
from src.application.ports.events import EventPublisher
from src.application.ports.transaction import TransactionManager
from src.application.dtos.request import UpdateUserRequestDTO
from src.application.dtos.response import UserResponseDTO
from src.application.dtos.events import UpdateUserEventDTO

logger = logging.getLogger(__name__)


class UpdateUserInteractor:
    def __init__(
            self,
            user_gateway: UserGateway,
            file_uploader: FileUploader,
            password_hasher: PasswordHasher,
            transaction_manager: TransactionManager,
            event_publisher: EventPublisher
    ):
        self._user_gateway = user_gateway
        self._file_uploader = file_uploader
        self._password_hasher = password_hasher
        self._transaction_manager = transaction_manager
        self._event_publisher = event_publisher

    async def __call__(self, data: UpdateUserRequestDTO) -> UserResponseDTO:
        values_to_update: dict[str, Union[str, bytes]] = {}

        logger.info("Checking if user entered new username...")

        if data.username:
            username = Username(data.username)
            values_to_update["username"] = username.value

        logger.info("Checking if user uploaded new avatar...")

        if avatar := data.avatar:
            avatar_filename = self._file_uploader.upload_image(UploadedFile(avatar).value)
            values_to_update["avatar_filename"] = Filename(avatar_filename).value

        logger.info("Checking if user entered new password...")

        if data.password:

            logger.info("Checking if user entered repeat password...")

            if not data.repeat_password:
                raise FieldRequiredException("repeat_password")

            password = RawPassword(data.password)
            repeat_password = RawPassword(data.repeat_password)

            logging.info("Checking if 'password' and 'repeat_password' match...")

            if password != repeat_password:
                raise FieldsDoNotMatchException("password", "repeat_password")

            password_hash = self._password_hasher.hash(password.value)

            values_to_update["password_hash"] = PasswordHash(password_hash).value

        logger.info("Updating user information...")

        await self._user_gateway.update(user_id=data.user_id, **values_to_update)
        await self._transaction_manager.commit()

        user = await self._user_gateway.read(user_id=data.user_id)

        logger.info("Emitting event rest_api.update_user...")

        await self._event_publisher.update_user(dto=UpdateUserEventDTO(
            user_id=user["id"],
            username=user["username"],
            avatar_filename=user["avatar_filename"]
        ))

        logger.info("Returning updated user...")

        return user
