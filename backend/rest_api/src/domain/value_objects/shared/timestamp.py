from dataclasses import dataclass

from datetime import datetime, timezone

from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class Timestamp(ValueObject):
    value: datetime

    def __post_init__(self):
        super(Timestamp, self).__post_init__()

        if self.value.tzinfo is None:
            object.__setattr__(self, "value", self.value.replace(tzinfo=timezone.utc))
