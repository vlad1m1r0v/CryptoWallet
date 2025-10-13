from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID


class GetCurrentUserSchema(BaseModel):
    access_token: str


class GetCurrentUserResponseSchema(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    avatar_url: Optional[str] = None
