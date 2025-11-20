from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

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
    permissions: GetUserResponsePermissionsSchema
    wallets: List[GetUserResponseWalletSchema]
