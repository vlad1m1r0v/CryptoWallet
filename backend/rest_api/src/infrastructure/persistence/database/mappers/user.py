from src.domain.value_objects.user.username import Username
from src.domain.value_objects.user.password_hash import PasswordHash
from src.domain.value_objects.shared.file_name import Filename
from src.domain.value_objects.shared.entity_id import EntityId
from src.domain.value_objects.user.email import Email

from src.domain.entities.user import User as UserE

from src.infrastructure.persistence.database.models.user import User as UserM
from src.infrastructure.persistence.database.mappers.base import BaseMapper


class UserMapper(BaseMapper[UserE, UserM]):
    @staticmethod
    def to_entity(model: UserM) -> UserE:
        return UserE(
            id_=EntityId(model.id),
            username=Username(model.username),
            email=Email(model.email),
            password_hash=PasswordHash(value=model.password_hash),
            avatar_filename=Filename(model.avatar_filename) if model.avatar_filename else None,
            is_active=model.is_active,
        )

    @staticmethod
    def to_model(user: UserE) -> UserM:
        return UserM(
            id=user.id_.value,
            username=user.username.value,
            email=user.email.value,
            password_hash=user.password_hash.value,
            avatar_filename=user.avatar_filename.value if user.avatar_filename else None,
            is_active=user.is_active,
        )
