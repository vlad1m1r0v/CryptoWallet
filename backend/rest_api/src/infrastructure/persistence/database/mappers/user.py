from src.domain.value_objects import (
    Username,
    PasswordHash,
    Filename,
    EntityId,
    Email
)
from src.domain.entities import User as UserE

from src.infrastructure.persistence.database.models import User as UserM
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
