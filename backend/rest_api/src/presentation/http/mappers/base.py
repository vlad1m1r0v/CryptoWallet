from abc import ABC, abstractmethod
from typing import Generic, TypeVar

P = TypeVar("P")
RQ = TypeVar("RQ")
RS = TypeVar("RS")

class BaseMapper(ABC, Generic[P, RQ, RS]):
    @staticmethod
    @abstractmethod
    def to_request_dto(schema: P) -> RQ:
        ...

    @staticmethod
    @abstractmethod
    def to_response_schema(dto: RS) -> P:
        ...