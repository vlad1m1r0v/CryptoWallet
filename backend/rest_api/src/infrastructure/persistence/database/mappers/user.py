from src.domain.entities.user import User as UserE
from src.infrastructure.persistence.database.models.user import User as UserM
from src.infrastructure.persistence.database.mappers.base import BaseMapper
from src.domain.value_objects.username import Username
from src.domain.value_objects.password_hash import PasswordHash
from src.domain.value_objects.url import URL
from src.domain.value_objects.entity_id import EntityId
from src.domain.value_objects.email import Email

class UserMapper(BaseMapper[UserE, UserM]):
    @staticmethod
    def to_entity(model: UserM) -> UserE:

        return UserE(
            id_=EntityId(model.id),
            username=Username(model.username),
            email=Email(model.email),
            password_hash=PasswordHash(model.password_hash.encode("utf-8")),
            avatar_url=URL(model.avatar_url) if model.avatar_url else None,
            is_active=model.is_active,
        )

    @staticmethod
    def to_model(user: UserE) -> UserM:
        return UserM(
            id=user.id_.value,
            username=user.username.value,
            email=user.email.value,
            password_hash=str(user.password_hash.value),
            avatar_url=user.avatar_url.value if user.avatar_url else None,
            is_active=user.is_active,
        )