from typing import Generic, TypedDict, TypeVar, List

T = TypeVar("T")

class PaginatedResponseDTO(TypedDict, Generic[T]):
    items: List[T]
    page: int
    per_page: int
    total_pages: int
    total_records: int