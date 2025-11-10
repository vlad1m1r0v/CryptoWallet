from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateOrderRequestDTO:
    product_id: UUID
    wallet_id: UUID