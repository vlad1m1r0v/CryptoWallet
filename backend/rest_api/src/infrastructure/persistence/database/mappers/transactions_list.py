from typing import Sequence

from src.application.dtos.response import (
    PaginatedResponseDTO,
    TransactionsListItemResponseAssetDTO,
    TransactionsListItemResponseWalletDTO,
    TransactionsListItemResponseDTO
)

from src.infrastructure.persistence.database.mappers.base import BasePaginatedMapper
from src.infrastructure.persistence.database.models import Transaction


class TransactionsPaginatedMapper(BasePaginatedMapper[Transaction, TransactionsListItemResponseDTO]):
    @staticmethod
    def to_paginated_dto(
            models: Sequence[Transaction], page: int, total_pages: int
    ) -> PaginatedResponseDTO[TransactionsListItemResponseDTO]:
        return PaginatedResponseDTO(
            page=page,
            total_pages=total_pages,
            items=[
                TransactionsListItemResponseDTO(
                    id=m.id,
                    transaction_hash=m.transaction_hash,
                    from_address=m.from_address,
                    to_address=m.to_address,
                    value=m.value,
                    transaction_fee=m.transaction_fee,
                    transaction_status=m.transaction_status,
                    created_at=m.created_at,
                    wallet=TransactionsListItemResponseWalletDTO(
                        asset=TransactionsListItemResponseAssetDTO(
                            symbol=m.wallet.asset.symbol,
                            decimals=m.wallet.asset.decimals
                        )
                    )
                ) for m in models]
        )
