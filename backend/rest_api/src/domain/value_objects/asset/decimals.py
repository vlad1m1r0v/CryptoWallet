from dataclasses import dataclass

from src.domain.exceptions.fields import MinMaxValueException

from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class Decimals(ValueObject):
    value: int

    DECIMALS_MIN = 0
    DECIMALS_MAX = 30

    def __post_init__(self):
        super(Decimals, self).__post_init__()
        self._validate_decimals(self.value)

    def _validate_decimals(self, decimals_value: int) -> None:
        if not (self.DECIMALS_MIN <= decimals_value <= self.DECIMALS_MAX):
            raise MinMaxValueException(field="decimals", min_value=self.DECIMALS_MIN, max_value=self.DECIMALS_MAX)
