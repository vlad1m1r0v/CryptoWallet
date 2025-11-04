from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True, kw_only=True)
class PublishCreateTransactionRequestDTO:
    from_address: str
    to_address: str
    amount: Decimal