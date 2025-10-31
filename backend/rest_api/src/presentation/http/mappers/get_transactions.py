from src.application.dtos.response.transactions_list import TransactionListItemDTO
from src.application.dtos.response.paginated_response import PaginatedResult
from src.application.interactors.transaction.get_transactions import GetTransactionsRequest

from src.presentation.http.schemas.get_transactions import (
    GetTransactionsSchema,
    AssetSchema,
    WalletSchema,
    TransactionListItemSchema
)
from src.presentation.http.schemas.paginated_result import PaginatedResultSchema

from src.presentation.http.mappers.base import BaseMapper


class GetTransactionsMapper(
    BaseMapper[
        PaginatedResultSchema[TransactionListItemSchema],
        GetTransactionsRequest,
        PaginatedResult[TransactionListItemDTO]
    ]):
    @staticmethod
    def to_request_dto(schema: GetTransactionsSchema) -> GetTransactionsRequest:
        return GetTransactionsRequest(
            page=schema.page,
            wallet_id=schema.wallet_id,
            sort_by=schema.sort_by,
            order=schema.order
        )

    @staticmethod
    def to_response_schema(dto: PaginatedResult[TransactionListItemDTO]) -> PaginatedResultSchema[
        TransactionListItemSchema]:
        return PaginatedResultSchema[TransactionListItemSchema](
            page=dto.page,
            total_pages=dto.total_pages,
            items=[
                TransactionListItemSchema(
                    id=item.id,
                    transaction_hash=item.transaction_hash,
                    from_address=item.from_address,
                    to_address=item.to_address,
                    value=item.value,
                    transaction_fee=item.transaction_fee,
                    transaction_status=item.transaction_status,
                    created_at=item.created_at,
                    wallet=WalletSchema(
                        asset=AssetSchema(
                            symbol=item.wallet.asset.symbol,
                            decimals=item.wallet.asset.decimals
                        )
                    )
                ) for item in dto.items]
        )
