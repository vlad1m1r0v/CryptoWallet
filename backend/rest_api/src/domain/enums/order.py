from enum import StrEnum


class OrderStatusEnum(StrEnum):
    NEW = "NEW"
    FAILED = "FAILED"
    DELIVERING = "DELIVERING"
    RETURNED = "RETURNED"
    COMPLETED = "COMPLETED"
