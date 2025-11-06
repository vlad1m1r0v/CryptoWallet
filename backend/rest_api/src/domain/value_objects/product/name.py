import re
from dataclasses import dataclass
from typing import ClassVar

from src.domain.exceptions import (
    MinMaxLengthException,
    InvalidProductNameException
)
from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class ProductName(ValueObject):
    MAX_LEN: ClassVar[int] = 50
    MIN_LEN: ClassVar[int] = 3
    PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"^[A-Z][a-zA-Z]*(\s[A-Z][a-zA-Z]*)*(\s[0-9]+)?$")

    value: str

    def __post_init__(self) -> None:
        super(ProductName, self).__post_init__()
        self._validate_product_name(self.value)

    def _validate_product_name(self, name_value: str) -> None:
        if len(name_value) < self.MIN_LEN or len(name_value) > self.MAX_LEN:
            raise MinMaxLengthException(field="name", min_length=self.MIN_LEN, max_length=self.MAX_LEN)

        if not re.fullmatch(self.PATTERN, name_value):
            raise InvalidProductNameException()
