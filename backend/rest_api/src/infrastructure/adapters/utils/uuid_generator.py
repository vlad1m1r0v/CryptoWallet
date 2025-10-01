from uuid import UUID

import uuid6

from src.domain.ports.id_generator import IdGenerator


class UuidGenerator(IdGenerator):
    def __call__(self) -> UUID:
        return uuid6.uuid7()
