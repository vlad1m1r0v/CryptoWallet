from enum import StrEnum


class OrderStatusEnum(StrEnum):
    NEW = "new"
    FAILED = "failed"
    DELIVERING = "delivering"
    RETURNED = "returned"
    COMPLETED = "completed"
