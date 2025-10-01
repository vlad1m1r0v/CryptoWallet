from dataclasses import dataclass

from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class PasswordHash(ValueObject):
    value: bytes