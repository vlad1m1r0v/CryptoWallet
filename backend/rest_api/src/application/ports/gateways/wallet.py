from abc import abstractmethod
from typing import Protocol

from src.domain.value_objects.wallet.address import Address

from src.domain.entities.wallet import Wallet


class WalletGateway(Protocol):
    @abstractmethod
    def add(self, wallet: Wallet) -> Wallet:
        ...

    @abstractmethod
    async def read_by_address(self, address: Address) -> Wallet | None:
        ...