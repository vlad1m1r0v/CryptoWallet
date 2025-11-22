from datetime import datetime
from typing import Optional
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, computed_field

from src.domain.enums import TransactionStatusEnum

from src.application.enums import SortOrderEnum
from src.application.dtos.request import TransactionSortField

from src.presentation.http.schemas.fields import (
    TransactionHashStr,
    AddressStr
)


class GetTransactionsRequestSchema(BaseModel):
    page: Optional[int] = 1
    user_id: UUID
    wallet_id: UUID
    sort: TransactionSortField
    order: SortOrderEnum


class TransactionAssetSchema(BaseModel):
    symbol: str = Field(min_length=2, max_length=10)
    decimals: int


class TransactionWalletSchema(BaseModel):
    asset: TransactionAssetSchema


class TransactionResponseSchema(BaseModel):
    id: UUID
    transaction_hash: TransactionHashStr
    from_address: AddressStr
    to_address: AddressStr
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum
    created_at: datetime
    wallet: TransactionWalletSchema = Field(exclude=True)

    def model_post_init(self, __context=None):
        self.value = self.value / (10 ** self.wallet.asset.decimals)
        self.transaction_fee = self.transaction_fee / (10 ** self.wallet.asset.decimals)

    @computed_field
    @property
    def asset_symbol(self) -> str:
        return self.wallet.asset.symbol
