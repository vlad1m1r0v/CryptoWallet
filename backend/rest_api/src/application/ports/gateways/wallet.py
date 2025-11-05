from abc import abstractmethod
from typing import Protocol

from src.domain.value_objects import (
    EntityId,
    Address,
    Balance
)
from src.domain.entities import Wallet

from src.application.dtos.response import WalletsListItemResponseDTO



class WalletGateway(Protocol):
    @abstractmethod
    def add(self, wallet: Wallet) -> Wallet:
        ...

    @abstractmethod
    async def read_by_address(self, address: Address) -> Wallet | None:
        ...

    @abstractmethod
    async def read_by_id(self, wallet_id: EntityId) -> Wallet | None:
        ...

    @abstractmethod
    async def decrement_balance(self, wallet_id: EntityId, amount: Balance) -> Wallet:
        ...

    @abstractmethod
    async def increment_balance(self, wallet_id: EntityId, amount: Balance) -> Wallet:
        ...

    @abstractmethod
    async def get_user_wallets(self, user_id: EntityId) -> list[WalletsListItemResponseDTO]:
        ...