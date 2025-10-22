import re
from dataclasses import dataclass
from typing import ClassVar

from src.domain.exceptions.fields import (
    MinMaxLengthException,
    InvalidStartException,
    InvalidEndException,
    ForbiddenCharactersException,
    ForbiddenConsecutiveCharactersException
)
from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class AssetName(ValueObject):
    """raises ValueObjectException"""

    MIN_LEN: ClassVar[int] = 5
    MAX_LEN: ClassVar[int] = 32

    # Pattern for validating an asset_name:
    # - starts with a letter (A-Z, a-z) or a digit (0-9)
    PATTERN_START: ClassVar[re.Pattern[str]] = re.compile(
        r"^[a-zA-Z0-9]",
    )
    # - can contain multiple special characters . - _ between letters and digits,
    PATTERN_ALLOWED_CHARS: ClassVar[re.Pattern[str]] = re.compile(
        r"[a-zA-Z0-9._-]*",
    )
    #   but only one special character can appear consecutively
    PATTERN_NO_CONSECUTIVE_SPECIALS: ClassVar[re.Pattern[str]] = re.compile(
        r"^[a-zA-Z0-9]+([._-]?[a-zA-Z0-9]+)*[._-]?$",
    )
    # - ends with a letter (A-Z, a-z) or a digit (0-9)
    PATTERN_END: ClassVar[re.Pattern[str]] = re.compile(
        r".*[a-zA-Z0-9]$",
    )

    value: str

    def __post_init__(self) -> None:
        """:raises ValueObjectException:"""
        super(AssetName, self).__post_init__()
        self._validate_asset_name_length(self.value)
        self._validate_asset_name_pattern(self.value)

    def _validate_asset_name_length(self, asset_name_value: str) -> None:
        """:raises ValueObjectException:"""
        if len(asset_name_value) < self.MIN_LEN or len(asset_name_value) > self.MAX_LEN:
            raise MinMaxLengthException(field="asset_name", min_length=self.MIN_LEN, max_length=self.MAX_LEN)

    def _validate_asset_name_pattern(self, asset_name_value: str) -> None:
        """:raises ValueObjectException:"""
        if not re.match(self.PATTERN_START, asset_name_value):
            raise InvalidStartException(field="asset_name")

        if not re.fullmatch(self.PATTERN_ALLOWED_CHARS, asset_name_value):
            raise ForbiddenCharactersException(value=asset_name_value)

        if not re.fullmatch(self.PATTERN_NO_CONSECUTIVE_SPECIALS, asset_name_value):
            raise ForbiddenConsecutiveCharactersException(field="asset_name")

        if not re.match(self.PATTERN_END, asset_name_value):
            raise InvalidEndException(field="asset_name")
