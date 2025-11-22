from types import NoneType
from typing import List

from src.application.dtos.response import WalletsListItemResponseDTO

from src.presentation.http.schemas import (
    WalletResponseAssetSchema,
    WalletResponseSchema
)

from src.presentation.http.mappers.base import BaseMapper


class WalletsListMapper(
    BaseMapper[
        NoneType,
        List[WalletResponseAssetSchema],
        NoneType,
        List[WalletResponseSchema]
    ]):
    @staticmethod
    def to_request_dto(schema: NoneType) -> NoneType:
        raise NotImplementedError

    @staticmethod
    def to_response_schema(
            dto: List[WalletsListItemResponseDTO]
    ) -> List[WalletResponseSchema]:
        return [
            WalletResponseSchema(
                id=wallet.id,
                address=wallet.address,
                balance=wallet.balance,
                asset=WalletResponseAssetSchema(
                    symbol=wallet.asset.symbol,
                    decimals=wallet.asset.decimals
                )
            ) for wallet in dto
        ]
