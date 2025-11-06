from src.domain.entities import Product

from src.domain.ports import (
    IdGenerator,
    TimestampGenerator
)

from src.domain.value_objects import (
    EntityId,
    ProductPrice,
    ProductName,
    Filename
)


class ProductService:
    def __init__(
            self,
            id_generator: IdGenerator,
            timestamp_generator: TimestampGenerator,
    ) -> None:
        self._id_generator = id_generator
        self._timestamp_generator = timestamp_generator

    def create_product(
            self,
            wallet_id: EntityId,
            name: ProductName,
            price: ProductPrice,
            photo_filename: Filename,
    ) -> Product:
        product_id = self._id_generator()
        created_at = self._timestamp_generator()

        return Product(
            id_=product_id,
            wallet_id=wallet_id,
            name=name,
            price=price,
            photo_filename=photo_filename,
            created_at=created_at,
        )
