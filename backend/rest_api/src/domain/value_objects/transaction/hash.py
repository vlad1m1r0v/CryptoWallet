import re
from dataclasses import dataclass
from typing import ClassVar

from src.domain.exceptions import InvalidTransactionHashException

from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class TransactionHash(ValueObject):
    """raises InvalidTransactionHashException"""

    PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"^0x[a-fA-F0-9]{64}$")

    value: str

    def __post_init__(self) -> None:
        super(TransactionHash, self).__post_init__()
        self._validate_hash(self.value)

    def _validate_hash(self, tx_hash: str) -> None:
        if not re.fullmatch(self.PATTERN, tx_hash):
            raise InvalidTransactionHashException()