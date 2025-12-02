from src.application.dtos.request import GetTransactionsRequestDTO
from src.application.dtos.response import (
    PaginatedResponseDTO,
    TransactionResponseDTO
)

from src.presentation.http.schemas import (
    PaginatedResponseSchema,
    GetTransactionsRequestSchema,
    TransactionAssetSchema,
    TransactionWalletSchema,
    TransactionResponseSchema,
)


class GetTransactionsMapper:
    @staticmethod
    def to_request_dto(schema: GetTransactionsRequestSchema) -> GetTransactionsRequestDTO:
        return GetTransactionsRequestDTO(
            page=schema.page,
            per_page=schema.per_page,
            user_id=schema.user_id,
            wallet_id=schema.wallet_id,
            sort=schema.sort,
            order=schema.order
        )

    @staticmethod
    def to_response_schema(
            dto: PaginatedResponseDTO[TransactionResponseDTO]
    ) -> PaginatedResponseSchema[TransactionResponseSchema]:
        return PaginatedResponseSchema[TransactionResponseSchema](
            page=dto["page"],
            per_page=dto["per_page"],
            total_pages=dto["total_pages"],
            total_records=dto["total_records"],
            items=[
                TransactionResponseSchema(
                    id=item["id"],
                    transaction_hash=item["transaction_hash"],
                    from_address=item["from_address"],
                    to_address=item["to_address"],
                    value=item["value"],
                    transaction_fee=item["transaction_fee"],
                    transaction_status=item["transaction_status"],
                    created_at=item["created_at"],
                    wallet=TransactionWalletSchema(
                        asset=TransactionAssetSchema(
                            symbol=item["wallet"]["asset"]["symbol"],
                            decimals=item["wallet"]["asset"]["decimals"]
                        )
                    )
                ) for item in dto["items"]
            ]
        )
