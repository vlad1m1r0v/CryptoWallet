from src.configs import config

from src.application.dtos.request import CreateProductRequestDTO
from src.application.dtos.response import ProductResponseDTO

from src.presentation.http.schemas import (
    CreateProductRequestSchema,
    ProductResponseAssetSchema,
    ProductResponseWalletSchema,
    ProductResponseSchema
)

from src.presentation.http.mappers.base import BaseMapper


class ProductMapper(
    BaseMapper[
        CreateProductRequestDTO,
        ProductResponseDTO,
        CreateProductRequestSchema,
        ProductResponseSchema
    ]):
    @staticmethod
    async def to_request_dto(schema: CreateProductRequestSchema) -> CreateProductRequestDTO:
        return CreateProductRequestDTO(
            wallet_id=schema.wallet_id,
            name=schema.name,
            price=schema.price,
            photo=await schema.photo.read()
        )

    @staticmethod
    def to_response_schema(
            dto: ProductResponseDTO
    ) -> ProductResponseSchema:
        return ProductResponseSchema(
            id=dto["id"],
            name=dto["name"],
            price=dto["price"],
            photo_url=f"{config.s3.base_file_url}/{dto['photo_filename']}",
            created_at=dto["created_at"],
            wallet=ProductResponseWalletSchema(
                address=dto["wallet"]["address"],
                asset=ProductResponseAssetSchema(
                    symbol=dto["wallet"]["asset"]["symbol"],
                    decimals=dto["wallet"]["asset"]["decimals"]
                )
            )
        )

    @classmethod
    def to_response_schema_m2m(
            cls, dtos: list[ProductResponseDTO]
    ) -> list[ProductResponseSchema]:
        return [cls.to_response_schema(dto) for dto in dtos]
