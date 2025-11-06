from typing import Sequence

from src.domain.entities.product import Product as ProductE

from src.application.dtos.response import (
    ProductResponseDTO,
    ProductResponseWalletDTO,
    ProductResponseAssetDTO
)

from src.infrastructure.persistence.database.models import Product as ProductM


class ProductMapper:
    @staticmethod
    def to_model(product: ProductE) -> ProductM:
        return ProductM(
            id=product.id_.value,
            wallet_id=product.wallet_id.value,
            name=product.name.value,
            price=product.price.value,
            photo_filename=product.photo_filename.value,
            created_at=product.created_at.value
        )

    @staticmethod
    def to_dto(model: ProductM) -> ProductResponseDTO:
        return ProductResponseDTO(
            id=model.id,
            name=model.name,
            price=model.price,
            photo_filename=model.photo_filename,
            created_at=model.created_at,
            wallet=ProductResponseWalletDTO(
                asset=ProductResponseAssetDTO(
                    symbol=model.wallet.asset.symbol,
                    decimals=model.wallet.asset.decimals
                )
            )
        )

    @classmethod
    def to_dto_m2m(cls, models: Sequence[ProductM]) -> list[ProductResponseDTO]:
        return [cls.to_dto(model) for model in models]
