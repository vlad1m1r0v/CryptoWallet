from src.domain.entities.base import Entity

from src.domain.value_objects import (
    EntityId,
    HasChatAccess
)


class Permissions(Entity[EntityId]):
    def __init__(
            self,
            *,
            id_: EntityId,
            user_id: EntityId,
            has_chat_access: HasChatAccess
    ) -> None:
        super().__init__(id_=id_)
        self.user_id = user_id
        self.has_chat_access = has_chat_access
