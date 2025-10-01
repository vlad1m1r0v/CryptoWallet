from abc import abstractmethod, ABC
from uuid import UUID


class IdGenerator(ABC):
    @abstractmethod
    def __call__(self) -> UUID: ...