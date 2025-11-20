from src.domain.entities import Permissions
from src.domain.ports import IdGenerator

from src.domain.value_objects import (
    EntityId,
    HasChatAccess
)


class PermissionsService:
    def __init__(
            self,
            id_generator: IdGenerator
    ) -> None:
        self._id_generator = id_generator

    def create_permissions(
            self,
            user_id: EntityId,
    ) -> Permissions:
        permissions_id = self._id_generator()
        has_chat_access = HasChatAccess(False)

        return Permissions(
            id_=permissions_id,
            user_id=user_id,
            has_chat_access=has_chat_access
        )
