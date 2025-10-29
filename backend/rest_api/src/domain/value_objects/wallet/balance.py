from dataclasses import dataclass
from decimal import Decimal

from src.domain.exceptions.fields import NegativeValueException
from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class Balance(ValueObject):
    value: Decimal

    def __post_init__(self):
        super(Balance, self).__post_init__()
        self._validate_balance(self.value)

    @staticmethod
    def _validate_balance(balance_value: Decimal) -> None:
        if balance_value < 0:
            raise NegativeValueException(field="balance")

    def __lt__(self, other: "Balance") -> bool:
        return self.value < other.value
