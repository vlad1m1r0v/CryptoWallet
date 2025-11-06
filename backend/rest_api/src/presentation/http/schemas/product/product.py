from datetime import datetime
from decimal import Decimal
from uuid import UUID

from fastapi import UploadFile

from pydantic import BaseModel, Field, computed_field

from src.presentation.http.schemas.fields import ProductNameStr


class CreateProductRequestSchema(BaseModel):
    wallet_id: UUID
    name: ProductNameStr
    price: Decimal = Field(gt=0.00001)
    photo: UploadFile

class ProductResponseAssetSchema(BaseModel):
    symbol: str = Field(min_length=2, max_length=10)
    decimals: int


class ProductResponseWalletSchema(BaseModel):
    asset: ProductResponseAssetSchema


class ProductResponseSchema(BaseModel):
    id: UUID
    name: ProductNameStr
    price: Decimal = Field(gt=0.00001)
    photo_url: str
    created_at: datetime
    wallet: ProductResponseWalletSchema = Field(exclude=True)

    def model_post_init(self, __context=None):
        self.price = self.price / (10 ** self.wallet.asset.decimals)

    @computed_field
    @property
    def asset_symbol(self) -> str:
        return self.wallet.asset.symbol
