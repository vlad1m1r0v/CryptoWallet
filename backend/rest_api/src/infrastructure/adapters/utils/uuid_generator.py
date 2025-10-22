import uuid6

from src.domain.value_objects.shared.entity_id import EntityId

from src.domain.ports.id_generator import IdGenerator


class UuidGenerator(IdGenerator):
    def __call__(self) -> EntityId:
        return EntityId(uuid6.uuid7())
