from typing import (
    Sequence,
    Optional
)

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
            user_id=model.user_id,
            address=model.address,
            balance=model.balance,
            encrypted_private_key=model.private_key,
            asset=WalletResponseAssetDTO(
                symbol=model.asset.symbol,
                decimals=model.asset.decimals
            )
        )


    @staticmethod
    def to_dto(
            *,
            model: Optional[WalletM] = None,
            models: Optional[Sequence[WalletM]] = None
    ) -> WalletResponseDTO | list[WalletResponseDTO]:
        if model:
            return WalletMapper.__base_to_dto(model)
        else:
            return [WalletMapper.__base_to_dto(model) for model in models]
