from abc import abstractmethod
from typing import Protocol

from src.domain.entities.wallet import Wallet


class WalletGateway(Protocol):
    @abstractmethod
    def add(self, wallet: Wallet) -> Wallet:
        ...