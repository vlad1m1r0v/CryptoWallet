from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, computed_field, Field

from src.presentation.http.schemas.fields import AddressStr


class WalletResponseAssetSchema(BaseModel):
    symbol: str = Field(min_length=2, max_length=10)
    decimals: int


class WalletResponseSchema(BaseModel):
    id: UUID
    address: AddressStr
    balance: Decimal
    asset: WalletResponseAssetSchema = Field(exclude=True)

    def model_post_init(self, __context=None):
        self.balance = self.balance / (10 ** self.asset.decimals)

    @computed_field
    @property
    def asset_symbol(self) -> str:
        return self.asset.symbol
