from typing import Optional

from src.domain.entities.user import User

from src.domain.ports.password_hasher import PasswordHasher
from src.domain.ports.id_generator import IdGenerator

from src.domain.value_objects.email import Email
from src.domain.value_objects.raw_password import RawPassword
from src.domain.value_objects.entity_id import EntityId
from src.domain.value_objects.password_hash import PasswordHash
from src.domain.value_objects.username import Username
from src.domain.value_objects.url import URL


class UserService:
    def __init__(
            self,
            id_generator: IdGenerator,
            password_hasher: PasswordHasher,
    ) -> None:
        self._id_generator = id_generator
        self._password_hasher = password_hasher

    def create_user(
            self,
            username: Username,
            email: Email,
            raw_password: RawPassword,
            avatar_url: Optional[URL] = None,
            is_active: bool = True,
    ) -> User:
        user_id = EntityId(self._id_generator())
        password_hash = PasswordHash(self._password_hasher.hash(raw_password))

        return User(
            id_=user_id,
            username=username,
            email=email,
            avatar_url=avatar_url,
            password_hash=password_hash,
            is_active=is_active,
        )

    def is_password_valid(self, user: User, raw_password: RawPassword) -> bool:
        return self._password_hasher.verify(
            raw_password=raw_password,
            hashed_password=user.password_hash.value,
        )

    def change_password(
            self,
            user: User,
            raw_password: RawPassword
    ) -> None:
        hashed_password = PasswordHash(self._password_hasher.hash(raw_password))
        user.password_hash = hashed_password
