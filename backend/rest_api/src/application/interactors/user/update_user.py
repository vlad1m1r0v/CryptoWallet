from dataclasses import dataclass
from typing import TypedDict, Optional
from uuid import UUID

from src.domain.exceptions.auth import (
    UserNotFoundError
)
from src.domain.exceptions.fields import (
    FieldRequiredException,
    FieldsDoNotMatchException
)

from src.domain.services.user import UserService

from src.domain.value_objects.shared.entity_id import EntityId
from src.domain.value_objects.shared.uploaded_file import UploadedFile
from src.domain.value_objects.shared.file_name import Filename

from src.domain.value_objects.user.raw_password import RawPassword
from src.domain.value_objects.user.username import Username

from src.application.ports.providers.file_uploader import FileUploader
from src.application.ports.gateways.user import UserGateway
from src.application.ports.transaction.transaction_manager import TransactionManager


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateUserRequest:
    avatar: Optional[bytes] = None
    username: Optional[str] = None
    password: Optional[str] = None
    repeat_password: Optional[str] = None


class UpdateUserResponse(TypedDict):
    username: str
    email: str
    avatar_filename: Optional[str]


class UpdateUserInteractor:
    def __init__(
            self,
            user_gateway: UserGateway,
            file_uploader: FileUploader,
            user_service: UserService,
            transaction_manager: TransactionManager,
    ):
        self._user_gateway = user_gateway
        self._file_uploader = file_uploader
        self._user_service = user_service
        self._transaction_manager = transaction_manager

    async def __call__(self, user_id: UUID, data: UpdateUserRequest) -> UpdateUserResponse:
        user = await self._user_gateway.read_by_id(user_id=EntityId(value=user_id))

        print(data)

        if not user:
            raise UserNotFoundError()

        if data.username:
            user.username = Username(data.username)

        if data.password:
            if not data.repeat_password:
                raise FieldRequiredException("repeat_password")

            password = RawPassword(data.password)
            repeat_password = RawPassword(data.repeat_password)

            if password != repeat_password:
                raise FieldsDoNotMatchException("password", "repeat_password")

            self._user_service.change_password(user, password)

        if avatar := data.avatar:
            avatar_filename = self._file_uploader.upload_image(UploadedFile(avatar).value)
            user.avatar_filename = Filename(avatar_filename)

        updated = await self._user_gateway.update(user)
        await self._transaction_manager.commit()

        return UpdateUserResponse(
            username=updated.username.value,
            email=updated.email.value,
            avatar_filename=updated.avatar_filename.value if updated.avatar_filename else None,
        )
