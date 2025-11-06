from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateProductRequestDTO:
    wallet_id: UUID
    name: str
    price: Decimal
    photo: bytes
