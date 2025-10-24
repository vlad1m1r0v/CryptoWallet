from enum import StrEnum


class TransactionStatusEnum(StrEnum):
    SUCCESSFUL = "successful"
    PENDING = "pending"
    FAILED = "failed"
