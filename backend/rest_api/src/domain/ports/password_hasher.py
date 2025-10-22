from abc import abstractmethod
from typing import Protocol

from src.domain.value_objects.user.password_hash import PasswordHash
from src.domain.value_objects.user.raw_password import RawPassword


class PasswordHasher(Protocol):
    @abstractmethod
    def hash(self, raw_password: RawPassword) -> PasswordHash: ...

    @abstractmethod
    def verify(self, *, raw_password: RawPassword, hashed_password: PasswordHash) -> bool: ...
