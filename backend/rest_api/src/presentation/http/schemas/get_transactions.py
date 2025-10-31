from datetime import datetime
from typing import Optional
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, computed_field

from src.domain.enums.transaction import TransactionStatusEnum

from src.application.enums.sort_order import SortOrderEnum
from src.application.ports.gateways.transaction import SortFieldEnum


class GetTransactionsSchema(BaseModel):
    page: Optional[int] = 1
    wallet_id: UUID
    sort_by: SortFieldEnum
    order: SortOrderEnum

class AssetSchema(BaseModel):
    symbol: str
    decimals: int


class WalletSchema(BaseModel):
    asset: AssetSchema


class TransactionListItemSchema(BaseModel):
    id: UUID
    transaction_hash: str
    from_address: str
    to_address: str
    value: Decimal
    transaction_fee: Decimal
    transaction_status: TransactionStatusEnum
    created_at: datetime
    wallet: WalletSchema = Field(exclude=True)

    def model_post_init(self, __context=None):
        self.value = self.value / (10 ** self.wallet.asset.decimals)

    @computed_field
    @property
    def asset_symbol(self) -> str:
        return self.wallet.asset.symbol
