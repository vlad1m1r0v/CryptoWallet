from typing import Optional

from src.domain.entities.user import User

from src.domain.ports.password_hasher import PasswordHasher
from src.domain.ports.id_generator import IdGenerator

from src.domain.value_objects.user.email import Email
from src.domain.value_objects.user.raw_password import RawPassword
from src.domain.value_objects.user.username import Username
from src.domain.value_objects.shared.file_name import Filename


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
        password_hash = self._password_hasher.hash(raw_password)

        return User(
            id_=user_id,
            username=username,
            email=email,
            avatar_filename=avatar_filename,
            password_hash=password_hash,
            is_active=is_active,
        )

    def is_password_valid(self, user: User, raw_password: RawPassword) -> bool:
        return self._password_hasher.verify(
            raw_password=raw_password,
            hashed_password=user.password_hash,
        )

    def change_password(
            self,
            user: User,
            raw_password: RawPassword
    ) -> None:
        user.password_hash = self._password_hasher.hash(raw_password)
