from typing import (
    Sequence,
    Optional,
    Union
)

from src.application.dtos.response import (
    PaginatedResponseDTO,
    TransactionResponseDTO,
    TransactionResponseWalletDTO,
    TransactionResponseAssetDTO
)

from src.domain.entities import Transaction as TransactionE

from src.infrastructure.persistence.database.models import Transaction as TransactionM


class TransactionMapper:
    @staticmethod
    def __base_to_model(entity: TransactionE) -> TransactionM:
        return TransactionM(
            id=entity.id_.value,
            wallet_id=entity.wallet_id.value,
            transaction_hash=entity.transaction_hash.value,
            from_address=entity.from_address.value,
            to_address=entity.to_address.value,
            value=entity.value.value,
            transaction_status=entity.transaction_status.value,
            transaction_fee=entity.transaction_fee.value,
            created_at=entity.created_at.value if entity.created_at else None,
        )

    @staticmethod
    def to_model(
            *,
            entity: Optional[TransactionE] = None,
            entities: Optional[Sequence[TransactionE]] = None,
    ) -> Union[TransactionM | list[TransactionM]]:
        if entity:
            return TransactionMapper.__base_to_model(entity)
        else:
            return [TransactionMapper.__base_to_model(entity) for entity in entities]

    @staticmethod
    def __base_to_dto(model: TransactionM) -> TransactionResponseDTO:
        return TransactionResponseDTO(
            id=model.id,
            transaction_hash=model.transaction_hash,
            from_address=model.from_address,
            to_address=model.to_address,
            value=model.value,
            transaction_fee=model.transaction_fee,
            transaction_status=model.transaction_status,
            created_at=model.created_at,
            wallet=TransactionResponseWalletDTO(
                id=model.wallet.id,
                user_id=model.wallet.user_id,
                address=model.wallet.address,
                asset=TransactionResponseAssetDTO(
                    symbol=model.wallet.asset.symbol,
                    decimals=model.wallet.asset.decimals
                )
            )
        )

    @staticmethod
    def to_dto(
            *,
            model: Optional[TransactionM] = None,
            models: Optional[Sequence[TransactionM]] = None,
            page: Optional[int] = None,
            per_page: Optional[int] = None,
            total_pages: Optional[int] = None,
            total_records: Optional[int] = None,
    ) -> Union[
        TransactionResponseDTO,
        list[TransactionResponseDTO],
        PaginatedResponseDTO[TransactionResponseDTO]
    ]:
        if model:
            return TransactionMapper.__base_to_dto(model)

        elif all([models, page, total_pages]):
            return PaginatedResponseDTO(
                page=page,
                per_page=per_page,
                total_pages=total_pages,
                total_records=total_records,
                items=[TransactionMapper.__base_to_dto(model) for model in models]
            )

        return [TransactionMapper.__base_to_dto(model) for model in models]
