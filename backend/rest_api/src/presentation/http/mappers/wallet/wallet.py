from typing import List

from src.application.dtos.response import WalletResponseDTO

from src.presentation.http.schemas import (
    WalletResponseAssetSchema,
    WalletResponseSchema
)


class WalletMapper:
    @staticmethod
    def to_response_schema(
            dto: List[WalletResponseDTO]
    ) -> List[WalletResponseSchema]:
        return [
            WalletResponseSchema(
                id=wallet["id"],
                address=wallet["address"],
                balance=wallet["balance"],
                asset=WalletResponseAssetSchema(
                    symbol=wallet["asset"]["symbol"],
                    decimals=wallet["asset"]["decimals"]
                )
            ) for wallet in dto
        ]
