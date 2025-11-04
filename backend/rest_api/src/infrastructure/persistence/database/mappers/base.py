from typing import Generic, TypeVar, Sequence
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.entities.base import Entity

from src.application.dtos.response.paginated_response import PaginatedResponseDTO

# Типи для generic
E = TypeVar("E", bound=Entity)  # Domain entity
M = TypeVar("M")  # ORM model (SQLAlchemy)
DTO = TypeVar("DTO", bound=dataclass)  # DTOs


class BaseMapper(ABC, Generic[E, M]):
    @staticmethod
    @abstractmethod
    def to_entity(model: M) -> E:
        ...

    @staticmethod
    @abstractmethod
    def to_model(entity: E) -> M:
        ...

    @classmethod
    def to_entity_m2m(cls, models: Sequence[M]) -> list[E]:
        return [cls.to_entity(model) for model in models]

    @classmethod
    def to_model_m2m(cls, entities: list[E]) -> list[M]:
        return [cls.to_model(entity) for entity in entities]


class BasePaginatedMapper(ABC, Generic[M, DTO]):
    @staticmethod
    @abstractmethod
    def to_paginated_dto(models: Sequence[M], page: int, total_pages: int) -> PaginatedResponseDTO[DTO]:
        ...
