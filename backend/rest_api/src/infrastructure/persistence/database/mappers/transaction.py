from typing import Sequence, overload, Union

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

    @overload
    @staticmethod
    def to_model(entity: TransactionE) -> TransactionM:
        ...

    @overload
    @staticmethod
    def to_model(entities: list[TransactionE]) -> list[TransactionM]:
        ...

    @staticmethod
    def to_model(arg: Union[TransactionE, list[TransactionE]]) -> Union[TransactionM | list[TransactionM]]:
        if isinstance(arg, TransactionE):
            return TransactionMapper.__base_to_model(arg)
        else:
            return [TransactionMapper.__base_to_model(item) for item in arg]

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
                user_id=model.wallet.user_id,
                address=model.wallet.address,
                asset=TransactionResponseAssetDTO(
                    symbol=model.wallet.asset.symbol,
                    decimals=model.wallet.asset.decimals
                )
            )
        )

    @overload
    @staticmethod
    def to_dto(model: TransactionM) -> TransactionResponseDTO:
        ...

    @overload
    @staticmethod
    def to_dto(
            models: Sequence[TransactionM],
            page: int,
            total_pages: int
    ) -> PaginatedResponseDTO[TransactionResponseDTO]:
        ...

    @staticmethod
    def to_dto(
            arg: Union[TransactionM, Sequence[TransactionM]],
            page: int = 0,
            total_pages: int = 0
    ) -> Union[TransactionResponseDTO, PaginatedResponseDTO[TransactionResponseDTO]]:
        if isinstance(arg, TransactionM):
            return TransactionMapper.__base_to_dto(arg)
        else:
            items = [TransactionMapper.__base_to_dto(item) for item in arg]

            return PaginatedResponseDTO(
                page=page,
                total_pages=total_pages,
                items=items
            )
