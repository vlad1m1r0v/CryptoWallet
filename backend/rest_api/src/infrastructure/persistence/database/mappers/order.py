from typing import Sequence

from src.domain.value_objects import (
    EntityId,
    OrderStatus,
    Timestamp
)

from src.domain.entities import Order as OrderE

from src.application.dtos.response import (
    OrderResponseProductWalletAssetDTO,
    OrderResponseProductWalletDTO,
    OrderResponseProductDTO,
    OrderResponseTransactionDTO,
    OrderResponseWalletDTO,
    OrderResponseDTO
)

from src.infrastructure.persistence.database.models import Order as OrderM


class OrderMapper:
    @staticmethod
    def to_model(entity: OrderE) -> OrderM:
        return OrderM(
            id=entity.id_.value,
            product_id=entity.product_id.value,
            wallet_id=entity.wallet_id.value,
            payment_transaction_id=entity.payment_transaction_id.value if entity.payment_transaction_id else None,
            return_transaction_id=entity.return_transaction_id.value if entity.return_transaction_id else None,
            status=entity.status.value,
            created_at=entity.created_at.value
        )

    @staticmethod
    def to_entity(model: OrderM) -> OrderE:
        return OrderE(
            id_=EntityId(model.id),
            product_id=EntityId(model.product_id),
            wallet_id=EntityId(model.wallet_id),
            payment_transaction_id=EntityId(model.payment_transaction_id) if model.payment_transaction_id else None,
            return_transaction_id=EntityId(model.return_transaction_id) if model.return_transaction_id else None,
            status=OrderStatus(model.status),
            created_at=Timestamp(model.created_at)
        )

    @staticmethod
    def to_dto(model: OrderM) -> OrderResponseDTO:
        return OrderResponseDTO(
            id=model.id,
            status=model.status,
            created_at=model.created_at,
            wallet=OrderResponseWalletDTO(
                address=model.wallet.address
            ),
            payment_transaction=OrderResponseTransactionDTO(
                transaction_hash=model.payment_transaction.transaction_hash
            ) if model.payment_transaction else None,
            return_transaction=OrderResponseTransactionDTO(
                transaction_hash=model.return_transaction.transaction_hash
            ) if model.return_transaction else None,
            product=OrderResponseProductDTO(
                name=model.product.name,
                price=model.product.price,
                photo_filename=model.product.photo_filename,
                wallet=OrderResponseProductWalletDTO(
                    address=model.wallet.address,
                    asset=OrderResponseProductWalletAssetDTO(
                        symbol=model.wallet.asset.symbol,
                        decimals=model.wallet.asset.decimals
                    )
                )
            )
        )

    @classmethod
    def to_dto_m2m(cls, models: Sequence[OrderM]) -> list[OrderResponseDTO]:
        return [cls.to_dto(model) for model in models]
