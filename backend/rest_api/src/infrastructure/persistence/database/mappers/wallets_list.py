from typing import Sequence

from src.application.dtos.response import (
    WalletsListItemResponseDTO,
    WalletsListItemResponseAssetDTO
)

from src.infrastructure.persistence.database.models import Wallet as WalletM


class WalletsListMapper:
    @staticmethod
    def to_dto(model: WalletM) -> WalletsListItemResponseDTO:
        return WalletsListItemResponseDTO(
            id=model.id,
            address=model.address,
            balance=model.balance,
            asset=WalletsListItemResponseAssetDTO(
                symbol=model.asset.symbol,
                decimals=model.asset.decimals
            )
        )

    @classmethod
    def to_dto_m2m(cls, models: Sequence[WalletM]) -> list[WalletsListItemResponseDTO]:
        return [cls.to_dto(model) for model in models]
