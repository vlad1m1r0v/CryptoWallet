from typing import Optional

from src.domain.entities.base import Entity

from src.domain.value_objects import (
    EntityId,
    TransactionHash,
    Address,
    TransactionValue,
    TransactionStatus,
    TransactionFee,
    Timestamp
)

class Transaction(Entity[EntityId]):
    def __init__(
            self,
            *,
            id_: EntityId,
            wallet_id: EntityId,
            transaction_hash: TransactionHash,
            from_address: Address,
            to_address: Address,
            value: TransactionValue,
            transaction_status: TransactionStatus,
            transaction_fee: TransactionFee,
            created_at: Optional[Timestamp] = None,
    ) -> None:
        super().__init__(id_=id_)
        self.wallet_id = wallet_id
        self.transaction_hash = transaction_hash
        self.from_address = from_address
        self.to_address = to_address
        self.value = value
        self.transaction_status = transaction_status
        self.transaction_fee = transaction_fee
        self.created_at = created_at

