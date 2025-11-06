from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from src.presentation.http.schemas.fields import (
    UsernameStr,
    AddressStr
)


class GetUserProfileResponseWalletSchema(BaseModel):
    id: UUID
    address: AddressStr


class GetUserProfileResponseSchema(BaseModel):
    id: UUID
    username: UsernameStr
    email: EmailStr
    avatar_url: Optional[str]
    wallets: List[GetUserProfileResponseWalletSchema]
