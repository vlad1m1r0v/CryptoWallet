from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")

@dataclass
class PaginatedResponseDTO(Generic[T]):
    items: list[T]
    page: int
    total_pages: int