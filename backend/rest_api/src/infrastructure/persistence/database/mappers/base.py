from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.domain.entities.base import Entity

# Типи для generic
E = TypeVar("E", bound=Entity)   # Domain entity
M = TypeVar("M")                 # ORM model (SQLAlchemy)

class BaseMapper(ABC, Generic[E, M]):
    @staticmethod
    @abstractmethod
    def to_entity(model: M) -> E:
        ...

    @staticmethod
    @abstractmethod
    def to_model(entity: E) -> M:
        ...