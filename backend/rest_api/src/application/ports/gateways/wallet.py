from abc import abstractmethod
from typing import Protocol, overload, Union
from uuid import UUID
from decimal import Decimal

from src.domain.entities import Wallet

from src.application.dtos.response import WalletResponseDTO


class WalletGateway(Protocol):
    @abstractmethod
    def add(self, wallet: Wallet) -> None:
        ...

    @overload
    @abstractmethod
    async def read(self, address: str) -> WalletResponseDTO | None:
        ...

    @overload
    @abstractmethod
    async def read(self, wallet_id: UUID) -> WalletResponseDTO | None:
        ...

    @abstractmethod
    async def read(self, arg: Union[UUID | str]) -> WalletResponseDTO | None:
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
