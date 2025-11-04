from dataclasses import dataclass
from decimal import Decimal

from src.domain.exceptions import NegativeValueException

from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class TransactionFee(ValueObject):
    value: Decimal

    def __post_init__(self):
        super(TransactionFee, self).__post_init__()
        self._validate_balance(self.value)

    @staticmethod
    def _validate_balance(balance_value: Decimal) -> None:
        if balance_value < 0:
            raise NegativeValueException(field="fee")