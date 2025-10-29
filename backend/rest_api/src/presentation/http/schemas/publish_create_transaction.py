from decimal import Decimal

from pydantic import BaseModel, Field


class PublishCreateTransactionSchema(BaseModel):
    from_address: str = Field(min_length=42, max_length=42)
    to_address: str = Field(min_length=42, max_length=42)
    amount: Decimal