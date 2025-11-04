from decimal import Decimal

from pydantic import BaseModel

from src.presentation.http.schemas.fields import AddressStr

class PublishCreateTransactionRequestSchema(BaseModel):
    from_address: AddressStr
    to_address: AddressStr
    amount: Decimal