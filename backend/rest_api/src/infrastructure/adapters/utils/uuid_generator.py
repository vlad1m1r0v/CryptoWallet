import uuid6

from src.domain.value_objects import EntityId

from src.domain.ports import IdGenerator


class UuidGenerator(IdGenerator):
    def __call__(self) -> EntityId:
        return EntityId(uuid6.uuid7())
