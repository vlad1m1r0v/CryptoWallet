from typing import Optional, List

from uuid import UUID
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field


class TransactionSchema(BaseModel):
    blockNumber: int
    timeStamp: int
    hash: str
    nonce: int
    blockHash: str
    transactionIndex: int
    from_address: str = Field(..., alias="from")
    to: str
    value: int
    gas: int
    gasPrice: int
    isError: bool
    txreceipt_status: Optional[bool] = None
    input: str
    contractAddress: Optional[str] = ""
    cumulativeGasUsed: int
    gasUsed: int
    confirmations: int
    methodId: Optional[str] = ""
    functionName: Optional[str] = ""

    @classmethod
    def __get_validators__(cls):
        yield cls.convert_strings

    @classmethod
    def convert_strings(cls, values):
        int_fields = [
            "blockNumber", "timeStamp", "nonce", "transactionIndex",
            "value", "gas", "gasPrice", "cumulativeGasUsed",
            "gasUsed", "confirmations"
        ]

        bool_fields = ["isError", "txreceipt_status"]

        for field in int_fields:
            if field in values and isinstance(values[field], str):
                values[field] = int(values[field])

        for field in bool_fields:
            if field in values and isinstance(values[field], str):
                values[field] = bool(int(values[field]))

        return values


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
