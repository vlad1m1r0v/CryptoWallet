from dataclasses import dataclass

from src.domain.exceptions.fields import MinMaxLengthException
from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class RawPrivateKey(ValueObject):
    value: str

    PRIVATE_KEY_MIN_LENGTH = 32
    PRIVATE_KEY_MAX_LENGTH = 128

    def __post_init__(self):
        super(RawPrivateKey, self).__post_init__()
        self._validate_length(self.value)

    def _validate_length(self, key_value: str) -> None:
        if not (self.PRIVATE_KEY_MIN_LENGTH <= len(key_value) <= self.PRIVATE_KEY_MAX_LENGTH):
            raise MinMaxLengthException(
                field="private_key",
                min_length=self.PRIVATE_KEY_MIN_LENGTH,
                max_length=self.PRIVATE_KEY_MAX_LENGTH
            )
