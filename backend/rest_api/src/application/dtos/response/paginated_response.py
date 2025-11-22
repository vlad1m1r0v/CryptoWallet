from typing import Generic, TypedDict, TypeVar

T = TypeVar("T")

class PaginatedResponseDTO(TypedDict, Generic[T]):
    items: list[T]
    page: int
    total_pages: int