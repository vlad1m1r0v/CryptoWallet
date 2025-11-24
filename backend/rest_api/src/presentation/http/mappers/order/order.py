from typing import overload

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


class OrderMapper:
    @staticmethod
    async def to_request_dto(schema: CreateOrderRequestSchema) -> CreateOrderRequestDTO:
        return CreateOrderRequestDTO(
            product_id=schema.product_id,
            wallet_id=schema.wallet_id
        )

    @staticmethod
    def __base_to_response_schema(
            dto: OrderResponseDTO
    ) -> OrderResponseSchema:
        product_schema = OrderResponseProductSchema(
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
        )

        payment_transaction_schema = OrderResponseTransactionSchema(
            transaction_hash=dto["payment_transaction"]["transaction_hash"],
        ) if dto.get("payment_transaction") else None

        return_transaction_schema = OrderResponseTransactionSchema(
            transaction_hash=dto["return_transaction"]["transaction_hash"],
        ) if dto.get("return_transaction") else None

        return OrderResponseSchema(
            id=dto["id"],
            status=dto["status"],
            created_at=dto["created_at"],
            product=product_schema,
            payment_transaction=payment_transaction_schema,
            return_transaction=return_transaction_schema,
        )

    @overload
    @staticmethod
    def to_response_schema(
            dto: OrderResponseDTO
    ) -> OrderResponseSchema:
        ...

    @overload
    @staticmethod
    def to_response_schema(
            dtos: list[OrderResponseDTO]
    ) -> list[OrderResponseSchema]:
        ...

    @staticmethod
    def to_response_schema(
            arg: OrderResponseDTO | list[OrderResponseDTO]
    ) -> OrderResponseSchema | list[OrderResponseSchema]:
        if isinstance(arg, list):
            return [OrderMapper.__base_to_response_schema(dto) for dto in arg]
        else:
            return OrderMapper.__base_to_response_schema(arg)
