from dataclasses import dataclass
from typing import Any

from src.domain.exceptions import InvalidChoiceException

from src.domain.enums import TransactionStatusEnum

from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class TransactionStatus(ValueObject):
    value: TransactionStatusEnum

    def __post_init__(self):
        super(TransactionStatus, self).__post_init__()
        self._validate_transaction_status(transaction_status=self.value)

    @staticmethod
    def _validate_transaction_status(transaction_status: Any) -> None:
        if not isinstance(transaction_status, TransactionStatusEnum):
            raise InvalidChoiceException(
                field="transaction_status",
                enum_cls=TransactionStatusEnum,
                actual_value=transaction_status
            )