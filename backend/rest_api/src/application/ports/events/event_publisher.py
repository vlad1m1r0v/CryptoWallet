from abc import abstractmethod
from typing import Protocol

from src.application.dtos.events import (
    SaveUserEventDTO,
    GiveChatAccessEventDTO,
    UpdateUserEventDTO,
    CreateWalletEventDTO,
    SaveWalletEventDTO,
    UpdateWalletEventDTO,
    ImportWalletEventDTO,
    CreateTransactionEventDTO,
    SavePendingTransactionEventDTO,
    CompleteTransactionEventDTO,
    RequestFreeETHEventDTO,
    SaveProductEventDTO,
    CreateOrderEventDTO,
    PayOrderEventDTO,
    UpdateOrderEventDTO
)


class EventPublisher(Protocol):
    @abstractmethod
    async def save_user(self, dto: SaveUserEventDTO) -> None:
        ...

    @abstractmethod
    async def give_chat_access_to_user(self, dto: GiveChatAccessEventDTO) -> None:
        ...

    @abstractmethod
    async def update_user(self, dto: UpdateUserEventDTO) -> None:
        ...

    @abstractmethod
    async def create_eth_wallet(self, dto: CreateWalletEventDTO) -> None:
        ...

    @abstractmethod
    async def import_eth_wallet(self, dto: ImportWalletEventDTO) -> None:
        ...

    @abstractmethod
    async def save_wallet(self, dto: SaveWalletEventDTO) -> None:
        ...

    @abstractmethod
    async def update_wallet(self, dto: UpdateWalletEventDTO) -> None:
        ...

    @abstractmethod
    async def create_transaction(self, dto: CreateTransactionEventDTO) -> None:
        ...

    @abstractmethod
    async def save_pending_transaction(self, dto: SavePendingTransactionEventDTO) -> None:
        ...

    @abstractmethod
    async def complete_transaction(self, dto: CompleteTransactionEventDTO) -> None:
        ...

    @abstractmethod
    async def request_free_eth(self, dto: RequestFreeETHEventDTO) -> None:
        ...

    @abstractmethod
    async def save_product(self, dto: SaveProductEventDTO) -> None:
        ...

    @abstractmethod
    async def create_order(self, dto: CreateOrderEventDTO) -> None:
        ...

    @abstractmethod
    async def pay_order(self, dto: PayOrderEventDTO) -> None:
        ...

    @abstractmethod
    async def update_order(self, dto: UpdateOrderEventDTO) -> None:
        ...
