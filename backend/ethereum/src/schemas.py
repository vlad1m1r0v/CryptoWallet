from enum import StrEnum
from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field, computed_field


class TransactionStatusEnum(StrEnum):
    SUCCESSFUL = "successful"
    PENDING = "pending"
    FAILED = "failed"


class TransactionSchema(BaseModel):
    hash: str
    from_address: str = Field(alias="from", serialization_alias="from_address")
    to_address: str = Field(alias="to", serialization_alias="to_address")
    value: int
    gas: int
    gasPrice: int

    timeStamp: Optional[int] = None
    isError: Optional[bool] = None
    txreceipt_status: Optional[bool] = None

    class Config:
        populate_by_name = True
        extra = "ignore"

    @computed_field
    @property
    def transaction_fee(self) -> Decimal:
        return Decimal(self.gas) * Decimal(self.gasPrice)

    @computed_field
    @property
    def transaction_status(self) -> TransactionStatusEnum:
        if self.isError or (self.txreceipt_status is not None and not self.txreceipt_status):
            return TransactionStatusEnum.FAILED
        elif self.txreceipt_status is None:
            return TransactionStatusEnum.PENDING
        return TransactionStatusEnum.SUCCESSFUL

    @computed_field
    @property
    def created_at(self) -> Optional[datetime]:
        if self.timeStamp is None:
            return None
        return datetime.fromtimestamp(int(self.timeStamp))


class CompleteTransactionSchema(BaseModel):
    hash: str
    transaction_status: TransactionStatusEnum
    created_at: datetime


class EtherscanTransactionListResponseSchema(BaseModel):
    status: int
    message: str
    result: List[TransactionSchema]

    @classmethod
    def __get_validators__(cls):
        yield cls.convert_strings

    @classmethod
    def convert_strings(cls, values):
        values["status"] = int(values["status"])

        return values


class ETHWalletSchema(BaseModel):
    user_id: UUID
    address: str
    private_key: str
    balance: Optional[Decimal] = Field(default=Decimal(0.0))
    created_at: datetime
    transactions: List[TransactionSchema] = Field(default=[])
