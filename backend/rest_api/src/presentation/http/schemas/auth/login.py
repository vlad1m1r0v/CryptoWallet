from pydantic import BaseModel, EmailStr

from src.presentation.http.schemas.fields import PasswordStr


class LoginUserRequestSchema(BaseModel):
    email: EmailStr
    password: PasswordStr


class LoginUserResponseSchema(BaseModel):
    access_token: str
