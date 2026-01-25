from datetime import datetime
from decimal import Decimal
from uuid import UUID

from fastapi import UploadFile

from pydantic import BaseModel, Field, computed_field, model_validator

from src.presentation.http.constants import (
    ACCEPTED_IMAGE_TYPES,
    MAX_FILE_SIZE
)

from src.presentation.http.schemas.fields import (
    ProductNameStr,
    AddressStr
)

class CreateProductRequestSchema(BaseModel):
    wallet_id: UUID
    name: ProductNameStr
    price: Decimal = Field(gt=0.0002)
    photo: UploadFile

    @model_validator(mode="after")
    @classmethod
    def validate_photo_file(cls, model: "CreateProductRequestSchema") -> "CreateProductRequestSchema":

        file = model.photo

        if file.content_type not in ACCEPTED_IMAGE_TYPES:
            raise ValueError(
                f"Invalid file type: {file.content_type}. "
                f"Supported: {', '.join(ACCEPTED_IMAGE_TYPES)}"
            )

        if file.size > MAX_FILE_SIZE:
            size_mb = file.size / (1024 * 1024)
            raise ValueError(f"File is too large: {size_mb:.2f}MB. Max allowed: 2MB")

        return model

class ProductResponseAssetSchema(BaseModel):
    symbol: str = Field(min_length=2, max_length=10)
    decimals: int


class ProductResponseWalletSchema(BaseModel):
    asset: ProductResponseAssetSchema
    address: AddressStr

class ProductResponseSchema(BaseModel):
    id: UUID
    name: ProductNameStr
    price: Decimal = Field(gt=0.0002)
    photo_url: str
    created_at: datetime
    wallet: ProductResponseWalletSchema = Field(exclude=True)

    def model_post_init(self, __context=None):
        self.price = self.price / (10 ** self.wallet.asset.decimals)

    @computed_field
    @property
    def asset_symbol(self) -> str:
        return self.wallet.asset.symbol

    @computed_field
    @property
    def wallet_address(self) -> AddressStr:
        return self.wallet.address
