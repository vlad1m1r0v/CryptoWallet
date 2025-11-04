from abc import ABC, abstractmethod
from typing import Generic, TypeVar

RQ_DTO = TypeVar("RQ_DTO")
RS_DTO = TypeVar("RS_DTO")
RQ_SCHEMA = TypeVar("RQ_SCHEMA")
RS_SCHEMA = TypeVar("RS_SCHEMA")

class BaseMapper(ABC, Generic[RQ_DTO, RS_DTO, RQ_SCHEMA, RS_SCHEMA]):
    @staticmethod
    @abstractmethod
    def to_request_dto(schema: RQ_SCHEMA) -> RQ_DTO:
        ...

    @staticmethod
    @abstractmethod
    def to_response_schema(dto: RS_DTO) -> RS_SCHEMA:
        ...