from pydantic import BaseModel, Field


class ImportWalletSchema(BaseModel):
    private_key: str = Field(min_length=32, max_length=128)
