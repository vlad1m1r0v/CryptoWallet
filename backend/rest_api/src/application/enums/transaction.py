from enum import StrEnum


class TransactionSortFieldEnum(StrEnum):
    CREATED_AT = "created_at"
    STATUS = "status"
    TRANSACTION_FEE = "transaction_fee"