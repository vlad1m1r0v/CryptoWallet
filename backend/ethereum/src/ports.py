from abc import ABC, abstractmethod
from uuid import UUID

from src.schemas import ETHWalletSchema

class EthereumServicePort(ABC):
    @abstractmethod
    def create_wallet(self, user_id: UUID) -> ETHWalletSchema:
        ...

    @abstractmethod
    def import_wallet(self, user_id: UUID, private_key: str) -> ETHWalletSchema:
        ...