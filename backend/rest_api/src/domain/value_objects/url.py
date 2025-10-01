import re
from dataclasses import dataclass
from typing import ClassVar, Final

from src.domain.exceptions.base import DomainFieldError
from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class URL(ValueObject):
    """Validates URL value object. Raises DomainFieldError on invalid input."""

    PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"^(https?://)"         # http or https
        r"([a-zA-Z0-9.-]+)"            # somain
        r"(\.[a-zA-Z]{2,})"            # zone (.com, .org, .ua, etc.)
        r"(:\d+)?(/.*)?$",             # port (optional)
        re.IGNORECASE,
    )

    value: str

    def __post_init__(self) -> None:
        super(URL, self).__post_init__()
        self._validate_url(self.value)

    def _validate_url(self, url_value: str) -> None:
        if not re.fullmatch(self.PATTERN, url_value):
            raise DomainFieldError("Invalid URL format.")