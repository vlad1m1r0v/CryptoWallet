from typing import Sequence, overload

from src.domain.entities.product import Product as ProductE

from src.application.dtos.response import (
    ProductResponseDTO,
    ProductResponseWalletDTO,
    ProductResponseAssetDTO
)

from src.infrastructure.persistence.database.models import Product as ProductM


class ProductMapper:
    @staticmethod
    def to_model(entity: ProductE) -> ProductM:
        return ProductM(
            id=entity.id_.value,
            wallet_id=entity.wallet_id.value,
            name=entity.name.value,
            price=entity.price.value,
            photo_filename=entity.photo_filename.value,
            created_at=entity.created_at.value
        )

    @staticmethod
    def __base_to_dto(model: ProductM) -> ProductResponseDTO:
        return ProductResponseDTO(
            id=model.id,
            name=model.name,
            price=model.price,
            photo_filename=model.photo_filename,
            created_at=model.created_at,
            wallet=ProductResponseWalletDTO(
                user_id=model.wallet.user_id,
                address=model.wallet.address,
                asset=ProductResponseAssetDTO(
                    symbol=model.wallet.asset.symbol,
                    decimals=model.wallet.asset.decimals
                )
            )
        )

    @overload
    @staticmethod
    def to_dto(model: ProductM) -> ProductResponseDTO:
        ...

    @overload
    @staticmethod
    def to_dto(models: Sequence[ProductM]) -> list[ProductResponseDTO]:
        ...

    @staticmethod
    def to_dto(arg: ProductM | Sequence[ProductM]) -> ProductResponseDTO | list[ProductResponseDTO]:
        if isinstance(arg, ProductM):
            return ProductMapper.__base_to_dto(arg)
        else:
            return [ProductMapper.__base_to_dto(arg) for arg in arg]
