from typing import Sequence, overload

from src.domain.entities import Wallet as WalletE
from src.application.dtos.response import (
    WalletResponseDTO,
    WalletResponseAssetDTO
)
from src.infrastructure.persistence.database.models import Wallet as WalletM


class WalletMapper:
    @staticmethod
    def to_model(entity: WalletE) -> WalletM:
        return WalletM(
            id=entity.id_.value,
            user_id=entity.user_id.value,
            asset_id=entity.asset_id.value,
            private_key=entity.encrypted_private_key.value,
            address=entity.address.value,
            balance=entity.balance.value,
            created_at=entity.created_at.value,
        )

    @staticmethod
    def __base_to_dto(model: WalletM) -> WalletResponseDTO:
        return WalletResponseDTO(
            id=model.id,
            address=model.address,
            balance=model.balance,
            asset=WalletResponseAssetDTO(
                symbol=model.asset.symbol,
                decimals=model.asset.decimals
            )
        )

    @overload
    @staticmethod
    def to_dto(model: WalletM) -> WalletResponseDTO:
        ...

    @overload
    @staticmethod
    def to_dto(models: Sequence[WalletM]) -> list[WalletResponseDTO]:
        ...

    @staticmethod
    def to_dto(arg: WalletM | Sequence[WalletM]) -> WalletResponseDTO | list[WalletResponseDTO]:
        if isinstance(arg, WalletM):
            return WalletMapper.__base_to_dto(arg)
        else:
            return [WalletMapper.__base_to_dto(arg) for arg in arg]
