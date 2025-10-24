from src.domain.entities.transaction import Transaction

from src.domain.ports.id_generator import IdGenerator

from src.domain.value_objects.shared.entity_id import EntityId
from src.domain.value_objects.shared.timestamp import Timestamp

from src.domain.value_objects.wallet.address import Address

from src.domain.value_objects.transaction.hash import TransactionHash
from src.domain.value_objects.transaction.value import TransactionValue
from src.domain.value_objects.transaction.status import TransactionStatus
from src.domain.value_objects.transaction.fee import TransactionFee


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
            created_at: Timestamp,
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
