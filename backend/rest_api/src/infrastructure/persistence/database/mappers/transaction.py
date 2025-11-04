from src.domain.value_objects import (
    EntityId,
    Timestamp,
    Address,
    TransactionHash,
    TransactionValue,
    TransactionStatus,
    TransactionFee
)
from src.domain.entities import Transaction as TransactionE

from src.infrastructure.persistence.database.models import Transaction as TransactionM
from src.infrastructure.persistence.database.mappers.base import BaseMapper


class TransactionMapper(BaseMapper[TransactionE, TransactionM]):
    @staticmethod
    def to_entity(model: TransactionM) -> TransactionE:
        return TransactionE(
            id_=EntityId(model.id),
            wallet_id=EntityId(model.wallet_id),
            transaction_hash=TransactionHash(model.transaction_hash),
            from_address=Address(model.from_address),
            to_address=Address(model.to_address),
            value=TransactionValue(model.value),
            transaction_status=TransactionStatus(model.transaction_status),
            transaction_fee=TransactionFee(model.transaction_fee),
            created_at=Timestamp(model.created_at) if model.created_at else None,
        )

    @staticmethod
    def to_model(entity: TransactionE) -> TransactionM:
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
