from typing import Optional

from src.domain.entities.base import Entity
from src.domain.value_objects.entity_id import EntityId
from src.domain.value_objects.password_hash import PasswordHash
from src.domain.value_objects.username import Username
from src.domain.value_objects.email import Email
from src.domain.value_objects.url import URL


class User(Entity[EntityId]):
    def __init__(
            self,
            *,
            id_: EntityId,
            username: Username,
            email: Email,
            password_hash: PasswordHash,
            avatar_url: Optional[URL] = None,
            is_active: bool,
    ) -> None:
        super().__init__(id_=id_)
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.avatar_url = avatar_url
        self.is_active = is_active
