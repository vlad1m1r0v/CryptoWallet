import re
from dataclasses import dataclass
from typing import ClassVar

from src.domain.exceptions import InvalidFilenameException

from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class Filename(ValueObject):
    PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"^[\w\-\s]+\.[A-Za-z0-9]+$")
    value: str

    def __post_init__(self) -> None:
        super(Filename, self).__post_init__()
        self._validate_filename(self.value)

    def _validate_filename(self, filename_value: str) -> None:
        if not re.fullmatch(self.PATTERN, filename_value):
            raise InvalidFilenameException(filename=filename_value)
