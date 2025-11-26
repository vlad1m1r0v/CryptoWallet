from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, computed_field

from src.presentation.http.schemas.fields import (
    UsernameStr,
    AddressStr
)


class GetUserResponsePermissionsSchema(BaseModel):
    has_chat_access: bool


class GetUserResponseWalletSchema(BaseModel):
    id: UUID
    address: AddressStr


class GetUserResponseSchema(BaseModel):
    id: UUID
    username: UsernameStr
    email: EmailStr
    avatar_url: Optional[str]
    total_messages: int
    permissions: GetUserResponsePermissionsSchema
    wallets: List[GetUserResponseWalletSchema]

    @computed_field
    @property
    def total_wallets(self) -> int:
        return len(self.wallets)

