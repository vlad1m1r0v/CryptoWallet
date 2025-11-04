from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class SaveCreateWalletRequestDTO:
    user_id: UUID
    address: str
    private_key: str
    balance: Decimal
    created_at: datetime