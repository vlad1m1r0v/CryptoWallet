from abc import abstractmethod, ABC

from src.domain.value_objects import EntityId


class IdGenerator(ABC):
    @abstractmethod
    def __call__(self) -> EntityId: ...