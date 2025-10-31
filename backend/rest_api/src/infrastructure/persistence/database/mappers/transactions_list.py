from typing import Sequence

from src.application.dtos.response.paginated_response import PaginatedResult
from src.application.dtos.response.transactions_list import (
    AssetDTO,
    WalletDTO,
    TransactionListItemDTO
)

from src.infrastructure.persistence.database.mappers.base import BasePaginatedMapper
from src.infrastructure.persistence.database.models.transaction import Transaction


class TransactionsListMapper(BasePaginatedMapper[Transaction, TransactionListItemDTO]):
    @staticmethod
    def to_paginated_dto(
            models: Sequence[Transaction], page: int, total_pages: int
    ) -> PaginatedResult[TransactionListItemDTO]:
        return PaginatedResult(
            page=page,
            total_pages=total_pages,
            items=[
                TransactionListItemDTO(
                    id=m.id,
                    transaction_hash=m.transaction_hash,
                    from_address=m.from_address,
                    to_address=m.to_address,
                    value=m.value,
                    transaction_fee=m.transaction_fee,
                    transaction_status=m.transaction_status,
                    created_at=m.created_at,
                    wallet=WalletDTO(
                        asset=AssetDTO(
                            symbol=m.wallet.asset.symbol,
                            decimals=m.wallet.asset.decimals
                        )
                    )
                ) for m in models]
        )
