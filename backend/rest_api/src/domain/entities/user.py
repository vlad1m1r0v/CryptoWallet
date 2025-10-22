from typing import Optional

from src.domain.entities.base import Entity

from src.domain.value_objects.shared.entity_id import EntityId
from src.domain.value_objects.shared.file_name import Filename

from src.domain.value_objects.user.username import Username
from src.domain.value_objects.user.email import Email
from src.domain.value_objects.user.password_hash import PasswordHash


class User(Entity[EntityId]):
    def __init__(
            self,
            *,
            id_: EntityId,
            username: Username,
            email: Email,
            password_hash: PasswordHash,
            avatar_filename: Optional[Filename] = None,
            is_active: bool,
    ) -> None:
        super().__init__(id_=id_)
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.avatar_filename = avatar_filename
        self.is_active = is_active
