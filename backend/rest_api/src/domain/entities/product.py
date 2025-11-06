from src.domain.entities.base import Entity

from src.domain.value_objects import (
    EntityId,
    ProductPrice,
    ProductName,
    Filename,
    Timestamp
)


class Product(Entity[EntityId]):
    def __init__(
            self,
            *,
            id_: EntityId,
            wallet_id: EntityId,
            name: ProductName,
            price: ProductPrice,
            photo_filename: Filename,
            created_at: Timestamp

    ) -> None:
        super().__init__(id_=id_)
        self.wallet_id = wallet_id
        self.name = name
        self.price = price
        self.photo_filename = photo_filename
        self.created_at = created_at
