from dataclasses import dataclass
from uuid import UUID

from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class EntityId(ValueObject):
    value: UUID