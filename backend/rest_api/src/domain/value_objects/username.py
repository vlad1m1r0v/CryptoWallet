import re
from dataclasses import dataclass
from typing import ClassVar

from src.domain.exceptions.fields import (
    InvalidUsernameLengthError,
    InvalidUsernameStartError,
    InvalidUsernameCharacterError,
    InvalidUsernameConsecutiveCharactersError,
    InvalidUsernameEndError
)
from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class Username(ValueObject):
    """raises DomainFieldError"""

    MIN_LEN: ClassVar[int] = 5
    MAX_LEN: ClassVar[int] = 32

    # Pattern for validating a username:
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
        """:raises DomainFieldError:"""
        super(Username, self).__post_init__()
        self._validate_username_length(self.value)
        self._validate_username_pattern(self.value)

    def _validate_username_length(self, username_value: str) -> None:
        """:raises DomainFieldError:"""
        if len(username_value) < self.MIN_LEN or len(username_value) > self.MAX_LEN:
            raise InvalidUsernameLengthError()

    def _validate_username_pattern(self, username_value: str) -> None:
        """:raises DomainFieldError:"""
        if not re.match(self.PATTERN_START, username_value):
            raise InvalidUsernameStartError()

        if not re.fullmatch(self.PATTERN_ALLOWED_CHARS, username_value):
            raise InvalidUsernameCharacterError()

        if not re.fullmatch(self.PATTERN_NO_CONSECUTIVE_SPECIALS, username_value):
            raise InvalidUsernameConsecutiveCharactersError()

        if not re.match(self.PATTERN_END, username_value):
            raise InvalidUsernameEndError()
