from dataclasses import dataclass
from typing import Any

from src.domain.exceptions import InvalidChoiceException
from src.domain.enums import OrderStatusEnum
from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class OrderStatus(ValueObject):
    value: OrderStatusEnum

    def __post_init__(self):
        super(OrderStatus, self).__post_init__()
        self._validate_order_status(order_status=self.value)

    @staticmethod
    def _validate_order_status(order_status: Any) -> None:
        if not isinstance(order_status, OrderStatusEnum):
            raise InvalidChoiceException(
                field="order_status",
                enum_cls=OrderStatusEnum,
                actual_value=order_status
            )
