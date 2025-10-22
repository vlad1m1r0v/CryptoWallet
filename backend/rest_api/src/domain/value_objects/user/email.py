import re
from dataclasses import dataclass
from typing import ClassVar

from src.domain.exceptions.fields import InvalidEmailException

from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class Email(ValueObject):
    """Validates Email value object. Raises DomainFieldError on invalid input."""
    PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )

    value: str

    def __post_init__(self) -> None:
        super(Email, self).__post_init__()
        self._validate_email(self.value)

    def _validate_email(self, email_value: str) -> None:
        if not re.fullmatch(self.PATTERN, email_value):
            raise InvalidEmailException(email=email_value)
