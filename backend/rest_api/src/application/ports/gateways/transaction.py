from typing import Protocol, List, Optional
from abc import abstractmethod
from datetime import datetime
from uuid import UUID

from src.domain.enums import TransactionStatusEnum
from src.domain.entities import Transaction

from src.application.enums import SortOrderEnum
from src.application.dtos.request import TransactionSortField
from src.application.dtos.response import (
    PaginatedResponseDTO,
    TransactionResponseDTO
)

class TransactionGateway(Protocol):
    @abstractmethod
    def add(self, transactions: List[Transaction]) -> None:
        ...

    @abstractmethod
    async def read(self, tx_hash: str) -> TransactionResponseDTO | None:
        ...

    @abstractmethod
    async def update(
            self,
            created_at: datetime,
            tx_hash: str,
            status: TransactionStatusEnum,
    ) -> None:
        ...

    @abstractmethod
    async def list(
            self,
            wallet_id: UUID,
            sort: Optional[TransactionSortField] = "created_at",
            order: Optional[SortOrderEnum] = SortOrderEnum.ASC,
            page: Optional[int] = 1
    ) -> PaginatedResponseDTO[TransactionResponseDTO]:
        ...
