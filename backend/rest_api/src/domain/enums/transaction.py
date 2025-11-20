from enum import StrEnum, auto


class TransactionStatusEnum(StrEnum):
    SUCCESSFUL = auto()
    PENDING = auto()
    FAILED = auto()
