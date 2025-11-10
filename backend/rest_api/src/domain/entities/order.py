from typing import Optional

from src.domain.entities.base import Entity

from src.domain.value_objects import (
    EntityId,
    OrderStatus,
    Timestamp
)


class Order(Entity[EntityId]):
    def __init__(
            self,
            *,
            id_: EntityId,
            product_id: EntityId,
            wallet_id: EntityId,
            status: OrderStatus,
            created_at: Timestamp,
            payment_transaction_id: Optional[EntityId] = None,
            return_transaction_id: Optional[EntityId] = None,
    ) -> None:
        super().__init__(id_=id_)
        self.product_id = product_id
        self.wallet_id = wallet_id
        self.payment_transaction_id = payment_transaction_id
        self.return_transaction_id = return_transaction_id
        self.status = status
        self.created_at = created_at
