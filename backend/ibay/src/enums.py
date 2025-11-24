from enum import StrEnum, auto


class OrderStatusEnum(StrEnum):
    NEW = auto()
    FAILED = auto()
    DELIVERING = auto()
    RETURNED = auto()
    COMPLETED = auto()