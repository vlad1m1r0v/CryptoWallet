import re
from dataclasses import dataclass
from typing import ClassVar

from src.domain.exceptions.base import DomainFieldError
from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class RawPassword(ValueObject):
    """Validates password according to security rules."""

    MIN_LEN: ClassVar[int] = 8
    MAX_LEN: ClassVar[int] = 20

    # At least 1 uppercase, 1 lowercase, 1 digit, 1 special character
    PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"^(?=.*[a-z])"       # at least one lowercase
        r"(?=.*[A-Z])"        # at least one uppercase
        r"(?=.*\d)"           # at least one digit
        r"(?=.*[^A-Za-z0-9])" # at least one special character
        r".{8,20}$"           # length 8-20
    )

    value: str

    def __post_init__(self) -> None:
        super(RawPassword, self).__post_init__()
        self._validate_password(self.value)

    def _validate_password(self, password_value: str) -> None:
        if not re.fullmatch(self.PATTERN, password_value):
            raise DomainFieldError(
                f"Password must be {self.MIN_LEN}-{self.MAX_LEN} characters long, "
                "contain at least one lowercase, one uppercase, one digit, "
                "and one special character."
            )