from typing import Generic, TypeVar, List
from pydantic.generics import GenericModel

T = TypeVar("T")

class PaginatedResultSchema(GenericModel, Generic[T]):
    items: List[T]
    page: int
    total_pages: int