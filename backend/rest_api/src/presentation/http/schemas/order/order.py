from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, computed_field

from src.domain.enums import OrderStatusEnum

from src.presentation.http.schemas.fields import (
    ProductNameStr,
    AddressStr,
    TransactionHashStr
)


class CreateOrderRequestSchema(BaseModel):
    product_id: UUID
    wallet_id: UUID


class OrderResponseProductWalletAssetSchema(BaseModel):
    symbol: str = Field(min_length=2, max_length=10)
    decimals: int


class OrderResponseProductWalletSchema(BaseModel):
    asset: OrderResponseProductWalletAssetSchema
    address: AddressStr


class OrderResponseProductSchema(BaseModel):
    name: ProductNameStr
    price: Decimal
    photo_url: HttpUrl
    wallet: OrderResponseProductWalletSchema


class OrderResponseTransactionSchema(BaseModel):
    transaction_hash: TransactionHashStr


class OrderResponseSchema(BaseModel):
    id: UUID
    product: OrderResponseProductSchema = Field(exclude=True)
    payment_transaction: Optional[OrderResponseTransactionSchema] = Field(exclude=True)
    return_transaction: Optional[OrderResponseTransactionSchema] = Field(exclude=True)
    status: OrderStatusEnum
    created_at: datetime

    @computed_field
    @property
    def product_name(self) -> str:
        return self.product.name

    @computed_field
    @property
    def product_price(self) -> Decimal:
        return self.product.price / (10 ** self.product.wallet.asset.decimals)

    @computed_field
    @property
    def product_photo_url(self) -> HttpUrl:
        return self.product.photo_url

    @computed_field
    @property
    def asset_symbol(self) -> str:
        return self.product.wallet.asset.symbol

    @computed_field
    @property
    def payment_transaction_hash(self) -> str | None:
        return self.payment_transaction.transaction_hash if self.payment_transaction else None

    @computed_field
    @property
    def return_transaction_hash(self) -> str | None:
        return self.return_transaction.transaction_hash if self.return_transaction else None
