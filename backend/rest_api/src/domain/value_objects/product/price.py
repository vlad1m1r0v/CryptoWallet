from dataclasses import dataclass
from decimal import Decimal

from src.domain.exceptions import NegativeValueException

from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class ProductPrice(ValueObject):
    value: Decimal

    def __post_init__(self):
        super(ProductPrice, self).__post_init__()
        self._validate_price(self.value)

    @staticmethod
    def _validate_price(price_value: Decimal) -> None:
        if price_value < 0:
            raise NegativeValueException(field="price")

    def __lt__(self, other: "ProductPrice") -> bool:
        return self.value < other.value
