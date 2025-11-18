from enum import StrEnum


class TransactionStatusEnum(StrEnum):
    SUCCESSFUL = "SUCCESSFUL"
    PENDING = "PENDING"
    FAILED = "FAILED"
