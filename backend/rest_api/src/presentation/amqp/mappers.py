from typing import Generic, TypeVar
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.application.dtos.request import (
    SaveCreateWalletRequestDTO,
    SaveImportWalletRequestTransactionDTO,
    SaveImportWalletRequestDTO,
    CreatePendingTransactionRequestDTO,
    UpdateTransactionRequestDTO
)

from src.presentation.amqp.types import (
    SaveCreateWalletRequestDict,
    SaveImportWalletRequestTransactionDict,
    SaveImportWalletRequestDict,
    CreatePendingTransactionRequestDict,
    UpdateTransactionRequestDict
)

TD = TypeVar("TD", bound=dict)
DC = TypeVar("DC", bound=dataclass)


class BaseMapper(ABC, Generic[TD, DC]):
    @staticmethod
    @abstractmethod
    def to_dataclass(td: TD) -> DC:
        ...


class SaveCreateWalletRequestMapper(
    BaseMapper[
        SaveCreateWalletRequestDict,
        SaveCreateWalletRequestDTO
    ]
):
    @staticmethod
    def to_dataclass(td: SaveCreateWalletRequestDict) -> SaveCreateWalletRequestDTO:
        return SaveCreateWalletRequestDTO(**td)


class SaveImportWalletRequestTransactionMapper(
    BaseMapper[
        SaveImportWalletRequestTransactionDict,
        SaveImportWalletRequestTransactionDTO
    ]
):
    @staticmethod
    def to_dataclass(td: SaveImportWalletRequestTransactionDict) -> SaveImportWalletRequestTransactionDTO:
        return SaveImportWalletRequestTransactionDTO(**td)


class SaveImportWalletRequestMapper(
    BaseMapper[
        SaveImportWalletRequestDict,
        SaveImportWalletRequestDTO
    ]
):
    @staticmethod
    def to_dataclass(td: SaveImportWalletRequestDict) -> SaveImportWalletRequestDTO:
        transactions_data = [
            SaveImportWalletRequestTransactionMapper.to_dataclass(t_dict)
            for t_dict in td['transactions']
        ]

        td_copy = dict(td)
        td_copy['transactions'] = transactions_data

        return SaveImportWalletRequestDTO(**td_copy)


class CreatePendingTransactionRequestMapper(
    BaseMapper[
        CreatePendingTransactionRequestDict,
        CreatePendingTransactionRequestDTO
    ]
):
    @staticmethod
    def to_dataclass(td: CreatePendingTransactionRequestDict) -> CreatePendingTransactionRequestDTO:
        return CreatePendingTransactionRequestDTO(**td)


class UpdateTransactionRequestMapper(
    BaseMapper[
        UpdateTransactionRequestDict,
        UpdateTransactionRequestDTO
    ]
):
    @staticmethod
    def to_dataclass(td: UpdateTransactionRequestDict) -> UpdateTransactionRequestDTO:
        return UpdateTransactionRequestDTO(**td)
