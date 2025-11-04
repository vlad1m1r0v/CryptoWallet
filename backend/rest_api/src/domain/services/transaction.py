from typing import Optional

from src.domain.entities import Transaction

from src.domain.ports import IdGenerator

from src.domain.value_objects import (
    EntityId,
    TransactionHash,
    Address,
    TransactionValue,
    TransactionStatus,
    TransactionFee,
    Timestamp
)


class TransactionService:
    def __init__(
            self,
            id_generator: IdGenerator
    ) -> None:
        self._id_generator = id_generator

    def create_transaction(
            self,
            wallet_id: EntityId,
            transaction_hash: TransactionHash,
            from_address: Address,
            to_address: Address,
            value: TransactionValue,
            transaction_status: TransactionStatus,
            transaction_fee: TransactionFee,
            created_at: Optional[Timestamp] = None,
    ) -> Transaction:
        transaction_id = self._id_generator()

        return Transaction(
            id_=transaction_id,
            wallet_id=wallet_id,
            transaction_hash=transaction_hash,
            from_address=from_address,
            to_address=to_address,
            value=value,
            transaction_status=transaction_status,
            transaction_fee=transaction_fee,
            created_at=created_at
        )
