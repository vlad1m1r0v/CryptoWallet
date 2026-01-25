from pydantic import BaseModel, EmailStr

from typing import Optional

from src.presentation.http.schemas.fields import PasswordStr


class LoginUserRequestSchema(BaseModel):
    email: EmailStr
    password: PasswordStr
    remember_me: Optional[bool] = False


class LoginUserResponseSchema(BaseModel):
    access_token: str
