from uuid import UUID

from src.domain.exceptions import (
    UserNotFoundException,
    FieldRequiredException,
    FieldsDoNotMatchException
)

from src.domain.services import UserService
from src.domain.value_objects import (
    EntityId,
    UploadedFile,
    Filename,
    RawPassword,
    Username
)

from src.application.ports.providers import FileUploader
from src.application.ports.gateways import UserGateway
from src.application.ports.transaction import TransactionManager
from src.application.dtos.request import UpdateUserRequestDTO
from src.application.dtos.response import UpdateUserResponseDTO


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

    async def __call__(self, user_id: UUID, data: UpdateUserRequestDTO) -> UpdateUserResponseDTO:
        user = await self._user_gateway.read_by_id(user_id=EntityId(value=user_id))

        if not user:
            raise UserNotFoundException()

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

        return UpdateUserResponseDTO(
            username=updated.username.value,
            email=updated.email.value,
            avatar_filename=updated.avatar_filename.value if updated.avatar_filename else None,
        )
