from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl
from uuid import UUID

from src.presentation.http.schemas.fields import UsernameStr


class GetCurrentUserRequestSchema(BaseModel):
    access_token: str


class GetCurrentUserResponseSchema(BaseModel):
    id: UUID
    username: UsernameStr
    email: EmailStr
    avatar_url: Optional[HttpUrl] = None