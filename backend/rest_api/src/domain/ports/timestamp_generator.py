from abc import abstractmethod, ABC

from src.domain.value_objects import Timestamp


class TimestampGenerator(ABC):
    @abstractmethod
    def __call__(self) -> Timestamp: ...