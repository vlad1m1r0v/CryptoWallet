from dataclasses import dataclass

from src.domain.exceptions.fields import (
    MinMaxLengthException,
    InvalidAddressStartException
)

from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class Address(ValueObject):
    value: str

    ADDRESS_LENGTH = 42

    def __post_init__(self):
        super(Address, self).__post_init__()

        self._validate_address(self.value)

    def _validate_address(self, address_value: str):
        if not address_value.startswith("0x"):
            raise InvalidAddressStartException(field="address")

        if not len(address_value) == self.ADDRESS_LENGTH:
            raise MinMaxLengthException(field="address", min_length=self.ADDRESS_LENGTH, max_length=self.ADDRESS_LENGTH)
