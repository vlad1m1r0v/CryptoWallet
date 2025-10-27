import asyncio
from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID

from src.consts import GAS, GAS_PRICE_GWEI
from src.schemas import (
    TransactionSchema,
    ETHWalletSchema
)


class StoragePort(ABC):
    @abstractmethod
    async def add_transaction_hash(self, tx_hash: str) -> None:
        pass

    @abstractmethod
    async def get_all_transaction_hashes(self) -> list[str]:
        pass

    @abstractmethod
    async def remove_transaction_hash(self, tx_hash: str) -> None:
        pass


class EthereumServicePort(ABC):
    @abstractmethod
    def create_wallet(self, user_id: UUID) -> ETHWalletSchema:
        ...

    @abstractmethod
    def import_wallet(self, user_id: UUID, private_key: str) -> ETHWalletSchema:
        ...

    @abstractmethod
    async def create_transaction(
            self,
            private_key: str,
            to_address: str,
            amount: Decimal,
            gas: int = GAS,
            gas_price_gwei: int = GAS_PRICE_GWEI,
    ) -> TransactionSchema:
        ...


class BlockListenerPort(ABC):
    @abstractmethod
    def run(self) -> asyncio.Task:
        ...