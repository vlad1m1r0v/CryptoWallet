from dataclasses import dataclass

from src.domain.exceptions.fields import NegativeValueException
from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class Balance(ValueObject):
    value: int

    def __post_init__(self):
        super(Balance, self).__post_init__()
        self._validate_balance(self.value)

    @staticmethod
    def _validate_balance(balance_value: int) -> None:
        if balance_value < 0:
            raise NegativeValueException(field="balance")
