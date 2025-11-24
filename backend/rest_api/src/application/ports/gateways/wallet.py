from abc import abstractmethod
from typing import Protocol, Optional
from uuid import UUID
from decimal import Decimal

from src.domain.entities import Wallet

from src.application.dtos.response import WalletResponseDTO


class WalletGateway(Protocol):
    @abstractmethod
    def add(self, wallet: Wallet) -> None:
        ...

    @abstractmethod
    async def read(
            self,
            *,
            address: Optional[str] = None,
            wallet_id: Optional[UUID] = None
    ) -> WalletResponseDTO | None:
        ...

    @abstractmethod
    async def decrement_balance(self, wallet_id: UUID, amount: Decimal) -> None:
        ...

    @abstractmethod
    async def increment_balance(self, wallet_id: UUID, amount: Decimal) -> None:
        ...

    @abstractmethod
    async def list(self, user_id: UUID) -> list[WalletResponseDTO]:
        ...
