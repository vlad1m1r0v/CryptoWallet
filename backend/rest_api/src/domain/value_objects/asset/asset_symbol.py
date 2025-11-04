from dataclasses import dataclass

from src.domain.exceptions import (
    UppercaseException,
    MinMaxLengthException
)

from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class AssetSymbol(ValueObject):
    value: str

    SYMBOL_MIN_LENGTH = 2
    SYMBOL_MAX_LENGTH = 10

    def __post_init__(self):
        super(AssetSymbol, self).__post_init__()
        self._validate_symbol(self.value)

    def _validate_symbol(self, symbol_value: str) -> None:
        if not symbol_value.isupper():
            raise UppercaseException(field="asset_symbol")
        if not (self.SYMBOL_MIN_LENGTH <= len(symbol_value) <= self.SYMBOL_MAX_LENGTH):
            raise MinMaxLengthException(
                field="asset_symbol",
                min_length=self.SYMBOL_MIN_LENGTH,
                max_length=self.SYMBOL_MAX_LENGTH
            )
