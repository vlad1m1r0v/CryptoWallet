from typing import Optional

from fastapi import UploadFile

from pydantic import BaseModel, model_validator, EmailStr, HttpUrl

from src.presentation.http.schemas.fields import UsernameStr, PasswordStr


class UpdateUserRequestSchema(BaseModel):
    avatar: Optional[UploadFile] = None
    username: Optional[UsernameStr] = None
    password: Optional[PasswordStr] = None
    repeat_password: Optional[PasswordStr] = None

    @model_validator(mode="after")
    @classmethod
    def passwords_match(cls, model: "UpdateUserRequestSchema") -> "UpdateUserRequestSchema":
        if model.password != model.repeat_password:
            raise ValueError("Passwords do not match.")
        return model


class UpdateUserResponseSchema(BaseModel):
    username: UsernameStr
    email: EmailStr
    avatar_url: Optional[HttpUrl]