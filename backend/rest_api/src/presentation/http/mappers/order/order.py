from src.configs import config

from src.application.dtos.request import CreateOrderRequestDTO
from src.application.dtos.response import OrderResponseDTO

from src.presentation.http.schemas import (
    CreateOrderRequestSchema,
    OrderResponseProductWalletAssetSchema,
    OrderResponseProductWalletSchema,
    OrderResponseProductSchema,
    OrderResponseTransactionSchema,
    OrderResponseSchema
)

from src.presentation.http.mappers.base import BaseMapper


class OrderMapper(
    BaseMapper[
        CreateOrderRequestDTO,
        OrderResponseDTO,
        CreateOrderRequestSchema,
        OrderResponseSchema
    ]):
    @staticmethod
    async def to_request_dto(schema: CreateOrderRequestSchema) -> CreateOrderRequestDTO:
        return CreateOrderRequestDTO(
            product_id=schema.product_id,
            wallet_id=schema.wallet_id
        )

    @staticmethod
    def to_response_schema(
            dto: OrderResponseDTO
    ) -> OrderResponseSchema:
        return OrderResponseSchema(
            id=dto["id"],
            status=dto["status"],
            created_at=dto["created_at"],
            product=OrderResponseProductSchema(
                name=dto["product"]["name"],
                price=dto["product"]["price"],
                photo_url=f"{config.s3.base_file_url}/{dto['product']['photo_filename']}",
                wallet=OrderResponseProductWalletSchema(
                    address=dto["product"]["wallet"]["address"],
                    asset=OrderResponseProductWalletAssetSchema(
                        symbol=dto["product"]["wallet"]["asset"]["symbol"],
                        decimals=dto["product"]["wallet"]["asset"]["decimals"]
                    )
                )
            ),
            payment_transaction=OrderResponseTransactionSchema(
                transaction_hash=dto["payment_transaction"]["transaction_hash"],
            ) if dto["payment_transaction"] else None,
            return_transaction=OrderResponseTransactionSchema(
                transaction_hash=dto["return_transaction"]["transaction_hash"],
            ) if dto["return_transaction"] else None,
        )

    @classmethod
    def to_response_schema_m2m(
            cls, dtos: list[OrderResponseDTO]
    ) -> list[OrderResponseSchema]:
        return [cls.to_response_schema(dto) for dto in dtos]
