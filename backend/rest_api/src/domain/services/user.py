from typing import Optional

from src.domain.entities import User

from src.domain.ports import (
    PasswordHasher,
    IdGenerator
)

from src.domain.value_objects import (
    Username,
    Email,
    RawPassword,
    PasswordHash,
    Filename
)


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
            avatar_filename: Optional[Filename] = None,
            is_active: bool = True,
    ) -> User:
        user_id = self._id_generator()
        password_hash = PasswordHash(self._password_hasher.hash(raw_password.value))

        return User(
            id_=user_id,
            username=username,
            email=email,
            avatar_filename=avatar_filename,
            password_hash=password_hash,
            is_active=is_active,
        )
