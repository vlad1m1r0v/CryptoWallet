from src.domain.enums import OrderStatusEnum

from src.domain.entities import Order

from src.domain.ports import (
    IdGenerator,
    TimestampGenerator
)

from src.domain.value_objects import (
    EntityId,
    OrderStatus
)


class OrderService:
    def __init__(
            self,
            id_generator: IdGenerator,
            timestamp_generator: TimestampGenerator,
    ) -> None:
        self._id_generator = id_generator
        self._timestamp_generator = timestamp_generator

    def create_order(
            self,
            wallet_id: EntityId,
            product_id: EntityId,
    ) -> Order:
        order_id = self._id_generator()
        created_at = self._timestamp_generator()

        return Order(
            id_=order_id,
            wallet_id=wallet_id,
            product_id=product_id,
            status=OrderStatus(OrderStatusEnum.NEW),
            created_at=created_at
        )
