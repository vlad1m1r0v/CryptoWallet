from src.application.dtos.request import GetTransactionsRequestDTO
from src.application.dtos.response import (
    PaginatedResponseDTO,
    TransactionsListItemResponseDTO
)

from src.presentation.http.schemas import (
    PaginatedResponseSchema,
    GetTransactionsRequestSchema,
    GetTransactionsListItemAssetSchema,
    GetTransactionsListItemWalletSchema,
    GetTransactionsListItemResponseSchema,
)

from src.presentation.http.mappers.base import BaseMapper


class GetTransactionsMapper(
    BaseMapper[
        GetTransactionsRequestDTO,
        PaginatedResponseDTO[TransactionsListItemResponseDTO],
        GetTransactionsRequestSchema,
        PaginatedResponseSchema[GetTransactionsListItemResponseSchema]
    ]):
    @staticmethod
    def to_request_dto(schema: GetTransactionsRequestSchema) -> GetTransactionsRequestDTO:
        return GetTransactionsRequestDTO(
            page=schema.page,
            wallet_id=schema.wallet_id,
            sort_by=schema.sort_by,
            order=schema.order
        )

    @staticmethod
    def to_response_schema(
            dto: PaginatedResponseDTO[TransactionsListItemResponseDTO]
    ) -> PaginatedResponseSchema[GetTransactionsListItemResponseSchema]:
        return PaginatedResponseSchema[GetTransactionsListItemResponseSchema](
            page=dto.page,
            total_pages=dto.total_pages,
            items=[
                GetTransactionsListItemResponseSchema(
                    id=item.id,
                    transaction_hash=item.transaction_hash,
                    from_address=item.from_address,
                    to_address=item.to_address,
                    value=item.value,
                    transaction_fee=item.transaction_fee,
                    transaction_status=item.transaction_status,
                    created_at=item.created_at,
                    wallet=GetTransactionsListItemWalletSchema(
                        asset=GetTransactionsListItemAssetSchema(
                            symbol=item.wallet.asset.symbol,
                            decimals=item.wallet.asset.decimals
                        )
                    )
                ) for item in dto.items]
        )
